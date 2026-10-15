Rekord danych: fizyczny produkt z metalu, który osoba prywatna kupi u dealera — moneta bulionowa albo sztabka — z wagą, VAT, marżą i dyskontem skupu. Zawiera wzory cen zakupu i odkupu. Lista produktów jest w ProductCatalog; MetalAnalyzer nakłada na wybrany produkt wartości z suwaków (`with_changes`). Czysty rekord — niepodłączony.

## key
Identyfikator, np. `gold_coin_1oz`.

## metal
`gold`, `silver` albo `platinum`.

## name
Nazwa na stronie.

## weight_oz
Czysty metal w uncjach trojańskich (sztabka 100 g = 3,215 oz).

## vat_pct
VAT przy zakupie: 0 dla złota inwestycyjnego (zwolnione), 23 dla srebra i platyny. Przy sprzedaży przez osobę prywatną VAT nie wraca, więc 23% to koszt, który cena musi najpierw odrobić.

## dealer_premium_pct
Marża dealera ponad spot przed VAT, w % (≥ 0). Wyższa = drożej kupujesz, dłużej do progu opłacalności.

## buyback_discount_pct
O ile % skup płaci mniej niż spot (0–100). Wyższy = mniej dostajesz przy sprzedaży.

## note
Uwaga o produkcie wyświetlana na stronie.

## buy_price(spot_per_oz)
spot × waga × (1 + marża) × (1 + VAT) — cena jednej sztuki.

## sell_price(spot_per_oz)
spot × waga × (1 − dyskonto) — ile skup zapłaci za sztukę.

## round_trip_cost_pct()
Strata przy zakupie i natychmiastowej sprzedaży, w %: dla złotych monet ~7%, dla srebra i platyny ~29–34% (VAT).

## with_changes(**changes)
Kopia z podmienionymi polami.
