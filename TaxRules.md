Podatek od zysku ze sprzedaży metalu, według polskich przepisów.

- **Fizyczny metal** to rzecz ruchoma (art. 10 ust. 1 pkt 8 lit. d ustawy o PIT): sprzedaż po upływie 6 miesięcy, licząc od końca miesiąca zakupu, jest **bez podatku**; wcześniej zysk wchodzi do skali podatkowej (12% lub 32%). **Podatek Belki (19%) fizycznego metalu nie dotyczy.**
- **Belka 19%** — tak opodatkowany jest metal „papierowy” (ETC/ETF, kontrakty): 19% od zysku niezależnie od czasu. Liczony obok, do porównania.

Strata nie daje podatku ani zwrotu.

**Dlaczego tu jest:** reguły podatkowe zmieniają się niezależnie od reszty — są w jednym miejscu. Wyjście `tax` → InvestmentCalculator.

## BELKA_PCT
19 — stawka podatku od zysków kapitałowych.

## FREE_AFTER_MONTHS
6 — po tylu miesiącach od końca miesiąca zakupu sprzedaż fizycznego metalu jest zwolniona.

## tax()
Wyjście bloku: zwraca tę instancję.

## is_tax_free(bought, months_held)
`True`, gdy sprzedaż `months_held` miesięcy po dacie `bought` przypada od 1. dnia 7. miesiąca po miesiącu zakupu (np. zakup 14.10.2026 → bez podatku od 1.05.2027, czyli po 7 miesiącach).

## physical_tax(gain, bought, months_held, pit_pct)
Podatek dla fizycznego metalu: 0 przy stracie lub po okresie zwolnienia, inaczej zysk × `pit_pct` %. `pit_pct` 12 albo 32 (wybór na stronie).

## belka_tax(gain)
19% od dodatniego zysku.

## first_tax_free_month(bought)
Pierwszy pełny miesiąc trzymania, po którym sprzedaż jest bez podatku (zwykle 7).

## add_months(day, months)
Data przesunięta o miesiące (dzień obcięty do końca krótszego miesiąca).
