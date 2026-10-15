Lista standardowych produktów inwestycyjnych dostępnych dla osoby prywatnej w Poznaniu — w punktach dealerów (np. Mennica Polska, Mennica Wrocławska, Tavex, Goldenmark) albo z wysyłką ubezpieczoną: złote monety 1 oz i sztabki 100 g / 10 g, srebrne monety 1 oz i sztabka 1 kg, platynowe moneta i sztabka 1 oz.

**Dlaczego tu jest:** oddziela „co można kupić i za ile” od rachunku. Marże i dyskonta to typowe wartości rynkowe (orientacyjnie, październik 2026) — przed zakupem sprawdź cennik dealera; każdą można zmienić suwakiem na stronie. Wyjście `catalog` → InvestmentCalculator (a przez niego MetalAnalyzer).

## PRODUCTS
Krotka MetalProduct z domyślnymi parametrami. Dopisanie produktu = nowa pozycja na liście wyboru i w tabeli porównania.

## METAL_NAMES
Polskie nazwy metali do tabel i wykresów.

## catalog()
Wyjście bloku: zwraca tę instancję.

## all()
Wszystkie produkty (tabela porównania).

## for_metal(metal)
Produkty jednego metalu (lista wyboru na stronie); pierwszy jest domyślny po zmianie metalu.

## get(key)
Produkt po kluczu; nieznany → `KeyError`.
