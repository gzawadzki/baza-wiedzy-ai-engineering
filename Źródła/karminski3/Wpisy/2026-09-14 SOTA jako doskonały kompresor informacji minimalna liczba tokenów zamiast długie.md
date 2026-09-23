---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 14 09:14:59 +0000 2026"
źródło: "https://x.com/karminski3/status/2099426676669366337"
kategoria: "Prompt Architecture / Reasoning / Benchmarking"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# SOTA jako doskonały kompresor informacji: minimalna liczba tokenów zamiast długiego rozumowania

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 14 09:14:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099426676669366337)
- **Konwersacja:** Odpowiedź w dyskusji (@karminski3)
- **Kluczowe pojęcia:** [[Test-Time Compute i Reasoning Tokens|Test-time compute]] [[Test-Time Compute i Reasoning Tokens|Reasoning effort]] [[Harness|SWE-bench]] [[Harness|Kompresja informacji]] [[Test-Time Compute i Reasoning Tokens|Token throughput]] [[Harness|Benchmarkowanie modeli]]

---

## Kontekst i problem
Komentarz będący kontynuacją dyskusji o zachowaniu modeli rozumujących. Autor zestawia trzy problemy: (1) dlaczego benchmark SWE-bench 'odwraca się' (倒挂) przy ustawieniu reasoning effort = max, (2) czy ustawienie 'max' jest w ogóle właściwe, (3) jak sprawić, by model poprawnie zatrzymywał rozumowanie. Teza nadrzędna: prawdziwie SOTA model to idealny kompresor informacji — rozwiązuje najtrudniejsze problemy przy minimalnej liczbie tokenów, a nie przez generowanie długich łańcuchów myślowych.

## Rada inżynierska
Oceniaj jakość modelu i rozwiązania przez pryzmat kompresji informacji, nie przez długość rozumowania. Optymalny wynik to maksymalna trafność przy minimalnej liczbie tokenów (elegancja typu E = mc²), a nie rozwlekły wywód dochodzący do banalnego wniosku ('42'). Przy strojeniu reasoning effort nie zakładaj z góry, że wyższe ustawienie = lepsze wyniki — waliduj na konkretnym benchmarku (np. SWE-bench), bo wyniki mogą się odwracać przy 'max'.

## Uwaga / Anty-wzorzec
Anty-wzorzec: ślepe przekonanie, że reasoning effort = max zawsze poprawia wyniki. Obserwacja autora: przy ustawieniu max wyniki na SWE-bench potrafią się odwracać (pogarszać) — nadmiar rozumowania degraduje skuteczność zamiast ją zwiększać. Drugi anty-wzorzec: utożsamianie 'SOTA' z długim, pozornie głębokim rozumowaniem kończącym się ogólnikową odpowiedzią.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Teza stoi w sprzeczności z dominującym konsensusem branżowym wokół test-time compute scaling, gdzie zakłada się, że więcej tokenów rozumowania (wyższy reasoning effort, dłuższy łańcuch myśli) przekłada się na lepsze wyniki w zadaniach trudnych. Autor twierdzi odwrotnie: prawdziwie SOTA to minimalna liczba tokenów przy najwyższej trafności, a 'max' reasoning effort może wręcz szkodzić (odwrócenie wyników na SWE-bench). Do rozstrzygnięcia: czy degradacja przy 'max' jest artefaktem konkretnego benchmarku/modelu, czy też ogólnym efektem nasycenia/rozmycia rozumowania (saturation/drift).

## Oryginalny cytat
> *"来, 走出民科, 咱们阅读论文. 为什么max测SWE会倒挂：... 设置为max真的就对吗：... 到底怎样才能让模型思考的时候正确的停下来：... 我重申我的观点, SOTA的模型永远是完美的信息压缩器. 用最少的token解决最难的问题. 思考一大堆得出宇宙的最终解是42不是SOTA. E = mc² 才是."*
