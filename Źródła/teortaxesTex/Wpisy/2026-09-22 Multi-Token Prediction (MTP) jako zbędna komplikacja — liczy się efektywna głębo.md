---
typ: wpis-źródłowy
autor: "@teortaxesTex"
data: "Tue Sep 22 22:59:28 +0000 2026"
źródło: "https://x.com/teortaxesTex/status/2102533265265500175"
kategoria: "Architektura modeli / Cel treningowy / Interpretowalność"
tagi:
  - teortaxestex
  - ai-engineering
  - wpis-atomowy
---

# Multi-Token Prediction (MTP) jako zbędna komplikacja — liczy się efektywna głębokość obwodu

- **Autor:** [[teortaxesTex — Indeks|@teortaxesTex]] | **Data:** `Tue Sep 22 22:59:28 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102533265265500175)
- **Konwersacja:** Odpowiedź w dyskusji (@rudzinskimaciej)
- **Kluczowe pojęcia:** [[Architektura KV Cache i Rozumowanie Latentne|Multi-Token Prediction]] [[Harness|Next-Token Prediction]] [[Harness|Effective Circuit Depth]] [[Harness|Activation Look-Ahead]] [[Harness|Cel treningowy LLM]] [[Harness|Interpretowalność modeli]]

---

## Kontekst i problem
Dyskusja dotyczy sensowności celu treningowego Multi-Token Prediction (MTP) jako środka do uzyskania 'wyprzedzającego' przetwarzania w aktywacjach modelu. Autor argumentuje, że cele MTP są rozpraszaczem (red herring) — sam standardowy cel przewidywania pojedynczego tokenu (next-token prediction) wystarcza, aby aktywacje warstw wykazywały już właściwości antycypacyjne ('look ahead'). Prawdziwym problemem badawczym nie jest więc liczba przewidywanych tokenów, lecz efektywna głębokość obwodu (effective circuit depth) — czyli ile realnych kroków obliczeniowych model faktycznie wykonuje między wejściem a wyjściem.

## Rada inżynierska
Nie zakładaj, że MTP daje przewagę nad klasycznym next-token prediction w zakresie 'planowania' czy antycypacji — aktywacje już przy pojedynczym tokenie wykazują look-ahead. Skup się na mierzeniu efektywnej głębokości obwodu (effective circuit depth): jak wiele sekwencyjnych kroków obliczeniowych model faktycznie realizuje, a nie jak wiele tokenów przewiduje na raz. MTP zmienia dystrybucję gradientu, ale niekoniecznie zwiększa realną pojemność obliczeniową na token.

## Uwaga / Anty-wzorzec
Traktowanie MTP jako magicznego rozwiązania poprawiającego 'rozumienie kontekstu' lub zdolność planowania — to błąd kategorii. MTP to modyfikacja celu treningowego, nie zmiana architektury obliczeniowej ani głębokości sieci. Zamiana celu bez zrozumienia efektywnej głębokości obwodu prowadzi do optymalizacji pod metrykę, a nie pod rzeczywistą zdolność obliczeniową.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor podważa popularny nurt badawczy (m.in. prace Meta/DeepSeek nad MTP jako ulepszaczem rozumowania i planowania). Formułuje tezę, że MTP nie wnosi nowej zdolności antycypacji — aktywacje już to robią przy zwykłym next-token prediction. Do rozstrzygnięcia: czy przewaga MTP w benchmarkach wynika z lepszego gradientu/regularizacji, czy z realnego zwiększenia efektywnej głębokości obwodu. Brakuje tu definicji operacyjnej 'effective circuit depth' i sposobu jej pomiaru.

## Oryginalny cytat
> *"MTP is a red herring. Single token prediction objective is sufficient for activations to already "look ahead"
my question is about *effective* circuit depth"*
