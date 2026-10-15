import json
import time
import urllib.error
import urllib.request
from datetime import date
from typing import Dict, List, Optional, Set, Tuple

from MetalSettings import MetalSettings
from CpiHistory import CpiHistory
from CpiReading import CpiReading
from InputFileLocator import InputFileLocator


class GusInflationClient:
    """Pobiera miesięczną inflację CPI (ogółem, Polska) z dwóch źródeł GUS.

    1. Plik CSV GUS „miesięczne wskaźniki cen towarów i usług konsumpcyjnych od 1982 roku” — jedno zapytanie,
       cała historia (GUS aktualizuje go z opóźnieniem).
    2. API Dziedzinowej Bazy Wiedzy (api-dbw.stat.gov.pl), zmienna 305 — tylko miesiące nowsze niż w CSV:
       przekrój 739 (COICOP 1999) do 2025 r., przekrój 1722 (COICOP 2018) od 2026 r. API ma limit zapytań,
       więc pytamy po kolei i czekamy, gdy odpowie 429.
    Wynik trafia do output/gus_cpi.json na dobę; bez sieci analiza korzysta z tej kopii.
    """

    CSV_URL = ("https://stat.gov.pl/download/gfx/portalinformacyjny/pl/defaultstronaopisowa/4741/1/1/"
               "miesieczne_wskazniki_cen_towarow_i_uslug_konsumpcyjnych_od_1982_roku.csv")
    API = "https://api-dbw.stat.gov.pl/api/1.1.0"
    VARIABLE = 305
    SECTION_TO_2025, SECTION_FROM_2026 = 739, 1722
    YOY, MOM = 5, 2                      # id-sposob-prezentacji-miara
    FIRST_MONTH_PERIOD = 247             # id-okres: 247 = styczeń … 258 = grudzień
    CACHE_HOURS = 24
    PAUSE_S = 0.4

    def __init__(self, settings: MetalSettings, locator: InputFileLocator):
        self.from_year = settings.cpi_history_from_year
        self.cache_file = locator.output_folder() / "gus_cpi.json"

    def inflation(self) -> CpiHistory:
        cached = self._read_cache()
        if cached and time.time() - cached[1] < self.CACHE_HOURS * 3600:
            return self._report(CpiHistory(readings=cached[0], source="GUS (kopia z output/gus_cpi.json)"))
        try:
            readings = self._download(cached[0] if cached else ())
            self._write_cache(readings)
            return self._report(CpiHistory(readings=readings, source="GUS: plik CSV + API DBW (zmienna 305)"))
        except Exception as error:
            if cached:
                print("[GUS] nie udało się pobrać (%s) — używam zapisanej kopii." % error, flush=True)
                return self._report(CpiHistory(readings=cached[0], source="GUS (zapisana kopia)"))
            raise RuntimeError("Nie udało się pobrać inflacji z GUS i nie ma zapisanej kopii: %s" % error)

    # --- pobieranie -------------------------------------------------------------------------------
    def _download(self, known: Tuple[CpiReading, ...]) -> Tuple[CpiReading, ...]:
        by_month: Dict[Tuple[int, int], CpiReading] = {(r.year, r.month): r for r in known}
        by_month.update({(r.year, r.month): r for r in self._from_csv()})
        last = max(by_month) if by_month else (self.from_year, 0)
        today = date.today()
        missing = []
        year, month = last
        while True:
            year, month = (year + 1, 1) if month == 12 else (year, month + 1)
            if (year, month) >= (today.year, today.month):
                break
            missing.append((year, month))
        if missing:
            totals: Dict[int, Set[int]] = {}
            for year, month in missing:
                section = self._section(year)
                if section not in totals:
                    totals[section] = self._total_positions(section)
                reading = self._month(year, month, section, totals[section])
                if reading is None:                    # kolejne miesiące też jeszcze nie wyszły
                    break
                by_month[(year, month)] = reading
        readings = tuple(by_month[k] for k in sorted(by_month) if k[0] >= self.from_year)
        if not readings:
            raise RuntimeError("GUS nie zwrócił żadnego odczytu")
        return readings

    def _from_csv(self) -> List[CpiReading]:
        """Plik CSV GUS (średniki, cp1250): rok, miesiąc, wartość przy „analogiczny miesiąc” i „poprzedni miesiąc”."""
        try:
            text = self._fetch(self.CSV_URL).decode("cp1250")
        except Exception as error:
            print("[GUS] plik CSV niedostępny (%s) — tylko API." % error, flush=True)
            return []
        values: Dict[Tuple[int, int], Dict[int, float]] = {}
        for line in text.splitlines()[1:]:
            cells = line.split(";")
            if len(cells) < 6 or not cells[5].strip():
                continue
            kind = cells[2].lower()
            measure = self.YOY if kind.startswith("analogiczny miesiąc") else \
                self.MOM if kind.startswith("poprzedni miesiąc") else None
            if measure is None or int(cells[3]) < self.from_year:
                continue
            values.setdefault((int(cells[3]), int(cells[4])), {})[measure] = float(cells[5].replace(",", "."))
        return [CpiReading(year=y, month=m, yoy_pct=round(v[self.YOY] - 100, 2), mom_pct=round(v[self.MOM] - 100, 2))
                for (y, m), v in values.items() if self.YOY in v and self.MOM in v]

    def _section(self, year: int) -> int:
        return self.SECTION_TO_2025 if year <= 2025 else self.SECTION_FROM_2026

    def _total_positions(self, section: int) -> Set[int]:
        """Pozycje „ogółem” i „Polska” we wszystkich wymiarach przekroju."""
        positions = self._api("/variable/variable-section-position?id-przekroj=%d&lang=pl" % section)
        wanted = set()
        for position in positions:
            name = position["nazwa-pozycja"].strip().lower()
            if name in ("ogółem", "polska") or name.startswith("0 - ogółem"):
                wanted.add(position["id-pozycja"])
        return wanted

    def _month(self, year: int, month: int, section: int, totals: Set[int]) -> Optional[CpiReading]:
        path = ("/variable/variable-data-section?id-zmienna=%d&id-przekroj=%d&id-rok=%d&id-okres=%d"
                "&ile-na-stronie=5000&numer-strony=0&lang=pl"
                % (self.VARIABLE, section, year, self.FIRST_MONTH_PERIOD + month - 1))
        try:
            rows = self._api(path).get("data", [])
        except urllib.error.HTTPError as error:
            if error.code == 404:              # miesiąc jeszcze nieopublikowany
                return None
            raise
        values = {}
        for row in rows:
            ids = [v for k, v in row.items() if k.startswith("id-pozycja-")]
            if ids and all(i in totals for i in ids):
                values[row["id-sposob-prezentacji-miara"]] = row["wartosc"]
        if self.YOY not in values or self.MOM not in values:
            return None
        return CpiReading(year=year, month=month, yoy_pct=round(values[self.YOY] - 100, 2),
                          mom_pct=round(values[self.MOM] - 100, 2))

    def _api(self, path: str):
        return json.loads(self._fetch(self.API + path).decode("utf-8"))

    def _fetch(self, url: str) -> bytes:
        request = urllib.request.Request(url, headers={"User-Agent": "MetalsAnalysis/1.0"})
        for attempt in range(4):
            time.sleep(self.PAUSE_S)
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    return response.read()
            except urllib.error.HTTPError as error:
                if error.code not in (429, 500, 502, 503) or attempt == 3:
                    raise
                wait = float(error.headers.get("Retry-After") or 5 * (attempt + 1))
                print("[GUS] limit zapytań API — czekam %.0f s" % wait, flush=True)
                time.sleep(min(wait, 60))

    # --- kopia lokalna ----------------------------------------------------------------------------
    def _read_cache(self) -> Optional[Tuple[Tuple[CpiReading, ...], float]]:
        try:
            payload = json.loads(self.cache_file.read_text(encoding="utf-8"))
            readings = tuple(CpiReading(**r) for r in payload["readings"])
            return (readings, payload["saved"]) if readings else None
        except (OSError, ValueError, KeyError, TypeError):
            return None

    def _write_cache(self, readings: Tuple[CpiReading, ...]) -> None:
        payload = {"saved": time.time(), "readings": [r.__dict__ for r in readings]}
        self.cache_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    @staticmethod
    def _report(history: CpiHistory) -> CpiHistory:
        last = history.latest
        print("[GUS] inflacja CPI %s: %.1f%% r/r (%d miesięcy od %s) — %s"
              % (last.label, last.yoy_pct, len(history.readings), history.readings[0].label, history.source),
              flush=True)
        return history
