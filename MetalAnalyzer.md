Liczy, ile na rękę i w dzisiejszych złotych da zakup fizycznego metalu sprzedanego za N miesięcy. Łańcuch: kwota → całe sztuki produktu po cenie dealera (spot × marża × VAT) → cena skupu z prognozy (5 kwantyli, opcjonalnie przesunięta scenariuszem) → podatek (fizyczny: PIT tylko przy sprzedaży przed upływem 6 miesięcy; porównawczo Belka 19%) → wartość w dzisiejszych złotych. Buduje też porównanie wszystkich produktów, wykresy i tabele scenariusza. Przy starcie wypisuje w konsoli porównanie produktów dla 20 000 zł i 24 miesięcy.

**Dlaczego tu jest:** jedyny punkt, w którym parametry strony zamieniają się w wynik — MetalsPage jest tylko widokiem. Jedno przeliczenie trwa ~0,02 s, bo prognozy i badanie wydarzeń są policzone przy starcie. Wejścia: `prices` ← MetalPriceClient, `inflation` ← GusInflationClient, `calculator` ← InvestmentCalculator, `forecaster` ← PriceForecaster, `scenario` ← ScenarioAnalyzer; wyjście `analyzer` → MetalsPage.

## prices, inflation, calculator, forecaster, scenario
Wejścia jak wyżej; `catalog` i `tax` są brane z kalkulatora.

## LEVEL_NAMES
Nazwy wariantów kwantyli w tabeli wyniku.

## max_months
Najdłuższy horyzont (z PriceForecaster) — górna granica suwaka.

## analyzer()
Wyjście bloku: wypisuje porównanie i zwraca tę instancję.

## defaults()
Stan startowy strony: złoto, moneta 1 oz, 20 000 zł, 24 mies., inflacja = ostatni odczyt GUS, PIT 12%, marża i skup z katalogu, 10 lat historii, wykres nominalny, scenariusz pusty, siła 1, trwałość 50%.

## product_defaults(key), product_options(metal)
Domyślna marża/skup produktu; lista produktów metalu do wyboru.

## scenario(text, severity, persistence_pct)
ScenarioResult z ScenarioAnalyzer (`persistence_pct` 0–100).

## evaluate(p, scenario=None)
MetalResult dla parametrów strony. Wpływ parametrów:
- **kwota** — kupowane są całe sztuki (reszta zostaje); za mało na 1 sztukę → liczone dla 1 z ostrzeżeniem;
- **horyzont** — dłuższy rozkłada koszt zakupu w czasie, ale poszerza pasmo; sprzedaż przed 7. miesiącem → PIT od zysku;
- **marża / skup** — wyższe podnoszą próg opłacalności;
- **inflacja** — wyższa obniża wartość w dzisiejszych zł i podnosi wymagany wzrost ceny;
- **PIT 12/32%** — tylko przy sprzedaży przed okresem zwolnienia;
- **scenariusz** — przesuwa i poszerza prognozę wszystkich metali.

## month_label(months), pct(value), pln(value), pln2(value)
Formatowanie: „2027-05”, „+8.1%”, „16 251”, „522,47”.

## print_baseline()
Porównanie produktów w konsoli.
