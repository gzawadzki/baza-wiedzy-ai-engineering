---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Tue Sep 22 07:10:43 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2102294506062385364"
kategoria: "Architektura systemów agentowych i ewaluacja"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Ewaluacja agentów przez wynik i wskaźnik reworku zamiast jakości promptu

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Tue Sep 22 07:10:43 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102294506062385364)
- **Konwersacja:** Odpowiedź w dyskusji (@kryptm4n)
- **Kluczowe pojęcia:** [[Harness|Ewaluacja agentów oparta na wyniku]] [[Rework Rate|Rework jako metryka]] [[Harness|Skalowanie nadzoru agentowego]] [[Harness|Agent-liść vs orkiestrator]] [[Firstmate i Agenci Wykonawczy]]

---

## Kontekst i problem
Odpowiedź na pytanie o jakość promptów generowanych przez system 'firstmate' w porównaniu do promptów pisanych ręcznie przez człowieka do pojedynczego agenta-liścia. Autor przyznaje, że nie prowadził dedykowanej ewaluacji jakości samych promptów, ponieważ jego interakcja z agentem-liściem jest iteracyjna, a nie jednorazowa — co utrudnia bezpośrednie porównanie.

## Rada inżynierska
Nie ewaluuj jakości promptu w izolacji — jest to niemiarodajne, gdy praca z agentem-liściem odbywa się iteracyjnie (brak jednego 'pełnego' promptu do porównania). Zamiast tego mierz wynik (outcome) oraz częstość reworku/korekt. Uznaj, że sterowanie bezpośrednie daje większą kontrolę i szybsze rezultaty, ale nie skaluje się, natomiast warstwa orkiestracji (firstmate) skaluje kosztem okazjonalnych rozjazdów wymagających późniejszej korekty — to analogia do tradeoffu między zarządzaniem dużą organizacją a robieniem wszystkiego samemu.

## Uwaga / Anty-wzorzec
Porównywanie jakości promptu w izolacji między trybem interaktywnym a autonomicznym — bezpośrednia rozmowa z agentem-liściem jest z natury iteracyjna i nie da się jej sprowadzić do jednego 'promptu' porównywalnego z tym, co pisze firstmate.

## Oryginalny cytat
> *"this is a very good question and i have not done a dedicated evaluation on just the quality of the prompts

it’s tricky because when i talk directly to a leaf node agent i don’t attempt to write a full requirement upfront and expect autonomous execution. i typically end up doing it a lot more iteratively, so often times i don’t have a single “prompt” that’s comparable to what firstmate would write

i think what’s more practical is to evaluate the outcome, and how often rework happens. i haven’t quantified this but it’s a good thing to look into. qualitatively i definitely think whenever i directly talk to a leaf node agent i can steer it more closely and get better results faster - but i end up spending a lot of time and it doesn’t scale. firstmate helps me scale but occasionally there will be misalignment and needs correction later on. much like  the tradeoff between managing a large human organization vs doing everything myself"*
