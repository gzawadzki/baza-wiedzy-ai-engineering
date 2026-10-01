---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 14 09:51:35 +0000 2026"
źródło: "https://x.com/karminski3/status/2099435885599367551"
kategoria: "Modele rozumujące / Test-time compute / Destylacja"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Budżet myślenia a destylacja długiego CoT: dlaczego małe modele 'rosną' wraz z długością rozumowania

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 14 09:51:35 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099435885599367551)
- **Konwersacja:** Odpowiedź w dyskusji (@sosolab13)
- **Kluczowe pojęcia:** [[Test-Time Compute i Reasoning Tokens|Test-time compute]] [[Harness|Chain-of-Thought]] [[Harness|Destylacja wiedzy]] [[Harness|Budżet myślenia]] [[Harness|DeepSeek R1]] [[Harness|Modele rozumujące]] [[Harness|Ollama]] [[Harness|Anti-wzorce wdrożeń LLM]]

---

## Kontekst i problem
Dyskusja dotyczy wyników pracy (Section 2/3) opisującej zachowanie modelu przy długim rozumowaniu. Autor przypomina, że skok skuteczności z 71.0% do 86.7% wynikał wprost z wydłużenia ścieżki myślenia (test-time compute scaling). Następnie długie łańcuchy myślowe (long CoT) wygenerowane przez DeepSeek R1 zostały zdestylowane do małych modeli Qwen (1.5B, 7B, 14B). Problem w tym, że wielu użytkowników nie pamięta tego kontekstu i błędnie utożsamia małe modele destylowane z pełnym R1.

## Rada inżynierska
W modelach rozumujących jakość rozwiązania jest silnie dodatnio skorelowana z udostępnionym budżetem myślenia (thinking budget) w czasie inferencji — zwiększenie liczby tokenów rozumowania potrafi podnieść skuteczność o kilkanaście punktów procentowych (np. 71.0% → 86.7%). Mechanizm ten przenosi się na małe modele przez destylację długich łańcuchów myślowych (R1 → Qwen 1.5B/7B/14B): wystarczy dać im odpowiednio duży budżet myślenia, aby ich zdolność rozwiązywania zadań gwałtownie wzrosła. Praktyczna reguła: przy ocenie i wdrażaniu modelu rozumującego zawsze jawnie konfiguruj i raportuj budżet myślenia — wyniki bez tego parametru są nieporównywalne.

## Uwaga / Anty-wzorzec
Mylenie modelu destylowanego z modelem źródłowym. dystrybucja 'deepseek-r1-distilled-qwen-7b' przez ollama pod nazwą sugerującą uruchamianie 'DeepSeek' prowadzi użytkowników do przekonania, że lokalnie działa pełny DeepSeek R1. W rzeczywistości to mały model Qwen uczony na zdestylowanych śladach rozumowania R1 — inna architektura, inne możliwości, inne wymagania co do budżetu myślenia. Anty-wzorzec: wyciąganie wniosków o zdolnościach modelu na podstawie nazwy artefaktu, a nie jego pochodzenia i konfiguracji inferencji.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor podważa rozpowszechnioną praktykę ekosystemu ollama polegającą na udostępnianiu modeli destylowanych pod etykietą sugerującą pełny model źródłowy. Spór dotyczy tego, czy takie nazewnictwo i komunikacja są akceptowalnym uproszczeniem, czy wprowadzającym w błąd anty-wzorcem zniekształcającym percepcję realnych możliwości modeli rozumujących.

## Oryginalny cytat
> *"请读完了Section 2后继续看Section 3 . 明确写了模型在长思考时的表现. 当时震撼人心的继续从71.0% 飙升到 86.7% 就是这么来的. 然后将 R1 生成的长思维链蒸馏到了小模型（ Qwen-1.5B、7B、14B）。在运行时给足其思考预算，然后解题能力就呈现出与思考长度正相关的暴涨。这不就是去年的新闻嘛....怎么还能记不住呢....然后就ollama吧deepseek-r1-distilled-qwen-7b 当deepseek给大家装到电脑上了, 美其名曰运行deepseek. 有印象没? 串起来了吧?"*
