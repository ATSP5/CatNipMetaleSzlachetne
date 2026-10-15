from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class EventCategory:
    """Rodzaj wydarzenia rynkowego z historycznymi przykładami.

    label     — opis po polsku, który lokalny model NLI porównuje z tekstem użytkownika;
    keywords  — rdzenie słów dla klasyfikatora zapasowego (bez modelu AI);
    events    — (data RRRR-MM-DD, opis) prawdziwych wydarzeń; reakcję cen mierzy EventStudy.
    """

    key: str
    label: str
    keywords: Tuple[str, ...]
    events: Tuple[Tuple[str, str], ...]
