---
typ: indeks-autora
autor: "@karminski3"
źródło: "https://x.com/karminski3"
tagi:
  - karminski3
  - ai-engineering
  - indeks
---

# @karminski3 — Indeks Bazy Wiedzy

> Kompletny indeks **51** wyodrębnionych, atomowych notatek inżynierskich z profilu @karminski3.

## ⚠️ Kwestie sporne i rozbieżności do rozstrzygnięcia

> Wpisy podważające powszechne przekonania branżowe lub prezentujące odmienne podejście:

- **[[2026-08-27 Harness Scaling skalowanie orkiestracji agentów i środowiska zamiast samych para|Harness Scaling: skalowanie orkiestracji agentów i środowiska zamiast samych parametrów modelu]]** — Autor kontruje dominujący w branży nacisk na skalowanie liczby parametrów modelu ('scale is all you need' / bigger model = better agent). Twierdzi, że parametry podnoszą wyłącznie 'inteligencję', natomiast realną zdolność wykonawczą (throughput, niezawodność na dużych zadaniach) daje dopiero skalowanie harnessu — frameworku, narzędzi i zespołu agentów. Do rozstrzygnięcia: czy dla zadań analitycznych na dużych wolumenach danych inwestycja w architekturę agentową (orkiestracja + izolowane środowisko + ekstrakcja skryptowa) jest istotniejsza niż dobór mocniejszego modelu bazowego. Teza jest spójna z nurtem 'context engineering > raw model size', ale podważa intuicję, że wystarczy poczekać na kolejny, większy model.
- **[[2026-08-27 System Scaling harness, pętla feedbacku środowiskowego i multi-agent skalowanie|System Scaling: harness, pętla feedbacku środowiskowego i multi-agent > skalowanie parametrów]]** — Teza kontrowersyjna względem dominującego konsensusu 'scale is all you need' / 'bigger models win': autor twierdzi, że przewaga konkurencyjna przesuwa się z liczby parametrów na skalowanie systemu (ujednolicenie pętli prób i błędów w środowisku oraz współpracy wielu agentów). Do rozstrzygnięcia: czy przyrost możliwości modeli bazowych nie zredukuje z czasem znaczenia ręcznie projektowanego harnessu, oraz jak mierzyć 'System Scaling' obiektywnymi metrykami (czas do artefaktu, koszt tokenów, odsetek poprawnych konfiguracji) zamiast pojedynczych anegdotycznych sukcesów.
- **[[2026-08-27 System Scaling kontra skalowanie parametrów wieloagentowy harness z pętlą sprzęż|System Scaling kontra skalowanie parametrów: wieloagentowy harness z pętlą sprzężenia zwrotnego z środowiskiem]]** — Teza 'przyszła konkurencja w AI to nie skalowanie liczby parametrów, lecz System Scaling' stoi w napięciu z dominującym w branży paradygmatem scaling laws / 'scale is all you need', w którym jakość wyniku jest przede wszystkim funkcją skali modelu i danych. Do rozstrzygnięcia: czy dla zadań inżynierskich (konfiguracja, security, kod) wartość dodana leży głównie w harnessie i pętli feedbacku, czy też przewaga systemowa jest tylko artefaktem obecnych ograniczeń modeli i zniknie wraz ze wzrostem ich możliwości. Dodatkowo wpis ma charakter częściowo promocyjny (linki do własnego frameworka i modelu), a dowód stanowi pojedynczy, anegdotyczny przypadek (10 minut na konfigurację firewalla) bez danych porównawczych ani baseline'u.
- **[[2026-08-31 Tier lista małych modeli w zadaniach agentowych Qwen3.8-27B Q4_K_XL, reasoning_e|Tier lista małych modeli w zadaniach agentowych: Qwen3.8-27B Q4_K_XL, reasoning_effort a wybór runtime (llama.cpp vs MLX)]]** — Sporne wobec typowego konsensusu branżowego: (a) autor zaleca MLX (z MTP) zamiast llama.cpp na macOS, podczas gdy domyślną rekomendacją w społeczności lokalnych LLM jest llama.cpp jako uniwersalny runtime — wymaga weryfikacji na konkretnym sprzęcie Apple Silicon; (b) autor twierdzi, że w zadaniach agentowych najlepszy jest NISKI reasoning_effort, co stoi w sprzeczności z popularną praktyką maksymalizowania rozumowania w agentach („thinking longer = lepsze planowanie”) — do rozstrzygnięcia empirycznie na własnym harnessie, z pomiarem sukcesu zadania, latencji i zużycia tokenów; (c) rekomendacja konkretnej kwantyzacji UD-Q4_K_XL jako „najbardziej opłacalnej” jest wynikiem pojedynczego setupu (1× H100 NVL + llama.cpp) i nie musi się przenosić na inne backendy.
- **[[2026-09-14 Budżet myślenia a destylacja długiego CoT dlaczego małe modele 'rosną' wraz z dł|Budżet myślenia a destylacja długiego CoT: dlaczego małe modele 'rosną' wraz z długością rozumowania]]** — Autor podważa rozpowszechnioną praktykę ekosystemu ollama polegającą na udostępnianiu modeli destylowanych pod etykietą sugerującą pełny model źródłowy. Spór dotyczy tego, czy takie nazewnictwo i komunikacja są akceptowalnym uproszczeniem, czy wprowadzającym w błąd anty-wzorcem zniekształcającym percepcję realnych możliwości modeli rozumujących.
- **[[2026-09-14 Długi łańcuch myśli i destylacja R1 budżet rozumowania a wyniki małych modeli|Długi łańcuch myśli i destylacja R1: budżet rozumowania a wyniki małych modeli]]** — Autor krytykuje popularne uproszczenie: Ollama instaluje deepseek-r1-distilled-qwen-7b, ale to nie jest pełny DeepSeek-R1, lecz model Qwen dostrojony na danych R1. Sporne jest nazywanie takich destylatów „DeepSeek” oraz pomijanie faktu, że ich wyniki zależą od przyznanego budżetu rozumowania.
- **[[2026-09-14 Isomorfizm kodu i danych w skillach metaprogramowanie Micro-Skill zamiast statyc|Isomorfizm kodu i danych w skillach: metaprogramowanie Micro-Skill zamiast statycznych dokumentów]]** — Autor podważa dominujący konsensus 'napisz raz dobry, uniwersalny prompt/skill i trzymaj się go'. Zamiast statycznej, ręcznie projektowanej definicji skilla proponuje podejście generatywne: skill tworzony ad hoc przez model dla każdego wejścia (Micro-Skill). Do rozstrzygnięcia: (a) koszt/latencja i powtarzalność dynamicznego generowania skilla przy każdym wywołaniu vs. utrzymanie jednego statycznego skilla; (b) niezawodność i weryfikowalność generowanego kodu (regex, Pydantic) — czy warto generować kod zamiast go po prostu napisać; (c) granica 'model wystarczająco zdolny' — kiedy metaprogramowanie przestaje być opłacalne i lepiej wrócić do statycznej definicji.
- **[[2026-09-14 Maksymalny budżet rozumowania nie zawsze poprawia SWE; SOTA jako kompresja infor|Maksymalny budżet rozumowania nie zawsze poprawia SWE; SOTA jako kompresja informacji]]** — Autor podważa popularny konsensus, że zwiększanie budżetu rozumowania do maksimum (max reasoning / test-time compute) zawsze poprawia wyniki. Wskazuje na możliwą inwersję metryk SWE przy ustawieniu max oraz na potrzebę poprawnego zatrzymywania myślenia modelu, co stoi w sprzeczności z prostym wnioskiem „więcej myślenia = lepszy wynik”.
- **[[2026-09-14 Przełącznik intensywności rozumowania (max vs high) realnie skaluje wyniki model|Przełącznik intensywności rozumowania (max vs high) realnie skaluje wyniki modelu — dowód z DeepSeek-R1-Zero]]** — Autor wprost podważa konsensus panujący w komentarzach pod wpisem, gdzie twierdzono, że ustawienie 'high' vs 'max' jest neutralne dla wydajności, a przełącznik to wyłącznie kontrola intensywności myślenia. Stanowisko autora (poparte paperem R1-Zero): wyższy budżet rozumowania = wyższa zdolność modelu. Do rozstrzygnięcia: czy obserwacja z R1-Zero (RL bez nowej wiedzy) przenosi się 1:1 na modele z rodziny V4.x z SFT/instruktażem, gdzie zjawisko saturacji i degradacji przy zbyt długim rozumowaniu może występować. Wymaga to własnego benchmarku na konkretnym zadaniu.
- **[[2026-09-14 Reasoning effort (thinking budget) realnie wpływa na wyniki modelu — dowody z De|Reasoning effort (thinking budget) realnie wpływa na wyniki modelu — dowody z DeepSeek-R1-Zero]]** — Autor wchodzi w spór z powszechną (jego zdaniem błędną) opinią części społeczności DeepSeek, że przełącznik思考强度 (thinking strength) jest niezależny od wydajności i że 'high' jest lepsze niż 'max'. Teza autora: wyższa intensywność rozumowania = wyższa zdolność modelu, co potwierdza praca DeepSeek-R1-Zero. Do rozstrzygnięcia: czy na poziomie 'max' występuje nasycenie (saturation) lub degradacja jakości przy zbyt długim CoT, oraz czy zalecenie 'high' wynika z realnych ograniczeń (latency, koszt, ryzyko over-thinkingu) czy z nieporozumienia — brak tu twardych danych, jedynie argumentacja przez odwołanie do paperu.
- **[[2026-09-14 Skalowanie budżetu rozumowania (test-time compute) i dystylacja CoT R1 do małych|Skalowanie budżetu rozumowania (test-time compute) i dystylacja CoT R1 do małych modeli — oraz anty-wzorzec „deepseek-r1-distilled-qwen-7b = DeepSeek”]]** — Autor podważa rozpowszechniony w branży skrót myślowy, że modele dystylowane R1 (np. `deepseek-r1-distilled-qwen-7b` w Ollama) są „DeepSeekiem”. Do rozstrzygnięcia: czy popularyzacja dystylatów pod marką modelu źródłowego to akceptowalny skrót marketingowy, czy realne źródło błędnych decyzji inżynierskich (zawyżone oczekiwania co do jakości, nieadekwatne benchmarki, mylne wnioski o koszcie inferencji). Dodatkowo teza o wprost proporcjonalnym wzroście jakości od długości rozumowania wymaga weryfikacji: przy zbyt dużym budżecie występuje nasycenie i degradacja (overthinking), czego wpis nie precyzuje.
- **[[2026-09-14 SOTA jako doskonały kompresor informacji minimalna liczba tokenów zamiast długie|SOTA jako doskonały kompresor informacji: minimalna liczba tokenów zamiast długiego rozumowania]]** — Teza stoi w sprzeczności z dominującym konsensusem branżowym wokół test-time compute scaling, gdzie zakłada się, że więcej tokenów rozumowania (wyższy reasoning effort, dłuższy łańcuch myśli) przekłada się na lepsze wyniki w zadaniach trudnych. Autor twierdzi odwrotnie: prawdziwie SOTA to minimalna liczba tokenów przy najwyższej trafności, a 'max' reasoning effort może wręcz szkodzić (odwrócenie wyników na SWE-bench). Do rozstrzygnięcia: czy degradacja przy 'max' jest artefaktem konkretnego benchmarku/modelu, czy też ogólnym efektem nasycenia/rozmycia rozumowania (saturation/drift).
- **[[2026-09-14 SOTA jako kompresor informacji minimalizacja tokenów zamiast reasoning max|SOTA jako kompresor informacji: minimalizacja tokenów zamiast reasoning max]]** — Teza stoi w sprzeczności z popularnym konsensusem, że zwiększanie reasoning effort/„max” oraz długie CoT zawsze poprawiają wyniki. Autor twierdzi, że na SWE-bench może wystąpić odwrócenie, a modele SOTA powinny maksymalnie kompresować informację i używać minimalnej liczby tokenów. Do rozstrzygnięcia pozostaje: kiedy długie rozumowanie pomaga, kiedy szkodzi oraz jak mierzyć optymalny budżet tokenów dla danego zadania.
- **[[2026-09-15 reasoning_effort jako marketing i problem porównywalności benchmarków|reasoning_effort jako marketing i problem porównywalności benchmarków]]** — Autor podważa powszechne traktowanie reasoning_effort jako użytecznego mechanizmu kontroli jakości. Twierdzi, że to głównie marketing i przenoszenie kosztów na użytkownika; sprzeczne z narracją vendorów, że 'high' jest optymalnym sweet spotem. Do rozstrzygnięcia: czy wyższy reasoning effort powinien być monotonicznie lepszy, czy trade-off compute-performance jest nieunikniony.
- **[[2026-09-15 reasoning_effort jako marketing przenoszenie kosztu obliczeń i ryzyka rozliczeni|reasoning_effort jako marketing: przenoszenie kosztu obliczeń i ryzyka rozliczeniowego na użytkownika]]** — Autor podważa branżowy konsensus, że wyższy reasoning_effort wprost przekłada się na wyższą jakość. Twierdzi, że reasoning_effort to narzędzie marketingowe przenoszące kompromis compute/precyzja oraz ryzyko kosztów na użytkownika. Jednocześnie zaznacza, że rozbieżność effort↔performance wynika z niedostatecznego post-trainingu i docelowo (idealnie) effort powinien być równoważny wydajności — co jest tezą przeciwną do obecnej praktyki dostawców. Do rozstrzygnięcia: czy reasoning_effort należy traktować jako realną dźwignię jakości, czy wyłącznie jako parametr budżetu obliczeń.
- **[[2026-09-15 reasoning_effort jako marketingowa dystrybucja ryzyka kosztowego i pułapka w ben|reasoning_effort jako marketingowa dystrybucja ryzyka kosztowego i pułapka w benchmarkach]]** — Autor podważa branżowy konsensus, że reasoning_effort to użyteczne, neutralne narzędzie kontroli jakości/ kosztu. Twierdzi, że to głównie marketing: przenosi na użytkownika decyzję o kompromisie dokładność/obliczenia oraz ryzyko rachunku, jednocześnie maskując to deklaracją, że benchmarki producenta są robione na max, a 'sweet spot' (cost–performance balance) leży na high. Do rozstrzygnięcia: (a) czy reasoning_effort to realna dźwignia jakości, czy optymalizacja kosztowa ubrana w narrację o jakości; (b) czy 'high' jest optymalne jakościowo, czy tylko kosztowo — autor wskazuje, że ludzie błędnie przyjmują 'high = najlepsze'; (c) teza, że rozjazd między thinking effort a performance wynika z niedomagań post-trainingu (a nie jest nieusuwalną cechą modeli rozumujących) i że docelowo należy dążyć do ich równoważności. Nowsze wpisy autora mają pierwszeństwo nad wcześniejszymi stanowiskami.
- **[[2026-09-15 reasoning_effort jako mechanizm przenoszenia ryzyka kosztowego na użytkownika —|reasoning_effort jako mechanizm przenoszenia ryzyka kosztowego na użytkownika — pułapki benchmarków i uczciwość porównań]]** — Autor podważa powszechny konsensus branżowy, że parametr reasoning_effort jest neutralnym, użytecznym narzędziem kontroli. Twierdzi, że to głównie marketing i mechanizm przenoszenia ryzyka kosztowego/billingowego na użytkownika, przy jednoczesnej niespójnej komunikacji (benchmarki na 'max', rekomendacja 'high'). Dodatkowo formułuje tezę, że thinking effort powinno być równoważne performance, a obecny brak tej równoważności wynika ze słabego post-trainingu — co jest opinią kontrowersyjną wobec stanowiska dostawców, że różnica effortów jest zamierzonym, sensownym kompromisem kosztowym.
- **[[2026-09-21 Jev (System-1) kontra generator liczb losowych w labiryncie — granice pojedyncze|Jev (System-1) kontra generator liczb losowych w labiryncie — granice pojedynczego kroku decyzyjnego]]** — Teza kontrowersyjna wobec powszechnego konsensusu, że lepszy/nowszy model zawsze bije baseline. Autor dowodzi, że w zadaniach nawigacyjnych szybki model System-1 może zostać systematycznie pobity przez czysty RNG (nawet bez równoległości), ponieważ sam RNG korzysta z własności nawracalności błądzenia losowego. Do rozstrzygnięcia: w jakich dokładnie klasach zadań 'głupi, ale szybki' random jest realnym baseline'em, którego nie wolno pomijać w ewaluacji, oraz kiedy dołożenie pamięci/heurystyki do System-1 daje regresję zamiast poprawy (bo reguły warunkowe nigdy nie zostają wywołane).
- **[[2026-09-21 Jev (System-1) vs. czysty random w labiryncie porażka planowania wieloetapowego|Jev (System-1) vs. czysty random w labiryncie: porażka planowania wieloetapowego]]** — Wyniki podważają powszechne przekonanie, że modele AI (nawet szybkie System-1) są lepsze od prostych algorytmów losowych w zadaniach planowania. Pokazują, że w niektórych przypadkach czysty random walk może być skuteczniejszy niż model oparty na heurystykach, co stoi w sprzeczności z optymizmem wobec agentów AI. Autor argumentuje, że Jev jest jedynie single-step structured judge, a nie plannerem, co może być kontrowersyjne dla zwolenników podejść end-to-end.
- **[[2026-09-21 Weryfikacja mitu o 'przełamaniu' safety alignmentu modelem językowym test hebraj|Weryfikacja mitu o 'przełamaniu' safety alignmentu modelem językowym: test hebrajskiego na Fable-5.1 i DeepSeek-V4.1-Flash]]** — Autor podważa viralowy konsensus na X, jakoby język hebrajski umożliwiał bypass safety alignmentu modeli (m.in. Anthropic) oraz obala (jako nieaktualne) ustalenia paperu 'Low-Resource Languages Jailbreak GPT-4' (2023) dotyczące obejść przez języki niskiego zasobu (zulu, gaelicki szkocki, hmong). Teza do rozstrzygnięcia: czy luka językowa jailbreak rzeczywiście została domknięta, czy wyniki są specyficzne dla testowanej klasy treści (autor nie testował promptów jailbreakowych ani zaawansowanych technik promptowych, co pozostawia otwarte pytanie o odporność na ataki hybrydowe: język + prompt).

