---
typ: wpis-źródłowy
autor: "@simonw"
data: "Wed Aug 12 02:15:05 +0000 2026"
źródło: "https://x.com/simonw/status/2087362205994139805"
kategoria: "Inżynieria promptów"
tagi:
  - simonw
  - ai-engineering
  - wpis-atomowy
---

# Wymuszanie generowania SVG przez jawny prompt

- **Autor:** [[simonw — Indeks|@simonw]] | **Data:** `Wed Aug 12 02:15:05 +0000 2026` | **Źródło:** [Post na X](https://x.com/simonw/status/2087362205994139805)
- **Konwersacja:** Odpowiedź w dyskusji (@kelkarhr)
- **Kluczowe pojęcia:** [[Prompt Architecture|Prompt Engineering]] [[Harness|SVG]] [[Harness|Generowanie kodu]] [[Harness|LLM]] [[Harness|Format wyjścia]]

---

## Kontekst i problem
Użytkownik @kelkarhr prawdopodobnie zapytał, jak uzyskać od modelu wyjście w formacie SVG. Simon Willison odpowiada, że konieczne jest jawne poproszenie modelu o SVG i podaje konkretny prompt, którego używa do testowania generowania SVG.

## Rada inżynierska
Aby model wygenerował kod SVG, należy w promptcie wprost zażądać formatu SVG. Sprawdzony prompt: 'Generate an SVG of a pelican riding a bicycle'. Ta zasada odnosi się ogólnie do wymuszania pożądanego formatu wyjścia – bez explicitnej instrukcji model może wygenerować inny format.

## Uwaga / Anty-wzorzec
Zakładanie, że model sam z siebie wygeneruje SVG bez wyraźnego polecenia. Może to skutkować wyjściem w niepożądanym formacie (np. tekst, Python, base64).

## Oryginalny cytat
> *"@kelkarhr You need to ask it to output SVG

The prompt I use is "Generate an SVG of a pelican riding a bicycle""*
