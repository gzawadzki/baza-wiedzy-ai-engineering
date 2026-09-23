---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 14 09:52:12 +0000 2026"
źródło: "https://x.com/karminski3/status/2099436039169536325"
kategoria: "Inżynieria LLM / Destylacja i wnioskowanie"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Destylacja długiego CoT z R1 do małych modeli i rola budżetu obliczeniowego

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 14 09:52:12 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099436039169536325)
- **Kluczowe pojęcia:** [[Harness|Chain-of-Thought]] [[Harness|Destylacja wiedzy]] [[Test-Time Compute i Reasoning Tokens|Test-time compute]] [[Harness|DeepSeek R1]] [[Harness|Ollama]]

---

## Kontekst i problem
Autor przypomina, że długi łańcuch myśli (long CoT) z DeepSeek R1 został zdestylowany do małych modeli (Qwen-1.5B/7B/14B). Przy odpowiednim budżecie obliczeniowym na wnioskowanie (thinking budget) ich zdolność rozwiązywania problemów rośnie proporcjonalnie do długości rozumowania – stąd skok z 71,0% do 86,7%. Wskazuje też na powszechne niezrozumienie: ollama instalowała deepseek-r1-distilled-qwen-7b jako „deepseek”, myląc destylowany model z oryginalnym R1.

## Rada inżynierska
Destylacja długiego CoT z dużego modelu do małego pozwala uzyskać znaczący wzrost jakości (np. z 71% do 86,7%) pod warunkiem zapewnienia wystarczającego budżetu tokenów na rozumowanie (test-time compute). Należy rozróżniać model destylowany od oryginalnego; etykietowanie destylatu jako pełnego modelu jest mylące.

## Uwaga / Anty-wzorzec
Traktowanie modeli destylowanych (np. deepseek-r1-distilled-qwen-7b) jako oryginalnego DeepSeek R1, co prowadzi do błędnych oczekiwań co do ich możliwości i rozmiaru.

## Oryginalny cytat
> *"请读完了Section 2后继续看Section 3 . 明确写了模型在长思考时的表现. 当时震撼人心的继续从71.0% 飙升到 86.7% 就是这么来的. 然后将 R1 生成的长思维链蒸馏到了小模型（ Qwen-1.5B、7B、14B）。在运行时给足其思考预算，然后解题能力就呈现出与思考长度正相关的暴涨。这不就是去年的新闻嘛....怎么还能记不住呢....然后就ollama把deepseek-r1-distilled-qwen-7b 当deepseek给大家装到电脑上了, 美其名曰运行deepseek. 有印象没? 串起来了吧?"*
