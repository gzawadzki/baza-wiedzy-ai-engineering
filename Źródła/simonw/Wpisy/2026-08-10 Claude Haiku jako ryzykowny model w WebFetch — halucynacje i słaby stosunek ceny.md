---
typ: wpis-źródłowy
autor: "@simonw"
data: "Mon Aug 10 21:45:26 +0000 2026"
źródło: "https://x.com/simonw/status/2086931955539742985"
kategoria: "Obserwacje zachowania modeli / dobór modeli do zadań"
tagi:
  - simonw
  - ai-engineering
  - wpis-atomowy
---

# Claude Haiku jako ryzykowny model w WebFetch — halucynacje i słaby stosunek ceny do jakości

- **Autor:** [[simonw — Indeks|@simonw]] | **Data:** `Mon Aug 10 21:45:26 +0000 2026` | **Źródło:** [Post na X](https://x.com/simonw/status/2086931955539742985)
- **Kluczowe pojęcia:** [[Harness|Halucynacje modeli]] [[Harness|Dobór modelu do zadania]] [[Harness|Claude Code]] [[Harness|WebFetch]] [[Weryfikacja krokowa|Zewnętrzna weryfikacja]]

---

## Kontekst i problem
Autor ocenia aktualną użyteczność Claude Haiku w praktycznych zastosowaniach agentowych. Model ma tendencję do halucynowania i przegrywa z tańszymi/porównywalnie wycenionymi konkurentami (np. GPT-5.6-Luna). Kluczowy problem inżynierski: Haiku jest nadal domyślnym modelem w narzędziu WebFetch w Claude Code, więc ryzyko halucynacji przenosi się na każdą operację pobrania URL-a w pipeline agentowym.

## Rada inżynierska
Nie ufaj modelom klasy 'cheap/fast' w zadaniach wymagających wierności faktograficznej — weryfikuj halucynacje zewnętrznie i nie opieraj krytycznych ścieżek (np. WebFetch) na najtańszym modelu tylko dlatego, że jest domyślny.

## Uwaga / Anty-wzorzec
Pozostawienie słabego, halucynującego modelu jako domyślnego w narzędziu pobierającym treść (WebFetch) — błąd propaguje się do całego kontekstu agenta i zatruwa dalsze rozumowanie.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Wpis podważa zaufanie do modeli klasy 'cheap/fast' (Haiku) jako domyślnego wyboru w narzędziach agentowych — sugeruje, że wcześniejsze założenie o wystarczalności małych modeli do prostych zadań (np. fetch URL) jest błędne, a halucynacje przenoszą się na wyższe warstwy harnessu.

## Oryginalny cytat
> *""Claude Haiku is my current least favorite model - it hallucinates wildly, and is out-performed now by other similarly priced models like GPT-5.6-Luna

Even worse: it seems to still be used by the Claude Code WebFetch tool, which means hallucination risk any time you fetch a URL!""*
