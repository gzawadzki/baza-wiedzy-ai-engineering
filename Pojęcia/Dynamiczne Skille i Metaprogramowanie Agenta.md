---
typ: pojęcie
aliases: [Dynamic Micro-Skills, Skill as Code, Metaprogramowanie skilli]
tagi: [agenci, skille, architektura, harness, metaprogramowanie]
źródła:
  - "[[karminski3 — Baza Wskazówek i Komentarzy]]"
  - "[[HamelHusain — Baza Wskazówek i Komentarzy]]"
---

# Dynamiczne Skille i Metaprogramowanie Agenta

W zaawansowanej inżynierii agentowej odchodzi się od traktowania skilli (umiejętności agenta) jako statycznych dokumentów tekstowych (*„skill to plik Markdown wklejany do promptu”*).

## Izomorfizm kodu i danych w skillach (Karminski)

Zamiast utrzymywać setki ręcznie napisanych instrukcji:
1. **Skill jako generator:** Agent posiada bazowe makro-skille, które dynamicznie generują wyspecjalizowane **Micro-Skille** w czasie wykonania (metaprogramowanie).
2. **Kompilacja pod wejście:** Jeśli agent napotyka nieznany format danych, generuje tymczasowy, lekki kod/parser, wykonuje zadanie i zrzuca go z pamięci.
3. Pozwala to na drastyczną redukcję stałego okna kontekstowego bez utraty elastyczności.

## Skill Discovery i klastrowanie błędów (Hamel Husain)

W procesie ewaluacji agentów stosuje się tzw. *Eval Skills Plugin*:
- Dedykowany moduł agentowy analizuje logi nieudanych uruchomień,
- Inteligentnie sampluje błędy i grupuje je w **tryby awarii** (*failure modes*),
- Automatycznie proponuje nowe instrukcje lub testy jednostkowe zapobiegające powtórzeniu danego błędu.

## Powiązane

- [[Prompt Architecture]]
- [[Harness]]
- [[Eval Set z realnych sesji]]
- [[Rework Rate]]
