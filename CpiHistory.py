from dataclasses import dataclass
from typing import Tuple

import pandas as pd

from CpiReading import CpiReading


@dataclass(frozen=True)
class CpiHistory:
    """Miesięczna inflacja CPI z GUS, od najstarszego miesiąca."""

    readings: Tuple[CpiReading, ...]
    source: str

    @property
    def latest(self) -> CpiReading:
        return self.readings[-1]

    def average_yoy(self, years: int) -> float:
        """Średnioroczna inflacja z ostatnich `years` lat, liczona z indeksów miesiąc do miesiąca."""
        recent = self.readings[-12 * years:]
        index = 1.0
        for reading in recent:
            index *= 1 + reading.mom_pct / 100
        return (index ** (12 / len(recent)) - 1) * 100 if recent else 0.0

    def price_index(self, months: pd.DatetimeIndex) -> pd.Series:
        """Poziom cen dla podanych miesięcy, 1.0 = ostatni miesiąc z `months`.

        Miesiące nowsze niż ostatni odczyt GUS dostają ostatnią inflację r/r rozłożoną na miesiące.
        """
        level, values = 1.0, {}
        for reading in self.readings:
            level *= 1 + reading.mom_pct / 100
            values[pd.Timestamp(reading.year, reading.month, 1)] = level
        series = pd.Series(values).sort_index()
        monthly_rate = (1 + self.latest.yoy_pct / 100) ** (1 / 12)
        stamp, level = series.index[-1], series.iloc[-1]
        while stamp < months.max():
            stamp, level = stamp + pd.DateOffset(months=1), level * monthly_rate
            series[stamp] = level
        aligned = series.reindex(months, method="ffill").bfill()
        return aligned / aligned.iloc[-1]
