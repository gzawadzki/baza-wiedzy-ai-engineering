---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Fri Sep 18 19:36:40 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2101032677940117875"
kategoria: "Inżynieria kontekstu / zarządzanie pamięcią agenta"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# compact-adviser: klasyfikator bezpiecznego momentu kompakcji kontekstu z adaptacyjnym progiem precision/recall

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Fri Sep 18 19:36:40 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101032677940117875)
- **Kluczowe pojęcia:** [[Context Compaction|Inżynieria kontekstu]] [[Context Compaction|Kompakcja kontekstu]] [[Harness|Zarządzanie pamięcią agenta]] [[Harness|Klasyfikator decyzyjny]] [[Eval Set z realnych sesji|Eval set]] [[Prompt Architecture|Prompt hillclimbing]] [[Harness|Precision vs Recall]] [[Harness|Harness agentowy]] [[Bezpieczny punkt kompaktowania]] [[Checkpointing sesji agenta]]

---

## Kontekst i problem
W harnessach agentowych typu Claude Code (oraz Pi) decyzja o wywołaniu /compact jest ręczna i nieoczywista: nie wiadomo, czy przyszłe kroki zadania będą jeszcze potrzebować szczegółowego kontekstu obecnego okna. Autor zbudował plugin-agent 'compact-adviser', który klasyfikuje, czy bieżący stan to bezpieczna granica zadania nadająca się do kompakcji.

## Rada inżynierska
Traktuj decyzję o kompakcji jako problem klasyfikacji 'bezpieczny vs niebezpieczny checkpoint zadania'. Klasyfikator należy stroić adaptacyjnie: gdy okno kontekstu jest małe — optymalizuj PRECISION (nie kompaktuj przedwcześnie i nie trać potrzebnego kontekstu); w miarę zapełniania okna stopniowo przechodź do optymalizacji RECALL (nie przepuszczaj okazji do kompakcji), bo koszt braku kompakcji rośnie, a przy pełnym oknie agent i tak zostanie zmuszony do kompakcji. Warto zbudować prywatny eval set z realnych sesji (tu: 40 sesji z ręcznie oznaczonymi checkpointami) i hillclimbować prompt klasyfikatora aż osiągnie dobrą skuteczność. Udostępnij dwa tryby: 'hint' (tylko podpowiedź, użytkownik sam uruchamia /compact) oraz 'auto' (automatyczna kompakcja, gdy klasyfikator uzna to za bezpieczne).

## Uwaga / Anty-wzorzec
Brak świadomej strategii kompakcji prowadzi do dwóch skrajności: przedwczesna kompakcja niszczy szczegółowy kontekst potrzebny do kolejnych akcji, a zbyt późna wymusza utratową, narzuconą kompakcję przy pełnym oknie. Anty-wzorzec: stosowanie stałego progu decyzyjnego niezależnie od stopnia zapełnienia okna zamiast adaptacyjnego przesunięcia precision→recall.

## Oryginalny cytat
> *"almost every day i hear people ask "when should i /compact my session" there's no easy answer because it depends on how likely your future action will need detailed context in the existing window but we have Jev now! introducing compact-adviser - an agent plugin you can use in claude and pi today to help determine whether you're likely at a task boundary that's safe to compact i built a private eval set from 40 real sessions and manually labeled all the safe vs unsafe checkpoints to evaluate this, and hillclimbed the Jev prompt till it performed quite well i also made it so that the classifier will - optimize for precision (not triggering a compaction prematurely) when context window is small - and gradually shift to optimize for recall (not missing an opportunity to compact) when context window fills up, because the cost of not compacting becomes higher, and at the end the agent will be forced to compact anyway it supports a "hint" mode (just give you a hint and it's up to you to run /compact) vs "auto" mode which runs compaction whenever Jev says it's safe to do so if you have Jev and want to put your compaction on autopilot, try this out and let me know how it goes! support for more harness is coming soon as well"*
