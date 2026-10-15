import re
from typing import List, Tuple

from EventCatalog import EventCatalog
from InputFileLocator import InputFileLocator
from MetalSettings import MetalSettings


class ScenarioClassifier:
    """Rozpoznaje, jakiego rodzaju jest wydarzenie opisane przez użytkownika (po polsku lub w innym języku).

    Model: lokalny, wielojęzyczny model NLI (domyślnie mDeBERTa-v3 XNLI) w trybie zero-shot — dla każdego rodzaju
    z EventCatalog ocenia, na ile prawdziwe jest zdanie „To wydarzenie dotyczy: <rodzaj>.”. Działa w całości na tym
    komputerze (CPU lub GPU), wagi (~1 GB) pobiera raz do folderu models. Bez pakietu transformers albo modelu —
    zapasowo dopasowuje słowa kluczowe.
    """

    TEMPLATE = "To wydarzenie dotyczy: {}."

    def __init__(self, settings: MetalSettings, catalog: EventCatalog, locator: InputFileLocator):
        self.model_id = settings.scenario_model
        self.catalog = catalog
        self.model_dir = locator.model_folder()
        self.problem = None
        self._pipeline = None
        self.model_label = "—"

    def classifier(self) -> "ScenarioClassifier":
        return self

    def classify(self, text: str) -> List[Tuple[str, float]]:
        """[(klucz rodzaju, pewność 0–1)] od najbardziej pasującego."""
        text = (text or "").strip()
        if not text:
            return []
        pipeline = self._load()
        if pipeline is not None:
            try:
                labels = {c.label: c.key for c in self.catalog.categories()}
                result = pipeline(text, candidate_labels=list(labels), hypothesis_template=self.TEMPLATE,
                                  multi_label=True)
                self.model_label = "lokalny model NLI: %s" % self.model_id
                return [(labels[label], float(score)) for label, score in zip(result["labels"], result["scores"])]
            except Exception as error:                  # noqa: BLE001
                self.problem = "model NLI nie zadziałał: %s" % error
        self.model_label = "słowa kluczowe (zapas%s)" % ("" if self.problem is None else ": " + self.problem)
        return self._keywords(text)

    def _load(self):
        if self._pipeline is not None or self.problem is not None:
            return self._pipeline
        try:
            import torch
            from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
        except ImportError as missing:
            self.problem = "brak pakietu (%s)" % missing
            return None
        try:
            print("[scenariusz] ładuję %s ..." % self.model_id, flush=True)
            tokenizer = AutoTokenizer.from_pretrained(self.model_id, cache_dir=str(self.model_dir))
            model = AutoModelForSequenceClassification.from_pretrained(self.model_id, cache_dir=str(self.model_dir))
            self._pipeline = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer,
                                      device=0 if torch.cuda.is_available() else -1)
        except Exception as error:                      # noqa: BLE001
            self.problem = "nie udało się wczytać %s: %s" % (self.model_id, error)
            print("[scenariusz] " + self.problem, flush=True)
        return self._pipeline

    def _keywords(self, text: str) -> List[Tuple[str, float]]:
        words = re.findall(r"\w+", text.lower())
        joined = " ".join(words)
        scores = []
        for category in self.catalog.categories():
            hits = sum(1 for k in category.keywords if (" " in k and k in joined) or any(w.startswith(k) for w in words))
            scores.append((category.key, hits / (hits + 1.0)))
        return sorted(scores, key=lambda item: -item[1])
