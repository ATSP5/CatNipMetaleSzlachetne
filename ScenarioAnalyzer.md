Zamienia opis wydarzenia na przewidywaną zmianę cen złota, srebra i platyny:

1. ScenarioClassifier (lokalny model) ocenia, do jakich rodzajów wydarzeń pasuje tekst.
2. Rodzaje z pewnością ≥ 50% (najwyżej 3) dostają wagi proporcjonalne do pewności; gdy żaden nie przekracza 50%, brany jest najlepszy, jeśli ma ≥ 20%; inaczej „nie rozpoznano” i prognoza się nie zmienia.
3. Oczekiwana zmiana = ważona średnia rzeczywistych reakcji cen na historyczne wydarzenia tych rodzajów (EventStudy) × siła; rozrzut = ważone odchylenie tych reakcji × siła.
4. Na ścieżce prognozy wpływ narasta od wartości 1-miesięcznej do 3-miesięcznej, potem wygasa: po kolejnych 12 miesiącach zostaje `persistence` jego wielkości.

**Dlaczego tu jest:** jedyne miejsce, gdzie tekst staje się liczbami — łączy rozpoznanie (AI) z historią (dane). Wejścia: `classifier` ← ScenarioClassifier, `event_study` ← EventStudy; wyjście `scenario` → MetalAnalyzer.

## classifier
ScenarioClassifier.

## event_study
EventStudy.

## MIN_SCORE, FALLBACK_SCORE, MAX_MATCHES
Progi: 0,5 (rodzaj wchodzi do wyniku), 0,2 (najlepszy rodzaj, gdy nic nie przekroczyło 0,5), 3 (najwięcej rodzajów naraz).

## scenario()
Wyjście bloku: zwraca tę instancję.

## analyze(text, severity, persistence)
ScenarioResult. `severity` 0–5 (poza → `ValueError`): 2 = wydarzenie dwa razy silniejsze niż przeciętnie w historii, wpływ i rozrzut ×2. `persistence` 0–1 (poza → `ValueError`): 0 = wpływ znika w ciągu roku po 3. miesiącu, 1 = zostaje na stałe.

## adjustment(result, metal, months)
Dwie tablice dla miesięcy 1..months: zmiana środka i rozrzut (ułamki). MetalAnalyzer mnoży kwantyl q prognozy przez (1 + zmiana + z(q) × rozrzut), gdzie z(0,1) = −1, z(0,9) = +1, więc pasmo się przesuwa i poszerza.
