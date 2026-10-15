Rekord danych: prognoza miesięcznej ceny jednego metalu [zł/oz] na kolejne miesiące, jako kwantyle 10/24/50/76/90%. Tworzy go PriceForecaster; MetalAnalyzer może go przesunąć scenariuszem (kopia z nowymi `bands`). Czysty rekord — niepodłączony.

## metal
`gold`, `silver` albo `platinum`.

## model
Opis modelu (Chronos-2, bootstrap, „+ scenariusz”) — pokazywany na stronie.

## start_price
Dzisiejsza cena spot — punkt startu wszystkich ścieżek (miesiąc 0).

## months
Etykiety miesięcy prognozy `RRRR-MM` (pierwszy = następny miesiąc).

## bands
`{kwantyl: numpy.ndarray}` — cena kwantyla w każdym miesiącu. Przy dobrej kalibracji 80% przyszłych cen mieści się między 10% a 90%, ~52% między 24% a 76%.

## horizon
Liczba miesięcy prognozy.

## levels
Posortowane kwantyle.

## at(quantile, month)
Cena kwantyla w miesiącu `month` (1 = za miesiąc; 0 = dziś).

## probability_below(price, month)
Przybliżone P(cena < `price`) z interpolacji między kwantylami; poza pasmem obcięte do 5% / 95%. Daje „Szansę realnej straty”.
