---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Wed Sep 16 05:13:05 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100090575106310498"
kategoria: "Architektura harnessów i routing modeli"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Eskalacja do cięższego panelu LLM na podstawie kwantyfikowanej pewności modelu

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Wed Sep 16 05:13:05 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100090575106310498)
- **Konwersacja:** Odpowiedź w dyskusji (@nicknow)
- **Kluczowe pojęcia:** [[Kaskady Modeli i Routing Pewności|Routing modeli według pewności]] [[Kaskady Modeli i Routing Pewności|Kaskada modeli]] [[Harness|Mixture of Agents]] [[Harness|Kalibracja pewności modelu]] [[Harness|Ewaluacje modeli]] [[Harness|Koszt vs jakość inferencji]]

---

## Kontekst i problem
Dyskusja o nowym modelu, którego przewaga — według własnych ewaluacji dostawcy — wynika głównie z efektywności (koszt/latency/throughput), a nie z realnego skoku jakościowego. Autor wskazuje jednak na praktyczną wartość nowej funkcji: model potrafi sam skwantyfikować swoją pewność co do wyniku, co otwiera drogę do budowy dwupoziomowej architektury inferencji.

## Rada inżynierska
Traktuj pewność zwracaną przez model jako sygnał sterujący w harnessie: tanim, szybkim modelem obsługuj ścieżkę domyślną, a gdy jego self-reported confidence spadnie poniżej progu, eskaluj zadanie do cięższego panelu LLM (ensemble / mixture-of-agents / droższy model reasoningowy). To daje kontrolę kosztu bez utraty jakości na trudnych przypadkach — płacisz za drogi panel tylko tam, gdzie tani model nie jest pewny. Kluczowe: próg pewności kalibruj na własnym zbiorze walidacyjnym, bo deklarowana pewność modelu bywa niedokalibrowana.

## Uwaga / Anty-wzorzec
Ślepa wiara w deklarowaną pewność modelu bez kalibracji — modele często bywają overconfident na błędnych odpowiedziach, więc routing oparty wyłącznie na self-reported confidence może przepuszczać błędy. Drugi anty-wzorzec: ocenianie nowego modelu po hype'ie marketingowym zamiast po własnych ewaluacjach — jeśli zysk dotyczy głównie efektywności, migracja ma sens ekonomiczny, a nie jakościowy.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor podważa narrację o skoku jakościowym nowego modelu, twierdząc, że własne ewaluacje dostawcy wskazują na poprawę głównie w efektywności. Sporne wobec konsensusu branżowego („nowszy model = lepszy wynik”): realna wartość migracji może leżeć w koszcie/latency, a nie w zdolnościach — co zmienia strategię adopcji z „wymień model” na „użyj go jako taniej warstwy pierwszego rzutu z eskalacją”.

## Oryginalny cytat
> *"@nicknow it’s hard to imagine it doing better - their own evals also indicate it’s mostly about efficiency

but i like its ability to quantify confidence - i can easily build a system that says “if the result is not confident then let’s run a heavier LLM powered panel”"*
