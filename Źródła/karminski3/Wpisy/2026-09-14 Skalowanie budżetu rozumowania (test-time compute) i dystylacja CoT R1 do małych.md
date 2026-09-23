---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 14 09:51:35 +0000 2026"
źródło: "https://x.com/karminski3/status/2099435885599367551"
kategoria: "Zachowanie modeli / Rozumowanie i dystylacja / Test-time compute"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Skalowanie budżetu rozumowania (test-time compute) i dystylacja CoT R1 do małych modeli — oraz anty-wzorzec „deepseek-r1-distilled-qwen-7b = DeepSeek”

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 14 09:51:35 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099435885599367551)
- **Konwersacja:** Odpowiedź w dyskusji (@sosolab13)
- **Kluczowe pojęcia:** [[Test-Time Compute i Reasoning Tokens|Test-time compute]] [[Harness|Budżet rozumowania]] [[Harness|Chain-of-Thought]] [[Harness|Dystylacja wiedzy]] [[Harness|DeepSeek-R1]] [[Harness|Qwen]] [[Harness|Ollama]] [[Harness|Skalowanie długości rozumowania]] [[Harness|Anty-wzorce w dystrybucji modeli]] [[Checkpointing sesji agenta]]

---

## Kontekst i problem
Autor odpowiada pod wpisem innego użytkownika, przypominając fakty z paperu DeepSeek-R1 (Sekcja 3) dotyczące zachowania modelu przy długim rozumowaniu. Problem, który adresuje: zbiorowa niepamięć branży co do tego, skąd wzięły się spektakularne skoki benchmarków oraz czym faktycznie są modele dystylowane krążące pod marką „DeepSeek”.

## Rada inżynierska
1) Wydajność rozumowania skalibruj przez budżet rozumowania w czasie inferencji (test-time compute), a nie tylko przez rozmiar modelu: w paperze R1 wydłużenie łańcucha myśli podniosło wynik z 71,0% do 86,7% — to jest ta sama zależność, którą później obserwowano na modelach dystylowanych. 2) Długie łańcuchy CoT (long CoT) generowane przez R1 można dystylować do małych modeli (Qwen 1,5B / 7B / 14B) i zachować przyrostową krzywą: przy dostatecznym budżecie tokenów rozumowania zdolność rozwiązywania zadań rośnie wprost proporcjonalnie do długości rozumowania. 3) Przy projektowaniu harnessu/agenta traktuj budżet rozumowania jako parametr pierwszoklasowy (osobny limit tokenów na thinking vs. odpowiedź), bo on realnie steruje jakością, a nie sam wybór checkpointu.

## Uwaga / Anty-wzorzec
Mylenie modelu dystylowanego z modelem źródłowym: `deepseek-r1-distilled-qwen-7b` to mały model Qwen uczony na długich CoT wygenerowanych przez R1 — nie jest to R1 ani „DeepSeek” w sensie modelu flagowego. Dystrybucja przez Ollama pod skróconą nazwą „deepseek” utrwaliła w środowisku błędne przekonanie o tożsamości i skali modelu, co prowadzi do błędnych wniosków o możliwościach, benchmarkach i wymaganiach sprzętowych. Drugi anty-wzorzec: pomijanie sekcji paperu opisujących zachowanie przy długim rozumowaniu i wyciąganie wniosków wyłącznie z nagłówków wyników.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor podważa rozpowszechniony w branży skrót myślowy, że modele dystylowane R1 (np. `deepseek-r1-distilled-qwen-7b` w Ollama) są „DeepSeekiem”. Do rozstrzygnięcia: czy popularyzacja dystylatów pod marką modelu źródłowego to akceptowalny skrót marketingowy, czy realne źródło błędnych decyzji inżynierskich (zawyżone oczekiwania co do jakości, nieadekwatne benchmarki, mylne wnioski o koszcie inferencji). Dodatkowo teza o wprost proporcjonalnym wzroście jakości od długości rozumowania wymaga weryfikacji: przy zbyt dużym budżecie występuje nasycenie i degradacja (overthinking), czego wpis nie precyzuje.

## Oryginalny cytat
> *"请读完了Section 2后继续看Section 3 . 明确写了模型在长思考时的表现. 当时震撼人心的继续从71.0% 飙升到 86.7% 就是这么来的. 然后将 R1 生成的长思维链蒸馏到了小模型（ Qwen-1.5B、7B、14B）。在运行时给足其思考预算，然后解题能力就呈现出与思考长度正相关的暴涨。这不就是去年的新闻嘛....怎么还能记不住呢....然后就ollama吧deepseek-r1-distilled-qwen-7b 当deepseek给大家装到电脑上了, 美其名曰运行deepseek. 有印象没? 串起来了吧?"*
