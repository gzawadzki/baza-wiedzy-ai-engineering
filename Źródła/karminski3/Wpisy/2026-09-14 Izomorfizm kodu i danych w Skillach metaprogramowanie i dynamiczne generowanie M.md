---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 14 06:23:09 +0000 2026"
źródło: "https://x.com/karminski3/status/2099383433034440811"
kategoria: "Architektura systemów agentowych / Inżynieria promptów"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Izomorfizm kodu i danych w Skillach: metaprogramowanie i dynamiczne generowanie Micro-Skill

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 14 06:23:09 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099383433034440811)
- **Konwersacja:** Odpowiedź w dyskusji (@kalasoo)
- **Kluczowe pojęcia:** [[Dynamiczne Skille i Metaprogramowanie Agenta|Skill]] [[Dynamiczne Skille i Metaprogramowanie Agenta|Micro-Skill]] [[Prompt Architecture|Metaprogramowanie promptów]] [[Harness|Izomorfizm kodu i danych]] [[Context Compaction|Inżynieria kontekstu]] [[Weryfikator|Zewnętrzny weryfikator / harness]] [[Harness|Pydantic jako walidator]] [[Harness|Ekstrakcja deterministyczna vs LLM]] [[Dynamiczne Skille i Metaprogramowanie Agenta|Anti-wzorce skilli]]

---

## Kontekst i problem
Autor polemizuje z dominującym podejściem do tworzenia 'skills' (umiejętności agenta) jako statycznych dokumentów z szablonem promptu i przykładowym formatem wejścia. Problem: skill napisany jako sztywny dokument (np. 'wyodrębnij datę i kwotę faktury w tym formacie') pęka, gdy pojawi się nieznany wariant formatu wejściowego. Rozwiązanie opiera się na traktowaniu skilla jako struktury izomorficznej z kodem i danymi — czyli takiej, która potrafi wygenerować samą siebie w wyspecjalizowanej wersji dopasowanej do konkretnego przypadku.

## Rada inżynierska
Projektuj skille jako programy, nie dokumenty. Zamiast wpisywać na sztywno schemat ekstrakcji, zbuduj skill, który najpierw analizuje topologię układu i konwencje nazewnicze wejścia, a następnie dynamicznie generuje wyspecjalizowany Micro-Skill (skill jednorazowy, dopasowany do danego przypadku). Micro-Skill powinien rozdzielać pracę: (1) pola deterministyczne — kompilowane do wyrażeń regularnych (tradycyjny kod, zero tokenów LLM, pełna powtarzalność), (2) pola niejednoznaczne — obsługiwane przez ultra-zwięzły prompt LLM (limit ~50 słów), (3) klasa walidacyjna Pydantic jako zewnętrzny harness weryfikujący spójność semantyczną (np. kwota z VAT == kwota netto + VAT). Taki podział przenosi koszt i ryzyko z modelu na deterministyczny kod tam, gdzie to możliwe.

## Uwaga / Anty-wzorzec
Anty-wzorzec: 'skill jako dokument'. Wpisanie na sztywno jednego formatu i jednego szablonu promptu bez warstwy generatywnej. Skutek: kruchość na nieznanych wariantach wejścia (fail na pierwszym odstępstwie od założonego schematu), brak walidacji wyników oraz marnowanie tokenów LLM na pola, które dałoby się wyekstrahować regexem. Drugi anty-wzorzec: wymuszanie natychmiastowego wyjścia JSON zamiast etapu 'analiza → generacja skilla → uruchomienie', co odbiera systemowi zdolność adaptacji.

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
