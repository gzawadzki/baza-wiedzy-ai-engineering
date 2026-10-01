---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Aug 31 06:27:32 +0000 2026"
źródło: "https://x.com/karminski3/status/2094311103987581033"
kategoria: "Benchmarking / Ewaluacja modeli lokalnych"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Arena małych modeli: 8 modeli × 4 kwantyzacje × MTP × 3 poziomy reasoning (pass@3)

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Aug 31 06:27:32 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2094311103987581033)
- **Kluczowe pojęcia:** [[Harness|Benchmark pass@k]] [[Harness|Kwantyzacja LLM]] [[Architektura KV Cache i Rozumowanie Latentne|Multi-Token Prediction (MTP)]] [[Test-Time Compute i Reasoning Tokens|Reasoning Effort]] [[Harness|Modele MoE (A3B/A4B)]] [[Harness|Ewaluacja modeli agentowych]] [[Harness|Arena małych modeli]]

---

## Kontekst i problem
Autor przeprowadził kompleksowy benchmark porównawczy małych modeli open-weight (Qwen3.8-27B, Qwen3.6-27B, Qwen3.6-35B-A3B, Ornith-1.5-35B-A3B, Gemma-4-31B/26B-A4B/12B, GPT-OSS-20B) w kontekście realnych zadań inżynierskich: generowania frontendu, kodu Pythona oraz zdolności agentowych. Celem było ustalenie, który z małych modeli jest praktycznie najlepszy, z uwzględnieniem wpływu kwantyzacji, mechanizmu MTP (Multi-Token Prediction) oraz poziomu intensywności rozumowania (low/medium/xhigh) na jakość końcową.

## Rada inżynierska
Pełna macierz ewaluacji modeli to nie tylko nazwa modelu, ale iloczyn kartezjański: (model × kwantyzacja × MTP on/off × poziom reasoning effort). Pomiar należy wykonywać z powtarzalnością (pass@3) i raportować koszt całkowity (tu: 148 USD, 48 h na H100). Sprzęt do ewaluacji dobrać pod szybkość generowania, nie pod jakość wyników — mocniejsza karta skraca czas, ale nie zmienia semantyki odpowiedzi. Poziom reasoning effort oraz włączony MTP trzeba traktować jako niezależne wymiary konfiguracji, bo istotnie modulują jakość i latencję przy tym samym checkpoincie.

## Uwaga / Anty-wzorzec
Naiwne benchmarkowanie modelu tylko po nazwie/skali — bez uwzględnienia konkretnego wariantu kwantyzacji, stanu MTP i poziomu reasoning — prowadzi do błędnych wniosków. Dodatkowo zakładanie, że mocniejszy GPU poprawi wyniki jakościowe, jest anty-wzorcem: sprzęt wpływa wyłącznie na czas generacji, nie na rezultat merytoryczny. Pomijanie kosztu (150 $/dwa dni) przy planowaniu benchmarku zaniża realną pracochłonność ewaluacji.

## Oryginalny cytat
> *"终于搞完了! 给大家带来小模型竞技场, 这次测试了8款模型... 每个模型4个量化版本, 还测试了 MTP 开启和关闭, 以及 low, medium, xhigh 三档思考强度... 测试主要集中在前端, python, Agent 能力上, 每个测试运行3次取最佳结果(pass@3). 测试使用H100显卡(注意用H100是为了生成快, 就这还跑了48小时, 显卡不影响生成效果, 只影响生成速度), 总成本148刀."*
