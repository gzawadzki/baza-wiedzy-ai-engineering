---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Thu Sep 17 06:16:35 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100468943853085061"
kategoria: "Architektura agentowa / Routing i dispatch zadań"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Zastąpienie routing'u zadań opartego na LLM dedykowanym, deterministycznym routerem (Jev) w orchestratorze Firstmate

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Thu Sep 17 06:16:35 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100468943853085061)
- **Kluczowe pojęcia:** [[Harness|Orchestrator]] [[Kaskady Modeli i Routing Pewności|Routing zadań]] [[Harness|Deterministyczny router]] [[Harness|LLM jako router]] [[Harness|Tool calls]] [[Harness|Latencja]] [[Harness|Koszt tokenów]] [[Harness|Agent harness]] [[Harness|Architektura systemów agentowych]] [[Firstmate i Agenci Wykonawczy]]

---

## Kontekst i problem
Firstmate działa jako orchestrator, który inteligentnie kieruje każde zadanie do odpowiedniego agenta (permutacja harnessu, modelu i poziomu reasoning effort) na podstawie preferencji użytkownika. Domyślnie decyzję o dispatchu podejmuje agent LLM: musi 'pomyśleć', wykonać wywołania narzędzi (odczyt reguł dispatchu, danych o kwotach/quota), a następnie dokonać przypisania. Ten proces jest wolny i konsumuje tokeny LLM. Autor zastąpił go dedykowanym routerem Jev, który podejmuje tę samą decyzję bez rozumowania i bez wywołań narzędzi w ~200 ms.

## Rada inżynierska
Decyzje deterministyczne w systemie agentowym (np. routing zadania do modelu/harnessu, dispatch) należy wyodrębnić z pętli LLM i przenieść do wyspecjalizowanego, taniego komponentu-routera. Na 25 ocenianych zadaniach Jev zwracał identyczną decyzję, jaką podjąłby LLM (poziom 'fable'), ale bez rozumowania i tool calls. Nawet uwzględniając pozostałe wywołanie narzędzia do inwokacji Jeva (nadal wykonywane przez agenta LLM), cały proces dispatchu uzyskał -71% kosztu i -90% czasu wall-clock. Jeśli liczyć wyłącznie zastąpiony fragment, oszczędność jest rzędu ~100x (100+ wywołań API Jeva = poniżej $0.01). Wniosek architektoniczny: LLM powinien być małym elementem systemu, a nie jego centrum decyzyjnym tam, gdzie reguła jest powtarzalna.

## Uwaga / Anty-wzorzec
Anty-wzorzec: używanie pełnego LLM z rozumowaniem i wywołaniami narzędzi do podejmowania deterministycznych, powtarzalnych decyzji (dispatch/routing). Prowadzi to do wysokiej latencji, marnowania tokenów i niepotrzebnych kosztów, mimo że wynik jest identyczny jak w prostym, specjalizowanym routerze. Kolejna pułapka: pomiar oszczędności bez rozróżnienia między całym systemem a zastąpionym fragmentem — autor wyraźnie rozdziela -71%/-90% (cały proces) od ~100x (sam zastąpiony fragment), co jest właściwą metodologią benchmarkingu.

## Oryginalny cytat
> *"alright - just got Jev deployed for a real production use case, which now performs at fable level quality but 10x faster and saves a ton of money ... i just replaced this dispatch process with Jev. it makes the same decision with no thinking or tool calls, done in ~200ms, and for the 25 tasks i evaluated this with, it gives the exact same answer fable would have given... there's still a tool call needed to invoke Jev, done by the firstmate agent which uses an LLM. but even with that counted, the saving from Jev still resulted in a -71% reduction in cost and -90% reduction in wall time ... Jev API calls themselves are almost free.. i made 100+ calls, and my usage dashboard still shows $0.01 ... i think this is starting to enable a whole new architectural paradigm for software. LLMs are just a small part of it."*
