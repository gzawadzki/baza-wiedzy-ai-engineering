---
typ: pojęcie
aliases: [No-mistakes verification, Selektywna weryfikacja]
tagi: [weryfikacja, code-review, harness, jakosc]
źródła:
  - "[[Kun Chen — Baza Wskazówek i Komentarzy]]"
---

# Selektywna weryfikacja kodu (No-Mistakes)

**Selektywna weryfikacja kodu** to reguła inżynierska zapobiegająca nadmiarowemu narzutowi procedur testowych i zewnętrznych weryfikatorów w workflow agentowym.

## Heurystyka decyzyjna Kuna Chena

> *"Czy poprosiłbym innego człowieka o code review dla tej zmiany?"*

- Jeśli odpowiedź brzmi **NIE** (np. trywialna zmiana formatowania, drobna poprawka literówki, prosty rename w małym module), to uruchamianie kosztownych agentów weryfikacyjnych (no-mistakes / sub-agent review) generuje niepotrzebny szum, fałszywe alarmy i spowalnia iterację.
- Jeśli odpowiedź brzmi **TAK** (zmiana logiki biznesowej, refaktoryzacja rdzenia, obsługa transakcji finansowych, uprawnień), należy wdrożyć pełny proces weryfikacji.

## Anty-wzorzec: Totalna weryfikacja

Wymuszanie rygorystycznego review LLM-em dla każdego wywołania narzędzia prowadzi do:
- eksplozji kosztów tokenów,
- drastycznego wydłużenia latencji,
- „zmęczenia alertami” (alert fatigue) u inżyniera nadzorującego agenta.

## Powiązane

- [[Weryfikator]]
- [[Harness]]
- [[Praca z harnessem]]
