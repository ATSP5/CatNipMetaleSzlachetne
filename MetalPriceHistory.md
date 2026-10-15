Rekord danych: dzienne ceny spot złota, srebra i platyny w złotych za uncję trojańską (31,1035 g) oraz kurs USD/PLN. Tworzy go MetalPriceClient, czytają PriceForecaster, EventStudy i MetalAnalyzer. Czysty rekord — niepodłączony na kanwie.

## daily
`pandas.DataFrame` z indeksem dat i kolumnami `gold`, `silver`, `platinum` [zł/oz] oraz `usdpln`.

## source
Opis źródła (pobrane teraz / kopia).

## METALS
Klucze metali: `gold`, `silver`, `platinum`.

## GRAMS_PER_OZ
31,1034768 g w uncji trojańskiej — do cen za gram.

## as_of
Data ostatniego notowania (RRRR-MM-DD).

## spot(metal)
Ostatnia cena [zł/oz] — od niej startuje prognoza i liczony jest zakup.

## monthly()
Średnie miesięczne [zł/oz], indeks = pierwszy dzień miesiąca; ostatni miesiąc jest niepełny.
