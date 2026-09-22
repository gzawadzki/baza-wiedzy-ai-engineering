---
typ: pojęcie
aliases: [Evaluation Dataset, Ground Truth Sessions, Zbiór walidacyjny sesji]
tagi: [ewaluacja, agenci, dataset, testy]
źródła:
  - "[[Kun Chen — Baza Wskazówek i Komentarzy]]"
---

# Eval Set z realnych sesji

**Eval Set z realnych sesji** to zbiór ewaluacyjny zbudowany z rzeczywistych, zarejestrowanych interakcji inżyniera z agentem kodującym, a nie z syntetycznych benchmarków.

## Ręczne etykietowanie (*Manual Labeling*)

Aby wytrenować lub skalibrować klasyfikatory sterujące pracą agenta (np. decydujące o momencie [[Bezpieczny punkt kompaktowania|kompakcji kontekstu]] lub routingu narzędzi):
1. Pobiera się surowe transkrypcje rzeczywistych sesji z harnessu (narzędzia, edycje, błędy kompilacji, odpowiedzi użytkownika).
2. Człowiek ręcznie oznacza punkty zwrotne (np. *"w tym kroku stan był bezpieczny i można było wyczyścić kontekst"* lub *"w tym kroku kontekst był krytyczny"*).
3. Na tak przygotowanym zbiorze uczy się lekki klasyfikator lub model System One (taki jak [[Jev]]).

## Dlaczego realne sesje przewyższają benchmarki

Syntetyczne benchmarki (np. pojedyncze zadania leetcode czy wyizolowane commity) nie oddają brudnej natury wielogodzinnej pracy:
- błądzeń w repozytorium,
- nieskutecznych prób edycji i cofania zmian,
- interakcji z zewnętrznymi procesami i serwerami.

Eval set z realnych sesji stanowi jedyne rzetelne źródło prawdy (*ground truth*) dla systemów sterujących zachowaniem agenta produkcyjnego.

## Powiązane

- [[Rework Rate]]
- [[Bezpieczny punkt kompaktowania]]
- [[Jev]]
- [[Harness]]
