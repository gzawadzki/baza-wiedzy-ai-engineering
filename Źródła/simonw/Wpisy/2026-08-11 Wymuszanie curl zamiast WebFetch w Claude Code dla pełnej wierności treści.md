---
typ: wpis-źródłowy
autor: "@simonw"
data: "Tue Aug 11 17:14:56 +0000 2026"
źródło: "https://x.com/simonw/status/2087226270413435082"
kategoria: "Inżynieria kontekstu / harness agentowy"
tagi:
  - simonw
  - ai-engineering
  - wpis-atomowy
---

# Wymuszanie curl zamiast WebFetch w Claude Code dla pełnej wierności treści

- **Autor:** [[simonw — Indeks|@simonw]] | **Data:** `Tue Aug 11 17:14:56 +0000 2026` | **Źródło:** [Post na X](https://x.com/simonw/status/2087226270413435082)
- **Konwersacja:** Odpowiedź w dyskusji (@asmeurer)
- **Kluczowe pojęcia:** [[Harness|Claude Code]] [[Harness|WebFetch]] [[Harness|curl]] [[Harness|Harness agentowy]] [[Context Compaction|Inżynieria kontekstu]] [[Context Compaction|Kompresja kontekstu]] [[Harness|Narzędzia agentowe]] [[Harness|Halucynacje agenta]]

---

## Kontekst i problem
Dyskusja dotyczy tego, jak agent kodujący (Claude Code) pozyskuje treści z sieci. Wbudowane narzędzie WebFetch nie zwraca surowego dokumentu — przepuszcza pobraną stronę przez model, który ją streszcza i przycina, więc agent widzi interpretację, a nie oryginał. Problem ujawnia się przy zadaniach wymagających dosłownej treści: czytania długiej dokumentacji, surowego HTML, odpowiedzi API, nagłówków HTTP, fragmentów kodu do skopiowania czy diagnostyki błędów sieciowych.

## Rada inżynierska
Gdy agent musi przeczytać całość materiału źródłowego, jawnie instruuj go w prompcie/system prompcie: 'użyj curl, nie WebFetch'. curl daje surowy, nieprzetworzony strumień (pełny tekst, nagłówki, kody statusu, możliwość zapisu do pliku), podczas gdy WebFetch wprowadza warstwę podsumowania i utraty informacji. To praktyczna reguła inżynierii kontekstu: narzędzie pobierające powinno być dobierane do wymaganej wierności danych, a nie do wygody — dla weryfikacji i precyzyjnej pracy na treści wybieraj transport niskopoziomowy, dla szybkiego rekonesansu wystarczy warstwa streszczająca.

## Uwaga / Anty-wzorzec
Traktowanie WebFetch jako źródła prawdy. Agent otrzymuje streszczenie zamiast oryginału, co prowadzi do halucynacji szczegółów, gubienia fragmentów kodu, pomijania istotnych sekcji długich dokumentów i błędnych wniosków o zachowaniu API. Efekt nasila się przy długich stronach, gdzie kompresja kontekstu jest najbardziej agresywna.

## Oryginalny cytat
> *"@asmeurer I tend to tell Claude Code "use curl, not WebFetch, you need to read the whole thing""*