---

## Spis tematów i notatek

### Architektura agentów / Edge AI (WebGPU, modele端侧) (1)

- [[2026-09-14 Coding Agent uruchamiany w całości w przeglądarce MiniCPM5-2B 4-bit ONNX + WebGP|Coding Agent uruchamiany w całości w przeglądarce: MiniCPM5-2B 4-bit ONNX + WebGPU bez Dockera i Node]] — [Post na X](https://x.com/karminski3/status/2099633181934907654) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Architektura agentów / Edge AI / WebGPU (1)

- [[2026-09-14 Agent kodujący uruchamiany w całości w przeglądarce MiniCPM5-2B 4-bit ONNX + Web|Agent kodujący uruchamiany w całości w przeglądarce: MiniCPM5-2B 4-bit ONNX + WebGPU (framework Pi)]] — [Post na X](https://x.com/karminski3/status/2099633181934907654) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Architektura agentów multimodalnych / Harness i systemy pluginowe (1)

- [[2026-09-18 Qwen3.8-Omni-Flash, Live-Harness i MM-Plugins multimodalna infrastruktura agento|Qwen3.8-Omni-Flash, Live-Harness i MM-Plugins: multimodalna infrastruktura agentowa z uczeniem skilli z demonstracji]] — [Post na X](https://x.com/karminski3/status/2100751056104026497) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Dynamiczne Skille i Metaprogramowanie Agenta]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Context Compaction]])

### Architektura modeli / Latencja i throughput / Systemy agentowe (System 1 vs System 2) (1)

- [[2026-09-17 Jev (TypeSafe AI) architektura równoległego próbkowania i 70 ms latencji w model|Jev (TypeSafe AI): architektura równoległego próbkowania i 70 ms latencji w modelach decyzyjnych]] — [Post na X](https://x.com/karminski3/status/2100717948881326224) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Architektura modeli / Latencja i wnioskowanie / Systemy agentowe (1)

- [[2026-09-17 Jev (TypeSafe AI) model System One z równoległym samplingiem i latencją 70 ms do|Jev (TypeSafe AI): model System One z równoległym samplingiem i latencją 70 ms do decyzji o niskim opóźnieniu]] — [Post na X](https://x.com/karminski3/status/2100717948881326224) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Architektura modeli / Type-Safe AI (1)

- [[2026-09-17 Jev nieautoregresyjny model decyzyjny z wymuszonym schematem wyjścia (decision s|Jev: nieautoregresyjny model decyzyjny z wymuszonym schematem wyjścia (decision slots)]] — [Post na X](https://x.com/karminski3/status/2100717944565354595) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Jev]], [[Harness]], [[Harness]])

### Architektura modeli / Type-Safe AI / Structured Output (1)

- [[2026-09-17 Model Jev rezygnacja z autoregRESji na rzecz type-safe wyjścia decyzyjnego opart|Model Jev: rezygnacja z autoregRESji na rzecz type-safe wyjścia decyzyjnego opartego na schemacie]] — [Post na X](https://x.com/karminski3/status/2100717944565354595) (kluczowe pojęcia: [[Jev]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Architektura systemów agentowych (Agentic Engineering) (1)

- [[2026-08-27 System Scaling kontra skalowanie parametrów wieloagentowy harness z pętlą sprzęż|System Scaling kontra skalowanie parametrów: wieloagentowy harness z pętlą sprzężenia zwrotnego z środowiskiem]] — [Post na X](https://x.com/karminski3/status/2092894849619874210) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Weryfikator]], [[Harness]], [[Harness]])

### Architektura systemów agentowych / Harness i pętle weryfikacji (1)

- [[2026-08-27 System Scaling harness, pętla feedbacku środowiskowego i multi-agent skalowanie|System Scaling: harness, pętla feedbacku środowiskowego i multi-agent > skalowanie parametrów]] — [Post na X](https://x.com/karminski3/status/2092894849619874210) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Architektura systemów agentowych / Inżynieria kontekstu (2)

- [[2026-08-27 Harness Scaling skalowanie orkiestracji agentów i środowiska zamiast samych para|Harness Scaling: skalowanie orkiestracji agentów i środowiska zamiast samych parametrów modelu]] — [Post na X](https://x.com/karminski3/status/2092894843429363871) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Context Compaction]], [[Harness]], [[Harness]], [[Harness]], [[Sandbox i Granice Bezpieczeństwa Agenta]])
- [[2026-08-27 Harness Scaling skalowanie rusztowania agentowego zamiast parametrów modelu (Apo|Harness Scaling: skalowanie rusztowania agentowego zamiast parametrów modelu (Apodex 1.1)]] — [Post na X](https://x.com/karminski3/status/2092894843429363871) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Context Compaction]], [[Harness]], [[Harness]], [[Harness]], [[Sandbox i Granice Bezpieczeństwa Agenta]])

### Architektura systemów agentowych / Inżynieria promptów (1)

- [[2026-09-14 Izomorfizm kodu i danych w Skillach metaprogramowanie i dynamiczne generowanie M|Izomorfizm kodu i danych w Skillach: metaprogramowanie i dynamiczne generowanie Micro-Skill]] — [Post na X](https://x.com/karminski3/status/2099383433034440811) (kluczowe pojęcia: [[Dynamiczne Skille i Metaprogramowanie Agenta]], [[Dynamiczne Skille i Metaprogramowanie Agenta]], [[Prompt Architecture]], [[Harness]], [[Context Compaction]], [[Weryfikator]], [[Harness]], [[Harness]], [[Dynamiczne Skille i Metaprogramowanie Agenta]])

### Architektura systemów agentowych / Ocena modeli / Planowanie wieloetapowe (1)

- [[2026-09-21 Jev (System-1) kontra generator liczb losowych w labiryncie — granice pojedyncze|Jev (System-1) kontra generator liczb losowych w labiryncie — granice pojedynczego kroku decyzyjnego]] — [Post na X](https://x.com/karminski3/status/2101941770003361893) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Architektura systemów agentowych / Projektowanie skilli (1)

- [[2026-09-14 Isomorfizm kodu i danych w skillach metaprogramowanie Micro-Skill zamiast statyc|Isomorfizm kodu i danych w skillach: metaprogramowanie Micro-Skill zamiast statycznych dokumentów]] — [Post na X](https://x.com/karminski3/status/2099383368999965122) (kluczowe pojęcia: [[Dynamiczne Skille i Metaprogramowanie Agenta]], [[Dynamiczne Skille i Metaprogramowanie Agenta]], [[Harness]], [[Harness]], [[Harness]], [[Weryfikator]], [[Prompt Architecture]], [[Dynamiczne Skille i Metaprogramowanie Agenta]])

### Architektura systemów agentowych i planowanie (1)

- [[2026-09-21 Jev (System-1) vs. czysty random w labiryncie porażka planowania wieloetapowego|Jev (System-1) vs. czysty random w labiryncie: porażka planowania wieloetapowego]] — [Post na X](https://x.com/karminski3/status/2101941770003361893) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Jev]], [[Harness]], [[Harness]], [[Harness]])

### Benchmarki i wydajność modeli / Agentic Coding (1)

- [[2026-09-22 MiMo-v2.6-Pro 3x skok w benchmarku AgenticCoding, 464 tps i pułapka wczesnego za|MiMo-v2.6-Pro: 3x skok w benchmarku AgenticCoding, 464 tps i pułapka wczesnego zatrzymania]] — [Post na X](https://x.com/karminski3/status/2102427860585841100) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Harness]])

### Benchmarki modeli / Agentic Coding (1)

- [[2026-09-22 MiMo-v2.6-Pro potrojony wynik w teście bazy wektorowej dzięki RL na żywo, proble|MiMo-v2.6-Pro: potrojony wynik w teście bazy wektorowej dzięki RL na żywo, problemy z early stopping i frontendem]] — [Post na X](https://x.com/karminski3/status/2102427860585841100) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Benchmarki modeli i wybór modelu do zadań agentowych (1)

- [[2026-09-14 Stabilność vs szczytowa jakość w AgenticCoding ranking modeli do generowania baz|Stabilność vs szczytowa jakość w AgenticCoding: ranking modeli do generowania bazy wektorowej]] — [Post na X](https://x.com/karminski3/status/2099375198986461418) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Prompt Architecture]], [[Harness]], [[Harness]], [[Stabilność modeli i przestrzeganie promptu]])

### Benchmarking / Ewaluacja modeli LLM (1)

- [[2026-08-20 Benchmarkowanie jakości wyjścia modeli GPU nie wpływa na jakość, tylko na przepu|Benchmarkowanie jakości wyjścia modeli: GPU nie wpływa na jakość, tylko na przepustowość testów]] — [Post na X](https://x.com/karminski3/status/2090495077873533333) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Benchmarking / Ewaluacja modeli lokalnych (1)

- [[2026-08-31 Arena małych modeli 8 modeli × 4 kwantyzacje × MTP × 3 poziomy reasoning (pass@3|Arena małych modeli: 8 modeli × 4 kwantyzacje × MTP × 3 poziomy reasoning (pass@3)]] — [Post na X](https://x.com/karminski3/status/2094311103987581033) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Architektura KV Cache i Rozumowanie Latentne]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Harness]])

### Benchmarking i ewaluacja modeli / Agenci lokalni (1)

- [[2026-08-31 Tier lista małych modeli w zadaniach agentowych Qwen3.8-27B Q4_K_XL, reasoning_e|Tier lista małych modeli w zadaniach agentowych: Qwen3.8-27B Q4_K_XL, reasoning_effort a wybór runtime (llama.cpp vs MLX)]] — [Post na X](https://x.com/karminski3/status/2094341123124985991) (kluczowe pojęcia: [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Harness]], [[Architektura KV Cache i Rozumowanie Latentne]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Benchmarking i ewaluacja modeli / Inżynieria wnioskowania (1)

- [[2026-09-15 reasoning_effort jako marketingowa dystrybucja ryzyka kosztowego i pułapka w ben|reasoning_effort jako marketingowa dystrybucja ryzyka kosztowego i pułapka w benchmarkach]] — [Post na X](https://x.com/karminski3/status/2099767018279084387) (kluczowe pojęcia: [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]])

### Benchmarking i ewaluacja modeli LLM (1)

- [[2026-08-31 Benchmark małych modeli LLM 8 modeli, 4 kwantyzacje, MTP onoff, poziomy rozumowa|Benchmark małych modeli LLM: 8 modeli, 4 kwantyzacje, MTP on/off, poziomy rozumowania low/medium/xhigh (pass@3)]] — [Post na X](https://x.com/karminski3/status/2094311103987581033) (kluczowe pojęcia: [[Harness]], [[Architektura KV Cache i Rozumowanie Latentne]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Benchmarking i konfiguracja modeli (reasoning_effort) (1)

- [[2026-09-15 reasoning_effort jako mechanizm przenoszenia ryzyka kosztowego na użytkownika —|reasoning_effort jako mechanizm przenoszenia ryzyka kosztowego na użytkownika — pułapki benchmarków i uczciwość porównań]] — [Post na X](https://x.com/karminski3/status/2099767018279084387) (kluczowe pojęcia: [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Benchmarking i obserwacje zachowania modeli (1)

- [[2026-09-22 Claude Opus 5.5 jako potencjalna kwantyzacjadestylacja Fable 5.1 — testy fronten|Claude Opus 5.5 jako potencjalna kwantyzacja/destylacja Fable 5.1 — testy frontendu i anomalie rozumowania]] — [Post na X](https://x.com/karminski3/status/2102479290420048093) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Stabilność modeli i przestrzeganie promptu]], [[Harness]], [[Harness]], [[Harness]])

### Benchmarking i wybór modeli LLM do kodu (1)

- [[2026-09-14 Stabilność vs. szczytowa wydajność modeli LLM w zadaniach programistycznych|Stabilność vs. szczytowa wydajność modeli LLM w zadaniach programistycznych]] — [Post na X](https://x.com/karminski3/status/2099375198986461418) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Benchmarking modeli / Agenci / Inference runtime (1)

- [[2026-08-31 Dobór reasoning_effort w małych modelach agentowych oraz MLX vs llama.cpp na Mac|Dobór reasoning_effort w małych modelach agentowych oraz MLX vs llama.cpp na Macu]] — [Post na X](https://x.com/karminski3/status/2094341123124985991) (kluczowe pojęcia: [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Architektura KV Cache i Rozumowanie Latentne]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Benchmarkowanie i ewaluacja modeli LLM (1)

- [[2026-09-15 reasoning_effort jako marketing i problem porównywalności benchmarków|reasoning_effort jako marketing i problem porównywalności benchmarków]] — [Post na X](https://x.com/karminski3/status/2099767043155218568) (kluczowe pojęcia: [[Harness]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]])

### Bezpieczeństwo modeli / Ewaluacja / Benchmarking (1)

- [[2026-09-21 Test empiryczny hipoteza 'jailbreak przez język hebrajski' obalona — spójność re|Test empiryczny: hipoteza 'jailbreak przez język hebrajski' obalona — spójność refusal rate między językami]] — [Post na X](https://x.com/karminski3/status/2101826076762857867) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Sandbox i Granice Bezpieczeństwa Agenta]], [[Harness]])

### Bezpieczeństwo modeli / Red Teaming / Alignment (1)

- [[2026-09-21 Weryfikacja mitu o 'przełamaniu' safety alignmentu modelem językowym test hebraj|Weryfikacja mitu o 'przełamaniu' safety alignmentu modelem językowym: test hebrajskiego na Fable-5.1 i DeepSeek-V4.1-Flash]] — [Post na X](https://x.com/karminski3/status/2101826076762857867) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Eval Set z realnych sesji]])

### Inżynieria LLM / Destylacja i wnioskowanie (1)

- [[2026-09-14 Destylacja długiego CoT z R1 do małych modeli i rola budżetu obliczeniowego|Destylacja długiego CoT z R1 do małych modeli i rola budżetu obliczeniowego]] — [Post na X](https://x.com/karminski3/status/2099436039169536325) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]])

### Inżynieria LLM / rozumowanie, destylacja i budżet kontekstu (1)

- [[2026-09-14 Długi łańcuch myśli i destylacja R1 budżet rozumowania a wyniki małych modeli|Długi łańcuch myśli i destylacja R1: budżet rozumowania a wyniki małych modeli]] — [Post na X](https://x.com/karminski3/status/2099436039169536325) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Inżynieria kontekstu / analiza wideo multimodalna (1)

- [[2026-08-21 Dwupoziomowa strategia próbkowania klatek wideo dla modeli multimodalnych|Dwupoziomowa strategia próbkowania klatek wideo dla modeli multimodalnych]] — [Post na X](https://x.com/karminski3/status/2090858868989706352) (kluczowe pojęcia: [[Harness]], [[Prompt Architecture]], [[Harness]], [[Harness]], [[Context Compaction]], [[Harness]])

### Inżynieria kontekstu multimodalnego / Analiza wideo (1)

- [[2026-08-21 Dwupoziomowa strategia próbkowania klatek w analizie wideo przez modele multimod|Dwupoziomowa strategia próbkowania klatek w analizie wideo przez modele multimodalne]] — [Post na X](https://x.com/karminski3/status/2090858868989706352) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Prompt Architecture]], [[Harness]], [[Harness]], [[Context Compaction]], [[Harness]])

### Inżynieria promptów / Benchmarking / Reasoning LLM (1)

- [[2026-09-14 SOTA jako kompresor informacji minimalizacja tokenów zamiast reasoning max|SOTA jako kompresor informacji: minimalizacja tokenów zamiast reasoning max]] — [Post na X](https://x.com/karminski3/status/2099421138069950509) (kluczowe pojęcia: [[Harness]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Prompt Architecture]])

### Inżynieria promptów / Reasoning Effort / Benchmarking (1)

- [[2026-09-14 Przełącznik intensywności rozumowania (max vs high) realnie skaluje wyniki model|Przełącznik intensywności rozumowania (max vs high) realnie skaluje wyniki modelu — dowód z DeepSeek-R1-Zero]] — [Post na X](https://x.com/karminski3/status/2099396323942547519) (kluczowe pojęcia: [[Test-Time Compute i Reasoning Tokens]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Inżynieria rozumowania / Test-time compute / Ewaluacja modeli (1)

- [[2026-09-14 Maksymalny budżet rozumowania nie zawsze poprawia SWE; SOTA jako kompresja infor|Maksymalny budżet rozumowania nie zawsze poprawia SWE; SOTA jako kompresja informacji]] — [Post na X](https://x.com/karminski3/status/2099421138069950509) (kluczowe pojęcia: [[Test-Time Compute i Reasoning Tokens]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Harness]], [[Prompt Architecture]])

### Modele LLM / Architektura i wdrożenia (1)

- [[2026-09-15 K2-Horizon-7B mały model Dense z pełną atencją zbliża się do 27B — koszt konteks|K2-Horizon-7B: mały model Dense z pełną atencją zbliża się do 27B — koszt kontekstu i strategia wdrożenia]] — [Post na X](https://x.com/karminski3/status/2099991128061919596) (kluczowe pojęcia: [[Harness]], [[Architektura KV Cache i Rozumowanie Latentne]], [[Harness]], [[Harness]], [[Harness]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Modele językowe / Benchmarki / Wdrożenia produkcyjne (1)

- [[2026-09-15 K2-Horizon-7B mały 7B Dense z pełną uwagą zbliża się do 27B i wymaga wysokiego b|K2-Horizon-7B: mały 7B Dense z pełną uwagą zbliża się do 27B i wymaga wysokiego budżetu kontekstu]] — [Post na X](https://x.com/karminski3/status/2099991128061919596) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Modele multimodalne / inżynieria danych wejściowych (wideo) (1)

- [[2026-08-21 DeepSeek-V4-Flash-Vision-Exp przetwarzanie wideo przez ekstrakcję klatek (pułapk|DeepSeek-V4-Flash-Vision-Exp: przetwarzanie wideo przez ekstrakcję klatek (pułapka GIF = tylko pierwsza klatka)]] — [Post na X](https://x.com/karminski3/status/2090858863679750280) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Modele rozumujące / Test-time compute / Destylacja (1)

- [[2026-09-14 Budżet myślenia a destylacja długiego CoT dlaczego małe modele 'rosną' wraz z dł|Budżet myślenia a destylacja długiego CoT: dlaczego małe modele 'rosną' wraz z długością rozumowania]] — [Post na X](https://x.com/karminski3/status/2099435885599367551) (kluczowe pojęcia: [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Multimodalne modele agentowe / Architektura harnessów (1)

- [[2026-09-18 Qwen3.8-Omni-Flash z Live-Harness i MM-Plugins multimodalne skille, realtime i i|Qwen3.8-Omni-Flash z Live-Harness i MM-Plugins: multimodalne skille, realtime i integracja z agentami CLI]] — [Post na X](https://x.com/karminski3/status/2100751056104026497) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Dynamiczne Skille i Metaprogramowanie Agenta]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Dynamiczne Skille i Metaprogramowanie Agenta]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Multimodalność / Obserwacje zachowania modeli (1)

- [[2026-08-21 Obsługa wideo w modelu deepseek-v4-flash-vision-exp ekstrakcja klatek zamiast GI|Obsługa wideo w modelu deepseek-v4-flash-vision-exp: ekstrakcja klatek zamiast GIF-a]] — [Post na X](https://x.com/karminski3/status/2090858863679750280) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Parametry inferencji / inżynieria rozumowania (reasoning effort, thinking budget) (1)

- [[2026-09-14 Reasoning effort (thinking budget) realnie wpływa na wyniki modelu — dowody z De|Reasoning effort (thinking budget) realnie wpływa na wyniki modelu — dowody z DeepSeek-R1-Zero]] — [Post na X](https://x.com/karminski3/status/2099396323942547519) (kluczowe pojęcia: [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Harness]])

### Prompt Architecture / Reasoning / Benchmarking (1)

- [[2026-09-14 SOTA jako doskonały kompresor informacji minimalna liczba tokenów zamiast długie|SOTA jako doskonały kompresor informacji: minimalna liczba tokenów zamiast długiego rozumowania]] — [Post na X](https://x.com/karminski3/status/2099426676669366337) (kluczowe pojęcia: [[Test-Time Compute i Reasoning Tokens]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Test-Time Compute i Reasoning Tokens]], [[Harness]])

### Prompt architecture / Benchmarking / Ekonomia inferencji (1)

- [[2026-09-15 reasoning_effort jako marketing przenoszenie kosztu obliczeń i ryzyka rozliczeni|reasoning_effort jako marketing: przenoszenie kosztu obliczeń i ryzyka rozliczeniowego na użytkownika]] — [Post na X](https://x.com/karminski3/status/2099767043155218568) (kluczowe pojęcia: [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Harness]], [[Test-Time Compute i Reasoning Tokens]], [[Prompt Architecture]])

### Prompt architecture / inżynieria kontekstu / systemy agentowe (1)

- [[2026-09-14 Izomorfizm kodu i danych w skillach metaprogramowanie zamiast statycznych prompt|Izomorfizm kodu i danych w skillach: metaprogramowanie zamiast statycznych promptów ekstrakcyjnych]] — [Post na X](https://x.com/karminski3/status/2099383368999965122) (kluczowe pojęcia: [[Prompt Architecture]], [[Harness]], [[Dynamiczne Skille i Metaprogramowanie Agenta]], [[Prompt Architecture]], [[Harness]], [[Harness]], [[Weryfikator]], [[Context Compaction]], [[Dynamiczne Skille i Metaprogramowanie Agenta]])

### Reverse engineering embedded / systemy agentowe AI (1)

- [[2026-09-19 Agent AI łamie firmware drukarki etykiet RFID, Cortex-M0 i patchowanie jasności|Agent AI łamie firmware drukarki etykiet: RFID, Cortex-M0 i patchowanie jasności wydruku]] — [Post na X](https://x.com/karminski3/status/2101431800920990074) (kluczowe pojęcia: [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])

### Systemy agentowe / Bezpieczeństwo (Blue Team) (1)

- [[2026-08-27 Agent Apodex 1.1 przetwarza 1,2 mln linii logów, wykrywa atak privilege escalati|Agent Apodex 1.1 przetwarza 1,2 mln linii logów, wykrywa atak privilege escalation i generuje reguły firewalla]] — [Post na X](https://x.com/karminski3/status/2092894838492655713) (kluczowe pojęcia: [[Harness]], [[Context Compaction]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Weryfikator]], [[Harness]], [[Harness]], [[Harness]])

### Systemy agentowe / Bezpieczeństwo (SecOps) (1)

- [[2026-08-27 Apodex 1.1 end-to-end analiza 1,2 mln linii logów i generowanie reguł firewall d|Apodex 1.1: end-to-end analiza 1,2 mln linii logów i generowanie reguł firewall dla realnego ataku]] — [Post na X](https://x.com/karminski3/status/2092894838492655713) (kluczowe pojęcia: [[Context Compaction]], [[Harness]], [[Harness]], [[Sandbox i Granice Bezpieczeństwa Agenta]], [[Harness]], [[Weryfikacja krokowa]])

### Zachowanie modeli / Rozumowanie i dystylacja / Test-time compute (1)

- [[2026-09-14 Skalowanie budżetu rozumowania (test-time compute) i dystylacja CoT R1 do małych|Skalowanie budżetu rozumowania (test-time compute) i dystylacja CoT R1 do małych modeli — oraz anty-wzorzec „deepseek-r1-distilled-qwen-7b = DeepSeek”]] — [Post na X](https://x.com/karminski3/status/2099435885599367551) (kluczowe pojęcia: [[Test-Time Compute i Reasoning Tokens]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]], [[Harness]])
