---
typ: pojęcie
aliases: [Checkpointing sesji agenta, Checkpoint, Session Checkpoint, Stan kontrolny]
tagi:
  - agenci
  - kontekst
  - checkpointing
  - persistencja
  - harness
źródła:
  - "[[kunchenguid — Indeks]]"
---

# Checkpointing sesji agenta

**Checkpointing sesji agenta** to mechanizm tworzenia zrzutów stanu (migawki pamięci, zmodyfikowanych plików, zmiennych środowiskowych i planu działania) w określonych punktach cyklu życia agenta, umożliwiający bezpieczne cofanie zmian (*time-travel debugging*) oraz resetowanie okna kontekstowego bez utraty postępu.

## Kluczowe zastosowania checkpointów

1. **Baza pod [[Bezpieczny punkt kompaktowania|kompakcję kontekstu]]:**
   - Zanim harness uruchomi procedurę `/compact` lub ucięcie historii tokenów, tworzy trwały checkpoint na dysku. Jeśli model po kompakcji zgubi wątek, harness może przywrócić sesję z ostatniego checkpointu.
2. **Ochrona przed pętlami halucynacji i degradacją:**
   - Gdy agent wpadnie w pętlę nieskutecznych edycji lub uszkodzi strukturę projektu, checkpoint pozwala cofnąć całe drzewo robocze do ostatniego stabilnego stanu bez restartowania całego zadania od zera.
3. **Ewaluacja i etykietowanie danych ([[Eval Set z realnych sesji]]):**
   - Zgodnie z metodologią Kuna Chena, zarejestrowane checkpointy z rzeczywistych sesji inżynierskich są ręcznie etykietowane jako `safe` lub `unsafe`, co tworzy zbiór uczący (*ground truth*) dla modeli decyzyjnych sterujących harnessem (np. [[Jev]], `compact-adviser`).

## Implementacja w architekturze harnessu

- **Poziom Git:** Małe, ukryte commity na gałęzi roboczej przed każdą ryzykowną operacją narzędziową.
- **Poziom plików stanu ([[Persistencja stanu agenta]]):** Serializacja bieżącej pamięci roboczej (`task_state.json` lub pliki Markdown w duchu [[Interpretable Context Methodology]]).
- **Poziom transkryptu:** Zrzut pełnej historii wywołań narzędzi do zewnętrznego logu przed czyszczeniem kontekstu modelu.

## Powiązane

- [[Bezpieczny punkt kompaktowania]]
- [[Context Compaction]]
- [[Persistencja stanu agenta]]
- [[Eval Set z realnych sesji]]
- [[Harness]]
