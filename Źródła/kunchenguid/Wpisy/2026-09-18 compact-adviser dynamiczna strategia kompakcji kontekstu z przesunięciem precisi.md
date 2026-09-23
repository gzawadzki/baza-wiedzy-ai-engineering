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

# compact-adviser: dynamiczna strategia kompakcji kontekstu z przesunięciem precision → recall

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Fri Sep 18 19:36:40 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101032677940117875)
- **Kluczowe pojęcia:** [[Context Compaction|Inżynieria kontekstu]] [[Context Compaction|Kompakcja kontekstu]] [[Harness|Zarządzanie pamięcią agenta]] [[Harness|Klasyfikator granic zadań]] [[Context Compaction|Precision vs Recall w kompakcji]] [[Prompt Architecture|Prompt hillclimbing]] [[Eval Set z realnych sesji|Eval set z realnych sesji]] [[Harness|Harness agentowy]] [[Harness|Auto vs Hint mode]] [[Bezpieczny punkt kompaktowania]] [[Checkpointing sesji agenta]]

---

## Kontekst i problem
W systemach agentowych opartych na Claude (i podobnych harnessach) decyzja o uruchomieniu /compact jest trudna, ponieważ zależy od tego, czy przyszłe działania agenta będą wymagały szczegółowego kontekstu znajdującego się w bieżącym oknie. Zbyt wczesna kompakcja niszczy potrzebny kontekst; zbyt późna prowadzi do przepełnienia okna i wymuszonej, kosztownej kompakcji. Autor zbudował plugin 'compact-adviser', który klasyfikuje, czy agent znajduje się na granicy zadania bezpiecznej do skompaktowania.

## Rada inżynierska
Traktuj decyzję o kompakcji jako problem klasyfikacji zależny od stopnia zapełnienia okna kontekstowego i dostrajaj ją asymetrycznie: (1) przy małym zajęciu okna optymalizuj PRECISION — nie wyzwalaj kompakcji przedwcześnie, bo ryzyko utraty potrzebnego kontekstu jest wysokie; (2) w miarę zapełniania okna stopniowo przechodź do optymalizacji RECALL — nie przegap okazji do kompakcji, bo koszt braku kompakcji rośnie, a pod koniec agent i tak zostanie zmuszony do kompakcji. Waliduj klasyfikator na ręcznie oznaczonym zbiorze realnych sesji (autor użył 40 sesji z etykietami safe/unsafe checkpointów) i hillclimbuj prompt klasyfikatora. Oferuj tryb 'hint' (sugestia, użytkownik decyduje) oraz tryb 'auto' (automatyczna kompakcja przy sygnale bezpieczeństwa).

## Uwaga / Anty-wzorzec
Anty-wzorzec: stosowanie jednej, stałej polityki kompakcji (np. zawsze przy tym samym progu tokenów) bez uwzględnienia prawdopodobieństwa, że przyszłe kroki będą potrzebować szczegółów z bieżącego okna. Drugi anty-wzorzec: optymalizacja wyłącznie pod recall (agresywna kompakcja) — powoduje utratę kontekstu potrzebnego do dalszej pracy; oraz wyłącznie pod precision — prowadzi do przepełnienia okna i wymuszonej kompakcji w najgorszym momencie.

## Oryginalny cytat
> *""almost every day i hear people ask "when should i /compact my session" there's no easy answer because it depends on how likely your future action will need detailed context in the existing window but we have Jev now! introducing compact-adviser - an agent plugin you can use in claude and pi today to help determine whether you're likely at a task boundary that's safe to compact i built a private eval set from 40 real sessions and manually labeled all the safe vs unsafe checkpoints to evaluate this, and hillclimbed the Jev prompt till it performed quite well i also made it so that the classifier will - optimize for precision (not triggering a compaction prematurely) when context window is small - and gradually shift to optimize for recall (not missing an opportunity to compact) when context window fills up, because the cost of not compacting becomes higher, and at the end the agent will be forced to compact anyway it supports a "hint" mode (just give you a hint and it's up to you to run /compact) vs "auto" mode which runs compaction whenever Jev says it's safe to do so if you have Jev and want to put your compaction on autopilot, try this out and let me know how it goes! support for more harness is coming soon as well""*
