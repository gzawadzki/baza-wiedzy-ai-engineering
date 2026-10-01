---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Wed Sep 23 05:09:57 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2102626499748938117"
kategoria: "Benchmarking i ekonomika tokenów / Cache"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Cached read tokens dominują w realnym użyciu — surowe liczby z benchmarków mylą

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Wed Sep 23 05:09:57 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102626499748938117)
- **Konwersacja:** Odpowiedź w dyskusji (@immanuelg)
- **Kluczowe pojęcia:** [[Prompt Architecture|Prompt Caching]] [[Prompt Architecture|Cached Read Tokens]] [[Harness|Benchmarkowanie LLM]] [[Harness|Ekonomika tokenów]] [[Context Compaction|Inżynieria kontekstu]] [[Test-Time Compute i Reasoning Tokens|Token Throughput]] [[Harness|Latencja TTFT]]

---

## Kontekst i problem
Odpowiedź w dyskusji o porównywaniu liczb z benchmarków (koszt/opóźnienie/przepustowość). Autor kwestionuje wiarygodność zagregowanych liczb publikowanych przez dostawców lub wyciąganych z prostych testów, wskazując, że nie odzwierciedlają one struktury ruchu w produkcyjnym użyciu, gdzie większość odczytów z kontekstu trafia w cache.

## Rada inżynierska
Rozbij każdą analizę kosztu i opóźnienia na osobne kategorie rozliczeniowe: (1) cached read tokens, (2) uncached (fresh) read tokens, (3) write tokens. Dopiero ten podział pozwala przewidzieć zachowanie systemu w produkcji, ponieważ przy powtarzalnych, długich kontekstach (system prompt, wklejone pliki, historia rozmowy) to właśnie cached read tokeny zdominują wolumen. Benchmarki raportujące jedną zagregowaną liczbę tokenów lub jedno 'średnie' opóźnienie należy traktować jako niewiarygodne i zawsze normalizować do własnego profilu ruchu (długość promptu, współczynnik trafień w cache, głębokość historii).

## Uwaga / Anty-wzorzec
Przyjmowanie liczb 'na twarz' (face value) z publicznych benchmarków lub cenników jako prognozy kosztu i latencji własnego obciążenia — prowadzi to do błędnej architektury kontekstu i błędnych decyzji o modelu, gdyż pomija dominujący udział cached read tokens oraz efekt współczynnika trafień w cache.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Sprzeczność z powszechną praktyką branżową, w której porównuje się modele i providery po zagregowanych liczbach z benchmarków (koszt za milion tokenów, średni throughput, średnie TTFT). Autor twierdzi, że te wartości są mylące, bo w rzeczywistym użyciu wolumen zdominowany jest przez cached read tokens, których proporcja nie jest reprezentowana w typowym benchmarku. Do rozstrzygnięcia: czy benchmarki powinny raportować rozbicie per typ tokena i per współczynnik trafień w cache, oraz jak standaryzować takie pomiary.

## Oryginalny cytat
> *"@immanuelg you are being misled by those face value numbers

in real use, cached read tokens dominate over uncached read, and that’s why we have to look closer into these details"*
