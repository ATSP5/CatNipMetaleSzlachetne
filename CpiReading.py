from dataclasses import dataclass


@dataclass(frozen=True)
class CpiReading:
    """Wskaźnik cen towarów i usług konsumpcyjnych GUS za jeden miesiąc (ogółem, Polska)."""

    year: int
    month: int
    yoy_pct: float          # analogiczny miesiąc roku poprzedniego = 100, minus 100
    mom_pct: float          # miesiąc poprzedni = 100, minus 100

    @property
    def label(self) -> str:
        return "%04d-%02d" % (self.year, self.month)
