---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Thu Sep 17 22:46:02 +0000 2026"
źródło: "https://x.com/karminski3/status/2100717944565354595"
kategoria: "Architektura modeli / Type-Safe AI"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Jev: nieautoregresyjny model decyzyjny z wymuszonym schematem wyjścia (decision slots)

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Thu Sep 17 22:46:02 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2100717944565354595)
- **Kluczowe pojęcia:** [[Harness|Nieautoregresyjne modele decyzyjne]] [[Harness|Type-Safe AI]] [[Harness|Decision Slots]] [[Harness|Structured Output / Schema Compilation]] [[Jev|Jev Model]] [[Harness|Protobuf]] [[Harness|GraphQL]]

---

## Kontekst i problem
Tradycyjne LLM-y generują tekst autoregresyjnie, co powoduje, że wyjście strukturalne (np. JSON) nie jest gwarantowane — wymaga walidacji, retry i parsowania. Model Jev porzuca architekturę autoregresyjną: nie potrafi wypisać zwykłego tekstu, a jedynie podejmować decyzje w ściśle zdefiniowanym schemacie (analogia do protobuf/GraphQL). Schemat jest kompilowany do tzw. slotów decyzyjnych (decision slots), a model wypełnia je wartościami, dzięki czemu wyjściowy JSON jest z definicji poprawny składniowo i strukturalnie.

## Rada inżynierska
Przy zadaniach decyzyjnych (klasyfikacja binarna, sterowanie agentem w grze, analiza rynku) rozważ model nieautoregresyjny typu Jev: zdefiniuj wejściowy Schema opisujący dopuszczalne akcje/decyzje i prawdopodobieństwa, skompiluj go do slotów decyzyjnych i podaj modelowi wyłącznie wejście tekstowe. Model zwraca ustrukturyzowany wynik z rozkładem prawdopodobieństw (np. {"decision":{"isSpam":true},"probabilities":{"isSpam":{"true":0.982,"false":0.018}}}), eliminując potrzebę walidacji formatu i retry. Złożone scenariusze (np. Slay the Spire, trading) sprowadzają się do konwersji stanu na tekst + deklaracji zestawu dostępnych akcji — model samodzielnie podejmuje decyzję.

## Uwaga / Anty-wzorzec
Błędne założenie, że taki model jest funkcjonalnie tożsamy ze zwykłym tekstowym LLM-em — powierzchowne podobieństwo interfejsu (wejście tekstowe, wyjście JSON) maskuje fundamentalnie inny paradygmat: brak generacji swobodnego tekstu, brak autoregresji, ograniczenie do predefiniowanych slotów decyzyjnych. Nie próbuj używać go do zadań wymagających płynnej generacji tekstu ani nie zakładaj elastyczności poza zadeklarowanym Schema.

## Oryginalny cytat
> *"简单讲, 这个模型放弃了传统自回归架构, 它没有办法直接输出普通文本. 但是他能进行决策! ... 它只能进行结构化输出, 甚至你输入的时候要定义 Schema (用过protobuf/GraphQL的同学应该能理解), 在送入模型时被编译为特定的决策槽位, 然后按照槽位输出, 所以输出JSON不可能出问题."*
