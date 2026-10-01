---
typ: wpis-źródłowy
autor: "@teortaxesTex"
data: "Mon Sep 21 23:06:12 +0000 2026"
źródło: "https://x.com/teortaxesTex/status/2102172573517701416"
kategoria: "Inżynieria promptów / systemy agentowe"
tagi:
  - teortaxestex
  - ai-engineering
  - wpis-atomowy
---

# Bootstrapowanie agentów LLM przez rubryki, przykłady i stopniowe prowadzenie

- **Autor:** [[teortaxesTex — Indeks|@teortaxesTex]] | **Data:** `Mon Sep 21 23:06:12 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102172573517701416)
- **Konwersacja:** Odpowiedź w dyskusji (@teortaxesTex)
- **Kluczowe pojęcia:** [[Prompt Architecture]] [[Harness|Rubryki oceny]] [[Prompt Architecture|Few-shot prompting]] [[Harness|Bootstrap agenta]] [[Context Compaction|Inżynieria kontekstu]]

---

## Kontekst i problem
Odpowiedź w dyskusji na temat tego, czy modele LLM nadają się do realizacji zadania. Autor twierdzi, że tak, ale kluczowe jest dostarczenie modelom rubryk oceny, przykładów oraz stopniowe bootstrapowanie. Zaznacza, że cały proces jest wolny i wymaga cierpliwości.

## Rada inżynierska
Aby uzyskać użyteczne zachowanie modelu, nie wystarczy ogólny prompt. Należy podać rubryki oceny, konkretne przykłady (few-shot) oraz prowadzić bootstrap krok po kroku, iteracyjnie budując kontekst i oczekiwane zachowania.

## Uwaga / Anty-wzorzec
Próba jednorazowego promptowania bez rubryk i przykładów oraz brak stopniowego bootstrapu prowadzą do nieprzewidywalnych wyników. Nawet przy poprawnym podejściu wdrożenie jest czasochłonne i wolno postępuje.

## Oryginalny cytat
> *"@phl43 btw the answer is "yes, with clankers damn it, you give them rubrics, examples, and bootstrap step by step"
but it's a slow going"*
