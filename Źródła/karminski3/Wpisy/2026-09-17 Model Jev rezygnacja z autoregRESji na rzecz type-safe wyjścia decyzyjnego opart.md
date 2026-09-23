---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Thu Sep 17 22:46:02 +0000 2026"
źródło: "https://x.com/karminski3/status/2100717944565354595"
kategoria: "Architektura modeli / Type-Safe AI / Structured Output"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Model Jev: rezygnacja z autoregRESji na rzecz type-safe wyjścia decyzyjnego opartego na schemacie

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Thu Sep 17 22:46:02 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2100717944565354595)
- **Kluczowe pojęcia:** [[Jev]] [[Harness|Type-Safe AI]] [[Harness|Structured Output]] [[Harness|Decision Slots]] [[Harness|Autoregressive vs Decision Models]] [[Harness|Schema-based Inference]] [[Harness|System One]] [[Harness|Diogo Almeida]]

---

## Kontekst i problem
Wprowadzenie do modelu Jev (powiązanego z #systemone, #vercel, Diogo Almeida), który porzuca klasyczną architekturę autoregRESyjną (token-by-token generację dowolnego tekstu) i zamiast tego emituje wyłącznie strukturalne decyzje zgodne z narzuconym z góry schematem. Adresuje problem niedeterministycznego, trudnego do walidacji wyjścia LLM-ów w zastosowaniach decyzyjnych (klasyfikacja, agenci, gry, trading).

## Rada inżynierska
Przy projektowaniu systemów decyzyjnych opartych na Jev należy: (1) zdefiniować wejściowy Schema analogicznie do protobuf/GraphQL — jest on kompilowany do konkretnych 'slotów decyzyjnych' (decision slots); (2) model wypełnia sloty i zwraca JSON zawierający zarówno wynik decyzyjny (np. isSpam: true), jak i rozkład prawdopodobieństw (np. true: 0.982, false: 0.018). Dzięki temu poprawność formatu wyjścia jest gwarantowana strukturalnie, a nie promptowo — nie ma ryzyka 'zepsutego JSON-a' ani halucynacji formatu. Dla złożonych scenariuszy (gra Slay the Spire, analiza rynku) wystarczy zserializować stan świata do tekstu (obecnie tylko wejście tekstowe) i zdefiniować przestrzeń dozwolonych akcji — model samodzielnie podejmuje decyzję w tym kontrakcie.

## Uwaga / Anty-wzorzec
Błędne założenie, że model decyzyjny można traktować jak zwykły LLM i podawać mu swobodny prompt lub oczekiwać dowolnej odpowiedzi tekstowej — Jev nie potrafi wygenerować zwykłego tekstu i wymaga jawnego schematu wejścia. Kolejna pułapka: brak zdefiniowania kompletnej i rozłącznej przestrzeni akcji/slotów — model nie wyjdzie poza zdefiniowany kontrakt, więc niedomknięty Schema = niedomknięta przestrzeń decyzyjna. Uwaga też na ograniczenie modalności: aktualnie tylko wejście tekstowe, co wymusza serializację stanu (obraz, tablica gry, wykres) do tekstu.

## Oryginalny cytat
> *"给大家写个简单的Jev模型介绍, 这绝对是个需要重点关注的模型. 简单讲, 这个模型放弃了传统自回归架构, 它没有办法直接输出普通文本. 但是他能进行决策! 比如最简单的二分类场景, 输入一条短信, 让它判断是否为垃圾短信, 它就可以输出这样的JSON: {"decision": { "isSpam": true }, "probabilities": { "isSpam": { "true": 0.982, "false": 0.018 } } } 没错, 它只能进行结构化输出, 甚至你输入的时候要定义 Schema (用过protobuf/GraphQL的同学应该能理解), 在送入模型时被编译为特定的决策槽位, 然后按照槽位输出, 所以输出JSON不可能出问题. 而复杂一些的场景, 比如让这个模型玩杀戮尖塔或者看盘, 只需要把内容转换为文本输入进去(没错, 目前模型只支持文本输入), 然后定义好模型能进行哪些动作, 模型就会自主决策了."*
