---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Tue Sep 15 07:47:29 +0000 2026"
źródło: "https://x.com/karminski3/status/2099767043155218568"
kategoria: "Prompt architecture / Benchmarking / Ekonomia inferencji"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# reasoning_effort jako marketing: przenoszenie kosztu obliczeń i ryzyka rozliczeniowego na użytkownika

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Tue Sep 15 07:47:29 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099767043155218568)
- **Kluczowe pojęcia:** [[Test-Time Compute i Reasoning Tokens|reasoning_effort]] [[Harness|Benchmark Methodology]] [[Harness|Cost-Performance Balance]] [[Harness|Thinking Effort vs Performance]] [[Test-Time Compute i Reasoning Tokens|Inference Compute Budget]] [[Prompt Architecture]]

---

## Kontekst i problem
Dyskusja wokół parametru reasoning_effort (thinking effort) w modelach rozumujących. Autor odpowiada na zarzuty, że w benchmarkach porównuje DeepSeek na poziomie 'high' z innymi modelami na 'max'. Problem dotyczy metodologii benchmarków oraz tego, jak dostawcy pozycjonują poziomy reasoning effort — oficjalne benchmarki są mierzone na 'max', ale marketingowo wskazuje się 'high' jako sweet spot (cost–performance balance), co prowadzi do błędnego wniosku, że 'high' = najlepsza jakość. Autor przytacza raport techniczny deepseek-v4-1-flash, w którym 'max' opisano jako 'best reserved for the most challenging tasks'.

## Rada inżynierska
Nie utożsamiaj poziomu reasoning effort z jakością odpowiedzi. Traktuj reasoning_effort jako parametr budżetu obliczeń (compute budget), a nie gwarancję wyższej precyzji. Przy benchmarkach porównuj modele przy tej samej efektywnej alokacji compute (max vs max albo high vs high), inaczej wynik jest nieważny metodologicznie. Czytaj raporty techniczne dosłownie: skoro producent pisze, że 'max' jest zarezerwowane dla najtrudniejszych zadań, to 'max' nie jest domyślnym trybem produkcyjnym — 'high' jest sweet spotem cost–performance według samych dostawców.

## Uwaga / Anty-wzorzec
Traktowanie reasoning_effort jako dźwigni jakości: użytkownik sądzi, że 'high' to optimum, bo benchmarki pokazują 'max', ale marketing wskazuje 'high'. To odwraca uwagę od realnego problemu: producenci transferują na użytkownika decyzję o kompromisie compute/precyzja oraz ryzyko kosztów rozliczeniowych. Anty-wzorzec: mieszanie poziomów effort między modelami w benchmarku (np. DeepSeek high vs inne max) — prowadzi do fałszywych porównań.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor podważa branżowy konsensus, że wyższy reasoning_effort wprost przekłada się na wyższą jakość. Twierdzi, że reasoning_effort to narzędzie marketingowe przenoszące kompromis compute/precyzja oraz ryzyko kosztów na użytkownika. Jednocześnie zaznacza, że rozbieżność effort↔performance wynika z niedostatecznego post-trainingu i docelowo (idealnie) effort powinien być równoważny wydajności — co jest tezą przeciwną do obecnej praktyki dostawców. Do rozstrzygnięcia: czy reasoning_effort należy traktować jako realną dźwignię jakości, czy wyłącznie jako parametr budżetu obliczeń.

## Oryginalny cytat
> *"问题在于我做的是 benchmark, 不是日常使用. 不能因其他模型都用max然后deepseek high 好单独用high测.

然后评论说应该用high测.

以及, reasoning_effort 在我看来是大模型厂商的营销手段. 把算力与精度的权衡交给了用户, 顺便把算力计费的风险也转移给了用户. 而且巧妙地进行掩饰: 宣称benchmark全是max跑出来的. 最后又说甜区(注意论文里称作cost–performance balance) 在high.

造成的结果就是, 有人认为high就是最好的.

我当然同意 thinking effort 不等价于 performance. 而且我认为之所以不等价是因为后训练拉了. 理想上应该追求让它等价.

但请注意, deepseek-v4-1-flash技术报告里给max评价为: best reserved for the most challenging tasks."*
