Ustawienia całej analizy metali: od kiedy brać historię cen, na ile miesięcy liczyć prognozę, jakie modele AI wczytać, ile ścieżek bootstrapu losować i gdzie trzymać pliki. Wartości ustawia się w INITIALISERZE bloku.

**Dlaczego tu jest:** jedno miejsce na parametry, które nie zmieniają się podczas pracy ze stroną (wymagają ponownego uruchomienia). Wyjście `settings` trafia do InputFileLocator, MetalPriceClient, GusInflationClient, PriceForecaster i ScenarioClassifier.

## history_from
Data początku historii cen (`"RRRR-MM-DD"`, domyślnie `"2004-01-01"`). Nie wcześniej niż 2004 — wcześniej Yahoo nie ma kursu USD/PLN (`ValueError`). Później = krótsza historia: mniej danych dla prognozy i mniej historycznych wydarzeń w EventStudy (wydarzenia sprzed tej daty są pomijane).

## max_forecast_months
Najdłuższy horyzont prognozy w miesiącach (12–240, domyślnie 120; poza zakresem `ValueError`). To górna granica suwaka „Sprzedaż za”. Dłuższy = dłuższe liczenie przy starcie i coraz szersze, mniej wiarygodne pasma.

## forecast_model
Model prognozy z Hugging Face (domyślnie `amazon/chronos-2`). Musi to być model Chronos-2; gdy się nie wczyta, PriceForecaster używa bootstrapu historycznego.

## scenario_model
Lokalny model NLI do rozpoznawania wydarzeń (domyślnie `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`, wielojęzyczny, rozumie polski). Dowolny model zero-shot-classification z Hugging Face; gdy się nie wczyta — słowa kluczowe.

## bootstrap_paths
Liczba losowanych ścieżek w zapasowej prognozie (≥ 200, domyślnie 4000). Więcej = gładsze kwantyle, dłuższy start.

## seed
Ziarno losowania bootstrapu (liczba całkowita); ta sama wartość = ta sama prognoza zapasowa.

## price_cache_hours
Ile godzin kopia cen `output/metal_prices.csv` jest uważana za świeżą (domyślnie 12). 0 = zawsze pobieraj; kopia i tak służy, gdy sieć zawiedzie.

## input_folder
Folder na pliki wejściowe obok projektu (domyślnie `Input`; obecnie nieużywany przez analizę, zostawiony dla InputFileLocator).

## model_cache
Folder obok projektu, do którego trafiają wagi modeli AI (domyślnie `models`). Dzięki niemu modele pobierają się raz, także w Dockerze.

## cpi_history_from_year
Od którego roku GusInflationClient pobiera inflację (domyślnie 2004). Powinien być ≤ rokowi z `history_from`, inaczej historia realna na wykresie zacznie się później.

## settings()
Wyjście bloku: zwraca tę instancję.
