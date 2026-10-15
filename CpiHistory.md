Rekord danych: miesięczna inflacja CPI z GUS od `cpi_history_from_year`. Tworzy go GusInflationClient (wyjście `inflation`), czyta MetalAnalyzer. Czysty rekord — niepodłączony.

## readings
Krotka CpiReading od najstarszego.

## source
Skąd dane (pobrane / kopia).

## latest
Ostatni odczyt — domyślna wartość suwaka „Założona inflacja”.

## average_yoy(years)
Średnioroczna inflacja z ostatnich `years` lat (z indeksów m/m); kafelek „średnio 10 lat”.

## price_index(months)
Poziom cen dla podanych miesięcy, 1,0 = ostatni z nich. Miesiące nowsze niż ostatni odczyt GUS dostają ostatnią inflację r/r rozłożoną na miesiące; wcześniejsze niż pierwszy odczyt — pierwszy poziom. Służy do przeliczenia historii cen na dzisiejsze złote i do indeksu „Inflacja (CPI GUS)” na wykresie.
