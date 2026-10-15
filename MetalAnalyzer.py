import math
from dataclasses import replace
from datetime import date
from statistics import NormalDist
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from CpiHistory import CpiHistory
from InvestmentCalculator import InvestmentCalculator
from MetalForecast import MetalForecast
from MetalPriceHistory import MetalPriceHistory
from MetalProduct import MetalProduct
from MetalResult import MetalResult
from PriceForecaster import PriceForecaster
from ProductCatalog import ProductCatalog
from ScenarioAnalyzer import ScenarioAnalyzer
from ScenarioResult import ScenarioResult


class MetalAnalyzer:
    """Liczy, ile na rękę i w dzisiejszych złotych da zakup fizycznego metalu sprzedanego za N miesięcy.

    Łańcuch (rachunek jednej ceny liczy InvestmentCalculator): kwota → całe sztuki produktu po cenie dealera (spot × marża × VAT) → cena skupu z prognozy
    (5 kwantyli, opcjonalnie przesunięta scenariuszem) → podatek (fizyczny: PIT tylko przy sprzedaży przed
    upływem 6 miesięcy od końca miesiąca zakupu; porównawczo Belka 19%) → wartość w dzisiejszych zł
    (deflacja założoną inflacją). Jedyny punkt, w którym parametry strony zamieniają się w wynik.
    """

    LEVEL_NAMES = {0.1: "Pesymistycznie (10%)", 0.24: "Ostrożnie (24%)", 0.5: "Mediana (50%)",
                   0.76: "Dobrze (76%)", 0.9: "Optymistycznie (90%)"}

    def __init__(self, prices: MetalPriceHistory, inflation: CpiHistory, calculator: InvestmentCalculator,
                 forecaster: PriceForecaster, scenario: ScenarioAnalyzer):
        self.prices = prices
        self.inflation = inflation
        self.calculator = calculator
        self.catalog = calculator.catalog
        self.tax = calculator.tax
        self.forecaster = forecaster
        self.scenario_analyzer = scenario
        self.today = date.today()

    def analyzer(self) -> "MetalAnalyzer":
        self.print_baseline()
        return self

    @property
    def max_months(self) -> int:
        return self.forecaster.horizon

    # -- parametry -----------------------------------------------------------------------------------
    def defaults(self) -> dict:
        product = self.catalog.get("gold_coin_1oz")
        return {"metal": "gold", "product": product.key, "amount": 20000, "horizon_months": 24,
                "cpi_forecast": round(self.inflation.latest.yoy_pct, 1), "pit_pct": "12",
                "premium": product.dealer_premium_pct, "discount": product.buyback_discount_pct,
                "history_years": 10, "chart_real": False,
                "scenario_text": "", "severity": 1.0, "persistence": 50}

    def product_defaults(self, key: str) -> dict:
        product = self.catalog.get(key)
        return {"premium": product.dealer_premium_pct, "discount": product.buyback_discount_pct}

    def product_options(self, metal: str) -> List[tuple]:
        return [(p.key, p.name) for p in self.catalog.for_metal(metal)]

    def scenario(self, text: str, severity: float, persistence_pct: float) -> ScenarioResult:
        return self.scenario_analyzer.analyze(text, float(severity), float(persistence_pct) / 100)

    # -- wynik ---------------------------------------------------------------------------------------
    def evaluate(self, p: dict, scenario: Optional[ScenarioResult] = None) -> MetalResult:
        metal = p["metal"]
        horizon = int(min(max(int(p["horizon_months"]), 1), self.max_months))
        cpi = float(p["cpi_forecast"])
        pit = float(p["pit_pct"])
        product = self.catalog.get(p["product"])
        if product.metal != metal:
            product = self.catalog.for_metal(metal)[0]
        product = product.with_changes(dealer_premium_pct=float(p["premium"]),
                                       buyback_discount_pct=float(p["discount"]))
        forecasts = {m: self._adjusted(self.forecaster.forecast(m), scenario) for m in MetalPriceHistory.METALS}
        forecast = forecasts[metal]
        warnings = []

        spot = self.prices.spot(metal)
        unit_price = product.buy_price(spot)
        units = math.floor(float(p["amount"]) / unit_price)
        if units < 1:
            warnings.append("Za %s zł nie kupisz ani jednej sztuki (%s zł/szt.) — liczę dla 1 sztuki."
                            % (self.pln(p["amount"]), self.pln(unit_price)))
            units = 1
        invested = units * unit_price

        outcome = [self._outcome_row(q, forecast, product, units, invested, horizon, cpi, pit) for q in forecast.levels]
        median = self._net(forecast.at(0.5, horizon), product, units, invested, horizon, cpi, pit)
        purchase = self._purchase(product, spot, units, unit_price, invested, horizon, cpi, pit, forecast)
        comparison = [self._compare(prod if prod.key != product.key else product, forecasts[prod.metal], invested,
                                    horizon, cpi, pit) for prod in self.catalog.all()]
        notes = self._notes(product, horizon, pit)
        if median["real"] < invested:
            notes.insert(0, "W medianie prognozy ten zakup po %d mies. NIE odrabia kosztów i inflacji." % horizon)
        result = MetalResult(
            kpis=self._kpis(cpi), purchase=purchase, outcome=outcome, comparison=comparison,
            value_path=self._value_path(forecast, product, units, invested, horizon, cpi, pit),
            price_chart=self._price_chart(metal, forecast, horizon, int(p["history_years"]), bool(p["chart_real"]),
                                          cpi, scenario),
            index_chart=self._index_chart(int(p["history_years"])), notes=notes, warnings=warnings)
        if scenario is not None:
            result = replace(result, **self._scenario_tables(scenario))
        return result

    def _adjusted(self, forecast: MetalForecast, scenario: Optional[ScenarioResult]) -> MetalForecast:
        """Prognoza przesunięta scenariuszem: kwantyl q × (1 + zmiana + z(q) × rozrzut)."""
        if scenario is None or not scenario.recognised:
            return forecast
        mid, spread = ScenarioAnalyzer.adjustment(scenario, forecast.metal, forecast.horizon)
        z_edge = NormalDist().inv_cdf(0.9)
        bands = {}
        for q, values in forecast.bands.items():
            z = NormalDist().inv_cdf(q) / z_edge
            bands[q] = np.maximum(values * (1 + mid + z * spread), 0.0)
        return replace(forecast, model=forecast.model + " + scenariusz", bands=bands)

    def _net(self, price, product, units, invested, month, cpi, pit) -> Dict[str, float]:
        return self.calculator.net(price, product, units, invested, month, cpi, pit, self.today)

    def _outcome_row(self, q, forecast, product, units, invested, horizon, cpi, pit) -> dict:
        n = self._net(forecast.at(q, horizon), product, units, invested, horizon, cpi, pit)
        return {"Wariant": self.LEVEL_NAMES.get(q, "%.0f%%" % (100 * q)),
                "Cena %s [zł/oz]" % forecast.months[horizon - 1]: round(n["price"]),
                "Skup płaci [zł]": round(n["sale"]), "Podatek [zł]": round(n["tax"]),
                "Na rękę [zł]": round(n["net"]), "W dzisiejszych zł": round(n["real"]),
                "Zwrot nominalny": self.pct(n["net"] / invested - 1),
                "Zwrot realny": self.pct(n["real"] / invested - 1),
                "Przy Belce 19%: na rękę [zł]": round(n["net_belka"]),
                "Przy Belce: zwrot realny": self.pct(n["real_belka"] / invested - 1)}

    def _purchase(self, product, spot, units, unit_price, invested, horizon, cpi, pit, forecast) -> Dict[str, str]:
        sell_now = units * product.sell_price(spot)
        deflator = self.calculator.deflator(horizon, cpi)
        needed_real = self._breakeven_price(product, units, invested, horizon, cpi, pit)
        months = self._breakeven_month(forecast, product, units, invested, cpi, pit)
        free_month = self.tax.first_tax_free_month(self.today)
        return {"product": product.name, "note": product.note, "units": "%d szt." % units,
                "unit_price": "%s zł" % self.pln(unit_price), "invested": "%s zł" % self.pln(invested),
                "spot": "%s zł/oz" % self.pln(spot),
                "sell_now": "%s zł (%s)" % (self.pln(sell_now), self.pct(sell_now / invested - 1)),
                "round_trip": "%.1f%%" % product.round_trip_cost_pct(),
                "vat": "zw." if not product.vat_pct else "%.0f%%" % product.vat_pct,
                "needed_nominal": self.pct(invested / sell_now - 1),
                "needed_real": "%s (do %s zł/oz)" % (self.pct(needed_real / spot - 1), self.pln(needed_real)),
                "inflation_loss": "%s" % self.pct(1 / deflator - 1),
                "breakeven_nominal": self._month_text(months[0]), "breakeven_real": self._month_text(months[1]),
                "tax_free_from": "%s (po %d mies.)" % (self.month_label(free_month), free_month),
                "p_real_loss": "%.0f%%" % (100 * forecast.probability_below(needed_real, horizon))}

    def _breakeven_price(self, product, units, invested, month, cpi, pit) -> float:
        return self.calculator.breakeven_price(product, units, invested, month, cpi, pit, self.today)

    def _breakeven_month(self, forecast, product, units, invested, cpi, pit):
        nominal = real = None
        for m in range(1, forecast.horizon + 1):
            n = self._net(forecast.at(0.5, m), product, units, invested, m, cpi, pit)
            if nominal is None and n["net"] >= invested:
                nominal = m
            if real is None and n["real"] >= invested:
                real = m
            if nominal and real:
                break
        return nominal, real

    def _compare(self, product: MetalProduct, forecast, amount, horizon, cpi, pit) -> dict:
        spot = self.prices.spot(product.metal)
        unit_price = product.buy_price(spot)
        units = max(math.floor(amount / unit_price), 1)
        invested = units * unit_price
        values = {q: self._net(forecast.at(q, horizon), product, units, invested, horizon, cpi, pit)["real"]
                  for q in (0.1, 0.5, 0.9)}
        needed = self._breakeven_price(product, units, invested, horizon, cpi, pit)
        return {"Produkt": product.name, "VAT": "zw." if not product.vat_pct else "%.0f%%" % product.vat_pct,
                "Cena szt. [zł]": round(unit_price), "Koszt kupno+sprzedaż": "%.1f%%" % product.round_trip_cost_pct(),
                "Cena musi wzrosnąć (realnie)": self.pct(needed / spot - 1),
                "Zwrot realny: mediana": self.pct(values[0.5] / invested - 1),
                "10%": self.pct(values[0.1] / invested - 1), "90%": self.pct(values[0.9] / invested - 1),
                "Szansa realnej straty": "%.0f%%" % (100 * forecast.probability_below(needed, horizon))}

    def _value_path(self, forecast, product, units, invested, horizon, cpi, pit) -> List[dict]:
        rows = []
        for m in range(0, horizon + 1):
            label = self.month_label(m)
            values = {q: self._net(forecast.at(q, m), product, units, invested, m, cpi, pit) for q in (0.1, 0.5, 0.9)}
            rows.append({"Miesiąc": label, "p10": round(values[0.1]["real"]), "mediana": round(values[0.5]["real"]),
                         "p90": round(values[0.9]["real"]), "mediana nominalnie": round(values[0.5]["net"]),
                         "Wpłacone": round(invested)})
        return rows

    def _price_chart(self, metal, forecast, horizon, years, real, cpi, scenario) -> Dict[str, list]:
        monthly = self.prices.monthly()[metal].dropna()
        monthly = monthly[monthly.index >= monthly.index[-1] - pd.DateOffset(years=years)]
        history = monthly.iloc[:-1]
        if real:
            history = history / self.inflation.price_index(history.index.append(monthly.index[-1:])).iloc[:-1]
        today_label = monthly.index[-1].strftime("%Y-%m")
        x_hist = [d.strftime("%Y-%m") for d in history.index] + [today_label]
        y_hist = [round(float(v)) for v in history] + [round(forecast.start_price)]
        x_fc = [today_label] + forecast.months[:horizon]
        chart = {"x_hist": x_hist, "y_hist": y_hist, "x_fc": x_fc, "today": today_label,
                 "unit": "zł dzisiejsze / oz" if real else "zł / oz", "model": forecast.model}
        for q in forecast.levels:
            values = [forecast.start_price] + [forecast.at(q, m) for m in range(1, horizon + 1)]
            if real:
                values = [v / (1 + cpi / 100) ** (m / 12) for m, v in enumerate(values)]
            chart["q%02d" % round(100 * q)] = [round(v) for v in values]
        if scenario is not None and scenario.recognised:
            base = self.forecaster.forecast(metal)
            values = [base.start_price] + [base.at(0.5, m) for m in range(1, horizon + 1)]
            if real:
                values = [v / (1 + cpi / 100) ** (m / 12) for m, v in enumerate(values)]
            chart["baseline"] = [round(v) for v in values]
        return chart

    def _index_chart(self, years: int) -> List[dict]:
        monthly = self.prices.monthly()
        monthly = monthly[monthly.index >= monthly.index[-1] - pd.DateOffset(years=years)]
        cpi = self.inflation.price_index(monthly.index)
        rows = []
        for stamp in monthly.index:
            row = {"Miesiąc": stamp.strftime("%Y-%m"),
                   "Inflacja (CPI GUS)": round(100 * float(cpi[stamp] / cpi.iloc[0]), 1)}
            for metal, name in ProductCatalog.METAL_NAMES.items():
                row[name] = round(100 * float(monthly[metal][stamp] / monthly[metal].iloc[0]), 1)
            rows.append(row)
        return rows

    def _scenario_tables(self, scenario: ScenarioResult) -> dict:
        matches = [{"Rodzaj wydarzenia": m["label"], "Pewność modelu": "%.0f%%" % (100 * m["score"]),
                    "Waga w wyniku": "%.0f%%" % (100 * m["weight"])} for m in scenario.matches]
        impacts = []
        for metal, name in ProductCatalog.METAL_NAMES.items():
            row = {"Metal": name}
            for horizon, label in (("1W", "1 tydzień"), ("1M", "1 miesiąc"), ("3M", "3 miesiące")):
                i = scenario.impacts[metal][horizon]
                row[label] = "%s ± %.1f pp" % (self.pct(i["mean"]), 100 * i["spread"])
            impacts.append(row)
        analogs = []
        for a in scenario.analogs:
            row = {"Data": a["date"], "Wydarzenie": a["event"], "Rodzaj": a["category_label"]}
            for metal, name in ProductCatalog.METAL_NAMES.items():
                value = a.get("%s_1M" % metal)
                row["%s 1M" % name] = "—" if value is None else self.pct(value)
            analogs.append(row)
        if scenario.recognised:
            names = ", ".join(m["label"] for m in scenario.matches)
            summary = "Rozpoznano: %s. Model: %s. Siła ×%.2f, po roku zostaje %.0f%% wpływu." % (
                names, scenario.model, scenario.severity, 100 * scenario.persistence)
        else:
            summary = ("Nie rozpoznano rodzaju wydarzenia (model: %s) — prognoza bez zmian. Opisz wydarzenie "
                       "konkretniej, np. „Chiny atakują Tajwan” albo „Fed obniża stopy o 1 pp”." % scenario.model)
        return {"scenario_matches": matches, "scenario_impacts": impacts, "scenario_analogs": analogs,
                "scenario_summary": summary}

    def _kpis(self, cpi) -> Dict[str, str]:
        g = MetalPriceHistory.GRAMS_PER_OZ
        k = {"as_of": self.prices.as_of, "usdpln": "%.4f" % self.prices.daily["usdpln"].iloc[-1],
             "cpi": "%.1f%%" % self.inflation.latest.yoy_pct, "cpi_label": self.inflation.latest.label,
             "cpi10": "%.1f%%" % self.inflation.average_yoy(10), "cpi_forecast": "%.1f%%" % cpi,
             "model": self.forecaster.model_label, "price_source": self.prices.source,
             "cpi_source": self.inflation.source}
        for metal in MetalPriceHistory.METALS:
            spot = self.prices.spot(metal)
            k[metal] = "%s zł/oz" % self.pln(spot)
            k[metal + "_g"] = "%s zł/g" % self.pln2(spot / g)
        return k

    def _notes(self, product, horizon, pit) -> List[str]:
        notes = ["Ceny spot: kontrakty COMEX/NYMEX z Yahoo Finance × kurs USD/PLN; produkty fizyczne: spot × marża "
                 "dealera × VAT. Marże i skup to wartości orientacyjne — sprawdź cennik dealera w Poznaniu przed zakupem.",
                 "Podatek: fizyczny metal to rzecz ruchoma — sprzedaż po 6 miesiącach od końca miesiąca zakupu jest "
                 "bez podatku; wcześniej zysk wchodzi do skali PIT (%.0f%%). Podatek Belki (19%%) dotyczy metalu "
                 "„papierowego” (ETC/ETF) i jest pokazany obok do porównania." % pit,
                 "Inflacja: wartości „w dzisiejszych zł” dzielone przez wzrost cen przy założonej inflacji; historia "
                 "realna — przez indeks CPI z GUS."]
        if product.vat_pct:
            notes.append("%s: VAT %.0f%% płacisz przy zakupie, a skup go nie zwraca — cena musi najpierw odrobić "
                         "ten VAT." % (product.name, product.vat_pct))
        if horizon < self.tax.first_tax_free_month(self.today):
            notes.append("Sprzedaż przed upływem 6 miesięcy od końca miesiąca zakupu — zysk jest opodatkowany PIT.")
        return notes

    # -- formatowanie --------------------------------------------------------------------------------
    def month_label(self, months: int) -> str:
        index = self.today.year * 12 + self.today.month - 1 + int(months)
        return "%04d-%02d" % (index // 12, index % 12 + 1)

    def _month_text(self, months) -> str:
        if months is None:
            return "nie w horyzoncie prognozy"
        return "%s (po %d l. %d m.)" % ((self.month_label(months),) + divmod(months, 12))

    @staticmethod
    def pct(value: float) -> str:
        return "%+.1f%%" % (100 * value)

    @staticmethod
    def pln(value) -> str:
        return "{:,.0f}".format(float(value)).replace(",", " ")

    @staticmethod
    def pln2(value) -> str:
        return "{:,.2f}".format(float(value)).replace(",", " ").replace(".", ",")

    # -- konsola -------------------------------------------------------------------------------------
    def print_baseline(self) -> None:
        p = self.defaults()
        p["horizon_months"] = 24
        result = self.evaluate(p)
        print("\nMETALE — %s, prognoza: %s, inflacja założona %s" % (result.kpis["as_of"], result.kpis["model"],
                                                                    result.kpis["cpi_forecast"]))
        print("%-58s %10s %14s %10s" % ("Produkt (kwota 20 000 zł, 24 mies.)", "kupno+sprz.", "realnie mediana",
                                         "P(straty)"))
        for row in result.comparison:
            print("%-58s %10s %14s %10s" % (row["Produkt"][:58], row["Koszt kupno+sprzedaż"],
                                            row["Zwrot realny: mediana"], row["Szansa realnej straty"]))
        print(flush=True)
