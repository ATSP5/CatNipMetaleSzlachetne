Interaktywna strona w zakładce Output: ceny spot, zakup wybranego produktu, wynik na rękę i w dzisiejszych złotych po wybranym horyzoncie (5 wariantów prognozy, obok podatek Belki), wykres ceny z historią i prognozą (pionowa kreskowana linia „dziś”), wartość inwestycji w czasie, metale a inflacja, porównanie wszystkich produktów i analiza scenariuszowa z tabelą podobnych wydarzeń z historii. Każda zmiana kontrolki przelicza stronę (~0,02 s).

**Dlaczego tu jest:** sam widok bez obliczeń — wszystko liczy MetalAnalyzer (wejście `analyzer`). Wyjście `show` → Main. Stan startuje od `MetalAnalyzer.defaults()`; przycisk „Przywróć ustawienia domyślne” do niego wraca.

## analyzer
Wejście: MetalAnalyzer.

## metal (radio: gold / silver / platinum)
Wybrany metal. Zmiana przestawia `product` na pierwszy produkt metalu i ustawia jego marżę i skup.

## product (lista produktów metalu)
Wybrany produkt z ProductCatalog. Zmiana ustawia domyślne `premium` i `discount`.

## amount (1 000–500 000 zł, krok 1 000; domyślnie 20 000)
Kwota do wydania. Kupowane są całe sztuki; niewykorzystana reszta nie jest liczona.

## horizon_months (1–max_months, domyślnie 24)
Za ile miesięcy sprzedajesz. Krótszy niż 7 miesięcy → PIT od zysku.

## premium (0–20%, krok 0,1)
Marża dealera ponad spot przed VAT. Wyższa = drożej, dłużej do progu opłacalności.

## discount (0–30%, krok 0,1)
O ile skup płaci mniej niż spot. Wyższy = mniej na rękę.

## pit_pct (radio: 12 / 32)
Stawka PIT od zysku przy sprzedaży przed upływem 6 miesięcy od końca miesiąca zakupu. Po tym okresie bez znaczenia.

## cpi_forecast (−1…15%, krok 0,1; domyślnie ostatni odczyt GUS)
Założona średnia inflacja do dnia sprzedaży. Wyższa = niższa wartość w dzisiejszych zł i wyższy wymagany wzrost ceny.

## history_years (3–22 lata)
Ile lat historii na wykresach.

## chart_real (przełącznik)
Wykres ceny w dzisiejszych złotych (historia deflowana CPI z GUS, prognoza założoną inflacją).

## scenario_text (pole tekstowe)
Opis wydarzenia po polsku, np. „Chiny atakują Tajwan”, „Fed obniża stopy o 1 pp”, „strajk w kopalniach platyny w RPA”.

## severity (0,25–3, krok 0,25; domyślnie 1)
Siła wydarzenia względem przeciętnej w historii; mnoży przewidywany wpływ i rozrzut.

## persistence (0–100%, krok 5; domyślnie 50)
Ile wpływu zostaje po roku od 3. miesiąca. 0 = efekt przejściowy, 100 = trwały.

## run_scenario() — przycisk „Przewiduj wpływ”
Uruchamia ScenarioAnalyzer dla `scenario_text` (pierwszy raz ładuje model NLI); wynik przesuwa prognozę wszystkich metali i wypełnia tabele scenariusza. Pusty tekst → komunikat.

## clear_scenario() — przycisk „Wyczyść scenariusz”
Usuwa scenariusz i tekst; prognoza wraca do bazowej.

## setup(), reset()
Stan startowy z `defaults()`; reset czyści też scenariusz.

## on_metal_change(value), on_product_change(value)
Synchronizacja produktu i jego kosztów z wybranym metalem/produktem.

## prepare()
Liczy MetalResult i figury Plotly dla znaczników.

## price_figure(result, metal), value_figure(result), today_line(x)
Wykres ceny (historia, pasma 10–90% i 24–76%, mediana, mediana bez scenariusza, kreskowana linia „dziś”) i wykres wartości na rękę.

## METAL_COLORS, METAL_GENITIVE
Kolory metali i nazwy w dopełniaczu do nagłówków.

## show
Wyjście: pokazuje lub odświeża stronę w zakładce Output.
