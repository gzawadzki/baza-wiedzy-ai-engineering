---
typ: wpis-źródłowy
autor: "@HamelHusain"
data: "Mon Aug 17 19:47:25 +0000 2026"
źródło: "https://x.com/HamelHusain/status/2089438973714440196"
kategoria: "Ewaluacja i analiza błędów (Error Analysis)"
tagi:
  - hamelhusain
  - ai-engineering
  - wpis-atomowy
---

# Eval Skills: agentowe odkrywanie błędów przez inteligentne próbkowanie i grupowanie failure modes

- **Autor:** [[HamelHusain — Indeks|@HamelHusain]] | **Data:** `Mon Aug 17 19:47:25 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2089438973714440196)
- **Kluczowe pojęcia:** [[Harness|Error Analysis]] [[Harness|Failure Modes]] [[Harness|Intelligent Sampling]] [[Eval Set z realnych sesji|Eval Pipeline]] [[Dynamiczne Skille i Metaprogramowanie Agenta|Agent Skills]] [[Harness|LLM Traces]] [[Harness|Annotation App]] [[Harness|Human-in-the-loop]]

---

## Kontekst i problem
Analiza błędów (error analysis) na zbiorze trace'ów i wyjść modelu jest zwykle ręczna i kosztowna: trzeba przejrzeć logi, ręcznie zbudować UI do adnotacji, a potem samodzielnie kategoryzować notatki w tryby awarii (failure modes). Hamel Husain i Shreya Shankar rozwijają plugin 'eval skills' dla agentów kodujących, który automatyzuje ten workflow: agent generuje dedykowaną aplikację przeglądową z inteligentnym próbkowaniem, a następnie klastruje adnotacje użytkownika w failure modes i podaje powiązane przykłady. Dodano też skill 'start', który na podstawie opisu sytuacji użytkownika routuje agenta do właściwego workflow (znajdowanie błędów w trace'ach vs audyt istniejącego pipeline'u ewaluacyjnego).

## Rada inżynierska
Nie zaczynaj od metryk ani od automatycznych scorerów — zacznij od danych: podaj agentowi plik z wyjściami AI lub trace'ami, pozwól mu zbudować dedykowaną aplikację do przeglądu z inteligentnym próbkowaniem, a następnie adnotuj próbkę. Adnotacje powinny być przez agenta automatycznie grupowane w failure modes wraz z wyszukiwaniem podobnych przykładów — to zamienia ręczną analizę błędów w iteracyjną pętlę odkrywania wzorców. Warto też użyć skilla routującego ('start'), który wybiera właściwy tryb pracy: odkrywanie błędów w zestawie trace'ów albo audyt już istniejącego pipeline'u ewaluacji.

## Uwaga / Anty-wzorzec
Anty-wzorzec: traktowanie ewaluacji jako jednorazowego zadania lub wyłącznie jako warstwy automatycznych metryk bez etapu ludzkiej adnotacji i kategoryzacji błędów. Pomijanie routingu prowadzi do stosowania niewłaściwego workflow (np. audyt pipeline'u, gdy realnie brakuje rozpoznania trybów awarii), a brak inteligentnego próbkowania powoduje marnowanie wysiłku adnotacyjnego na przypadki nieinformacyjne.

## Oryginalny cytat
> *"A few months ago,@sh_reya and I released eval skills plugin. We iterated on it a bunch and recently made it better. The biggest change is a new error-discovery skill. Give your coding agent a file of AI outputs or traces, and it builds a custom review app w/intelligent sampling. As you annotate the sample, the agent groups your notes into failure modes and finds related examples. We also added a start skill, which looks at your situation and routes your agent to the right workflow. It can help you find errors in a set of traces or audit an eval pipeline you already have."*
