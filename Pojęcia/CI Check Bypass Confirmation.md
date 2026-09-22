---
typ: pojęcie
aliases: [Wymóg potwierdzenia pominięcia CI, Bypass confirmation, Safe overrides]
tagi: [bezpieczenstwo, ci-cd, agenci, prompt-adherence]
źródła:
  - "[[Kun Chen — Baza Wskazówek i Komentarzy]]"
---

# CI Check Bypass Confirmation

**CI Check Bypass Confirmation** to wzorzec bezpieczeństwa w promptach agentów inżynieryjnych (np. w systemie [[Firstmate Agent|Firstmate]]), uniemożliwiający modelowi bezrefleksyjne pomijanie nieudanych testów lub czerwonych statusów CI.

## Zasada działania reguły

Gdy pipeline CI zgłasza błędy, inżynier może mieć pokusę napisania do agenta: *"ignoruj to i merguj/wypchnij"* (tzw. "yolo").

Prawidłowo zabezpieczony model (taki jak Grok 4.7):
1. **Odmawia prostego zignorowania** na jedno słowo.
2. **Wymusza jawne wskazanie**, które konkretnie czerwone checki użytkownik świadomie decyduje się pominąć i dlaczego.
3. Wymaga potwierdzenia przed wykonaniem nieodwracalnej akcji w repozytorium.

Do ujawnienia tego zachowania niezbędny jest model o wysokim stopniu przestrzegania instrukcji systemowych ([[Stabilność modeli i przestrzeganie promptu]]).

## Powiązane

- [[Stabilność modeli i przestrzeganie promptu]]
- [[Firstmate Agent]]
- [[Selektywna weryfikacja kodu]]
