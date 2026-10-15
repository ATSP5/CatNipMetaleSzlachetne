Znajduje foldery projektu niezależnie od tego, skąd uruchomiono program: folder z plikiem `.catnip` lokalnie albo `/app` w Dockerze. Tworzy `output` (kopie danych) i `models` (wagi modeli AI).

**Dlaczego tu jest:** ścieżki zależą od miejsca uruchomienia (venv, Docker, serwer) — ta logika jest w jednym bloku zamiast w każdym kliencie. Wejście `settings` ← MetalSettings; wyjście `locator` → MetalPriceClient, GusInflationClient, PriceForecaster, ScenarioClassifier.

## settings
MetalSettings: `input_folder` i `model_cache`.

## locator()
Wyjście bloku: zwraca tę instancję.

## find_input(file_name)
Ścieżka pliku z folderu `input_folder` albo z folderu projektu; brak → `FileNotFoundError`.

## output_folder()
Folder `output` obok projektu (tworzony w razie potrzeby): `metal_prices.csv`, `gus_cpi.json`.

## model_folder()
Folder `model_cache` obok projektu (tworzony w razie potrzeby) — cache Hugging Face dla Chronos-2 i modelu NLI.

## project_roots()
Kandydaci na folder projektu (bieżący, folder skryptu, folder nadrzędny), najpierw te z plikiem `.catnip`; nigdy korzeń dysku.
