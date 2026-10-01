---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 14 07:14:23 +0000 2026"
źródło: "https://x.com/karminski3/status/2099396323942547519"
kategoria: "Inżynieria promptów / Reasoning Effort / Benchmarking"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Przełącznik intensywności rozumowania (max vs high) realnie skaluje wyniki modelu — dowód z DeepSeek-R1-Zero

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 14 07:14:23 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099396323942547519)
- **Kluczowe pojęcia:** [[Test-Time Compute i Reasoning Tokens|Reasoning Effort / Thinking Budget]] [[Test-Time Compute i Reasoning Tokens|Test-time Compute Scaling]] [[Harness|DeepSeek-R1-Zero]] [[Harness|AIME24 Benchmark]] [[Harness|RL bez nowej wiedzy (Zero-SFT RL)]] [[Harness|Saturacja rozumowania]]

---

## Kontekst i problem
Autor przetestował model deepseek-v4.1-flash z ustawieniem intensywności rozumowania na 'max'. W komentarzach spotkał się z zarzutem, że powinien użyć 'high', a nie 'max', oraz z tezą, że przełącznik思考强度 (thinking effort) jest wyłącznie kosmetycznym parametrem stylu i 'nie ma nic wspólnego z wydajnością'. Problem dotyczy tego, czy budżet rozumowania (thinking budget / reasoning effort) należy traktować jako realny wymiar skalowania jakości, czy jako nieistotny suwak.

## Rada inżynierska
Traktuj intensywność rozumowania jako realny wymiar test-time compute scaling, a nie kosmetyczny przełącznik. Argumentacja opiera się na pracy DeepSeek-R1-Zero: RL bez SFT i bez dostarczenia jakiejkolwiek nowej wiedzy, gdzie wraz ze wzrostem długości rozumowania wynik AIME24 wzrósł z ok. 15% do ok. 71%. Wniosek inżynierski: jeśli zadanie jest trudne (matematyka, wieloetapowe rozumowanie, kod), podnoszenie budżetu rozumowania do 'max' jest uzasadnione i powinno być walidowane benchmarkiem, a nie odrzucane na podstawie intuicji. Przy ocenie modeli zawsze raportuj użyty poziom reasoning effort — wyniki bez tego parametru są nieporównywalne.

## Uwaga / Anty-wzorzec
Antywzorzec: uznanie, że przełącznik思考强度 to jedynie 'styl' i nie wpływa na jakość — prowadzi to do błędnych wniosków przy porównywaniu modeli (porównywanie wyników z 'high' i 'max' jako równoważnych) oraz do ignorowania publikacji naukowych potwierdzających skalowanie przez długość rozumowania. Drugi antywzorzec: dyskutowanie o zachowaniu modelu bez sprawdzenia źródłowej dokumentacji/paperu.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor wprost podważa konsensus panujący w komentarzach pod wpisem, gdzie twierdzono, że ustawienie 'high' vs 'max' jest neutralne dla wydajności, a przełącznik to wyłącznie kontrola intensywności myślenia. Stanowisko autora (poparte paperem R1-Zero): wyższy budżet rozumowania = wyższa zdolność modelu. Do rozstrzygnięcia: czy obserwacja z R1-Zero (RL bez nowej wiedzy) przenosi się 1:1 na modele z rodziny V4.x z SFT/instruktażem, gdzie zjawisko saturacji i degradacji przy zbyt długim rozumowaniu może występować. Wymaga to własnego benchmarku na konkretnym zadaniu.

## Oryginalny cytat
> *"DS民科怎么这么多, 我测完了 deepseek-v4.1-flash, 开 max, 然后评论跟我说应该开high, 不应该开max. 〇的我买法拉利然后你跟我说挂一档比挂二挡快是吧? 然后跟我说这只是思考强度开关, 跟性能没关系. 干你〇怎么就没关系..... 去年 deepseek 自家发的 DeepSeek-R1-Zero 论文怎么都忘了: ... 就这个论文证明了思考强度越强模型能力越强的. 论文里Zero-SFT RL了一波, 没有增加任何新知识, 随着思考长度增加, AIME24 跑分就从 15% 魔法般的飙到了 71%. 然后震撼业界的雷霆大思考就如同雨后春笋般普及了..... 劝D小鬼对线前看看论文, 大水冲了自家龙王庙了."*
