---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Wed Sep 23 15:51:25 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2102787931178176588"
kategoria: "Architektura systemów agentowych / obserwacje zachowania modeli"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# GPT-6 Luna jako „slow mode”: model wsadowy do pracy w tle, nie do interakcji

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Wed Sep 23 15:51:25 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102787931178176588)
- **Kluczowe pojęcia:** [[Harness|Systemy agentowe]] [[Firstmate Agent|Firstmate]] [[Harness|Przepustowość tur]] [[Harness|Latencja end-to-end]] [[Harness|Koszt tokenów]] [[Harness|Tryb rozumowania]] [[Harness|Benchmarking modeli]]

---

## Kontekst i problem
Autor testuje model GPT-6 Luna pod kątem pracy z agentami. Model jest bardzo tani i ostatecznie wykonuje zadania, ale potrzebuje wielu tur, przez co interaktywne użycie staje się praktycznie nieużywalne. Problem ujawnia się szczególnie, gdy Luna ma działać jako wysokorozumujący firstmate/orkiestrator: tempo napływu zdarzeń przewyższa tempo przetwarzania tur, więc kolejka rośnie i system nigdy nie kończy pracy.

## Rada inżynierska
Dobieraj model do trybu pracy agenta na podstawie przepustowości tur, czyli liczby tur potrzebnych do ukończenia zadania, a nie tylko TTFT lub tokenów na sekundę. Do interakcji wybieraj modele o krótkim horyzoncie działania i niskiej liczbie tur. Do zadań wsadowych w tle, gdzie latencja end-to-end nie jest krytyczna, opłaca się użyć bardzo taniego modelu typu „slow mode”, który ma wysokie ROI i dobrą jakość końcową, mimo wolnego domykania zadań.

## Uwaga / Anty-wzorzec
Używanie wolnego, wysokorozumującego modelu jako interaktywnego firstmate/orkiestratora, gdy zdarzenia napływają szybciej, niż model przetwarza kolejne tury. Powoduje to narastanie zaległości i teoretycznie nieskończone opóźnienie. Drugi anty-wzorzec to ocenianie modelu wyłącznie po czasie do pierwszego tokena lub tokenach na sekundę, bez pomiaru liczby tur do rezultatu.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor podważa dominujący trend „fast mode”, w którym modele przyspiesza się kosztem wyższej ceny, i twierdzi, że potrzebny jest także „slow mode” do pracy w tle. Sprzeciwia się też powszechnemu założeniu, że wysokie reasoning jako firstmate/orkiestrator jest zawsze właściwym wyborem: według niego w przypadku Luny taka konfiguracja nie działa z powodu przeciążenia zdarzeniami i braku przepustowości tur.

## Oryginalny cytat
> *"just took gpt 6 luna for a spin, and… it’s a very weird model

1. it’s insanely cheap, even with the point below considered

2. it’s extremely slow, not in terms of time to first token or toks/sec, but how many turns it takes to get something done

3. it eventually does get shit done.. 

this created an interesting condition - using it interactively feels totally unusable because you have to wait for many turns before a useful outcome comes back

i tried it with high reasoning as firstmate and it straight doesn’t work, because by the time it finishes the current turn there are already two more turns worth of events piled up for it to process. it cannot keep up and literally will never finish

but if used as a background workhorse, and you don’t care that much about e2e latency, then it’s _extremely_ cost-efficient and capable - nothing else even comes close to this ROI

when the labs brought us “fast mode” which makes the models faster but costs more, i jokingly said i actually wanted a “slow mode”

turns out luna is the slow mode"*
