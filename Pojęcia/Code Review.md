---
typ: pojęcie
aliases: [AI Code Review, Automated Code Review]
tagi: [code-review, weryfikacja, jakosc, agenci]
źródła:
  - "[[Kun Chen — Baza Wskazówek i Komentarzy]]"
---

# Code Review w procesie z AI

**Code Review w procesie z AI** obejmuje procedury przeglądu kodu tworzonego lub modyfikowanego przez autonomiczne modele i agentów inżynieryjnych.

## Heurystyka doboru procedury

Nie każdy artefakt wygenerowany przez LLM wymaga takiego samego rygoru:
- **Heurystyka Kuna Chena**: Jeśli nie poprosiłbyś drugiego programisty o formalny review (np. zmiana stylu CSS, prosty refaktor nazwy), nie uruchamiaj ciężkiego, zewnętrznego agenta review ("no-mistakes").
- **Krytyczne ścieżki**: Review AI powinno skupiać się na logice biznesowej, wyciekach pamięci, bezpieczeństwie i regresji testów.

Szczegółowe zasady opisano w notatce [[Selektywna weryfikacja kodu]].

## Powiązane

- [[Selektywna weryfikacja kodu]]
- [[Weryfikacja krokowa]]
- [[Weryfikator]]
