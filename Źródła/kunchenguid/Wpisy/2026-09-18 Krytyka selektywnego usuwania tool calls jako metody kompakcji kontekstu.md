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

# Krytyka selektywnego usuwania tool calls jako metody kompakcji kontekstu

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Fri Sep 18 04:15:10 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100800776620900454)
- **Konwersacja:** Odpowiedź w dyskusji (@tamarajtran)
- **Kluczowe pojęcia:** [[Context Compaction|Kompakcja kontekstu]] [[Context Compaction|Zarządzanie oknem kontekstowym]] [[Prompt Architecture|Cache promptów]] [[Harness|Ewaluacja agentów]] [[Harness|DeepSWE]] [[Harness|ProgramBench]]

---

## Kontekst i problem
Ktoś zaproponował metodę kompakcji kontekstu polegającą na selektywnym usuwaniu części wywołań narzędzi (tool calls) przy zachowaniu wszystkich wiadomości użytkownika i asystenta. Autor wskazuje, że to podejście jest wadliwe i może prowadzić do wyczerpania okna kontekstowego oraz wysokich kosztów.

## Rada inżynierska
Kompakcja kontekstu musi faktycznie zmniejszać rozmiar kontekstu. Selektywne usuwanie tylko tool calls bez usuwania wiadomości użytkownika i asystenta powoduje, że podsumowanie rośnie w nieskończoność, aż do wyczerpania okna kontekstowego, uniemożliwiając kontynuację długotrwałych zadań. Dodatkowo pozostawia dużo niecache'owanych treści, co zwiększa koszty kolejnego żądania. Należy przeprowadzić ewaluacje (np. DeepSWE, ProgramBench) przed uznaniem metody za praktyczną.

## Uwaga / Anty-wzorzec
Selektywne usuwanie tool calls z pominięciem wiadomości użytkownika/asystenta: podsumowanie rośnie, kontekst się nie kurczy, agent traci możliwość kontynuacji, a koszty rosną z powodu niecache'owanego promptu.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor krytykuje szeroko rozpowszechnioną metodę kompakcji kontekstu polegającą na selektywnym usuwaniu wywołań narzędzi, wskazując na fundamentalne wady: rosnące podsumowanie i wysokie koszty niecache'owanego promptu. Jest to sprzeczne z popularnym trendem stosowania tej techniki.

## Oryginalny cytat
> *"umm.. since this is somehow spreading so widely, i feel obligated to point out that this is unfortunately a bad idea

the fundamental flaws -

1. it only selectively remove some tool calls. user and assistant messages are kept FOREVER, which means the compaction summary will only keep growing and never shrink. so long running tasks will eventually completely run out of context window and cannot self recover, defeating the primary purpose of compaction which is to free up the context window so the agent can keep going

2. this operation leaves a lot more stuff in the context window than a real compaction, which means the next request after doing this becomes a massive uncached prompt which in some cases even more expensive than letting the long cached session continue, which defeats the other purpose of compaction which is cost saving

i suggest running some evals such as deepswe, programbench etc to actually measure the cost and performance tradeoff and share it if you are truly convinced this is practical"*
