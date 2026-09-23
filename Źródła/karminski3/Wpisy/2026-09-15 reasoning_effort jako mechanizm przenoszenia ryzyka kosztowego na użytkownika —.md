---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Tue Sep 15 07:47:23 +0000 2026"
źródło: "https://x.com/karminski3/status/2099767018279084387"
kategoria: "Benchmarking i konfiguracja modeli (reasoning_effort)"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# reasoning_effort jako mechanizm przenoszenia ryzyka kosztowego na użytkownika — pułapki benchmarków i uczciwość porównań

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Tue Sep 15 07:47:23 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099767018279084387)
- **Konwersacja:** Odpowiedź w dyskusji (@QuantumTransf)
- **Kluczowe pojęcia:** [[Test-Time Compute i Reasoning Tokens|reasoning_effort]] [[Harness|Benchmarkowanie modeli LLM]] [[Harness|Kompromis koszt-dokładność]] [[Harness|Uczciwość porównań benchmarkowych]] [[Harness|Post-training]] [[Harness|Przenoszenie ryzyka kosztowego na użytkownika]]

---

## Kontekst i problem
Autor broni metodologii swojego benchmarku przed krytyką, że model DeepSeek powinien być testowany na poziomie 'high' zamiast 'max'. Podnosi szerszy problem: parametr reasoning_effort (low/medium/high/max) to jego zdaniem narzędzie marketingowe dostawców LLM, które przenosi na użytkownika zarówno decyzję o kompromisie obliczenia/dokładność, jak i ryzyko rozliczeniowe za zużyte zasoby. Wskazuje na niespójność komunikacji: dostawcy twierdzą, że benchmarki są uruchamiane na 'max', a jednocześnie rekomendują 'high' jako sweet spot (w papierach: cost–performance balance).

## Rada inżynierska
W benchmarkach porównawczych utrzymuj spójny poziom reasoning_effort dla WSZYSTKICH testowanych modeli — nie można testować jednego modelu na 'high', gdy pozostałe działają na 'max', bo zaburza to uczciwość porównania. reasoning_effort traktuj jako oś kompromisu koszt–dokładność, a nie jako oś jakości: wyższy effort ≠ lepsza wydajność. 'max' rezerwuj dla najtrudniejszych zadań (tak explicite rekomenduje raport techniczny deepseek-v4-1-flash: 'best reserved for the most challenging tasks'), a 'high' jako domyślny sweet spot kosztowo-wydajnościowy.

## Uwaga / Anty-wzorzec
Naiwne założenie, że wyższy reasoning_effort = lepsza jakość — prowadzi do wybierania 'max' domyślnie i zawyżonych kosztów bez proporcjonalnego zysku. Drugi anty-wzorzec: mieszanie poziomów effort między modelami w jednym benchmarku (jeden na 'high', reszta na 'max'), co czyni wyniki nieporównywalnymi. Trzeci: bezkrytyczne przyjmowanie narracji marketingowej dostawców o benchmarkach 'na max' przy jednoczesnej rekomendacji 'high'.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor podważa powszechny konsensus branżowy, że parametr reasoning_effort jest neutralnym, użytecznym narzędziem kontroli. Twierdzi, że to głównie marketing i mechanizm przenoszenia ryzyka kosztowego/billingowego na użytkownika, przy jednoczesnej niespójnej komunikacji (benchmarki na 'max', rekomendacja 'high'). Dodatkowo formułuje tezę, że thinking effort powinno być równoważne performance, a obecny brak tej równoważności wynika ze słabego post-trainingu — co jest opinią kontrowersyjną wobec stanowiska dostawców, że różnica effortów jest zamierzonym, sensownym kompromisem kosztowym.

## Oryginalny cytat
> *"问题在于我做的是 benchmark, 不是日常使用. 不能因其他模型都用max然后deepseek high 好单独用high测. 然后评论说应该用high测. 以及, reasoning_effort 在我看来是大模型厂商的营销手段. 把算力与精度的权衡交给了用户, 顺便把算力计费的风险也转移给了用户. 而且巧妙地进行掩饰: 宣称benchmark全是max跑出来的. 最后又说甜区(注意论文里称作cost–performance balance) 在high. 造成的结果就是, 有人认为high就是最好的. 我当然同意 thinking effort 不等价于 performance. 而且我认为之所以不等价是因为后训练拉了. 理想上应该追求让它等价. 但请注意, deepseek-v4-1-flash技术报告里给max评价为: best reserved for the most challenging tasks."*
