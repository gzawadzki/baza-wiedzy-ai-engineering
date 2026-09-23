---
typ: wpis-źródłowy
autor: "@simonw"
data: "Fri Aug 14 20:26:14 +0000 2026"
źródło: "https://x.com/simonw/status/2088361577766691239"
kategoria: "Obserwacje zachowania modeli / Wydajność i benchmarking"
tagi:
  - simonw
  - ai-engineering
  - wpis-atomowy
---

# Narzut tokenów rozumowania: 22 276 reasoning tokens na 3 223 tokeny odpowiedzi (~7:1) w 21 minut

- **Autor:** [[simonw — Indeks|@simonw]] | **Data:** `Fri Aug 14 20:26:14 +0000 2026` | **Źródło:** [Post na X](https://x.com/simonw/status/2088361577766691239)
- **Konwersacja:** Odpowiedź w dyskusji (@simonw)
- **Kluczowe pojęcia:** [[Test-Time Compute i Reasoning Tokens|Reasoning tokens]] [[Test-Time Compute i Reasoning Tokens|Token throughput]] [[Harness|Latency]] [[Harness|Modele rozumujące]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Koszt inferencji]]

---

## Kontekst i problem
Autor dokumentuje rzeczywisty przebieg generowania przez model rozumujący: pełny czas odpowiedzi, liczbę tokenów rozumowania oraz liczbę tokenów wyjściowych, wraz z linkiem do pełnego transkryptu. To konkretny punkt danych do szacowania kosztu, opóźnienia i przepustowości przy zadaniach wymagających długiego łańcucha myślenia (reasoning).

## Rada inżynierska
Mierz i raportuj trzy metryki razem: czas generowania, tokeny rozumowania (ukryte/thinking) i tokeny wyjściowe. Stosunek reasoning:output rzędu 7:1 oznacza, że budżet kontekstu, koszt API i latency trzeba planować na podstawie tokenów rozumowania, a nie tylko widocznej odpowiedzi — do szacunków przyjmuj ~5–10x mnożnik względem długości finalnego tekstu. Zawsze zapisuj pełny transkrypt (link/artefakt), bo tylko on pozwala odtworzyć, gdzie model spalił budżet rozumowania i czy da się to skrócić (np. mocniejszym promptem, ograniczeniem zakresu, dostarczeniem kontekstu zamiast jego wyprowadzania).

## Uwaga / Anty-wzorzec
Planowanie kosztów i timeoutów na podstawie samych tokenów wyjściowych — prowadzi do niedoszacowania kosztu nawet o rząd wielkości oraz do przerywania długich, ale poprawnych generowań (21 minut) przez zbyt krótkie limity czasu.

## Oryginalny cytat
> *"It did take nearly 21 minutes to generate, and used 22,276 reasoning tokens to produce 3,223 tokens of output. Here's the full transcript: https://t.co/cjg2qhpBD4"*
