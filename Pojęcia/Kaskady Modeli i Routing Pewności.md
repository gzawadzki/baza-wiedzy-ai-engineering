---
typ: pojęcie
aliases: [Kaskada modeli, Model Tiering, Routing probabilistyczny, Escalation Policy]
tagi: [architektura, routing, koszty, modele, ewaluacja]
źródła:
  - "[[HamelHusain — Baza Wskazówek i Komentarzy]]"
  - "[[JustinLin610 — Baza Wskazówek i Komentarzy]]"
  - "[[karminski3 — Baza Wskazówek i Komentarzy]]"
---

# Kaskady Modeli i Routing Pewności

**Kaskada modeli** (*Model Cascading*) to wzorzec architektoniczny polegający na kierowaniu zapytań najpierw do taniego, szybkiego modelu (lub modelu decyzyjnego typu [[Jev]]), a eskalowaniu do drogiego modelu generatywnego (np. Claude Opus, o3) tylko w przypadku braku pewności lub wysokiej złożoności zadania.

## Pułapka log-probabilities (obserwacja Hamela Husaina)

Wielu inżynierów zakłada, że kaskadę można oprzeć bezpośrednio na prawdopodobieństwach tokenów (`logprobs`) zwracanych przez komercyjne LLM:
- **Problem:** W nowoczesnych modelach instrukcyjnych log-probs są często bardzo słabo skalibrowane (model potrafi halucynować z 99% pewnością).
- **Rozwiązanie:** Próg eskalacji kaskady (`escalation threshold`) musi być wyznaczony empirycznie na statystycznym zbiorze walidacyjnym ([[Eval Set z realnych sesji]]), a nie przyjęty intuicyjnie.

## Architektura deterministyczna wg Junyanga Lina (Qwen)

Zamiast wewnętrznego, nieprzewidywalnego routingu opartego na MoE w gigantycznych modelach, Lin rekomenduje **strategiczny dobór modeli według złożoności zadania**:
1. Zadania wąskie, deterministyczne i szybkie edycje kodu -> dedykowany mały model lokalny (np. Qwen-Coder-7B).
2. Zadania strategiczne, planowanie architektury -> model top-tier.
3. Decyzję podejmuje kod zewnętrzny ([[Harness]]) na podstawie metryk, a nie sam model.

## Powiązane

- [[Jev]]
- [[TypeSafe — przewodnik praktyczny]]
- [[Eval Set z realnych sesji]]
- [[Harness]]
