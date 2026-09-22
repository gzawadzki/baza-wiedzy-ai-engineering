---
typ: pojęcie
aliases: [Architektura promptów, Prompt Engineering Patterns]
tagi: [prompty, architektura, harness, agenci]
źródła:
  - "[[Kun Chen — Baza Wskazówek i Komentarzy]]"
---

# Prompt Architecture

**Prompt Architecture** (architektura promptów) to inżynierskie podejście do projektowania instrukcji dla modeli AI jako modularnych, wersjonowalnych i testowalnych komponentów oprogramowania, a nie doraźnych fraz językowych.

## Filary architektury promptów

1. **Separacja odpowiedzialności**:
   - Rozdzielenie instrukcji stałych (tożsamość, twarde zasady bezpieczeństwa) od danych dynamicznych (stan sesji, wyniki narzędzi).
2. **Kontrakty wejścia i wyjścia**:
   - Ścisłe definiowanie formatu oczekiwanej odpowiedzi (JSON schema, typowane prymitywy System One, tagi XML).
3. **Współpraca z harnessem**:
   - Zamiast obciążać jeden prompt wszystkimi regułami, zewnętrzny [[Harness]] wstrzykuje wybiórczy kontekst zależnie od etapu zadania (np. [[Interpretable Context Methodology]]).
4. **Odporność na drift i degradację**:
   - Projektowanie promptów pod kątem stabilności w długich sesjach i tolerancji na błędy parsowania.

## Powiązane

- [[Interpretable Context Methodology]]
- [[Stabilność modeli i przestrzeganie promptu]]
- [[Rework Rate]]
- [[Harness]]
