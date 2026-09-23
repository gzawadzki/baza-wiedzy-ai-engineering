---
typ: pojęcie
aliases: [Reasoning Tokens, Test-Time Compute, Koszt rozumowania, Overthinking]
tagi: [modele, reasoning, koszty, latencja]
źródła:
  - "[[simonw — Baza Wskazówek i Komentarzy]]"
  - "[[karminski3 — Baza Wskazówek i Komentarzy]]"
---

# Test-Time Compute i Reasoning Tokens

**Test-Time Compute** (skalowanie obliczeń w czasie inferencji) to paradygmat, w którym model otrzymuje dodatkowy budżet tokenów na „myślenie” (generowanie niewidocznego łańcucha rozumowania, *Chain-of-Thought*) przed sformułowaniem ostatecznej odpowiedzi.

## Rzeczywisty koszt i narzut tokenów

Z pomiarów inżynierskich Simona Willisona i Karminskiego wynika, że skalowanie reasoning tokens niesie ze sobą drastyczny narzut:
- **Stosunek tokenów:** Modele o głębokim rozumowaniu potrafią zużyć ponad **22 000 tokenów reasoning na zaledwie 3 000 tokenów faktycznej odpowiedzi** (proporcja ~7:1).
- **Latencja:** Czas odpowiedzi w złożonych zadaniach może wynosić od kilkudziesięciu sekund do nawet kilkunastu minut.
- **Koszty API:** Dostawcy rozliczają tokeny myślenia tak samo jak tokeny wyjściowe, co przy braku limitów drastycznie drenuje budżet.

## Zjawisko odwróconego skalowania (Overthinking na SWE-bench)

Wbrew obiegowej opinii, że *„im więcej tokenów myślenia, tym lepszy wynik”*, testy agentowego rozwiązywania problemów inżynierskich (np. na SWE-bench) wykazują zjawisko **inwersji**:
1. Ustawienie maksymalnego budżetu (`reasoning_effort = max`) potrafi **pogorszyć** skuteczność naprawy kodu.
2. Model zaczyna zapętlać się w rozważaniach, kwestionować poprawne założenia (*overthinking*) lub zatrzymywać się przedwcześnie (*early stopping*), gubiąc prosty kontekst błędu.
3. Kluczową miarą jakości systemów SOTA staje się **kompresja informacji** — umiejętność rozwiązania trudnego problemu przy minimalnym koszcie tokenowym, a nie maksymalnej długości wywodu.

## Powiązane

- [[Stabilność modeli i przestrzeganie promptu]]
- [[Prompt Architecture]]
- [[Context Compaction]]
- [[Harness]]
