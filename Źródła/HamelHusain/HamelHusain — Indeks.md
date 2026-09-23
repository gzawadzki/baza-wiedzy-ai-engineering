---
typ: indeks-autora
autor: "@HamelHusain"
źródło: "https://x.com/HamelHusain"
wygenerowano: "2026-09-23 20:57"
tagi:
  - hamelhusain
  - ai-engineering
  - indeks
---

# @HamelHusain — Indeks Bazy Wiedzy

> Baza wiedzy wyekstrahowana z wypowiedzi i dyskusji inżynierskich **@HamelHusain**. Zawiera **12** wyodrębnionych, atomowych notatek inżynierskich.

## ⚠️ Kwestie sporne i rozbieżności do rozstrzygnięcia

> Tezy podważające powszechne przekonania branżowe lub prezentujące odmienne podejście:

- **[[2026-08-15 Model cascade próg decyzyjny wyznaczaj analizą statystyczną, a nie z założenia o|Model cascade: próg decyzyjny wyznaczaj analizą statystyczną, a nie z założenia o kalibracji logprobs]]** — Spór z rozpowszechnionym w branży zarzutem (tu sformułowanym przez @ThePeshwa), że kaskada modeli opiera się na założeniu o kalibracji logprobs i przez to jest krucha. Husain twierdzi wprost, że jest odwrotnie: metoda jest agnostyczna wobec kalibracji i wymaga jedynie empirycznej analizy statystycznej sygnału proxy przed ustaleniem progu. Do rozstrzygnięcia pozostaje, na ile w praktyce inżynierskiej brak kalibracji logprobs psuje jakość routingu w konkretnych wdrożeniach oraz jak często da się w ogóle wyznaczyć użyteczny próg na realnych, szumiących datasetach.
- **[[2026-09-05 Test trójdrożny wpływ promptu systemowego na styl pisania jest znikomy|Test trójdrożny: wpływ promptu systemowego na styl pisania jest znikomy]]** — Wynik stoi w sprzeczności z powszechnym konsensusem branżowym, że prompt engineering (w tym prompt systemowy) ma duży wpływ na jakość i styl odpowiedzi. Autor zaobserwował, że prompt 'nie wydaje się mieć dużego znaczenia' w sterowaniu pisaniem, a wariant 'unmannered slop' bywał preferowany — co podważa założenie, że uprzejme, rozbudowane prompty są zawsze lepsze. Wymaga rozstrzygnięcia: czy to artefakt małej próby (5 przykładów), specyfiki zadania pisarskiego, czy realny sygnał o ograniczonej roli promptu systemowego w nowoczesnych modelach.

---

## Spis tematów i notatek

### Architektura agentów i protokoły integracyjne (MCP / WebMCP) (1)

