Rekord danych: rodzaj wydarzenia rynkowego (np. wojna, obniżka stóp, strajk w kopalni) z opisem dla modelu AI, słowami kluczowymi i listą prawdziwych wydarzeń z datami. Listę rodzajów trzyma EventCatalog. Czysty rekord — niepodłączony.

## key
Identyfikator, np. `war`, `rate_cut`.

## label
Opis po polsku, który lokalny model NLI porównuje z tekstem użytkownika („To wydarzenie dotyczy: <label>.”). Bardziej precyzyjny opis = trafniejsze rozpoznanie.

## keywords
Rdzenie słów (małe litery) dla klasyfikatora zapasowego bez AI; słowo pasuje, gdy zaczyna się od rdzenia.

## events
Krotka `(data RRRR-MM-DD, opis)` — dzień, w którym wiadomość dotarła do rynku. Wydarzenia sprzed historii cen są pomijane.
