Pobiera miesięczną inflację CPI (ogółem, Polska) z GUS: plik CSV z całą historią (aktualizowany z opóźnieniem) i brakujące miesiące z API Dziedzinowej Bazy Wiedzy (zmienna 305). API ma limit zapytań, więc pyta po kolei i czeka po odpowiedzi 429. Wynik zapisuje w `output/gus_cpi.json` na dobę. Blok przeniesiony z projektu SavingsAnalysys.

**Dlaczego tu jest:** inflacja przelicza wyniki na dzisiejsze złote i daje domyślne założenie na przyszłość. Wejścia: `settings` ← MetalSettings (`cpi_history_from_year`), `locator` ← InputFileLocator; wyjście `inflation` (CpiHistory) → MetalAnalyzer.

## settings
`cpi_history_from_year` — pierwszy rok historii.

## locator
Folder `output` na kopię.

## inflation()
Wyjście bloku: CpiHistory. Kopia młodsza niż 24 h → bez sieci; błąd sieci → stara kopia; brak kopii → `RuntimeError`.

## CSV_URL, API, VARIABLE, SECTION_TO_2025, SECTION_FROM_2026
Adresy i identyfikatory GUS: przekrój 739 (COICOP 1999) do 2025 r., 1722 od 2026 r.

## CACHE_HOURS, PAUSE_S
Ważność kopii (24 h) i przerwa między zapytaniami do API (0,4 s).
