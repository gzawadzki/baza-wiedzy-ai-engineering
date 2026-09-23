---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 14 08:52:59 +0000 2026"
źródło: "https://x.com/karminski3/status/2099421138069950509"
kategoria: "Inżynieria promptów / Benchmarking / Reasoning LLM"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# SOTA jako kompresor informacji: minimalizacja tokenów zamiast reasoning max

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 14 08:52:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099421138069950509)
- **Kluczowe pojęcia:** [[Harness|SWE-bench]] [[Test-Time Compute i Reasoning Tokens|Reasoning Effort]] [[Harness|Chain-of-Thought]] [[Test-Time Compute i Reasoning Tokens|Overthinking]] [[Harness|Kompresja informacji]] [[Test-Time Compute i Reasoning Tokens|Token Throughput]] [[Harness|Early Stopping w LLM]] [[Harness|Benchmarkowanie modeli]] [[Prompt Architecture|Inżynieria promptów]]

---

## Kontekst i problem
Autor analizuje paradoks ustawiania modeli reasoningowych na maksymalny wysiłek (max). Wskazuje, że na benchmarku SWE wyniki mogą się odwracać, a ustawienie max nie zawsze jest właściwe. Podnosi problem poprawnego zatrzymywania rozumowania oraz tezę, że modele SOTA są idealnymi kompresorami informacji: rozwiązują najtrudniejsze problemy przy minimalnej liczbie tokenów.

## Rada inżynierska
Nie zakładaj, że zwiększanie budżetu rozumowania (reasoning effort = max) i wydłużanie CoT zawsze poprawiają wynik. Na zadaniach typu SWE-bench może wystąpić odwrócenie: dłuższe myślenie prowadzi do gorszych wyników. Optymalizuj prompt i model pod minimalizację tokenów potrzebnych do poprawnego rozwiązania oraz wczesne zatrzymywanie rozumowania po osiągnięciu wystarczającej pewności. SOTA to gęsta kompresja informacji — najkrótsza ścieżka do poprawnej odpowiedzi, a nie najdłuższa.

## Uwaga / Anty-wzorzec
Ślepe ustawianie reasoning effort = max, wymuszanie długiego myślenia i ocenianie jakości modelu po długości CoT. Prowadzi to do overthinkingu, dryfu rozumowania, marnowania tokenów, gorszych wyników na zadaniach inżynierskich oraz fałszywego wniosku, że więcej myślenia zawsze oznacza lepszy wynik.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Teza stoi w sprzeczności z popularnym konsensusem, że zwiększanie reasoning effort/„max” oraz długie CoT zawsze poprawiają wyniki. Autor twierdzi, że na SWE-bench może wystąpić odwrócenie, a modele SOTA powinny maksymalnie kompresować informację i używać minimalnej liczby tokenów. Do rozstrzygnięcia pozostaje: kiedy długie rozumowanie pomaga, kiedy szkodzi oraz jak mierzyć optymalny budżet tokenów dla danego zadania.

## Oryginalny cytat
> *"来, 走出民科, 咱们阅读论文. 
为什么max测SWE会倒挂：https://t.co/9cV5oLJLLH
设置为max真的就对吗：https://t.co/7QgZzJws0W
到底怎样才能让模型思考的时候正确的停下来: https://t.co/m1M1t03vJi 
我重申我的观点, SOTA的模型永远是完美的信息压缩器. 用最少的token解决最难的问题. 思考一大堆得出宇宙的最终解是42不是SOTA. E = mc² 才是."*
