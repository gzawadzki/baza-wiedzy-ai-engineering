---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 14 06:22:54 +0000 2026"
źródło: "https://x.com/karminski3/status/2099383368999965122"
kategoria: "Prompt architecture / inżynieria kontekstu / systemy agentowe"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Izomorfizm kodu i danych w skillach: metaprogramowanie zamiast statycznych promptów ekstrakcyjnych

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 14 06:22:54 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099383368999965122)
- **Kluczowe pojęcia:** [[Prompt Architecture|Prompt architecture]] [[Harness|Izomorfizm kodu i danych]] [[Dynamiczne Skille i Metaprogramowanie Agenta|Micro-Skill]] [[Prompt Architecture|Metaprogramowanie promptów]] [[Harness|Ekstrakcja deterministyczna vs LLM]] [[Harness|Pydantic jako harness weryfikujący]] [[Weryfikator|Zewnętrzny weryfikator]] [[Context Compaction|Inżynieria kontekstu]] [[Dynamiczne Skille i Metaprogramowanie Agenta|Anti-pattern: skill jako dokument]]

---

## Kontekst i problem
Autor krytykuje dominujący anty-wzorzec pisania skilli (umiejętności agenta) jako statycznych dokumentów: sztywnego promptu 'wyciągnij pole X i Y według poniższego formatu'. Takie skille łamią się przy pierwszym nieprzewidzianym formacie wejścia, bo z góry zakodowano konkretne przypadki. Proponuje traktowanie skilla jako bytu, w którym kod i dane są izomorficzne — czyli skill sam może generować wyspecjalizowane pod-skille (Micro-Skills) dopasowane do konkretnego dokumentu.

## Rada inżynierska
Zamiast statycznej instrukcji ekstrakcji pisz skill meta-poziomu, który: (1) najpierw analizuje topologię układu i konwencje nazewnicze dokumentu, (2) NIE zwraca od razu JSON-a, lecz dynamicznie generuje dedykowany Micro-Skill dla tego formatu, (3) rozdziela pola deterministyczne (ekstrahowane regexem, kompilowane do klasycznego kodu) od pól niejednoznacznych (ekstrahowane LLM-em przez ultra-zwięzły prompt <50 znaków), (4) generuje klasę walidacji Pydantic jako prosty, zewnętrzny harness weryfikujący spójność danych (np. kwota_z_podatkiem == kwota_netto + podatek). Skill staje się samoutrzymujący — przy wystarczająco zdolnym modelu nie wymaga ręcznej aktualizacji przy nowych formatach.

## Uwaga / Anty-wzorzec
Wypisywanie sztywnego promptu 'wyciągnij datę i kwotę według poniższego formatu' — to de facto spisanie dokumentu, nie skill. Każdy format spoza założeń powoduje 'wybuch' (błąd ekstrakcji). Inna pułapka: powierzanie LLM-owi pól, które da się wyekstrahować deterministycznie regexem — marnuje tokeny i wprowadza niedeterminizm tam, gdzie nie jest potrzebny.

## Oryginalny cytat
> *"传统文档大多数时间只是【代码】或【数据】其中的一种. 而skill能实现代码与数据同构的特性.

比如写一个处理发票的skill, 大部分人只会写:

"帮我按照下面的格式提取发票日期, 金额"

万一遇到个skill中没有的格式就炸了. 这其实就是把skill写成了文档.  

而理解了skill的同构性就能玩元编程: 

"分析这张发票的排版拓扑和命名惯例, 不要直接输出 JSON 结果, 动态生成一个专用的skill(Micro-Skill)并运行它来提取配置, 包括:
哪些字段可以通过正则表达式确定性提取(编译为传统代码).
哪些歧义字段需要 LLM 提取, 并生成一份不超过 50 字的超精简 Prompt.
生成严格验证该格式的 Pydantic 校验类(简单harness, 类似含税金额 == 不含税金额 + 税额). "

这样这个skill只要模型够聪明就不用管了."*
