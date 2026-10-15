Rekord danych: przewidywany wpływ wydarzenia na ceny metali. Tworzy go ScenarioAnalyzer; MetalAnalyzer przesuwa nim prognozę i buduje tabele scenariusza. Czysty rekord — niepodłączony.

## text
Opis wydarzenia wpisany przez użytkownika.

## model
Którym klasyfikatorem rozpoznano (model NLI albo słowa kluczowe).

## severity
Mnożnik siły wydarzenia (0–5; 1 = jak przeciętnie w historii).

## persistence
Ile wpływu zostaje po roku (0–1).

## matches
Rozpoznane rodzaje: `key`, `label`, `score` (pewność modelu 0–1), `weight` (udział w wyniku, sumuje się do 1).

## impacts
`impacts[metal][horyzont]` = `{mean, spread}` — oczekiwana nadwyżkowa zmiana ceny i typowy rozrzut (ułamki, już × `severity`); horyzonty `1W`, `1M`, `3M`.

## analogs
Historyczne wydarzenia rozpoznanych rodzajów z ich zmierzonymi reakcjami.

## recognised
`True`, gdy rozpoznano co najmniej jeden rodzaj.
