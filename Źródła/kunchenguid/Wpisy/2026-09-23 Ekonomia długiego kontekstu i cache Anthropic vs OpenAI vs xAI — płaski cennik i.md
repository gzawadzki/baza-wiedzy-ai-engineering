---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Wed Sep 23 04:27:34 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2102615836242678094"
kategoria: "Ekonomia API / Inżynieria kontekstu i cache"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Ekonomia długiego kontekstu i cache: Anthropic vs OpenAI vs xAI — płaski cennik i tani cache read

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Wed Sep 23 04:27:34 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102615836242678094)
- **Kluczowe pojęcia:** [[Prompt Architecture|Cache promptu]] [[Prompt Architecture|Cached read]] [[Harness|Long context]] [[Harness|Koszt inferencji]] [[Prompt Architecture|Cache hit rate]] [[Harness|Anthropic Claude]] [[Harness|OpenAI]] [[Harness|xAI Grok]] [[Harness|Harness agentowy]]

---

## Kontekst i problem
Porównanie modeli rozliczeń trzech wiodących dostawców LLM (Anthropic, OpenAI, xAI) pod kątem dwóch czynników kosztowych, które są łatwe do przeoczenia przy projektowaniu systemów agentowych: (1) dopłaty za długi kontekst oraz (2) ceny odczytu z cache promptu. Ma to bezpośrednie znaczenie dla długich sesji kodowania i harnessów agentowych, gdzie kontekst rośnie w czasie.

## Rada inżynierska
Przy projektowaniu długich sesji agentowych/kodowania licz koszt jako funkcję dwóch wymiarów: (a) czy dostawca stosuje mnożnik 2x powyżej progu długiego kontekstu — Anthropic nalicza płaską stawkę nawet przy 1M tokenów, podczas gdy OpenAI podwaja cenę powyżej 272k, a Grok powyżej 200k; (b) cenę odczytu z cache (cached read) — u Anthropic najnowsze modele mają ją ekstremalnie niską. Ponieważ typowa sesja kodowania osiąga 95%+ cache hit rate, dominującym składnikiem kosztu staje się odczyt z cache, nie generacja. Wybierając providera i projektując architekturę promptu (stabilny prefiks, minimalizacja unieważnień cache), optymalizuj przede wszystkim cache hit rate — to on decyduje o rachunku, a nie sam rozmiar kontekstu.

## Uwaga / Anty-wzorzec
Naiwne porównywanie modeli wyłącznie po cenie za token wejściowy/wyjściowy bez uwzględnienia mnożników długiego kontekstu i ceny cached read. Przy 95% cache hit rate różnica w cenie odczytu z cache przekłada się na rząd wielkości kosztów, a dopłata 2x powyżej progu (272k u OpenAI, 200k u Grok) może niespodziewanie podwoić rachunek w długich sesjach.

## Oryginalny cytat
> *"since it’s been a good day for anthropic with a strong opus 5.5 release, i’m going to highlight one more thing that may not be obvious

across xai, openai and anthropic -

1. anthropic is the only provider that does not charge 2x for long context requests

even at 1M context, anthropic charge at the same flat rate, while openai charges 2x above 272k tokens, and grok charges 2x above 200k

2. anthropic’s latest models have ridiculously low pricing for cached read. see chart below

most coding sessions have 95%+ cache hit rate, so this difference is massive

my hunch is that eventually this will even out, but for now, this is a very material difference that’s easy to overlook"*
