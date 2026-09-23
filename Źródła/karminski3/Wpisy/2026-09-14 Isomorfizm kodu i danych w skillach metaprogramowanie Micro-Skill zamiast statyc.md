---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 14 06:22:54 +0000 2026"
źródło: "https://x.com/karminski3/status/2099383368999965122"
kategoria: "Architektura systemów agentowych / Projektowanie skilli"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Isomorfizm kodu i danych w skillach: metaprogramowanie Micro-Skill zamiast statycznych dokumentów

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 14 06:22:54 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099383368999965122)
- **Kluczowe pojęcia:** [[Dynamiczne Skille i Metaprogramowanie Agenta|Micro-Skill]] [[Dynamiczne Skille i Metaprogramowanie Agenta|Metaprogramowanie skilli]] [[Harness|Isomorfizm kodu i danych]] [[Harness|Ekstrakcja hybrydowa regex + LLM]] [[Harness|Pydantic jako harness walidacyjny]] [[Weryfikator|Zewnętrzny weryfikator]] [[Prompt Architecture|Dynamiczna generacja promptów]] [[Dynamiczne Skille i Metaprogramowanie Agenta|Skill vs dokument]]

---

## Kontekst i problem
Problem: większość ludzi pisze 'skille' agentowe jak statyczne dokumenty — sztywne instrukcje typu 'wyciągnij datę i kwotę w tym formacie'. Taki skill działa tylko dla formatów przewidzianych przez autora i 'wybucha' przy każdej nieznanej odmianie dokumentu (np. nowy layout faktury). Autor pokazuje, że skill — inaczej niż zwykły dokument — może łączyć w sobie jednocześnie warstwę danych i warstwę kodu (kod i dane są izomorficzne), co otwiera drogę do metaprogramowania: model generuje na miejscu dedykowany, jednorazowy skill dopasowany do konkretnego wejścia.

## Rada inżynierska
Traktuj skill jako nośnik izomorficzny kod+dane, nie jako dokumentację. Zamiast zakodować z góry schemat ekstrakcji, zleć modelowi przeanalizowanie topologii układu i konwencji nazewniczych wejścia, a następnie dynamiczne wygenerowanie Micro-Skill składającego się z trzech warstw: (1) pola deterministyczne wyciągane regexem — kompilowane do klasycznego kodu; (2) pola niejednoznaczne obsługiwane przez LLM, z ultra-zwięzłym promptem ≤50 znaków; (3) klasa walidacyjna Pydantic jako prosty harness egzekwujący reguły spójności (np. kwota z VAT == kwota netto + VAT). Dzięki temu skill jest odporny na nieznane formaty, o ile model jest wystarczająco zdolny.

## Uwaga / Anty-wzorzec
Anty-wzorzec: 'skill jako dokument' — wpisanie na sztywno jednego formatu i jednego schematu ekstrakcji (np. 'wyciągnij datę i kwotę zgodnie z poniższym formatem'). Skutek: kruchość na nowych layoutach i brak jakiejkolwiek walidacji wyniku. Drugi błąd: wymuszanie bezpośredniego wyjścia JSON przez LLM bez rozdzielenia zadań deterministycznych (regex) od niejednoznacznych oraz bez zewnętrznego weryfikatora — prowadzi do halucynacji i cichych błędów w danych.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor podważa dominujący konsensus 'napisz raz dobry, uniwersalny prompt/skill i trzymaj się go'. Zamiast statycznej, ręcznie projektowanej definicji skilla proponuje podejście generatywne: skill tworzony ad hoc przez model dla każdego wejścia (Micro-Skill). Do rozstrzygnięcia: (a) koszt/latencja i powtarzalność dynamicznego generowania skilla przy każdym wywołaniu vs. utrzymanie jednego statycznego skilla; (b) niezawodność i weryfikowalność generowanego kodu (regex, Pydantic) — czy warto generować kod zamiast go po prostu napisać; (c) granica 'model wystarczająco zdolny' — kiedy metaprogramowanie przestaje być opłacalne i lepiej wrócić do statycznej definicji.

## Oryginalny cytat
> *"传统文档大多数时间只是【代码】或【数据】其中的一种. 而skill能实现代码与数据同构的特性... 而理解了skill的同构性就能玩元编程: "分析这张发票的排版拓扑和命名惯例, 不要直接输出 JSON 结果, 动态生成一个专用的skill(Micro-Skill)并运行它来提取配置, 包括: 哪些字段可以通过正则表达式确定性提取(编译为传统代码). 哪些歧义字段需要 LLM 提取, 并生成一份不超过 50 字的超精简 Prompt. 生成严格验证该格式的 Pydantic 校验类(简单harness, 类似含税金额 == 不含税金额 + 税额).""*
