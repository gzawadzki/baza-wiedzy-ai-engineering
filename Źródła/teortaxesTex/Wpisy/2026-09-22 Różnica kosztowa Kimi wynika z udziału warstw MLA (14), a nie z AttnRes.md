---
typ: wpis-źródłowy
autor: "@teortaxesTex"
data: "Tue Sep 22 07:12:35 +0000 2026"
źródło: "https://x.com/teortaxesTex/status/2102294974876536906"
kategoria: "Architektura modeli / Koszty inferencji"
tagi:
  - teortaxestex
  - ai-engineering
  - wpis-atomowy
---

# Różnica kosztowa Kimi wynika z udziału warstw MLA (1/4), a nie z AttnRes

- **Autor:** [[teortaxesTex — Indeks|@teortaxesTex]] | **Data:** `Tue Sep 22 07:12:35 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102294974876536906)
- **Konwersacja:** Odpowiedź w dyskusji (@SpXMerlin1D)
- **Kluczowe pojęcia:** [[Harness|MLA]] [[Architektura KV Cache i Rozumowanie Latentne|Multi-head Latent Attention]] [[Harness|AttnRes]] [[Harness|Koszt inferencji]] [[Harness|Architektura modeli LLM]] [[Harness|Porównanie modeli]]

---

## Kontekst i problem
Dyskusja nad źródłem wyższego kosztu modelu Kimi względem porównywanego modelu. Autor odrzuca hipotezę, że odpowiada za to mechanizm AttnRes (attention residual), wskazując jako rzeczywistą przyczynę kosztu specyficzną konfigurację warstw uwagi — MLA (Multi-head Latent Attention) stanowiące proporcję 1/4 warstw. Problem: błędne przypisywanie różnic kosztowych do ogólnego mechanizmu uwagi, zamiast do udziału konkretnych, kosztownych typów warstw.

## Rada inżynierska
Analizując koszt inferencji/trainingu między modelami, identyfikuj konkretne typy warstw i ich proporcję w architekturze (np. MLA, GQA, MHA) zamiast przypisywać różnice ogólnym mechanizmom uwagi. Koszt modelu jest silnie sprzężony z liczebnością i rozkładem konkretnych warstw uwagi, a nie tylko z deklarowanym wariantem architektury.

## Uwaga / Anty-wzorzec
Przypisywanie różnic w koszcie modeli domniemanym innowacjom architektonicznym (np. AttnRes) bez weryfikacji rzeczywistego udziału kosztownych warstw (np. MLA przy proporcji 1/4) w całym modelu.

## Oryginalny cytat
> *"@SpXMerlin1D we know it's not AttnRes, Kimi is just hella more expensive due to 1/4 MLA layers"*
