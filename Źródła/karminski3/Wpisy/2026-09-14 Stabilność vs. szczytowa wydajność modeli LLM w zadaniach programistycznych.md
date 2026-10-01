---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 14 05:50:26 +0000 2026"
źródło: "https://x.com/karminski3/status/2099375198986461418"
kategoria: "Benchmarking i wybór modeli LLM do kodu"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Stabilność vs. szczytowa wydajność modeli LLM w zadaniach programistycznych

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 14 05:50:26 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099375198986461418)
- **Kluczowe pojęcia:** [[Harness|Benchmarking modeli LLM]] [[Harness|Agentic Coding]] [[Harness|Wariancja wyników]] [[Harness|Koszt tokenów]] [[Harness|Wybór modelu]]

---

## Kontekst i problem
Autor przeprowadził testy modeli LLM w zadaniu implementacji bazy wektorowej od zera, oceniając wydajność bazy danych. Porównuje stabilność wyników (wariancję) oraz szczytową wydajność modeli, aby dostarczyć wskazówek dotyczących wyboru modelu w zależności od złożoności zadania i kosztu tokenów.

## Rada inżynierska
Dla zadań wymagających przewidywalności i oszczędności tokenów wybieraj modele o niskiej wariancji, takie jak GPT6-Astra. Dla złożonych zadań, gdzie można poświęcić więcej tokenów na iteracje, rozważ modele o wyższym potencjale (np. Fable-5.1), ale wymagają one starannego promptowania. Dla prostych zadań najlepszym stosunkiem jakości do kosztu jest DeepSeek-V4.1-Flash.

## Uwaga / Anty-wzorzec
Ocena modelu wyłącznie na podstawie najlepszego wyniku jest myląca – wysoka wariancja (np. Fable-5.1, Hy4-dev) może prowadzić do marnowania tokenów na wielokrotne próby. Nieodpowiednie użycie modelu o wysokiej wariancji bez doświadczenia w promptowaniu może być nieefektywne.

## Oryginalny cytat
> *"同步一波大模型写后端代码排行榜

GPT6-Astra 和 Fable-5.1 没来得及做视频, 直接给大家同步图文了.

就结论来说, 单纯后端 AgenticCoding 场景(注意我只说我这个测试, 用大模型从0实现向量数据库, 使用数据库性能计分. 别的我不知道). 目前Fable-5.1 还是SOTA. 写出来的向量数据库直接是第二名的2x.

不过Fable的表现反而跟GPT 完全反过来了, 之前测Anthropic的模型(opus/sonnet) 系列, 反而是最稳的, 三次测试中最高分和最低分差距不超过10%. 而这次 GPT6-Astra 三次得分反而很接近(12985.28, 12134.83, 10676.74), 这证明这个模型的后训练极其稳定, 而 Fable-5.1 则是  21191.51, 11915.19, 7998.93. Δ超过50%. 

所以从省token的角度, 其实更推荐使用 GPT6-Astra. 因为发挥稳定, 不需要重复抽卡. 而 Fable-5.1 更适合经验丰富的工程师好好写提示词后再使用.

国产模型正好也是这个局面, Hy4-dev 虽然分数高, 但是三次得分差距巨大, 10778.51, 6011.78, 4915.22. 而 Kimi-K3 则相对稳定. 另外最具性价比无疑是 DeepSeek-V4.1-Flash. 得分几乎跟 kimi-k3没区别了. 而且Δ<20%. 所以只要不是复杂的代码任务, 直接无脑 DeepSeek-V4.1-Flash最划算. 而复杂的尝试使用GPT6-Astra 和 Fable-5.1.

> #gpt6astra #fable51 #deepseekv41flash"*
