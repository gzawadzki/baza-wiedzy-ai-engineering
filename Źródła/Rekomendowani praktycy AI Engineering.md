---
typ: źródło
aliases: [AI Engineering Practitioners, Źródła wiedzy AI, Obserwowani eksperci]
tagi:
  - ai-engineering
  - agenci
  - prompt-engineering
  - evals
  - kontekst
  - harness
  - zrodla
---

# Rekomendowani praktycy AI Engineering do bazy wiedzy

Zestawienie wybitnych inżynierów i badaczy praktyków z platformy X/Twitter, których autorskie wpisy i techniczne komentarze cechują się najwyższą gęstością merytoryczną w obszarach: architektury harnessów, systemów agentowych, zarządzania oknem kontekstowym i rygorystycznej ewaluacji (evals).

---

## Elitarna czwórka (produkcja, harnessy, ewaluacja)

### 1. Hamel Husain — `@HamelHusain`
- **Rola / Afiliacja:** Niezależny konsultant, ex-GitHub (współtwórca GitHub Copilot), autor branżowego kursu *Evals for AI*.
- **Dlaczego warto:** Najbardziej bezkompromisowy praktyk w temacie **ewaluacji LLM i error analysis**. Zamiast syntetycznych benchmarków pokazuje, jak budować zbiory testowe z realnego ruchu, diagnozować fałszywe alarmy i mierzyć jakość modeli w kodzie.
- **Kluczowe pojęcia do vaulta:** `[[Eval Set z realnych sesji]]`, `[[Weryfikator]]`, `[[Error Analysis]]`, `[[LLM-as-judge failure modes]]`.

### 2. Simon Willison — `@simonw`
- **Rola / Afiliacja:** Twórca Datasette, współtwórca Django, niezależny badacz bezpieczeństwa AI.
- **Dlaczego warto:** Prekursor badań nad podatnościami modeli (odkrywca terminu *Prompt Injection*). Publikuje surowe logi, konkretne instrukcje CLI i analizy zachowania modeli w środowisku deweloperskim.
- **Kluczowe pojęcia do vaulta:** `[[Prompt Injection]]`, `[[CLI Agent Harness]]`, `[[Tool Calling Security]]`.

### 3. Eugene Yan — `@eugeneyan`
- **Rola / Afiliacja:** Applied ML/LLM Engineer w Amazon, autor branżowych syntez inżynierskich na *eugeneyan.com*.
- **Dlaczego warto:** Publikuje kompletne frameworki decyzyjne i drzewa decyzyjne dla inżynierów (np. kiedy RAG vs Fine-tuning vs In-Context Learning, jak projektować systemy o niskiej latencji i kosztach).
- **Kluczowe pojęcia do vaulta:** `[[Cost and Latency Tradeoffs]]`, `[[Deterministic vs Generative Routing]]`, `[[RAG Architecture Patterns]]`.

### 4. Armin Ronacher — `@mitsuhiko`
- **Rola / Afiliacja:** Twórca frameworka Flask, Jinja oraz współtwórca Sentry.
- **Dlaczego warto:** Spojrzenie twardego inżyniera systemowego na AI. Skupia się na architekturze protokołów komunikacji agentowej (np. Model Context Protocol — MCP), izolacji środowisk wykonawczych, sandboxingu narzędzi i harnessach produkcyjnych.
- **Kluczowe pojęcia do vaulta:** `[[Model Context Protocol (MCP)]]`, `[[Sandbox Isolation]]`, `[[Agent Protocol Design]]`.

---

## Architektura agentowa, optymalizacja promptów i kontekst

### 5. Omar Khattab — `@lateinteraction`
- **Rola / Afiliacja:** MIT / Stanford, twórca frameworka **DSPy** oraz architektury **ColBERT**.
- **Dlaczego warto:** Twórca paradygmatu *„Prompting as Compiling”*. Zamiast ręcznego pisania promptów (tzw. prompt craftingu) wprowadza programowalne moduły, kompilatory promptów i automatyczną optymalizację wag i telemetrii.
- **Kluczowe pojęcia do vaulta:** `[[Prompt Architecture]]`, `[[DSPy Optimization]]`, `[[Programmatic Prompt Compilation]]`.

