---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Aug 31 06:27:32 +0000 2026"
źródło: "https://x.com/karminski3/status/2094311103987581033"
kategoria: "Benchmarking i ewaluacja modeli LLM"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Benchmark małych modeli LLM: 8 modeli, 4 kwantyzacje, MTP on/off, poziomy rozumowania low/medium/xhigh (pass@3)

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Aug 31 06:27:32 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2094311103987581033)
- **Kluczowe pojęcia:** [[Harness|pass@k]] [[Architektura KV Cache i Rozumowanie Latentne|Multi-Token Prediction (MTP)]] [[Test-Time Compute i Reasoning Tokens|Reasoning Effort / Thinking Budget]] [[Harness|Kwantyzacja modeli LLM]] [[Harness|Mixture of Experts (MoE)]] [[Harness|Benchmark agentowy]] [[Harness|Throughput vs Latency]] [[Harness|H100]] [[Harness|Ewaluacja modeli open-source]]

---

## Kontekst i problem
Autor (karminski3) przeprowadził kompleksowy, wielowymiarowy benchmark małych modeli open-source w realnych zadaniach inżynierskich: frontend, Python oraz zdolności agentowe. Celem było ustalenie, który z modeli klasy ~12-35B (gęstych i MoE) jest najlepszym wyborem do praktycznej pracy inżynierskiej, przy jednoczesnym uwzględnieniu wpływu kwantyzacji, mechanizmu Multi-Token Prediction (MTP) oraz poziomu rozumowania (reasoning effort) na jakość wyników. Wynik ma charakter operacyjny: pozwala wybrać model i konfigurację pod rzeczywisty workload agentowy, zamiast opierać się na ogólnikowych benchmarkach (MMLU itp.).

## Rada inżynierska
Przy ewaluacji modeli do zadań inżynierskich stosuj macierz konfiguracji, a nie pojedynczy punkt pomiarowy: (1) krzyżuj poziom kwantyzacji (np. 4 warianty), (2) stan MTP (on/off), (3) poziom rozumowania (low/medium/xhigh). To ujawnia interakcje, których pojedynczy run nie pokaże – np. że wyższy reasoning_effort może być kontrproduktywny przy niskiej kwantyzacji. Używaj metryki pass@3 (best-of-3) do zadań generatywnych/agentowych, bo pojedynczy przebieg jest zbyt zaszumiony przez niedeterminizm próbkowania. Pamiętaj, że sprzęt (H100 vs A100 itp.) wpływa wyłącznie na czas generacji (throughput/latency), a nie na jakość wyjścia – dobieraj GPU pod budżet czasowy, nie pod „jakość modelu”, i zawsze raportuj łączny koszt obliczeniowy (autor: ~148 USD, ~48h) dla reprodukowalności.

## Uwaga / Anty-wzorzec
Częsty błąd: ocenianie modelu na podstawie jednego runu i jednej kwantyzacji, oraz błędne przypisywanie różnic w jakości do sprzętu GPU zamiast do konfiguracji modelu. Drugi anty-wzorzec: ignorowanie interakcji parametrów (MTP × reasoning effort × kwantyzacja) – można błędnie odrzucić model, który przy innej konfiguracji wygrywa. Trzeci: benchmarkowanie tylko na ogólnych zadaniach, a nie na docelowym profilu (frontend/Python/Agent), co prowadzi do wyboru modelu nieoptymalnego dla realnego harnessu agentowego.

## Oryginalny cytat
> *"终于搞完了! 给大家带来小模型竞技场, 这次测试了8款模型, 包括: Qwen3.8-27B / Qwen3.6-27B / Qwen3.6-35B-A3B / Ornith-1.5-35B-A3B / Gemma-4-31B / Gemma-4-26B-A4B / Gemma-4-12B / GPT-OSS-20B。每个模型4个量化版本, 还测试了 MTP 开启和关闭, 以及 low, medium, xhigh 三档思考强度, 做了个全面横评. 测试主要集中在前端, python, Agent 能力上, 每个测试运行3次取最佳结果(pass@3). 测试使用H100显卡(注意用H100是为了生成快, 就这还跑了48小时, 显卡不影响生成效果, 只影响生成速度), 总成本148刀."*
