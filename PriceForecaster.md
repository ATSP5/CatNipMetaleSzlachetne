Prognozuje miesięczne ceny złota, srebra i platyny w złotych na `max_forecast_months` miesięcy naprzód — raz, przy starcie, dla wszystkich metali; strona tylko przycina prognozę do wybranego horyzontu.

- **Model główny: Chronos-2** (`amazon/chronos-2`) — wytrenowany model bazowy dla szeregów czasowych (w 2026 r. w czołówce rankingu GIFT-Eval), prognozuje bez doszkalania i podaje kwantyle. Dostaje średnie miesięczne ceny od 2004 r. z dzisiejszym spotem na końcu.
- **Zapas: bootstrap historyczny** — gdy nie ma pakietu `chronos-forecasting` albo model się nie wczyta: 4000 ścieżek sklejonych z losowych 12-miesięcznych bloków prawdziwych zmian cen od 2004 r. (zachowuje trendy i zmienność historii, ale zakłada, że przyszłość będzie do niej podobna).

To prognoza statystyczna z samej historii cen — nie zna wiadomości; do „co, jeśli” służy analiza scenariuszowa.

**Dlaczego tu jest:** izoluje model AI (torch, transformers, pobieranie wag) od rachunku inwestycji. Wejścia: `settings` ← MetalSettings, `prices` ← MetalPriceClient, `locator` ← InputFileLocator (folder `models`); wyjście `forecaster` → MetalAnalyzer.

## settings
`max_forecast_months`, `forecast_model`, `bootstrap_paths`, `seed`.

## prices
MetalPriceHistory — historia i dzisiejszy spot.

## locator
Folder `models` na wagi Chronos-2 (~0,5 GB, pobierane raz).

## QUANTILES
(0,1; 0,24; 0,5; 0,76; 0,9) — pasma 10–90% i 24–76% (mediana ±26 pp) oraz mediana.

## BLOCK_MONTHS
Długość losowanego bloku w bootstrapie (12 miesięcy) — zachowuje zależności między kolejnymi miesiącami.

## forecaster()
Wyjście bloku: liczy prognozy (z Chronos-2 albo bootstrapu) i zwraca tę instancję.

## forecast(metal)
MetalForecast metalu.

## model_label
Opis użytego modelu (kafelek na stronie).

## horizon
Długość prognozy w miesiącach (= `max_forecast_months`).

## problem
Dlaczego Chronos-2 nie został użyty (brak pakietu, błąd ładowania) albo `None`.
