from typing import Dict, List

import numpy as np
import pandas as pd

from EventCatalog import EventCatalog
from MetalPriceHistory import MetalPriceHistory


class EventStudy:
    """Mierzy, jak ceny metali w złotych naprawdę zareagowały na historyczne wydarzenia z EventCatalog.

    Dla każdego wydarzenia: zmiana ceny od ostatniego notowania przed nim do +1 tygodnia, +1 i +3 miesięcy
    (5, 21, 63 sesji), pomniejszona o przeciętną zmianę w tak długim okresie w całej historii („nadwyżkowa”),
    bo prognoza bazowa już zawiera typowy trend. Statystyki rodzaju = średnia, odchylenie, min i max przykładów.
    """

    HORIZONS = {"1W": 5, "1M": 21, "3M": 63}

    def __init__(self, prices: MetalPriceHistory, catalog: EventCatalog):
        self.daily = prices.daily
        self.catalog = catalog
        self.rows: List[dict] = []
        self.stats: Dict[str, Dict[str, Dict[str, Dict[str, float]]]] = {}

    def event_study(self) -> "EventStudy":
        self._measure()
        return self

    def _measure(self) -> None:
        drift = {metal: {h: float((self.daily[metal].shift(-n) / self.daily[metal] - 1).mean())
                         for h, n in self.HORIZONS.items()} for metal in MetalPriceHistory.METALS}
        index = self.daily.index
        for category in self.catalog.categories():
            per_metal = {metal: {h: [] for h in self.HORIZONS} for metal in MetalPriceHistory.METALS}
            for day, title in category.events:
                start = index.searchsorted(pd.Timestamp(day)) - 1
                if start < 0:
                    continue
                row = {"category": category.key, "date": day, "event": title}
                for metal in MetalPriceHistory.METALS:
                    base = float(self.daily[metal].iloc[start])
                    for h, n in self.HORIZONS.items():
                        if start + n >= len(index):
                            continue
                        move = float(self.daily[metal].iloc[start + n]) / base - 1 - drift[metal][h]
                        per_metal[metal][h].append(move)
                        row["%s_%s" % (metal, h)] = move
                self.rows.append(row)
            self.stats[category.key] = {
                metal: {h: self._summary(values) for h, values in horizons.items()}
                for metal, horizons in per_metal.items()}
        print("[wydarzenia] zmierzono %d wydarzeń w %d rodzajach" % (len(self.rows), len(self.stats)), flush=True)

    @staticmethod
    def _summary(values: List[float]) -> Dict[str, float]:
        if not values:
            return {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0, "n": 0}
        array = np.array(values)
        return {"mean": float(array.mean()), "std": float(array.std(ddof=1)) if len(array) > 1 else 0.0,
                "min": float(array.min()), "max": float(array.max()), "n": int(len(array))}

    def impact(self, category: str, metal: str, horizon: str) -> Dict[str, float]:
        """Statystyki nadwyżkowej zmiany ceny (ułamek, 0.05 = +5%) dla rodzaju wydarzenia."""
        return self.stats[category][metal][horizon]

    def examples(self, category: str) -> List[dict]:
        return [row for row in self.rows if row["category"] == category]
