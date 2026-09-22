---
typ: pojęcie
aliases: [Compaction, Kompakcja kontekstu, Context Window Management]
tagi: [agenci, kontekst, harness, optymalizacja]
źródła:
  - "[[Kun Chen — Baza Wskazówek i Komentarzy]]"
---

# Context Compaction

**Context Compaction** (kompakcja kontekstu) to proces kompresji, czyszczenia lub streszczania historii sesji agenta w celu zwolnienia miejsca w oknie kontekstowym (`context window`) bez utraty informacji krytycznych dla dalszego wykonania zadania.

W miarę jak agent wykonuje narzędzia (bash, edycje, odczyty dużych plików), kontekst ulega degradacji (*context drift*, *context saturation*) oraz zbliża się do twardego limitu okna.

## Kluczowe wyzwania inżynierskie

1. **Kiedy kompaktować (Decision timing)**:
   - Zbyt wczesna kompakcja ucina stan i zależności potrzebne do bieżącego etapu.
   - Zbyt późna kompakcja grozi błędem `context_length_exceeded` lub drastycznym spadkiem precyzji modelu (*lost in the middle*).
2. **Kompakcja natychmiastowa vs opóźniona**:
   - Jak wskazuje Kun Chen, natychmiastowa kompakcja po przekroczeniu progu tokenów (*instant compaction*) jest anty-wzorcem.
   - Kompakcja powinna nastąpić w **bezpiecznym punkcie** ([[Bezpieczny punkt kompaktowania]]), np. po zakończeniu logicznego podzadania lub testu.
3. **Automatyzacja vs ręczne wywołanie**:
   - Zamiast sztywnych heurystyk (np. zawsze po 50k tokenów) decyzję można delegować do wyspecjalizowanego klasyfikatora lub modelu System One (np. [[Jev]], `compact-adviser`), który klasyfikuje czy obecny stan jest bezpieczny do ścięcia.

## Powiązane

- [[Bezpieczny punkt kompaktowania]]
- [[Checkpointing sesji agenta]]
- [[Persistencja stanu agenta]]
- [[Jev]]
- [[Harness]]
