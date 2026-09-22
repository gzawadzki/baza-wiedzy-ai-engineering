---
typ: pojęcie
aliases: [State Persistence, Trwały stan sesji, Pamięć agenta]
tagi: [agenci, stan, architektura, harness]
źródła:
  - "[[Kun Chen — Baza Wskazówek i Komentarzy]]"
---

# Persistencja stanu agenta

**Persistencja stanu agenta** to praktyka utrwalania kluczowych faktów, podjętych decyzji, planów i wyników pośrednich poza ulotną pamięcią podręczną modelu (oknem kontekstowym).

## Ulotny kontekst vs trwały nośnik

Gdy agent operuje wyłącznie w ramach jednej ciągłej konwersacji:
1. Każde zresetowanie lub ucięcie sesji (`/compact`, `context window reset`) grozi utratą kontekstu.
2. Z zapełnianiem kontekstu rośnie ryzyko halucynacji i ignorowania wcześniejszych wytycznych (*context drift*).

Rozwiązaniem jest wymuszenie zapisu stanu na trwałym nośniku (system plików, git, baza danych):
- **Artefakty na dysku**: pliki specyfikacji, pliki `TODO.md`, notatki Markdown (np. w duchu [[Interpretable Context Methodology]]).
- **Commity Git**: małe, atomowe commity utrwalające działający kod przed przejściem do kolejnego kroku.
- **Logi i checkpointy**: jawna serializacja stanu do formatu maszynowego.

Dzięki temu agent w dowolnym momencie może zrzucić pamięć podręczną i odtworzyć swój stan z dysku, co bezpośrednio umożliwia wyznaczenie [[Bezpieczny punkt kompaktowania|bezpiecznego punktu kompaktowania]].

## Powiązane

- [[Context Compaction]]
- [[Bezpieczny punkt kompaktowania]]
- [[Interpretable Context Methodology]]
- [[Harness]]
