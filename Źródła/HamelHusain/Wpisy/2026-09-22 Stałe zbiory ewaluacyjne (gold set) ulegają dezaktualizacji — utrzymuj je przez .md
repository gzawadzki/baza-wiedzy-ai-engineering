---
typ: wpis-źródłowy
autor: "@HamelHusain"
data: "Tue Sep 22 17:00:01 +0000 2026"
źródło: "https://x.com/HamelHusain/status/2102442807575076880"
kategoria: "Ewaluacja i benchmarki LLM"
tagi:
  - hamelhusain
  - ai-engineering
  - wpis-atomowy
---

# Stałe zbiory ewaluacyjne (gold set) ulegają dezaktualizacji — utrzymuj je przez ciągłą analizę błędów

- **Autor:** [[HamelHusain — Indeks|@HamelHusain]] | **Data:** `Tue Sep 22 17:00:01 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2102442807575076880)
- **Kluczowe pojęcia:** [[Harness|Ewaluacja LLM]] [[Harness|Gold dataset]] [[Harness|Error analysis]] [[Harness|Data drift]] [[Harness|Overfitting ewaluacji]] [[Harness|LLM-as-a-judge]]

---

## Kontekst i problem
Zespół produktowy zbudował ręcznie oznaczony, 'złoty' zbiór ewaluacyjny do pomiaru jakości modelu/promptu. Z czasem produkt, dane wejściowe użytkowników i wymagania się zmieniają, więc test set przestaje odzwierciedlać realne rozkłady i przestaje wykrywać nowe klasy błędów (overfitting ewaluacji, fałszywe poczucie bezpieczeństwa). Autor odpowiada na pytanie, co zrobić, gdy gold set staje się 'stale'.

## Rada inżynierska
Traktuj zbiór ewaluacyjny jako żywy artefakt, a nie jednorazowy deliverable: prowadź regularną analizę błędów (error analysis) na produkcyjnych przypadkach, wyłapuj nowe wzorce awarii i dodawaj je jako nowe przykłady do eval setu. Aktualizuj ewaluacje równolegle z ewolucją produktu i zachowań użytkowników — dopasowanie test setu do realnego rozkładu jest ważniejsze niż jego 'zamrożenie' dla porównywalności między iteracjami.

## Uwaga / Anty-wzorzec
Zamrożenie gold setu raz na zawsze i bezkrytyczne porównywanie wyników względem nieaktualnych danych — prowadzi do optymalizacji pod przestarzały rozkład, pomijania nowych klas błędów i fałszywego wrażenia regresji lub poprawy.

## Oryginalny cytat
> *""Q: What should you do when your "gold" eval dataset becomes stale?

A: Use regular error analysis to find new problems. Keep updating your evals as your product and users change.""*