- [[2026-08-26 WebMCP protokół współdzielonej pracy agentów i ludzi na interfejsie przeglądarki|WebMCP: protokół współdzielonej pracy agentów i ludzi na interfejsie przeglądarki]] — [Post na X](https://x.com/HamelHusain/status/2092628886572200169) ([[Harness|WebMCP]] [[Harness|MCP]] [[Harness|Agent kodujący]] [[Harness|Notebook interaktywny]] [[Harness|Runbook]] [[Harness|Ewaluacja modeli fundacyjnych]] [[Harness|Open Source]] [[Harness|Human-in-the-loop]])

### Architektura systemów agentowych / Ewaluacja (1)

- [[2026-09-18 Agentów używaj, ale weryfikuj na danych|Agentów używaj, ale weryfikuj na danych]] — [Post na X](https://x.com/HamelHusain/status/2100996105127534723) ([[Harness|Systemy agentowe]] [[Harness|Ewaluacja agentów]] [[Harness|Data-driven development]] [[Harness|Observability LLM]])

### Ewaluacja / Narzędzia eval dla agentów (1)

- [[2026-09-11 Projektowanie narzędzi eval dla agentów in-situ feedback i error discovery zamia|Projektowanie narzędzi eval dla agentów: in-situ feedback i error discovery zamiast ankiet wstępnych]] — [Post na X](https://x.com/HamelHusain/status/2098559434138206421) ([[Harness|Ewaluacja agentów]] [[Harness|Error discovery]] [[Harness|Trace annotation]] [[Harness|In-situ feedback]] [[Harness|LLM-as-a-judge]] [[Context Compaction|Inżynieria kontekstu]] [[Dynamiczne Skille i Metaprogramowanie Agenta|Plugin / Skill w agentach]])

### Ewaluacja agentów / Inżynieria promptów (few-shot) (1)

- [[2026-09-02 Zbieranie ~10 przykładów pozytywnych i negatywnych jako minimum do hill-climbing|Zbieranie ~10 przykładów pozytywnych i negatywnych jako minimum do hill-climbingu agenta]] — [Post na X](https://x.com/HamelHusain/status/2095003500992503835) ([[Harness|Hill Climbing agenta]] [[Harness|Few-shot examples]] [[Harness|Ewaluacja agentów]] [[Harness|Kontrprzykłady negatywne]] [[Prompt Architecture|Iteracyjne doskonalenie promptów]] [[Harness|Zbiór ewaluacyjny]])

### Ewaluacja i analiza błędów (Error Analysis) (1)

- [[2026-08-17 Eval Skills agentowe odkrywanie błędów przez inteligentne próbkowanie i grupowan|Eval Skills: agentowe odkrywanie błędów przez inteligentne próbkowanie i grupowanie failure modes]] — [Post na X](https://x.com/HamelHusain/status/2089438973714440196) ([[Harness|Error Analysis]] [[Harness|Failure Modes]] [[Harness|Intelligent Sampling]] [[Eval Set z realnych sesji|Eval Pipeline]] [[Dynamiczne Skille i Metaprogramowanie Agenta|Agent Skills]] [[Harness|LLM Traces]] [[Harness|Annotation App]] [[Harness|Human-in-the-loop]])

### Ewaluacja i benchmarki LLM (1)

- [[2026-09-22 Stałe zbiory ewaluacyjne (gold set) ulegają dezaktualizacji — utrzymuj je przez |Stałe zbiory ewaluacyjne (gold set) ulegają dezaktualizacji — utrzymuj je przez ciągłą analizę błędów]] — [Post na X](https://x.com/HamelHusain/status/2102442807575076880) ([[Harness|Ewaluacja LLM]] [[Harness|Gold dataset]] [[Harness|Error analysis]] [[Harness|Data drift]] [[Harness|Overfitting ewaluacji]] [[Harness|LLM-as-a-judge]])

### Ewaluacja i metodologia pomiaru modeli AI (1)

- [[2026-08-29 Projektowanie eksperymentów i testowanie hipotez wobec stochastycznych wyjść mod|Projektowanie eksperymentów i testowanie hipotez wobec stochastycznych wyjść modeli AI]] — [Post na X](https://x.com/HamelHusain/status/2093796057063006529) ([[Harness|Ewaluacja modeli LLM]] [[Harness|Projektowanie eksperymentów]] [[Harness|Testowanie hipotez]] [[Harness|Stochastyczność wyjść modeli]] [[Harness|Metryki produktów AI]])

### Ewaluacja modeli / LLM-as-a-Judge (1)

- [[2026-09-20 LLM Judge jako klasyfikator użycie Jev do ewaluacji i walidacja względem etykiet|LLM Judge jako klasyfikator: użycie Jev do ewaluacji i walidacja względem etykiet ludzkich]] — [Post na X](https://x.com/HamelHusain/status/2101533413010440593) ([[Harness|LLM-as-a-Judge]] [[Harness|Ewaluacja modeli]] [[Harness|Klasyfikator]] [[Harness|Overfitting]] [[Eval Set z realnych sesji|Ground Truth]] [[Jev]])

### Inżynieria agentowa / Debugging i obserwowalność (1)

- [[2026-09-18 Przegląd dużych trace'ów skupienie na pierwszej awarii w górę strumienia|Przegląd dużych trace'ów: skupienie na pierwszej awarii w górę strumienia]] — [Post na X](https://x.com/HamelHusain/status/2100993257555529902) ([[Harness|Trace]] [[Harness|First upstream failure]] [[Harness|Debugowanie systemów agentowych]] [[Harness|Progressive disclosure w narzędziach debugowania]] [[Harness|Obserwowalność agentów]] [[Kaskady Modeli i Routing Pewności|Kaskadowe błędy w łańcuchach agentowych]])

### Inżynieria promptów / Ewaluacja (1)

- [[2026-09-05 Test trójdrożny wpływ promptu systemowego na styl pisania jest znikomy|Test trójdrożny: wpływ promptu systemowego na styl pisania jest znikomy]] — [Post na X](https://x.com/HamelHusain/status/2096040183502373248) ([[Prompt Architecture|Prompt Engineering]] [[Stabilność modeli i przestrzeganie promptu|System Prompt]] [[Harness|Ewaluacja modeli]] [[Prompt Architecture|A/B Testing promptów]] [[Prompt Architecture|Writing Density Prompt]] [[Harness|Slop]])

### Obserwowalność / systemy agentowe (1)

- [[2026-09-19 Definicja trace'a w systemach agentowych pełny zapis sesji użytkownika|Definicja trace'a w systemach agentowych: pełny zapis sesji użytkownika]] — [Post na X](https://x.com/HamelHusain/status/2101325452484735231) ([[Harness|Trace]] [[Harness|Obserwowalność LLM]] [[Harness|Systemy agentowe]] [[Harness|Tool calling]] [[Harness|Span]] [[Harness|Ewaluacja agentów]])

### Routing modeli / Model Cascade — optymalizacja kosztów i ewaluacja (1)

- [[2026-08-15 Model cascade próg decyzyjny wyznaczaj analizą statystyczną, a nie z założenia o|Model cascade: próg decyzyjny wyznaczaj analizą statystyczną, a nie z założenia o kalibracji logprobs]] — [Post na X](https://x.com/HamelHusain/status/2088689040027775300) ([[Kaskady Modeli i Routing Pewności|Model Cascade]] [[Harness|Proxy score]] [[Harness|Kalibracja logprobs]] [[Harness|Dobór progu decyzyjnego]] [[Kaskady Modeli i Routing Pewności|Routing modeli]] [[Harness|Ewaluacja klasyfikatorów]] [[Harness|Analiza szumu sygnału]])
