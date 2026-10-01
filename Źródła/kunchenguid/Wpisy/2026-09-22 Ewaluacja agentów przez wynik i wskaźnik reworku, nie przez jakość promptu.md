---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Tue Sep 22 07:10:43 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2102294506062385364"
kategoria: "Architektura systemów agentowych / Ewaluacja i metryki"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Ewaluacja agentów przez wynik i wskaźnik reworku, nie przez jakość promptu

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Tue Sep 22 07:10:43 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102294506062385364)
- **Konwersacja:** Odpowiedź w dyskusji (@kryptm4n)
- **Kluczowe pojęcia:** [[Harness|Ewaluacja agentów]] [[Firstmate Agent|Architektura firstmate]] [[Harness|Skalowanie agentów]] [[Harness|Koszt iteracji]] [[Rework Rate|Metryki reworku]] [[Firstmate i Agenci Wykonawczy]]

---

## Kontekst i problem
Odpowiedź na pytanie o jakość promptów generowanych przez system 'firstmate' w porównaniu do promptów pisanych ręcznie. Autor wyjaśnia, że bezpośrednia rozmowa z agentem-liściem (leaf node agent) jest z natury iteracyjna, więc nie istnieje pojedynczy, porównywalny prompt do oceny — co utrudnia bezpośrednie porównanie jakości promptów.

## Rada inżynierska
Nie oceniaj jakości promptu w izolacji — mierz wynik (outcome) oraz częstotliwość reworku. Bezpośrednia, iteracyjna interakcja z agentem-liściem daje większą kontrolę i szybsze rezultaty, ale nie skaluje się; system orkiestrujący (firstmate) skaluje, lecz wymaga korekt przy błędach wyrównania. Kluczowa metryka to odsetek przypadków wymagających poprawy, a nie jakość pojedynczego promptu.

## Uwaga / Anty-wzorzec
Porównywanie promptu generowanego przez system z pojedynczym promptem pisanym ad hoc w trybie iteracyjnym — to porównanie nieadekwatne, bo interakcja iteracyjna nie tworzy jednego artefaktu promptu. Ocena jakości promptu w izolacji jest myląca; właściwą metryką jest wynik i koszt korekty.

## Oryginalny cytat
> *"this is a very good question and i have not done a dedicated evaluation on just the quality of the prompts

it’s tricky because when i talk directly to a leaf node agent i don’t attempt to write a full requirement upfront and expect autonomous execution. i typically end up doing it a lot more iteratively, so often times i don’t have a single “prompt” that’s comparable to what firstmate would write

i think what’s more practical is to evaluate the outcome, and how often rework happens. i haven’t quantified this but it’s a good thing to look into. qualitatively i definitely think whenever i directly talk to a leaf node agent i can steer it more closely and get better results faster - but i end up spending a lot of time and it doesn’t scale. firstmate helps me scale but occasionally there will be misalignment and needs correction later on. much like  the tradeoff between managing a large human organization vs doing everything myself"*