### 6. Harrison Chase — `@hwchase17`
- **Rola / Afiliacja:** CEO LangChain / LangGraph.
- **Dlaczego warto:** Główne źródło wiedzy o architekturze maszyn stanowych dla agentów (*state machines*, cykliczne grafy zależności, mechanizmy *human-in-the-loop* i kontrola punktów cofania stanu).
- **Kluczowe pojęcia do vaulta:** `[[Firstmate i Agenci Wykonawczy]]`, `[[State Machine Agent Loop]]`, `[[Human-in-the-loop]]`.

### 7. Lance Martin — `@RLanceMartin`
- **Rola / Afiliacja:** LangChain Applied AI, ex-Meta.
- **Dlaczego warto:** Specjalizuje się w dekonstrukcji wzorców pamięci agentowej, planowania i wieloetapowego retrievalu za pomocą precyzyjnych schematów architektonicznych.
- **Kluczowe pojęcia do vaulta:** `[[Context Compaction]]`, `[[Memory Retention Patterns]]`, `[[Agentic RAG]]`.

### 8. Jerry Liu — `@jerryjliu0`
- **Rola / Afiliacja:** CEO LlamaIndex.
- **Dlaczego warto:** Koncentruje się na inżynierii kontekstu (*Context Engineering*): zaawansowane techniki rerankingu, dzielenia na fragmenty (chunking), kompresji i usuwania szumu z okna kontekstowego.
- **Kluczowe pojęcia do vaulta:** `[[Context Compaction]]`, `[[Reranking]]`, `[[Lost in the Middle Mitigation]]`.

---

## Metodologia naukowa i systemowa

### 9. Shreya Shankar — `@sh_reya`
- **Rola / Afiliacja:** UC Berkeley, badaczka systemów danych i ewaluacji modeli.
- **Dlaczego warto:** Rygorystyczna metodologia pomiaru dryfu modeli, pułapek automatycznych sędziów LLM (*LLM-as-a-judge bias*) i stabilności pipeline'ów predykcyjnych.
- **Kluczowe pojęcia do vaulta:** `[[Eval Set z realnych sesji]]`, `[[Judge Calibration]]`, `[[Model Drift Detection]]`.

### 10. Chip Huyen — `@chipro`
- **Rola / Afiliacja:** Autorka bestsellerów *Designing Machine Learning Systems* oraz *AI Engineering*, ex-NVIDIA/Netflix.
- **Dlaczego warto:** Kompleksowa, podręcznikowa taksonomia inżynierii AI: od zarządzania kosztami inferencji, przez architekturę pamięci podręcznej, po bezpieczeństwo systemów opartych na modelach fundamentowych.
- **Kluczowe pojęcia do vaulta:** `[[Stabilność modeli i przestrzeganie promptu]]`, `[[Inference Caching]]`, `[[System Design for AI]]`.

---

## Jak wykorzystać te profile w ekstraktorze

Ekstraktor w katalogu `extractor/` można uruchomić dla dowolnego z tych autorów za pomocą flagi `--handle`:

```bash
# Ekstrakcja Hamela Husaina (fokus: evals i błędy ewaluacji)
python extractor/extract_kunchen_tips.py --handle HamelHusain --output "Źródła/Hamel Husain — Baza Wskazówek i Komentarzy.md"

# Ekstrakcja Simona Willisona (fokus: prompt security i harnessy CLI)
python extractor/extract_kunchen_tips.py --handle simonw --output "Źródła/Simon Willison — Baza Wskazówek i Komentarzy.md"

# Ekstrakcja Armina Ronachera (fokus: protokoły agentowe i narzędzia)
python extractor/extract_kunchen_tips.py --handle mitsuhiko --output "Źródła/Armin Ronacher — Baza Wskazówek i Komentarzy.md"
```
