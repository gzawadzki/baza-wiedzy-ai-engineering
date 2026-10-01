---
typ: pojęcie
aliases: [External Verifier, Weryfikator zewnętrzny, Automated Judge, Guardrail]
tagi:
  - weryfikacja
  - evals
  - jakosc
  - bezpieczenstwo
źródła:
  - "[[kunchenguid — Indeks]]"
  - "[[HamelHusain — Indeks]]"
  - "[[teortaxesTex — Indeks]]"
  - "[[TypeSafe i Jev — wywiad z Diogo Almeidą]]"
---

# Weryfikator

**Weryfikator** to niezależny od generującego agenta moduł weryfikacyjny (skrypt deterministyczny, test jednostkowy, wyspecjalizowany model decyzji typu [[Jev]] lub zewnętrzny panel sędziowski LLM), którego jedynym zadaniem jest ocena poprawności, bezpieczeństwa i kompletności wygenerowanego artefaktu.

## Zasada asymetrii weryfikacji

Weryfikacja poprawności rozwiązania inżynierskiego jest fundamentalnie tańsza i bardziej niezawodna niż jego synteza:
- Wygenerowanie skomplikowanej funkcji może zająć modelowi tysiące tokenów rozumowania ([[Test-Time Compute i Reasoning Tokens]]).
- Weryfikator (uruchomienie testu w [[Sandbox i Granice Bezpieczeństwa Agenta|sandboxie]], linter AST lub sprawdzenie typowanego kontraktu przez [[Jev]]) ocenia wynik w milisekundach bez ryzyka halucynacji.

## Formy weryfikatorów w systemach produkcyjnych

1. **Weryfikatory deterministyczne (kodowe):**
   - Kompilatory, testy jednostkowe, reguły typowania, skrypty lintera. Są bezwzględnym źródłem prawdy (*ground truth*).
2. **Weryfikatory probabilistyczne / semantyczne ([[Jev]] / LLM-as-a-judge):**
   - Stosowane tam, gdzie brak twardych testów matematycznych (np. zgodność tonu, kompletność odpowiedzi, spójność architektury).
   - Wymagają empirycznej kalibracji progów pewności na zbiorach walidacyjnych ([[Eval Set z realnych sesji]]), jak wskazuje [[HamelHusain — Indeks|Hamel Husain]].
3. **Bramki selektywne ([[Selektywna weryfikacja kodu]]):**
   - Zgodnie z heurystyką Kuna Chena weryfikator nie powinien blokować każdej drobnej operacji, a jedynie zmiany, które w normalnym procesie skierowano by do formalnego [[Code Review]].

## Powiązane

- [[Selektywna weryfikacja kodu]]
- [[Weryfikacja krokowa]]
- [[Eval Set z realnych sesji]]
- [[Rework Rate]]
- [[CI Check Bypass Confirmation]]
- [[Harness]]
- [[Jev]]
