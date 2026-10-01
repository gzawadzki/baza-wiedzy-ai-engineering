---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Tue Sep 15 22:37:55 +0000 2026"
źródło: "https://x.com/karminski3/status/2099991128061919596"
kategoria: "Modele LLM / Architektura i wdrożenia"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# K2-Horizon-7B: mały model Dense z pełną atencją zbliża się do 27B — koszt kontekstu i strategia wdrożenia

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Tue Sep 15 22:37:55 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099991128061919596)
- **Kluczowe pojęcia:** [[Harness|Full Attention vs GQA/MQA]] [[Architektura KV Cache i Rozumowanie Latentne|KV Cache]] [[Harness|Kwantyzacja LLM 8bit/4bit]] [[Harness|vLLM]] [[Harness|SGLang]] [[Test-Time Compute i Reasoning Tokens|Thinking Effort / Reasoning Budget]] [[Harness|Dense vs MoE]] [[Harness|Benchmarki LLM: AA Bench, BrowseComp, SWEBench Verified, Terminal Bench]] [[Harness|K2-Horizon-7B]] [[Harness|Qwen3.6-27B]]

---

## Kontekst i problem
IFM wypuściło K2-Horizon-7B — gęsty (Dense) model 7B z pełną atencją (full attention), obsługujący kontekst do 512K. Na AA Bench osiąga 21 pkt, podczas gdy Qwen3.6-27B ma 22 pkt, co sugeruje, że mała, gęsta architektura może zbliżyć się do większych modeli MoE. Model przebija poprzednie flagowce (GPT-5/DeepSeek-V4) m.in. w BrowseComp oraz radzi sobie w testach inżynierskich (SWEBench Verified, Terminal Bench). Cała receptura — dane treningowe, kod treningowy i metody ewaluacji — jest open source, co czyni go gwiazdą społeczności.

## Rada inżynierska
Przy wyborze małego modelu nie kieruj się wyłącznie liczbą parametrów. Kluczowe są: (1) typ atencji — pełna atencja w 7B oznacza liniowy wzrost kosztu KV cache i bardzo drogi długi kontekst; (2) dostępna precyzja — w BF16 przy 128K kontekstu 7B zajmuje ~18 GB VRAM/unified memory; (3) poziom thinking effort — model udostępnia low/medium/high z oficjalną rekomendacją używania high. Jeśli masz wystarczająco VRAM i potrzebujesz go teraz, używaj vLLM lub SGLang (oba już wspierają ten model). W przeciwnym razie poczekaj na kwantyzację 8-bit/4-bit — pełny BF16 jest nieefektywny pamięciowo przy długim kontekście. Prowadź systematyczne porównania małych modeli (<10B) zamiast polegać na pojedynczych benchmarkach.

## Uwaga / Anty-wzorzec
Błąd: zakładanie, że mniejszy model = tańszy inference przy długim kontekście. W modelach z pełną atencją (bez kompresji KV/GQA-podobnych optymalizacji, jak tu w 7B) koszt pamięci KV cache rośnie liniowo z długością kontekstu — 7B w BF16 nie jest tanim rozwiązaniem przy 512K/128K. Nie wdrażaj na produkcję bez kwantyzacji 8/4-bit, jeśli zależy ci na pamięci. Drugi antywzorzec: wnioskowanie o jakości modelu na podstawie jednego benchmarku (AA Bench) przy pominięciu domain-specific (BrowseComp, SWEBench, Terminal Bench).

## Oryginalny cytat
> *"IFM刚放出了个神奇7B Dense小模型 K2-Horizon-7B. 神奇的是这玩意在AA Bench里面有21分, 而Qwen3.6-27B是22分, 也就是说这7B参数量快追平了27B的水平. 甚至这个模型在诸如BrowseComp测试中碾压了前几代旗舰模型(GPT-5/DeepSeek-V4). 而且工程能力比如SWEBench Verified/ Terminal Bench 分数表现也很亮眼. 所以敲打一波Qwen, 赶紧放出你们压箱底的Qwen3.8-35B-A3B, 别藏着掖着了. 要被偷家了! 这个模型现在完全是社区明星了, 它的训练数据, 怎么训练的(recipe), 训练代码以及评估方法全都是开源的. 参数上这个模型最大支持512K上下文, 但是注意, 这玩意虽然参数只有7B, 但是它是全注意力的, 所以上下文成本相当高. 目前还只有原始BF16精度, 如果要用128K上下文, 就要18G显存/统一内存. 所以还是等等8bit/4bit量化版本比较好(我刚在X上 @ unsloth 了一波, 看看哥俩会不会有时间做量化吧) 以及这个模型同样支持设置思考强度. 分为low/medium/high, 然后默认/官方强烈推荐用high. 如果现在不差显存想直接用可以使用vLLM/SGLang. 这俩已经支持了. 等 unsloth 放出量化版我给大家来一期10B以下小模型横评.  MiniCPM5-2B 和其他几个小模型已经在跑了. #K2Horizon7B #MiniCPM52B #Qwen3835BA3B"*
