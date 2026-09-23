---
typ: wpis-źródłowy
autor: "@HamelHusain"
data: "Wed Aug 26 15:03:00 +0000 2026"
źródło: "https://x.com/HamelHusain/status/2092628886572200169"
kategoria: "Architektura agentów i protokoły integracyjne (MCP / WebMCP)"
tagi:
  - hamelhusain
  - ai-engineering
  - wpis-atomowy
---

# WebMCP: protokół współdzielonej pracy agentów i ludzi na interfejsie przeglądarki

- **Autor:** [[HamelHusain — Indeks|@HamelHusain]] | **Data:** `Wed Aug 26 15:03:00 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2092628886572200169)
- **Kluczowe pojęcia:** [[Harness|WebMCP]] [[Harness|MCP]] [[Harness|Agent kodujący]] [[Harness|Notebook interaktywny]] [[Harness|Runbook]] [[Harness|Ewaluacja modeli fundacyjnych]] [[Harness|Open Source]] [[Harness|Human-in-the-loop]]

---

## Kontekst i problem
OpenAI opublikowało blog post (autorstwa Jeremy'ego Lewi) opisujący WebMCP — podejście do integracji agentów z UI, w którym protokół jest wystawiany bezpośrednio przez przeglądarkę, a nie przez serwer API czy klasyczny serwer MCP. Celem jest scenariusz współdzielonej pracy człowieka i agenta nad tym samym interfejsem (np. równoczesna edycja komórek notebooka). Autor wątku zwraca uwagę, że to nowy wariant architektoniczny o odmiennych kompromisach niż MCP/API, oraz że wraz z nim powstał nowy typ notebooka (open source), w którym pliki są po prostu markdownem, a użytkownik przyprowadza własnego agenta kodującego. Notebook ma służyć kurowaniu runbooków i wysokiej jakości przykładów uruchamiania ewaluacji modeli fundacyjnych na własnej infrastrukturze — bo wymaga interaktywnego dłubania w stanie długotrwałych zadań przy jednoczesnym notowaniu inline.

## Rada inżynierska
Gdy projektujesz interakcję, w której agent i człowiek mają współpracować na tym samym UI (a nie tylko wywoływać operacje w tle), rozważ WebMCP zamiast klasycznego MCP/API: wystawienie możliwości bezpośrednio przez przeglądarkę daje wspólny kontekst stanu widocznego dla obu stron. Równolegle stosuj zasadę 'meet people where they are': pliki w formacie otwartym (markdown), brak vendor lock-in na agenta — użytkownik przyprowadza własnego agenta kodującego. Taki zestaw sprawdza się w zadaniach wymagających jednoczesnego notowania i interaktywnego sterowania stanem długotrwałych zadań (runbooki, ewaluacje modeli fundacyjnych).

## Uwaga / Anty-wzorzec
Traktowanie WebMCP jako zamiennika MCP/API bez analizy kompromisów — protokół wystawiany przez przeglądarkę ma inne ograniczenia (m.in. zakres, bezpieczeństwo, izolację od backendu) i nie jest uniwersalnym rozwiązaniem. Anty-wzorcem jest też zamknięty format plików i wymuszanie konkretnego agenta, co łamie zasadę 'bring your own agent'.

## Oryginalny cytat
> *"1) Shows an example of building with WebMCP, meant for when you want agents and and humans to collaborate on using a UI (like co-editing notebook cells). It's different than MCPs or APIs in that its exposed directly through the browser. Read the post for discussion of the tradeoffs. 2) They created a new kind of notebook which works with WebMCP that prioritizes meeting people where they are: you bring your own coding agent and files are just markdown."*
