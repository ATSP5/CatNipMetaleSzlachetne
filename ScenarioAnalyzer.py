import math
from typing import Tuple

import numpy as np

from EventStudy import EventStudy
from MetalPriceHistory import MetalPriceHistory
from ScenarioClassifier import ScenarioClassifier
from ScenarioResult import ScenarioResult


class ScenarioAnalyzer:
    """Zamienia opis wydarzenia na przewidywaną zmianę cen złota, srebra i platyny.

    1. ScenarioClassifier (lokalny model) ocenia, do jakich rodzajów wydarzeń pasuje tekst.
    2. Rodzaje z pewnością ≥ MIN_SCORE (najwyżej MAX_MATCHES) dostają wagi proporcjonalne do pewności.
    3. Oczekiwana zmiana = ważona średnia z rzeczywistych reakcji cen na historyczne wydarzenia tych rodzajów
       (EventStudy), × severity. Rozrzut = ważone odchylenie tych reakcji.
    4. Na ścieżce prognozy wpływ narasta do 3 miesięcy, potem wygasa: po kolejnych 12 miesiącach zostaje
       `persistence` (0–1) jego wielkości.
    """

    MIN_SCORE = 0.5
    FALLBACK_SCORE = 0.2
    MAX_MATCHES = 3

    def __init__(self, classifier: ScenarioClassifier, event_study: EventStudy):
        self.classifier = classifier
        self.event_study = event_study

    def scenario(self) -> "ScenarioAnalyzer":
        return self

    def analyze(self, text: str, severity: float = 1.0, persistence: float = 0.5) -> ScenarioResult:
        if not 0 < severity <= 5:
            raise ValueError("severity: od 0 do 5")
        if not 0 <= persistence <= 1:
            raise ValueError("persistence: od 0 do 1")
        scores = self.classifier.classify(text)
        chosen = [(k, s) for k, s in scores if s >= self.MIN_SCORE][:self.MAX_MATCHES]
        if not chosen and scores and scores[0][1] >= self.FALLBACK_SCORE:
            chosen = scores[:1]
        total = sum(s for _, s in chosen) or 1.0
        catalog = self.event_study.catalog
        matches = [{"key": k, "label": catalog.get(k).label, "score": s, "weight": s / total} for k, s in chosen]
        impacts = {}
        for metal in MetalPriceHistory.METALS:
            impacts[metal] = {}
            for horizon in EventStudy.HORIZONS:
                mean = sum(m["weight"] * self.event_study.impact(m["key"], metal, horizon)["mean"] for m in matches)
                var = sum(m["weight"] * self.event_study.impact(m["key"], metal, horizon)["std"] ** 2 for m in matches)
                impacts[metal][horizon] = {"mean": mean * severity, "spread": math.sqrt(var) * severity}
        analogs = [dict(row, category_label=catalog.get(m["key"]).label)
                   for m in matches for row in self.event_study.examples(m["key"])]
        return ScenarioResult(text=text, model=self.classifier.model_label, severity=severity,
                              persistence=persistence, matches=matches, impacts=impacts, analogs=analogs)

    @staticmethod
    def adjustment(result: ScenarioResult, metal: str, months: int) -> Tuple[np.ndarray, np.ndarray]:
        """Mnożniki ścieżki dla miesięcy 1..months: (zmiana środka, rozrzut), ułamki."""
        one, three = result.impacts[metal]["1M"], result.impacts[metal]["3M"]
        mid, spread = np.zeros(months), np.zeros(months)
        for m in range(1, months + 1):
            if m <= 3:
                share = (m - 1) / 2.0
                mid[m - 1] = one["mean"] + share * (three["mean"] - one["mean"])
                spread[m - 1] = one["spread"] + share * (three["spread"] - one["spread"])
            else:
                decay = result.persistence ** ((m - 3) / 12.0)
                mid[m - 1], spread[m - 1] = three["mean"] * decay, three["spread"] * decay
        return mid, spread
