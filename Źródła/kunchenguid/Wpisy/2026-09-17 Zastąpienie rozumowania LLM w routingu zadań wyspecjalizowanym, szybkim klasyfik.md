---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Thu Sep 17 06:16:35 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100468943853085061"
kategoria: "Architektura systemów agentowych / Routing zadań / Optymalizacja kosztów i latencji"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Zastąpienie rozumowania LLM w routingu zadań wyspecjalizowanym, szybkim klasyfikatorem (Jev) — architektura hybrydowa orkiestratora

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Thu Sep 17 06:16:35 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100468943853085061)
- **Kluczowe pojęcia:** [[Kaskady Modeli i Routing Pewności|Routing zadań agentowych]] [[Harness|Orkiestrator agentów]] [[Test-Time Compute i Reasoning Tokens|Reasoning effort]] [[Harness|Model harness]] [[Harness|Dystylacja decyzji do klasyfikatora]] [[Harness|Optymalizacja kosztów LLM]] [[Harness|Latencja i wall time]] [[Harness|Hybrydowa architektura agentowa]] [[Firstmate i Agenci Wykonawczy]]

---

## Kontekst i problem
Firstmate to orkiestrator, który inteligentnie przydziela każde zadanie do odpowiedniego agenta — rozumianego jako permutacja trzech wymiarów: harnessu (środowiska wykonawczego), modelu oraz poziomu reasoning effort (nakładu rozumowania). Domyślnie decyzję dispatchu podejmuje sam agent LLM: musi 'pomyśleć', wykonać wywołania narzędzi (odczyt reguł dispatchu, danych o kwotach/limicie), a dopiero potem zrealizować przydział. Ten proces jest wolny i konsumuje tokeny LLM. Problem: routowanie zadań to w istocie deterministyczna decyzja klasyfikacyjna, którą niepotrzebnie realizuje kosztowny model rozumujący.

## Rada inżynierska
Rozdzielaj zadania agentowe na dwa typy: (1) te wymagające rozumowania i (2) deterministyczne decyzje klasyfikacyjne/routujące. Dla tych drugich zbuduj wyspecjalizowany, szybki model/klasyfikator (tu: 'Jev'), który podejmuje tę samą decyzję bez rozumowania i bez wywołań narzędzi, w czasie ~200 ms. Warunkiem poprawności jest walidacja zgodności z decyzją modelu frontier: w ocenie na 25 zadaniach Jev zwracał dokładnie tę samą odpowiedź, którą dałby model frontier ('fable'). Efekt końcowy przy zachowaniu pojedynczego wywołania narzędzia do inwokacji Jev: -71% kosztu i -90% czasu ściennego (wall time) całego procesu dispatchu; licząc tylko zastąpiony fragment — oszczędność rzędu ~100x. Kluczowa zasada: LLM jest tylko małym elementem architektury — nie każdy krok agenta wymaga rozumowania.

## Uwaga / Anty-wzorzec
Anty-wzorzec: używanie kosztownego modelu rozumującego (z myśleniem i łańcuchem wywołań narzędzi) do realizacji deterministycznych, powtarzalnych decyzji routujących, które da się skompilować do szybkiego klasyfikatora. Pułapki wdrożeniowe: (1) brak walidacji parytetu decyzji względem modelu frontier przed produkcyjnym zastąpieniem — ryzyko cichej regresji jakości; (2) pominięcie kosztu wywołania narzędzia inwokującego klasyfikator (nadal realizowanego przez LLM) w kalkulacji oszczędności — zawyża to wynik; (3) zbyt mała próba ewaluacyjna (25 zadań) jako podstawa twierdzenia o parytecie jakości.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Teza stoi w napięciu z powszechnym konsensusem branżowym, według którego orkiestracja i routing zadań powinny być realizowane przez 'inteligentny' agent LLM z pętlą rozumowania i wywołaniami narzędzi. Autor twierdzi, że dla deterministycznych decyzji routujących LLM jest zbędny i należy go zastąpić wyspecjalizowanym, niemal darmowym klasyfikatorem, redukując rolę LLM do 'małego elementu' architektury. Do rozstrzygnięcia pozostaje: (a) czy parytet decyzji utrzymuje się poza wąskim zbiorem 25 zadań ewaluacyjnych i przy zmianach reguł dispatchu/kwot, (b) czy klasyfikator nie wymaga ciągłej re-dystylacji przy ewolucji polityki routingu, (c) czy oszczędność ~100x liczy się wyłącznie dla zastąpionego fragmentu, a nie całego systemu (dla całości -71% kosztu i -90% wall time).

## Oryginalny cytat
> *"i just replaced this dispatch process with Jev. it makes the same decision with no thinking or tool calls, done in ~200ms, and for the 25 tasks i evaluated this with, it gives the exact same answer fable would have given... there's still a tool call needed to invoke Jev, done by the firstmate agent which uses an LLM. but even with that counted, the saving from Jev still resulted in a -71% reduction in cost and -90% reduction in wall time of completing the whole dispatching process ... if we just look at the part Jev replaced and not the whole system, then the saving is on the magnitude of ~100x ... i think this is starting to enable a whole new architectural paradigm for software. LLMs are just a small part of it."*
