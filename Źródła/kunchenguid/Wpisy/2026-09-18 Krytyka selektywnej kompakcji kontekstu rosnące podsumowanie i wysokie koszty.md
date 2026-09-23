---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Fri Sep 18 04:15:10 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100800776620900454"
kategoria: "Inżynieria kontekstu"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Krytyka selektywnej kompakcji kontekstu: rosnące podsumowanie i wysokie koszty

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Fri Sep 18 04:15:10 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100800776620900454)
- **Konwersacja:** Odpowiedź w dyskusji (@tamarajtran)
- **Kluczowe pojęcia:** [[Context Compaction|Kompakcja kontekstu]] [[Context Compaction|Zarządzanie oknem kontekstowym]] [[Prompt Architecture|Pamięć podręczna promptów]] [[Harness|Ewaluacja modeli]]

---

## Kontekst i problem
Autor krytykuje rozpowszechniający się pomysł na kompakcję kontekstu, który polega na selektywnym usuwaniu tylko niektórych wywołań narzędzi, podczas gdy wiadomości użytkownika i asystenta są zachowywane na zawsze. Wskazuje dwa fundamentalne błędy: 1) podsumowanie kompakcji będzie rosło w nieskończoność, prowadząc do wyczerpania okna kontekstowego w długotrwałych zadaniach i uniemożliwiając samodzielne odzyskanie; 2) operacja pozostawia więcej treści w kontekście niż prawdziwa kompakcja, przez co następne zapytanie staje się ogromnym niebuforowanym promptem, co może być droższe niż kontynuacja długiej sesji z pamięcią podręczną. Sugeruje przeprowadzenie ewaluacji (deepswe, programbench) w celu zmierzenia kompromisu koszt/wydajność.

## Rada inżynierska
W kompakcji kontekstu należy usuwać również starsze wiadomości użytkownika i asystenta, a nie tylko wywołania narzędzi. W przeciwnym razie podsumowanie rośnie w nieskończoność, co prowadzi do wyczerpania okna kontekstowego. Ponadto, niepełna kompakcja generuje duży niebuforowany prompt, który może być kosztowniejszy niż kontynuacja sesji z pamięcią podręczną. Zawsze należy mierzyć kompromis koszt/wydajność za pomocą ewaluacji.

## Uwaga / Anty-wzorzec
Selektywne usuwanie tylko wywołań narzędzi przy zachowaniu wszystkich wiadomości użytkownika i asystenta prowadzi do nieograniczonego wzrostu podsumowania kompakcji, co ostatecznie wyczerpuje okno kontekstowe i uniemożliwia kontynuację zadania. Dodatkowo, taki zabieg generuje duży niebuforowany prompt, który może być droższy niż kontynuacja długiej sesji z pamięcią podręczną.

## Oryginalny cytat
> *"umm.. since this is somehow spreading so widely, i feel obligated to point out that this is unfortunately a bad idea

the fundamental flaws -

1. it only selectively remove some tool calls. user and assistant messages are kept FOREVER, which means the compaction summary will only keep growing and never shrink. so long running tasks will eventually completely run out of context window and cannot self recover, defeating the primary purpose of compaction which is to free up the context window so the agent can keep going

2. this operation leaves a lot more stuff in the context window than a real compaction, which means the next request after doing this becomes a massive uncached prompt which in some cases even more expensive than letting the long cached session continue, which defeats the other purpose of compaction which is cost saving

i suggest running some evals such as deepswe, programbench etc to actually measure the cost and performance tradeoff and share it if you are truly convinced this is practical"*
