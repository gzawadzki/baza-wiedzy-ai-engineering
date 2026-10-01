---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 14 08:52:59 +0000 2026"
źródło: "https://x.com/karminski3/status/2099421138069950509"
kategoria: "Inżynieria rozumowania / Test-time compute / Ewaluacja modeli"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Maksymalny budżet rozumowania nie zawsze poprawia SWE; SOTA jako kompresja informacji

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 14 08:52:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099421138069950509)
- **Kluczowe pojęcia:** [[Test-Time Compute i Reasoning Tokens|Test-time compute]] [[Test-Time Compute i Reasoning Tokens|Reasoning budget]] [[Harness|SWE-bench]] [[Test-Time Compute i Reasoning Tokens|Overthinking]] [[Harness|Stopping criteria]] [[Harness|Information compression]] [[Harness|LLM benchmarking]] [[Prompt Architecture|Prompt architecture]]

---

## Kontekst i problem
Autor zachęca do czytania prac naukowych zamiast powielania mitów. Omawia zjawisko odwrócenia wyników SWE (prawdopodobnie SWE-bench) przy ustawieniu maksymalnego rozumowania, kwestionuje sensowność ustawienia „max” oraz podkreśla problem właściwego zatrzymywania procesu myślenia modelu. Na koniec formułuje tezę, że modele SOTA są idealnymi kompresorami informacji: rozwiązują najtrudniejsze problemy przy minimalnej liczbie tokenów.

## Rada inżynierska
Nie utożsamiaj długości rozumowania z jakością. Przed ustawieniem reasoning budget na max zweryfikuj metryki na swoim zadaniu, ponieważ zbyt długie myślenie może powodować spadek wyników (inwersję). Projektuj jawne kryteria stopu i testuj różne poziomy budżetu tokenów. Celem modelu SOTA jest minimalna liczba tokenów przy najtrudniejszych problemach — traktuj go jak kompresor informacji.

## Uwaga / Anty-wzorzec
Anty-wzorzec: ślepe ustawianie reasoning effort / max thinking tokens na najwyższą wartość i wiara, że model „im dłużej myśli, tym lepiej odpowie”. Prowadzi to do overthinkingu, błędnego zatrzymania, marnowania tokenów i możliwej regresji na benchmarkach typu SWE.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor podważa popularny konsensus, że zwiększanie budżetu rozumowania do maksimum (max reasoning / test-time compute) zawsze poprawia wyniki. Wskazuje na możliwą inwersję metryk SWE przy ustawieniu max oraz na potrzebę poprawnego zatrzymywania myślenia modelu, co stoi w sprzeczności z prostym wnioskiem „więcej myślenia = lepszy wynik”.

## Oryginalny cytat
> *"来, 走出民科, 咱们阅读论文. 
为什么max测SWE会倒挂：https://t.co/9cV5oLJLLH
设置为max真的就对吗：https://t.co/7QgZzJws0W
到底怎样才能让模型思考的时候正确的停下来: https://t.co/m1M1t03vJi 
我重申我的观点, SOTA的模型永远是完美的信息压缩器. 用最少的token解决最难的问题. 思考一大堆得出宇宙的最终解是42不是SOTA. E = mc² 才是."*
