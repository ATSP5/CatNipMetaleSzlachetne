from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class MetalPriceHistory:
    """Dzienne ceny spot w złotych za uncję trojańską (31,1035 g): kolumny gold, silver, platinum, usdpln."""

    daily: pd.DataFrame
    source: str

    METALS = ("gold", "silver", "platinum")
    GRAMS_PER_OZ = 31.1034768

    @property
    def as_of(self) -> str:
        return self.daily.index[-1].strftime("%Y-%m-%d")

    def spot(self, metal: str) -> float:
        """Ostatnia cena spot [zł/oz]."""
        return float(self.daily[metal].iloc[-1])

    def monthly(self) -> pd.DataFrame:
        """Średnie miesięczne cen [zł/oz]; indeks = pierwszy dzień miesiąca."""
        frame = self.daily[list(self.METALS)].resample("MS").mean()
        return frame.dropna(how="all")
