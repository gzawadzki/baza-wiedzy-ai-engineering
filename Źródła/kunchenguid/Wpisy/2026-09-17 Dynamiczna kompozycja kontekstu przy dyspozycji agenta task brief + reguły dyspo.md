---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Thu Sep 17 07:59:19 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100494796687340001"
kategoria: "Architektura systemów agentowych / Inżynieria kontekstu"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Dynamiczna kompozycja kontekstu przy dyspozycji agenta: task brief + reguły dyspozycji + dane o kwotach

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Thu Sep 17 07:59:19 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100494796687340001)
- **Konwersacja:** Odpowiedź w dyskusji (@ArtifexPraxis)
- **Kluczowe pojęcia:** [[Context Compaction|Inżynieria kontekstu]] [[Harness|Orkiracja agentów]] [[Harness|Task Brief]] [[Prompt Architecture|Dynamiczna kompozycja promptu]] [[Harness|Zarządzanie budżetem tokenów]] [[Harness|Reguły dyspozycji użytkownika]] [[Harness|Recykling artefaktów pośrednich]] [[Firstmate i Agenci Wykonawczy]]

---

## Kontekst i problem
Autor opisuje wewnętrzną mechanikę systemu orkiestracji agentów (firstmate → crewmate). W momencie, gdy orkiestrator ('firstmate') deleguje zadanie do agenta-wykonawcy ('crewmate'), system i tak musi najpierw wygenerować zwięzły opis zadania (task brief). Ten artefakt nie jest tracony — staje się częścią wejściowego kontekstu dla komponentu decyzyjnego/planującego ('Jev'). Kontekst ten jest składany dynamicznie z trzech heterogenicznych źródeł: (1) treści zadania, (2) reguł dyspozycji zdefiniowanych przez użytkownika, (3) danych o wykorzystaniu kwot (quota/limity). Rozwiązuje to problem rozproszonej wiedzy o stanie systemu i intencjach użytkownika przy podejmowaniu decyzji o delegacji.

## Rada inżynierska
Traktuj prompt wejściowy agenta decyzyjnego jako wynik deterministycznej kompozycji wielu źródeł, a nie jako statyczny szablon. Artefakty pośrednie procesu (np. task brief tworzony na potrzeby delegacji) powinny być recyklingowane jako kontekst dla kolejnych kroków — nie generuj ich ponownie ani nie wyrzucaj. Zawsze dołączaj do kontekstu decyzyjnego: (a) znormalizowany opis zadania, (b) jawne reguły polityki użytkownika/systemu, (c) metryki operacyjne (kwoty, limity, koszt, dostępność). Taki rozdział na trzy warstwy ułatwia testowanie i podmianę pojedynczego źródła bez przepisywania całego promptu.

## Uwaga / Anty-wzorzec
Anty-wzorzec: przekazywanie agentowi decyzyjnemu jedynie surowego żądania użytkownika, bez reguł polityki i danych o limitach — prowadzi to do decyzji o delegacji, które ignorują budżet tokenowy/kwoty lub naruszają reguły użytkownika. Drugi anty-wzorzec: ponowne generowanie opisu zadania w każdym kroku zamiast wykorzystania już powstałego task briefu — marnotrawstwo tokenów, ryzyko dryfu semantycznego między wersjami opisu i niespójność między intencją delegacji a jej wykonaniem.

## Oryginalny cytat
> *"@ArtifexPraxis when firstmate is about to dispatch a crewmate to do a task, it first has to write a task brief anyway

that task brief + the user's dispatch rules + the user's quota data = input context to Jev here"*
