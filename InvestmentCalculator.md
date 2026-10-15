Zamienia cenę spot w dniu sprzedaży na kwotę na rękę i jej wartość w dzisiejszych złotych: sprzedaż = sztuki × cena skupu, zysk = sprzedaż − wydane, podatek wg TaxRules (fizyczny i porównawczo Belka), wartość realna = na rękę / wzrost cen.

**Dlaczego tu jest:** jeden rachunek „cena → na rękę → realnie” używany przez wszystkie tabele i wykresy, oddzielony od wyboru produktu i prognozy. Łączy ProductCatalog i TaxRules, żeby MetalAnalyzer zmieścił się w 5 wejściach. Wejścia: `catalog` ← ProductCatalog, `tax` ← TaxRules; wyjście `calculator` → MetalAnalyzer.

## catalog
ProductCatalog (udostępniany dalej MetalAnalyzerowi).

## tax
TaxRules.

## calculator()
Wyjście bloku: zwraca tę instancję.

## net(price, product, units, invested, month, cpi, pit, bought)
Słownik: `price`, `sale` (skup płaci), `tax` (podatek fizyczny), `net` (na rękę), `real` (na rękę w dzisiejszych zł), `net_belka`, `real_belka` (gdyby był podatek Belki), `deflator`. `month` = miesiące od zakupu, `cpi` = inflacja % rocznie, `pit` = 12 lub 32.

## deflator(month, cpi)
(1 + cpi/100)^(month/12) — ile razy wzrosną ceny; inflacja 4% przez 24 mies. → 1,0816.

## breakeven_price(product, units, invested, month, cpi, pit, bought)
Cena spot [zł/oz], przy której na rękę w dzisiejszych zł = wydana kwota (uwzględnia dyskonto skupu, podatek i inflację). Na niej opiera się „Cena musi wzrosnąć (realnie)” i „Szansa realnej straty”.
