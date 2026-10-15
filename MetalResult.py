from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class MetalResult:
    """Wszystko, co strona raportu pokazuje dla jednego zestawu parametrów — gotowe tabele i serie wykresów.

    kpis        — kafelki (ceny spot, kurs, inflacja, model);
    purchase    — co kupujesz: produkt, sztuki, cena, koszt w obie strony, próg opłacalności;
    outcome     — wynik inwestycji po horyzoncie w 5 wariantach (kwantyle prognozy);
    comparison  — wszystkie produkty obok siebie w tym samym horyzoncie;
    value_path  — wartość na rękę miesiąc po miesiącu (mediana i pasmo);
    price_chart — historia ceny + prognoza (+ scenariusz) do wykresu;
    index_chart — metale i inflacja jako indeks 100 = początek okna;
    scenario_*  — wynik analizy scenariuszowej (puste, gdy jej nie było).
    """

    kpis: Dict[str, str]
    purchase: Dict[str, str]
    outcome: List[dict]
    comparison: List[dict]
    value_path: List[dict]
    price_chart: Dict[str, list]
    index_chart: List[dict]
    notes: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    scenario_matches: List[dict] = field(default_factory=list)
    scenario_impacts: List[dict] = field(default_factory=list)
    scenario_analogs: List[dict] = field(default_factory=list)
    scenario_summary: str = ""
