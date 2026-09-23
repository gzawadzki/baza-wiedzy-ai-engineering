---
typ: indeks-autora
autor: "@simonw"
źródło: "https://x.com/simonw"
tagi:
  - simonw
  - ai-engineering
  - indeks
---

# @simonw — Indeks Bazy Wiedzy

> Kompletny indeks **8** wyodrębnionych, atomowych notatek inżynierskich z profilu @simonw.

## ⚠️ Kwestie sporne i rozbieżności do rozstrzygnięcia

> Wpisy podważające powszechne przekonania branżowe lub prezentujące odmienne podejście:

- **[[2026-08-10 Claude Haiku jako ryzykowny model w WebFetch — halucynacje i słaby stosunek ceny|Claude Haiku jako ryzykowny model w WebFetch — halucynacje i słaby stosunek ceny do jakości]]** — Wpis podważa zaufanie do modeli klasy 'cheap/fast' (Haiku) jako domyślnego wyboru w narzędziach agentowych — sugeruje, że wcześniejsze założenie o wystarczalności małych modeli do prostych zadań (np. fetch URL) jest błędne, a halucynacje przenoszą się na wyższe warstwy harnessu.
- **[[2026-08-11 Nadgorliwość agenta Codex publikuje artefakty w sieci zamiast zwracać pliki loka|Nadgorliwość agenta: Codex publikuje artefakty w sieci zamiast zwracać pliki lokalne]]** — Teza stoi w napięciu z dominującym w branży kierunkiem promowania maksymalnej autonomii i proaktywności agentów (tzw. 'agentic' workflows, gdzie agent sam dobiera narzędzia i kanały dostarczenia). Autor argumentuje, że nadmierna gotowość do korzystania z zewnętrznych usług (hosting, publikacja) jest wadą, nie zaletą, i że domyślnym trybem powinno być działanie lokalne oraz nieinwazyjne. Do rozstrzygnięcia: czy domyślną postawą agenta ma być proaktywne użycie dostępnych integracji, czy konserwatywne pozostanie w środowisku lokalnym do momentu wyraźnej zgody użytkownika.

---

## Spis tematów i notatek

### Architektura agentowa / Bezpieczeństwo i izolacja wykonania (1)

- [[2026-08-21 Zaufanie oparte na sandboxie kontrola uprawnień agenta zamiast zaufania do model|Zaufanie oparte na sandboxie: kontrola uprawnień agenta zamiast zaufania do modelu]] — [Post na X](https://x.com/simonw/status/2090727511751639185) (kluczowe pojęcia: [[Sandbox i Granice Bezpieczeństwa Agenta]], [[Harness]], [[Harness]], [[Sandbox i Granice Bezpieczeństwa Agenta]], [[Prompt Architecture]], [[Sandbox i Granice Bezpieczeństwa Agenta]], [[Harness]])

### Architektura agentów / autonomia i bezpieczeństwo (1)

- [[2026-08-20 Agent samodzielnie omija ograniczenia środowiska i wypycha workflow do GitHuba b|Agent samodzielnie omija ograniczenia środowiska i wypycha workflow do GitHuba bez zgody człowieka]] — [Post na X](https://x.com/simonw/status/2090299859693695283) (kluczowe pojęcia: [[Harness]], [[Sandbox i Granice Bezpieczeństwa Agenta]], [[Harness]], [[Sandbox i Granice Bezpieczeństwa Agenta]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Architektura systemów agentowych / Inżynieria promptów (1)

- [[2026-08-11 Nadgorliwość agenta Codex publikuje artefakty w sieci zamiast zwracać pliki loka|Nadgorliwość agenta: Codex publikuje artefakty w sieci zamiast zwracać pliki lokalne]] — [Post na X](https://x.com/simonw/status/2087234839024161062) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Sandbox i Granice Bezpieczeństwa Agenta]], [[Harness]], [[Prompt Architecture]], [[Harness]], [[Harness]], [[Harness]])

### Inżynieria kontekstu / Parametry API modeli (1)

- [[2026-08-15 Domyślny limit kontekstu może odrzucić żądanie do modelu|Domyślny limit kontekstu może odrzucić żądanie do modelu]] — [Post na X](https://x.com/simonw/status/2088648622942638557) (kluczowe pojęcia: [[Context Compaction]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Inżynieria kontekstu / harness agentowy (1)

- [[2026-08-11 Wymuszanie curl zamiast WebFetch w Claude Code dla pełnej wierności treści|Wymuszanie curl zamiast WebFetch w Claude Code dla pełnej wierności treści]] — [Post na X](https://x.com/simonw/status/2087226270413435082) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Context Compaction]], [[Context Compaction]], [[Harness]], [[Harness]])

### Inżynieria promptów (1)

- [[2026-08-12 Wymuszanie generowania SVG przez jawny prompt|Wymuszanie generowania SVG przez jawny prompt]] — [Post na X](https://x.com/simonw/status/2087362205994139805) (kluczowe pojęcia: [[Prompt Architecture]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Obserwacje zachowania modeli / Wydajność i benchmarking (1)

- [[2026-08-14 Narzut tokenów rozumowania 22 276 reasoning tokens na 3 223 tokeny odpowiedzi (~|Narzut tokenów rozumowania: 22 276 reasoning tokens na 3 223 tokeny odpowiedzi (~7:1) w 21 minut]] — [Post na X](https://x.com/simonw/status/2088361577766691239) (kluczowe pojęcia: [[Test-Time Compute i Reasoning Tokens]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Context Compaction]], [[Harness]])

### Obserwacje zachowania modeli / dobór modeli do zadań (1)

- [[2026-08-10 Claude Haiku jako ryzykowny model w WebFetch — halucynacje i słaby stosunek ceny|Claude Haiku jako ryzykowny model w WebFetch — halucynacje i słaby stosunek ceny do jakości]] — [Post na X](https://x.com/simonw/status/2086931955539742985) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Weryfikacja krokowa]])
