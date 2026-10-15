Rekord danych: wszystko, co strona pokazuje dla jednego zestawu parametrów — gotowe tabele i serie wykresów. Tworzy go MetalAnalyzer.evaluate przy każdej zmianie kontrolki; strona MetalsPage tylko go wyświetla. Czysty rekord — niepodłączony.

## kpis
Teksty kafelków: ceny spot za uncję i gram, kurs USD/PLN, inflacja GUS, średnia 10-letnia, założona inflacja, model prognozy, źródła.

## purchase
Co kupujesz: produkt, sztuki, cena sztuki, wydana kwota, spot, sprzedaż od razu, koszt kupno+sprzedaż, VAT, wymagany wzrost ceny (nominalnie i realnie), utrata siły nabywczej, miesiące do progu opłacalności, data zwolnienia z podatku, szansa realnej straty.

## outcome
Wynik po horyzoncie w 5 wariantach (kwantyle): cena metalu, skup płaci, podatek, na rękę, w dzisiejszych zł, zwrot nominalny i realny, oraz to samo przy podatku Belki.

## comparison
Wszystkie produkty przy tej samej kwocie i horyzoncie: VAT, cena sztuki, koszt kupno+sprzedaż, wymagany wzrost, zwrot realny (mediana, 10%, 90%), szansa realnej straty.

## value_path
Na rękę miesiąc po miesiącu: p10, mediana, p90 (dzisiejsze zł), mediana nominalnie, wydana kwota.

## price_chart
Serie wykresu ceny: historia (`x_hist`, `y_hist`), prognoza (`x_fc`, `q10`…`q90`), `baseline` (mediana bez scenariusza), `today`, `unit`, `model`.

## index_chart
Indeks 100 = początek okna dla trzech metali i CPI.

## notes, warnings
Założenia i ostrzeżenia (np. za mała kwota na jedną sztukę).

## scenario_matches, scenario_impacts, scenario_analogs, scenario_summary
Tabele i podsumowanie analizy scenariuszowej; puste, gdy jej nie uruchomiono.
