from datetime import date
from typing import Dict

from MetalProduct import MetalProduct
from ProductCatalog import ProductCatalog
from TaxRules import TaxRules


class InvestmentCalculator:
    """Zamienia cenę spot w dniu sprzedaży na kwotę na rękę i jej wartość w dzisiejszych złotych.

    sprzedaż = sztuki × cena skupu (spot × waga × (1 − dyskonto)); zysk = sprzedaż − wydane;
    podatek fizyczny wg TaxRules (PIT tylko przed upływem 6 mies.), porównawczo Belka 19%;
    w dzisiejszych zł = na rękę / (1 + inflacja)^(miesiące / 12).
    """

    def __init__(self, catalog: ProductCatalog, tax: TaxRules):
        self.catalog = catalog
        self.tax = tax

    def calculator(self) -> "InvestmentCalculator":
        return self

    def net(self, price: float, product: MetalProduct, units: int, invested: float, month: int, cpi: float,
            pit: float, bought: date) -> Dict[str, float]:
        sale = units * product.sell_price(price)
        gain = sale - invested
        tax_physical = self.tax.physical_tax(gain, bought, month, pit)
        tax_belka = self.tax.belka_tax(gain)
        deflator = self.deflator(month, cpi)
        return {"price": price, "sale": sale, "tax": tax_physical, "net": sale - tax_physical,
                "real": (sale - tax_physical) / deflator, "net_belka": sale - tax_belka,
                "real_belka": (sale - tax_belka) / deflator, "deflator": deflator}

    @staticmethod
    def deflator(month: int, cpi: float) -> float:
        """Ile razy wzrosną ceny przez `month` miesięcy przy inflacji `cpi` % rocznie."""
        return (1 + cpi / 100) ** (month / 12)

    def breakeven_price(self, product: MetalProduct, units: int, invested: float, month: int, cpi: float,
                        pit: float, bought: date) -> float:
        """Cena spot [zł/oz], przy której na rękę w dzisiejszych zł = wydana kwota."""
        target = invested * self.deflator(month, cpi)                 # potrzebne nominalnie na rękę
        rate = 0.0 if self.tax.is_tax_free(bought, month) else pit / 100
        sale = target if target <= invested else (target - rate * invested) / (1 - rate)
        return sale / (units * product.weight_oz * (1 - product.buyback_discount_pct / 100))
