---
typ: pojęcie
aliases: [Safe Compaction Point, Safe Checkpoint, Granica zadania]
tagi: [agenci, kontekst, harness, bezpieczenstwo]
źródła:
  - "[[Kun Chen — Baza Wskazówek i Komentarzy]]"
---

# Bezpieczny punkt kompaktowania

**Bezpieczny punkt kompaktowania** to moment w sesji agenta, w którym ucięcie lub skompresowanie dotychczasowej historii rozmowy i logów narzędzi nie spowoduje utraty stanu wymaganego do dokończenia bieżącego zadania.

## Kryterium bezpiecznego punktu

Według heurystyki Kuna Chena:
- Punkt jest **bezpieczny**, jeśli stan agenta został utrwalony na dysku (w plikach, testach, commicie gita) i agent nie posiada w pamięci ulotnej (kontekście) niezrealizowanych założeń lub pośrednich wyników.
- Punkt jest **niebezpieczny**, gdy agent znajduje się w trakcie wielokrokowego procesu (np. zmodyfikował 2 z 4 plików i pamięta powiązanie między nimi tylko w promptcie).

## Zastosowanie klasyfikatorów (np. Jev, compact-adviser)

Zamiast ciąć kontekst natychmiast po osiągnięciu progu tokenów, harness agentowy włącza stan podwyższonej czujności:
- Na początku sesji wymagana jest wysoka precyzja (*precision*) — ucinamy tylko w idealnych momentach.
- Przy bardzo wysokim zapełnieniu okna priorytet przesuwa się w stronę czułości (*recall*) — harness musi zaakceptować punkt wystarczająco dobry, by zapobiec przekroczeniu limitu.

## Powiązane

- [[Context Compaction]]
- [[Checkpointing sesji agenta]]
- [[Persistencja stanu agenta]]
- [[Jev]]
- [[Harness]]
