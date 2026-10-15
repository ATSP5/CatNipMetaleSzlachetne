Katalog 11 rodzajów wydarzeń i ~65 historycznych przykładów od 2004 r.: wojna/geopolityka, kryzys bankowy, krach/recesja, obniżka stóp/QE, podwyżka stóp, szok inflacyjny, cła/wojna handlowa, wybory, ożywienie gospodarcze, zakłócenia podaży metali (kopalnie RPA, sankcje na Rosję), kryzys złotego.

**Dlaczego tu jest:** baza analogii dla analizy scenariuszowej — oddziela wiedzę „co się działo i kiedy” od mierzenia reakcji (EventStudy) i rozpoznawania tekstu (ScenarioClassifier). Lista jest dobrana ręcznie; dopisanie wydarzeń poszerza bazę i zmienia średnie reakcje. Wyjście `events` → EventStudy i ScenarioClassifier.

## CATEGORIES
Krotka EventCategory. Nowy rodzaj = nowa etykieta dla modelu NLI i nowy wiersz analogii.

## events()
Wyjście bloku: zwraca tę instancję.

## categories()
Lista rodzajów.

## get(key)
Rodzaj po kluczu; nieznany → `KeyError`.
