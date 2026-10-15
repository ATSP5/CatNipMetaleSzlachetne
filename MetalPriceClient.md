Pobiera dzienne ceny złota, srebra i platyny (kontrakty COMEX/NYMEX: GC=F, SI=F, PL=F, w USD za uncję) i kurs USD/PLN (PLN=X) z Yahoo Finance i przelicza je na złote za uncję trojańską. Zwraca MetalPriceHistory.

**Dlaczego tu jest:** jedyne źródło cen w projekcie; reszta pracuje na złotówkach i nie wie, skąd są dane. Darmowe i bez klucza; NBP podaje tylko złoto, dlatego Yahoo. Kopia w `output/metal_prices.csv` pozwala pracować bez sieci. Wejścia: `settings` ← MetalSettings, `locator` ← InputFileLocator; wyjście `prices` → PriceForecaster, EventStudy, MetalAnalyzer.

Uwaga: to ceny hurtowe (spot/futures), nie ceny w sklepie — marżę dealera, VAT i skup dolicza MetalProduct.

## settings
`history_from` (start pobierania) i `price_cache_hours` (świeżość kopii).

## locator
Folder `output` na kopię.

## TICKERS
Symbole Yahoo: `gold` GC=F, `silver` SI=F, `platinum` PL=F, `usdpln` PLN=X.

## prices()
Wyjście bloku: MetalPriceHistory. Świeża kopia → bez sieci; inaczej pobiera; błąd pobierania → stara kopia (z komunikatem); brak kopii → `RuntimeError`. Braki do 5 dni są uzupełniane poprzednią wartością (święta na różnych giełdach), dni bez którejkolwiek ceny są pomijane; mniej niż 500 notowań → błąd.
