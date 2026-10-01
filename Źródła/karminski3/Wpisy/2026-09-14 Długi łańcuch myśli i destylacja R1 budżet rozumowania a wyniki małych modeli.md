---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 14 09:52:12 +0000 2026"
źródło: "https://x.com/karminski3/status/2099436039169536325"
kategoria: "Inżynieria LLM / rozumowanie, destylacja i budżet kontekstu"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Długi łańcuch myśli i destylacja R1: budżet rozumowania a wyniki małych modeli

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 14 09:52:12 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099436039169536325)
- **Kluczowe pojęcia:** [[Harness|Long Chain-of-Thought]] [[Harness|Destylacja modeli]] [[Harness|DeepSeek-R1]] [[Harness|Budżet rozumowania]] [[Harness|Ollama]] [[Harness|Qwen]]

---

## Kontekst i problem
Autor przypomina, że przełom DeepSeek-R1 opierał się na długim łańcuchu myśli oraz destylacji trajektorii rozumowania R1 do małych modeli Qwen-1.5B/7B/14B. Przy odpowiednio dużym budżecie tokenów na rozumowanie małe modele destylowane osiągają radykalny wzrost skuteczności — jakość jest silnie dodatnio skorelowana z długością CoT. Problem: wielu użytkowników myli lokalnie uruchamiany model destylowany z pełnym DeepSeek-R1, m.in. przez sposób prezentacji w Ollama.

## Rada inżynierska
Traktuj budżet rozumowania jako sterowalny hiperparametr: małym modelom destylowanym z R1 dawaj wystarczający limit tokenów myślowych, bo wyniki rosną wraz z długością CoT. Rygorystycznie rozróżniaj model nauczyciela od destylatu — deepseek-r1-distilled-qwen-7b to Qwen dostrojony na danych R1, a nie pełny DeepSeek-R1.

## Uwaga / Anty-wzorzec
Mylenie destylatu, np. DeepSeek-R1-Distill-Qwen-7B, z pełnym DeepSeek-R1 i wdrażanie go jako „DeepSeek” bez świadomości różnic w architekturze, skali i jakości. Bagatelizowanie długiego CoT oraz zbyt mały budżet rozumowania zaniżają wyniki małych modeli.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor krytykuje popularne uproszczenie: Ollama instaluje deepseek-r1-distilled-qwen-7b, ale to nie jest pełny DeepSeek-R1, lecz model Qwen dostrojony na danych R1. Sporne jest nazywanie takich destylatów „DeepSeek” oraz pomijanie faktu, że ich wyniki zależą od przyznanego budżetu rozumowania.

## Oryginalny cytat
> *"请读完了Section 2后继续看Section 3 . 明确写了模型在长思考时的表现. 当时震撼人心的继续从71.0% 飙升到 86.7% 就是这么来的. 然后将 R1 生成的长思维链蒸馏到了小模型（ Qwen-1.5B、7B、14B）。在运行时给足其思考预算，然后解题能力就呈现出与思考长度正相关的暴涨。这不就是去年的新闻嘛....怎么还能记不住呢....然后就ollama把deepseek-r1-distilled-qwen-7b 当deepseek给大家装到电脑上了, 美其名曰运行deepseek. 有印象没? 串起来了吧?"*
