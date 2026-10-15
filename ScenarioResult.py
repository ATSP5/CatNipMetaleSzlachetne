from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class ScenarioResult:
    """Przewidywany wpływ wydarzenia na ceny metali.

    matches  — rozpoznane rodzaje: {key, label, score (pewność modelu 0–1), weight (udział w wyniku)};
    impacts  — impacts[metal][horyzont] = {"mean": oczekiwana nadwyżkowa zmiana ceny, "spread": typowy rozrzut},
               ułamki (0.05 = +5%), już przemnożone przez severity; horyzonty 1W, 1M, 3M;
    analogs  — historyczne wydarzenia z rozpoznanych rodzajów i ich zmierzone reakcje.
    """

    text: str
    model: str
    severity: float
    persistence: float
    matches: List[dict]
    impacts: Dict[str, Dict[str, Dict[str, float]]]
    analogs: List[dict] = field(default_factory=list)

    @property
    def recognised(self) -> bool:
        return bool(self.matches)
