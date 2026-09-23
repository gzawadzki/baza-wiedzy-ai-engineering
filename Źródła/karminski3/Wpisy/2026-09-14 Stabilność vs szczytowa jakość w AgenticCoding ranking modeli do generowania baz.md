---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 14 05:50:26 +0000 2026"
źródło: "https://x.com/karminski3/status/2099375198986461418"
kategoria: "Benchmarki modeli i wybór modelu do zadań agentowych"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Stabilność vs szczytowa jakość w AgenticCoding: ranking modeli do generowania bazy wektorowej

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 14 05:50:26 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099375198986461418)
- **Kluczowe pojęcia:** [[Harness|Agentic Coding]] [[Harness|Benchmarkowanie LLM]] [[Harness|Wariancja wyników modeli]] [[Prompt Architecture|Inżynieria promptów]] [[Harness|Koszt tokenów]] [[Harness|Bazy wektorowe]] [[Stabilność modeli i przestrzeganie promptu|Stabilność post-trainingu]]

---

## Kontekst i problem
Autor porównuje modele w konkretnym scenariuszu AgenticCoding: implementacja bazy wektorowej od zera, oceniana przez wydajność działania bazy. Test obejmuje GPT6-Astra, Fable-5.1, Hy4-dev, Kimi-K3 i DeepSeek-V4.1-Flash. Główny wniosek nie dotyczy tylko szczytowego wyniku, ale wariancji między trzema próbami — ma to bezpośredni wpływ na koszt tokenów, potrzebę re-try i stabilność harnessu agentowego.

## Rada inżynierska
W AgenticCoding oceniaj model nie tylko po maksymalnym wyniku, ale po wariancji Δ między próbami. Fable-5.1 osiąga SOTA (2x drugiego miejsca), ale przy Δ>50% wymaga doświadczonego prompt engineeringu i budżetu na wielokrotne próbkowanie. GPT6-Astra ma niższy szczyt, lecz bardzo stabilne wyniki (12985.28, 12134.83, 10676.74), więc jest lepszy, gdy zależy na oszczędzaniu tokenów i unikaniu „losowania”. Do prostych zadań backendowych najbardziej opłacalny jest DeepSeek-V4.1-Flash (wynik blisko Kimi-K3, Δ<20%); do złożonych — GPT6-Astra lub Fable-5.1. Wcześniej modele Anthropic opus/sonnet były najstabilniejsze (<10% różnicy), co pokazuje, że stabilność post-trainingu zmienia się między generacjami.

## Uwaga / Anty-wzorzec
Wybieranie modelu wyłącznie na podstawie pojedynczego najlepszego wyniku lub leaderboardu, bez analizy wariancji. Modele o wysokim szczycie, ale dużej zmienności (Fable-5.1, Hy4-dev) powodują przepalanie tokenów na kolejne próby i niestabilne pętle agentowe. Odwrotny błąd to wybór zbyt słabego modelu do złożonego zadania tylko dlatego, że jest stabilny i tani.

## Oryginalny cytat
> *"同步一波大模型写后端代码排行榜

GPT6-Astra 和 Fable-5.1 没来得及做视频, 直接给大家同步图文了.

就结论来说, 单纯后端 AgenticCoding 场景(注意我只说我这个测试, 用大模型从0实现向量数据库, 使用数据库性能计分. 别的我不知道). 目前Fable-5.1 还是SOTA. 写出来的向量数据库直接是第二名的2x.

不过Fable的表现反而跟GPT 完全反过来了, 之前测Anthropic的模型(opus/sonnet) 系列, 反而是最稳的, 三次测试中最高分和最低分差距不超过10%. 而这次 GPT6-Astra 三次得分反而很接近(12985.28, 12134.83, 10676.74), 这证明这个模型的后训练极其稳定, 而 Fable-5.1 则是  21191.51, 11915.19, 7998.93. Δ超过50%. 

所以从省token的角度, 其实更推荐使用 GPT6-Astra. 因为发挥稳定, 不需要重复抽卡. 而 Fable-5.1 更适合经验丰富的工程师好好写提示词后再使用.

国产模型正好也是这个局面, Hy4-dev 虽然分数高, 但是三次得分差距巨大, 10778.51, 6011.78, 4915.22. 而 Kimi-K3 则相对稳定. 另外最具性价比无疑是 DeepSeek-V4.1-Flash. 得分几乎跟 kimi-k3没区别了. 而且Δ<20%. 所以只要不是复杂的代码任务, 直接无脑 DeepSeek-V4.1-Flash最划算. 而复杂的尝试使用GPT6-Astra 和 Fable-5.1.

> #gpt6astra #fable51 #deepseekv41flash"*
