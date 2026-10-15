from dataclasses import dataclass
from typing import Dict, List

import numpy as np


@dataclass(frozen=True)
class MetalForecast:
    """Prognoza miesięcznej ceny spot jednego metalu [zł/oz] na kolejne miesiące.

    bands[q][m] — kwantyl q (np. 0.1, 0.5, 0.9) ceny w miesiącu m+1 od dziś; months[m] — ten miesiąc (RRRR-MM).
    start_price — dzisiejsza cena spot, punkt startu wszystkich ścieżek.
    """

    metal: str
    model: str
    start_price: float
    months: List[str]
    bands: Dict[float, np.ndarray]

    @property
    def horizon(self) -> int:
        return len(self.months)

    @property
    def levels(self) -> List[float]:
        return sorted(self.bands)

    def at(self, quantile: float, month: int) -> float:
        """Cena kwantyla w miesiącu `month` (1 = za miesiąc); 0 = dziś."""
        return self.start_price if month <= 0 else float(self.bands[quantile][month - 1])

    def probability_below(self, price: float, month: int) -> float:
        """Przybliżone P(cena < price) w miesiącu `month`, z interpolacji między kwantylami (obcięte do 5–95%)."""
        levels = self.levels
        values = [self.at(q, month) for q in levels]
        if price <= values[0]:
            return min(levels[0], 0.05) if price < values[0] else levels[0]
        if price >= values[-1]:
            return max(levels[-1], 0.95) if price > values[-1] else levels[-1]
        return float(np.interp(price, values, levels))
