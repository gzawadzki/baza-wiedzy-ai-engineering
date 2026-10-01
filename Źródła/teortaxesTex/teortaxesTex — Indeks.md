---
typ: indeks-autora
autor: "@teortaxesTex"
źródło: "https://x.com/teortaxesTex"
tagi:
  - teortaxestex
  - ai-engineering
  - indeks
---

# @teortaxesTex — Indeks Bazy Wiedzy

> Kompletny indeks **17** wyodrębnionych, atomowych notatek inżynierskich z profilu @teortaxesTex.

## ⚠️ Kwestie sporne i rozbieżności do rozstrzygnięcia

> Wpisy podważające powszechne przekonania branżowe lub prezentujące odmienne podejście:

- **[[2026-09-21 Brak intencji artystycznej w LLM a wrogość nagrody opartej na wyniku|Brak intencji artystycznej w LLM a wrogość nagrody opartej na wyniku]]** — Teza kontrowersyjna wobec dominującego konsensusu branżowego, że skalowanie capability + outcome-based reward (np. RLVR, verifiable rewards) wystarcza do poprawy jakości generacji we wszystkich domenach. Autor twierdzi, że dla zadań wymagających intencji artystycznej outcome-based reward jest aktywnie szkodliwy (task-hostile), co podważa uniwersalność paradygmatu nagród weryfikowalnych i sugeruje potrzebę nagród procesowych lub innych sygnałów dla domen twórczych. Do rozstrzygnięcia: czy brak intencji artystycznej wynika z ograniczeń architektury nagrody, czy z natury samego modelu.
- **[[2026-09-22 Kompakcja treningowa zmniejsza znaczenie rozmiaru cache KV przy długim kontekści|Kompakcja treningowa zmniejsza znaczenie rozmiaru cache KV przy długim kontekście]]** — Autor podważa powszechny konsensus, że rozmiar cache KV i koszt pamięciowy długiego kontekstu są głównym ograniczeniem wymuszającym quantyzację, eviction lub agresywną kompresję kontekstu. Twierdzi, że kompakcja treningowa oraz zużycie rzędu 890 MB na 1 mln tokenów sprawiają, że można trzymać pełne wyjścia reasoning w kontekście bez większych strat.
- **[[2026-09-22 Marnotrawstwo CPU w sandboxach przy wielkoskalowym agentic RL — DSec i 3FS|Marnotrawstwo CPU w sandboxach przy wielkoskalowym agentic RL — DSec i 3FS]]** — Autor świadomie kontruje przewidywany konsensus rynkowy: „the usual suspects” mieliby uznać pełne wykorzystanie zasobów (efektywność sandboxów) za sygnał niedźwiedzi dla producentów CPU. Teza autora sugeruje odwrotność — efektywność napędza wolumen, a wąskim gardłem staje się storage/I/O, nie surowa moc obliczeniowa. Wymaga rozstrzygnięcia: czy optymalizacja utilization faktycznie redukuje popyt na CPU, czy go zwiększa poprzez obniżenie kosztu jednostkowego eksperymentu.
- **[[2026-09-22 Marnotrawstwo zasobów w sandboxach agentowego RL — DSec i 3FS jako odpowiedź na|Marnotrawstwo zasobów w sandboxach agentowego RL — DSec i 3FS jako odpowiedź na 5% wykorzystania CPU]]** — Autor formułuje kontrarian tezę wobec narracji rynkowej: powszechny konsensus interpretuje nowe, wydajniejsze systemy (DSec, 3FS) jako sygnał spadku popytu na CPU ('bearish for CPUs'). Autor twierdzi, że jest odwrotnie — lepsze wykorzystanie zasobów zwiększa realną przepustowość treningu agentowego przy tym samym sprzęcie, więc nie jest to sygnał niedźwiedzi. Spór dotyczy interpretacji efektywności infrastruktury jako wskaźnika popytu na sprzęt — do rozstrzygnięcia empirycznie (czy wzrost wykorzystania prowadzi do wzrostu, czy spadku zakupów CPU).
- **[[2026-09-22 MTP to ślepy zaułek — liczy się efektywna głębokość obwodu (effective circuit de|MTP to ślepy zaułek — liczy się efektywna głębokość obwodu (effective circuit depth)]]** — Autor podważa powszechny konsensus branżowy, że Multi-Token Prediction (stosowany m.in. w DeepSeek-V3) jest istotnym ulepszeniem celu treningowego poprawiającym jakość i zdolności planowania. Teza: MTP to 'red herring' — look-ahead w aktywacjach wynika już z samego next-token prediction, a prawdziwym problemem badawczym jest efektywna głębokość obwodu, nie cel treningowy. Do rozstrzygnięcia: czy MTP wnosi wartość niezależną od zwykłego NTP, czy jest jedynie kosztowną redundancją.
- **[[2026-09-22 Multi-Token Prediction (MTP) jako zbędna komplikacja — liczy się efektywna głębo|Multi-Token Prediction (MTP) jako zbędna komplikacja — liczy się efektywna głębokość obwodu]]** — Autor podważa popularny nurt badawczy (m.in. prace Meta/DeepSeek nad MTP jako ulepszaczem rozumowania i planowania). Formułuje tezę, że MTP nie wnosi nowej zdolności antycypacji — aktywacje już to robią przy zwykłym next-token prediction. Do rozstrzygnięcia: czy przewaga MTP w benchmarkach wynika z lepszego gradientu/regularizacji, czy z realnego zwiększenia efektywnej głębokości obwodu. Brakuje tu definicji operacyjnej 'effective circuit depth' i sposobu jej pomiaru.

---

## Spis tematów i notatek

### Architektura modeli / Cel treningowy / Interpretowalność (1)

- [[2026-09-22 Multi-Token Prediction (MTP) jako zbędna komplikacja — liczy się efektywna głębo|Multi-Token Prediction (MTP) jako zbędna komplikacja — liczy się efektywna głębokość obwodu]] — [Post na X](https://x.com/teortaxesTex/status/2102533265265500175) (kluczowe pojęcia: [[Architektura KV Cache i Rozumowanie Latentne]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Architektura modeli / Cel treningowy / Mechanistyczna interpretowalność (1)

- [[2026-09-22 MTP to ślepy zaułek — liczy się efektywna głębokość obwodu (effective circuit de|MTP to ślepy zaułek — liczy się efektywna głębokość obwodu (effective circuit depth)]] — [Post na X](https://x.com/teortaxesTex/status/2102533265265500175) (kluczowe pojęcia: [[Architektura KV Cache i Rozumowanie Latentne]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Architektura modeli / Inferencja (1)

- [[2026-09-22 Rozumowanie w przestrzeni ukrytej a skalowanie KV cache — tokeny wypełniające i|Rozumowanie w przestrzeni ukrytej a skalowanie KV cache — tokeny wypełniające i efektywna głębokość szeregowa]] — [Post na X](https://x.com/teortaxesTex/status/2102523033499877448) (kluczowe pojęcia: [[Architektura KV Cache i Rozumowanie Latentne]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Context Compaction]], [[Harness]])

### Architektura modeli / Koszty inferencji (1)

- [[2026-09-22 Różnica kosztowa Kimi wynika z udziału warstw MLA (14), a nie z AttnRes|Różnica kosztowa Kimi wynika z udziału warstw MLA (1/4), a nie z AttnRes]] — [Post na X](https://x.com/teortaxesTex/status/2102294974876536906) (kluczowe pojęcia: [[Harness]], [[Architektura KV Cache i Rozumowanie Latentne]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Architektura modeli / Rozumowanie latentne / Inżynieria kontekstu (1)

- [[2026-09-22 Rozumowanie w przestrzeni ukrytej KV cache jako nośnik obliczeń, filler tokens a|Rozumowanie w przestrzeni ukrytej: KV cache jako nośnik obliczeń, filler tokens a efektywna głębokość szeregowa po RL]] — [Post na X](https://x.com/teortaxesTex/status/2102523033499877448) (kluczowe pojęcia: [[Architektura KV Cache i Rozumowanie Latentne]], [[Architektura KV Cache i Rozumowanie Latentne]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Context Compaction]], [[Harness]])

### Ewaluacja i weryfikacja modeli (Benchmarking) (1)

- [[2026-09-21 Brak ground truth jako fundamentalna bariera w ewaluacji wyników modeli|Brak ground truth jako fundamentalna bariera w ewaluacji wyników modeli]] — [Post na X](https://x.com/teortaxesTex/status/2102172327232385279) (kluczowe pojęcia: [[Eval Set z realnych sesji]], [[Harness]], [[Weryfikacja krokowa]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Infrastruktura agentowa / RL / Benchmarking (1)

- [[2026-09-22 Marnotrawstwo zasobów w sandboxach agentowego RL — DSec i 3FS jako odpowiedź na|Marnotrawstwo zasobów w sandboxach agentowego RL — DSec i 3FS jako odpowiedź na 5% wykorzystania CPU]] — [Post na X](https://x.com/teortaxesTex/status/2102456112066998550) (kluczowe pojęcia: [[Harness]], [[Sandbox i Granice Bezpieczeństwa Agenta]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Infrastruktura treningowa / Agentic RL / Efektywność wykorzystania zasobów (1)

- [[2026-09-22 Marnotrawstwo CPU w sandboxach przy wielkoskalowym agentic RL — DSec i 3FS|Marnotrawstwo CPU w sandboxach przy wielkoskalowym agentic RL — DSec i 3FS]] — [Post na X](https://x.com/teortaxesTex/status/2102456112066998550) (kluczowe pojęcia: [[Harness]], [[Sandbox i Granice Bezpieczeństwa Agenta]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Inżynieria danych treningowych / Prognozowanie (1)

- [[2026-09-21 Wykorzystanie historycznych danych jako ground truth do treningu prognozowania (|Wykorzystanie historycznych danych jako ground truth do treningu prognozowania (maskowanie czasowe)]] — [Post na X](https://x.com/teortaxesTex/status/2102173977879757153) (kluczowe pojęcia: [[Harness]], [[Eval Set z realnych sesji]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Inżynieria kontekstu / Pamięć i KV cache (1)

- [[2026-09-22 Kompakcja treningowa zmniejsza znaczenie rozmiaru cache KV przy długim kontekści|Kompakcja treningowa zmniejsza znaczenie rozmiaru cache KV przy długim kontekście]] — [Post na X](https://x.com/teortaxesTex/status/2102545198199038197) (kluczowe pojęcia: [[Architektura KV Cache i Rozumowanie Latentne]], [[Context Compaction]], [[Context Compaction]], [[Context Compaction]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]])

### Inżynieria kontekstu / Zarządzanie pamięcią / KV cache (1)

- [[2026-09-22 Kompakcja KV cache po stronie treningu redukuje potrzebę agresywnego zarządzania|Kompakcja KV cache po stronie treningu redukuje potrzebę agresywnego zarządzania kontekstem]] — [Post na X](https://x.com/teortaxesTex/status/2102545198199038197) (kluczowe pojęcia: [[Architektura KV Cache i Rozumowanie Latentne]], [[Context Compaction]], [[Context Compaction]], [[Context Compaction]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]])

### Inżynieria promptów / systemy agentowe (2)

- [[2026-09-21 Bootstrapowanie agentów LLM przez rubryki, przykłady i stopniowe prowadzenie|Bootstrapowanie agentów LLM przez rubryki, przykłady i stopniowe prowadzenie]] — [Post na X](https://x.com/teortaxesTex/status/2102172573517701416) (kluczowe pojęcia: [[Prompt Architecture]], [[Harness]], [[Prompt Architecture]], [[Harness]], [[Context Compaction]])
- [[2026-09-21 Skuteczne użycie modeli wymaga rubryk, przykładów i etapowego bootstrapowania|Skuteczne użycie modeli wymaga rubryk, przykładów i etapowego bootstrapowania]] — [Post na X](https://x.com/teortaxesTex/status/2102172573517701416) (kluczowe pojęcia: [[Prompt Architecture]], [[Harness]], [[Prompt Architecture]], [[Harness]], [[Context Compaction]], [[Harness]])

### Inżynieria treningu / RLHF / Architektura nagród (1)

- [[2026-09-21 Brak intencji artystycznej w LLM a wrogość nagrody opartej na wyniku|Brak intencji artystycznej w LLM a wrogość nagrody opartej na wyniku]] — [Post na X](https://x.com/teortaxesTex/status/2102175093229080616) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Trening modeli / Generalizacja umiejętności (1)

- [[2026-09-21 Ustrukturyzowany sygnał treningowy generalizuje rozumowanie|Ustrukturyzowany sygnał treningowy generalizuje rozumowanie]] — [Post na X](https://x.com/teortaxesTex/status/2102174532547080559) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Trening modeli / Transfer wiedzy / Architektura sygnału treningowego (1)

- [[2026-09-21 Logicznie ustrukturyzowany sygnał treningowy generalizuje rozumowanie, ale styl|Logicznie ustrukturyzowany sygnał treningowy generalizuje rozumowanie, ale styl nie jest g-loaded]] — [Post na X](https://x.com/teortaxesTex/status/2102174532547080559) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Weryfikacja i benchmarki / Architektura zewnętrznych weryfikatorów (1)

- [[2026-09-21 Brak ground truth dla zadań online — dlaczego weryfikacja odpowiedzi w sieci jes|Brak ground truth dla zadań online — dlaczego weryfikacja odpowiedzi w sieci jest trudna]] — [Post na X](https://x.com/teortaxesTex/status/2102172327232385279) (kluczowe pojęcia: [[Eval Set z realnych sesji]], [[Weryfikator]], [[Harness]], [[Weryfikacja krokowa]], [[Harness]], [[Harness]], [[Harness]])
