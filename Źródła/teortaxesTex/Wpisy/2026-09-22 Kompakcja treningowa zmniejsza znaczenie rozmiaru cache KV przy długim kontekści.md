---
typ: wpis-źródłowy
autor: "@teortaxesTex"
data: "Tue Sep 22 23:46:53 +0000 2026"
źródło: "https://x.com/teortaxesTex/status/2102545198199038197"
kategoria: "Inżynieria kontekstu / Pamięć i KV cache"
tagi:
  - teortaxestex
  - ai-engineering
  - wpis-atomowy
---

# Kompakcja treningowa zmniejsza znaczenie rozmiaru cache KV przy długim kontekście

- **Autor:** [[teortaxesTex — Indeks|@teortaxesTex]] | **Data:** `Tue Sep 22 23:46:53 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102545198199038197)
- **Konwersacja:** Odpowiedź w dyskusji (@awesome_ruler_)
- **Kluczowe pojęcia:** [[Architektura KV Cache i Rozumowanie Latentne|KV cache]] [[Context Compaction|Kompakcja treningowa]] [[Context Compaction|Długi kontekst]] [[Context Compaction|Inżynieria kontekstu]] [[Test-Time Compute i Reasoning Tokens|Reasoning modele]] [[Harness|Harness agentowy]]

---

## Kontekst i problem
Wpis dotyczy ograniczeń pamięciowych długiego kontekstu i cache KV. Autor odpowiada w dyskusji, że rozmiar cache przestaje być krytycznym wąskim gardłem, ponieważ modele zaczynają mieć dobrą kompakcję wyuczoną podczas treningu. Przy zużyciu około 890 MB na 1 mln tokenów kontekstu można po prostu utrzymywać pełne wyjścia rozumowania w kontekście, zamiast agresywnie je przycinać.

## Rada inżynierska
Nie optymalizuj przedwcześnie rozmiaru cache KV, jeśli model ma dobrą kompakcję treningową, a budżet pamięci pozwala na ok. 890 MB na 1 mln tokenów kontekstu. Utrzymuj pełne ślady reasoning w kontekście: upraszcza to harness agentowy, poprawia ciągłość rozumowania i redukuje potrzebę zewnętrznej kompresji oraz eviction.

## Uwaga / Anty-wzorzec
Antywzorzec: założenie, że mniejszy cache KV jest zawsze konieczny, i w efekcie agresywne przycinanie, streszczanie lub wyrzucanie wyjść reasoning. Przy dobrej kompakcji treningowej takie zabiegi mogą usuwać istotny kontekst i pogarszać stabilność oraz jakość długich sesji agentowych.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor podważa powszechny konsensus, że rozmiar cache KV i koszt pamięciowy długiego kontekstu są głównym ograniczeniem wymuszającym quantyzację, eviction lub agresywną kompresję kontekstu. Twierdzi, że kompakcja treningowa oraz zużycie rzędu 890 MB na 1 mln tokenów sprawiają, że można trzymać pełne wyjścia reasoning w kontekście bez większych strat.

## Oryginalny cytat
> *"@awesome_ruler_ @industriaalist @jayden_teoh_ Well, smaller cache doesn't matter much now
we're starting to have good training compaction, and at 890 Mb/1M context, you can just keep reasoning with outputs"*
