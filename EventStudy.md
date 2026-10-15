Mierzy, jak ceny metali w złotych naprawdę zareagowały na historyczne wydarzenia z EventCatalog: zmiana ceny od ostatniego notowania przed wydarzeniem do +1 tygodnia, +1 i +3 miesięcy (5, 21, 63 sesji), pomniejszona o przeciętną zmianę w tak długim okresie w całej historii („nadwyżkowa” — bo prognoza bazowa już zawiera typowy trend). Dla każdego rodzaju liczy średnią, odchylenie, minimum i maksimum.

**Dlaczego tu jest:** daje liczbową, sprawdzalną podstawę przewidywań scenariusza — model AI tylko rozpoznaje rodzaj wydarzenia, a wielkość wpływu pochodzi z danych. Wejścia: `prices` ← MetalPriceClient, `catalog` ← EventCatalog; wyjście `event_study` → ScenarioAnalyzer.

## prices
MetalPriceHistory (dzienne ceny w zł).

## catalog
EventCatalog.

## HORIZONS
`1W` = 5 sesji, `1M` = 21, `3M` = 63.

## event_study()
Wyjście bloku: mierzy reakcje i zwraca tę instancję.

## rows
Lista zmierzonych wydarzeń: `category`, `date`, `event` i pola `<metal>_<horyzont>` (ułamki, 0,05 = +5%); brak pola = za mało danych po wydarzeniu.

## stats
`stats[rodzaj][metal][horyzont]` = `{mean, std, min, max, n}`.

## impact(category, metal, horizon)
Statystyki nadwyżkowej zmiany ceny dla rodzaju wydarzenia.

## examples(category)
Wydarzenia jednego rodzaju (tabela „Podobne wydarzenia w historii”).
