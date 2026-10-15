Rozpoznaje, jakiego rodzaju jest wydarzenie opisane przez użytkownika na stronie (po polsku albo w innym języku). Używa **lokalnego, wielojęzycznego modelu NLI** (domyślnie mDeBERTa-v3 XNLI) w trybie zero-shot: dla każdego rodzaju z EventCatalog ocenia, na ile prawdziwe jest zdanie „To wydarzenie dotyczy: <rodzaj>.”, i zwraca pewność 0–1. Model działa w całości na tym komputerze (CPU albo GPU), wagi (~1 GB) pobiera raz do folderu `models`, ładuje się przy pierwszym scenariuszu (kilkanaście sekund), potem odpowiada w ~1 s.

Bez pakietu `transformers` (oraz `sentencepiece`, `protobuf` dla tokenizera) albo modelu przechodzi na **słowa kluczowe** — strona mówi wtedy, którego modelu użyto.

**Dlaczego tu jest:** oddziela rozumienie tekstu od liczenia wpływu, więc model można wymienić bez ruszania reszty. Duży model językowy (np. przez Ollamę) nie jest potrzebny: liczby i tak pochodzą z historii (EventStudy). Wejścia: `settings` ← MetalSettings (`scenario_model`), `catalog` ← EventCatalog, `locator` ← InputFileLocator; wyjście `classifier` → ScenarioAnalyzer.

## settings
`scenario_model` — identyfikator modelu z Hugging Face.

## catalog
Rodzaje wydarzeń i ich opisy (etykiety dla modelu).

## locator
Folder `models`.

## TEMPLATE
Szablon hipotezy NLI: „To wydarzenie dotyczy: {}.”

## classifier()
Wyjście bloku: zwraca tę instancję (model ładuje się dopiero przy pierwszym `classify`).

## classify(text)
Lista `(klucz rodzaju, pewność 0–1)` od najlepiej pasującego. Pusty tekst → pusta lista. Z modelem NLI pewności są niezależne (kilka rodzajów naraz może mieć wysokie); ze słowami kluczowymi pewność = trafienia / (trafienia + 1).

## model_label
Opis użytego klasyfikatora po ostatnim `classify`.

## problem
Dlaczego model NLI nie działa, albo `None`.
