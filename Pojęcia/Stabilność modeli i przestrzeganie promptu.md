---
typ: pojęcie
aliases: [System Prompt Adherence, Model Stability, Benchmark Skepticism]
tagi: [modele, prompt-engineering, ewaluacja, stabilnosc]
źródła:
  - "[[Kun Chen — Baza Wskazówek i Komentarzy]]"
---

# Stabilność modeli i przestrzeganie promptu

W inżynierii agentowej wybór modelu fundamentowego (LLM) zależy w mniejszym stopniu od syntetycznych benchmarków, a w kluczowym od **przewidywalności** i **zdolności do bezwzględnego przestrzegania instrukcji systemowych** (*system prompt adherence*).

## Kluczowe wymiary oceny modelu

1. **Przestrzeganie system promptu (Adherence)**:
   - Wiele modeli ignoruje negacje lub warunki brzegowe zdefiniowane w promptcie systemowym (np. wymóg potwierdzenia pominięcia testów CI).
   - Modele o wysokiej zgodności ujawniają mechanizmy bezpieczeństwa zapisane w harnessie, które na słabszych modelach pozostawały uśpione.
2. **Stabilność vs "Spikiness"**:
   - Modele typu *spiky* mają momenty geniuszu, ale przeplatają je trywialnymi, trudnymi do przewidzenia wpadkami.
   - Modele *stabilne* oferują stały, bezpieczny poziom wykonania, co jest kluczowe w systemach produkcyjnych.
3. **Konserwatyzm w działaniu**:
   - Model konserwatywny prosi o potwierdzenie lub dopytuje przed wykonaniem nieodwracalnych akcji, co minimalizuje kosztowne pomyłki.
4. **Sceptycyzm wobec publicznych benchmarków**:
   - Syntetyczne rankingi (np. benchmarki kodowania czy gry 3D) nie odzwierciedlają wielogodzinnej pracy agenta w rzeczywistym repozytorium z narzędziami i brudnym kontekstem.

## Powiązane

- [[Harness]]
- [[Prompt Architecture]]
- [[Rework Rate]]
- [[Kun Chen — Baza Wskazówek i Komentarzy]]
