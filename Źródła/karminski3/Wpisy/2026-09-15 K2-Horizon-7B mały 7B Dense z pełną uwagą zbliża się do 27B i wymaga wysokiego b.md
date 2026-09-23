---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Tue Sep 15 22:37:55 +0000 2026"
źródło: "https://x.com/karminski3/status/2099991128061919596"
kategoria: "Modele językowe / Benchmarki / Wdrożenia produkcyjne"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# K2-Horizon-7B: mały 7B Dense z pełną uwagą zbliża się do 27B i wymaga wysokiego budżetu kontekstu

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Tue Sep 15 22:37:55 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099991128061919596)
- **Kluczowe pojęcia:** [[Harness|K2-Horizon-7B]] [[Harness|AA Bench]] [[Harness|Full Attention]] [[Harness|Long Context]] [[Harness|Kwantyzacja 8-bit]] [[Harness|Kwantyzacja 4-bit]] [[Harness|Unsloth]] [[Harness|vLLM]] [[Harness|SGLang]] [[Harness|Thinking Budget]] [[Harness|SWE-bench Verified]] [[Harness|Terminal Bench]]

---

## Kontekst i problem
IFM wypuścił otwarty model K2-Horizon-7B: 7B Dense, który w AA Bench osiąga 21 pkt przy 22 pkt Qwen3.6-27B, a w BrowseComp, SWE-bench Verified i Terminal Bench wypada bardzo dobrze. Model ma w pełni otwarte dane treningowe, recipe, kod treningowy i metody ewaluacji, wspiera 512K kontekstu oraz poziomy thinking low/medium/high. Problem inżynierski: jak wdrożyć tak mały model, nie ignorując kosztu pełnej uwagi przy długim kontekście.

## Rada inżynierska
Używaj K2-Horizon-7B z thinking=high (oficjalnie rekomendowane). Jeśli nie brakuje VRAM, uruchamiaj przez vLLM/SGLang, które już go wspierają. Do długiego kontekstu 128K w BF16 potrzebujesz ok. 18 GB VRAM/unified memory, więc przed produkcyjnym wdrożeniem lepiej poczekać na kwantyzację 8-bit/4-bit, np. od Unsloth. Pełna uwaga (full attention) oznacza, że koszt pamięci rośnie wraz z kontekstem mimo małej liczby parametrów.

## Uwaga / Anty-wzorzec
Anty-wzorzec: zakładanie, że model 7B zawsze ma tani długi kontekst. K2-Horizon-7B jest w pełni attention-based, więc 128K w BF16 wymaga ok. 18 GB pamięci. Wdrażanie wersji BF16 na małej GPU bez kwantyzacji może być niepraktyczne.

## Oryginalny cytat
> *"IFM刚放出了个神奇7B Dense小模型 K2-Horizon-7B. 神奇的是这玩意在AA Bench里面有21分, 而Qwen3.6-27B是22分, 也就是说这7B参数量快追平了27B的水平.
甚至这个模型在诸如BrowseComp测试中碾压了前几代旗舰模型(GPT-5/DeepSeek-V4). 而且工程能力比如SWEBench Verified/ Terminal Bench 分数表现也很亮眼.
所以敲打一波Qwen, 赶紧放出你们压箱底的Qwen3.8-35B-A3B, 别藏着掖着了. 要被偷家了!

这个模型现在完全是社区明星了, 它的训练数据, 怎么训练的(recipe), 训练代码以及评估方法全都是开源的. 参数上这个模型最大支持512K上下文, 但是注意, 这玩意虽然参数只有7B, 但是它是全注意力的, 所以上下文成本相当高. 目前还只有原始BF16精度, 如果要用128K上下文, 就要18G显存/统一内存. 所以还是等等8bit/4bit量化版本比较好(我刚在X上 @ unsloth 了一波, 看看哥俩会不会有时间做量化吧)

以及这个模型同样支持设置思考强度. 分为low/medium/high, 然后默认/官方强烈推荐用high.

如果现在不差显存想直接用可以使用vLLM/SGLang. 这俩已经支持了. 等 unsloth 放出量化版我给大家来一期10B以下小模型横评.  MiniCPM5-2B 和其他几个小模型已经在跑了.

#K2Horizon7B #MiniCPM52B #Qwen3835BA3B"*
