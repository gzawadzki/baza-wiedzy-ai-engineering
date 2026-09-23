---
typ: indeks-autora
autor: "@kunchenguid"
źródło: "https://x.com/kunchenguid"
wygenerowano: "2026-09-23 20:34"
tagi:
  - kunchenguid
  - ai-engineering
  - indeks
---

# @kunchenguid — Indeks Bazy Wiedzy

> Baza wiedzy wyekstrahowana z wypowiedzi i dyskusji inżynierskich **@kunchenguid**. Zawiera **67** wyodrębnionych, atomowych notatek inżynierskich.

## ⚠️ Kwestie sporne i rozbieżności do rozstrzygnięcia

> Tezy podważające powszechne przekonania branżowe lub prezentujące odmienne podejście:

- **[[2026-09-12 Dobór modelu do debugowania Grok 4.5 vs Opus 4.8 w diagnozie awarii GitHub Actio|Dobór modelu do debugowania: Grok 4.5 vs Opus 4.8 w diagnozie awarii GitHub Actions]]** — Teza stoi w sprzeczności z powszechnym konsensusem branżowym, w którym modele Claude (Opus) uchodzą za domyślny wybór do zadań koderskich i agentowych. Autor twierdzi na podstawie własnych doświadczeń, że Grok 4.5 jest skuteczniejszy i tańszy w diagnostyce infrastruktury, i domyślnie go wybiera. Jest to jednak dowód anegdotyczny (N=1) — do rozstrzygnięcia pozostaje, czy przewaga wynika z rzeczywistej różnicy w strategii eksploracji narzędzi (tool-use / inspekcja stanu systemu) między modelami, czy z wariancji pojedynczego uruchomienia. Warto zweryfikować na większej próbie zadań diagnostycznych.
- **[[2026-09-12 Przejrzyste subsydiowanie modeli a harnessy dostawcy jako dług techniczny|Przejrzyste subsydiowanie modeli a harnessy dostawcy jako dług techniczny]]** — Teza stoi w sprzeczności z dominującym konsensusem branżowym, w którym dostawcy modeli wiążą korzystną cenę z użyciem własnego harnessa i domyślnym zbieraniem danych ('data-for-discount'). Autor twierdzi, że subsydiowanie da się rozdzielić od harnessa i że harness dostawcy jest długiem technicznym, a nie przewagą — do rozstrzygnięcia: czy istnieje ekonomicznie trwały model sprzedaży modeli bez pośrednictwa własnego harnessa, oraz czy niezależne harnessy rzeczywiście pokrywają pełen zakres funkcji (np. specyficzne narzędzia, pamięć, cache promptów) oferowanych przez harnessy pierwszej strony.
- **[[2026-09-12 Routing modeli w debugowaniu operacyjnym Grok 4.5 vs Opus 4.8 na zapchanych runn|Routing modeli w debugowaniu operacyjnym: Grok 4.5 vs Opus 4.8 na zapchanych runnerach GitHub Actions]]** — Teza sprzeczna z dominującym konsensusem, że Opus to najsilniejszy model do złożonych zadań agentowych. Autor twierdzi, że w debugowaniu operacyjnym Grok 4.5 jest ~8x tańszy i ~3x szybszy do rezultatu niż Opus 4.8. Zastrzeżenie: autor sam przyznaje, że to przykład anegdotyczny (n=1), bez powtarzalnego benchmarku — spór do rozstrzygnięcia wymaga systematycznych testów na zbiorze incydentów infrastrukturalnych.
- **[[2026-09-12 Transparentne subsydiowanie danych treningowych zamiast wymuszania własnego harn|Transparentne subsydiowanie danych treningowych zamiast wymuszania własnego harnessu]]** — Teza kontrowersyjna wobec dominującego konsensusu branżowego. Główny nurt (Anthropic z Claude Code, OpenAI z Codex, dostawcy chińscy) traktuje własny harness jako produkt strategiczny: kanał dystrybucji, źródło danych treningowych i mechanizm różnicowania oferty oraz przywiązania użytkownika. Autor twierdzi odwrotnie — że własny harness dostawcy to dług techniczny, który fragmentuje środowisko użytkownika i nie wnosi wartości, a przewagę konkurencyjną daje wyłącznie transparentność (jawna subsydiacja + opcjonalna, wyceniona kontrybucja danych) oraz zgodność ze standardowym API. Do rozstrzygnięcia: czy harness jest realnym źródłem przewagi produktowej, czy tylko kosztem — oraz czy zbieranie danych treningowych da się skalować bez pośrednictwa własnego harnessu (dowód: model cenowy Meta/muse spark). Wniosek zaktualizowany względem wcześniejszych wpisów, jeśli te zakładały wyższość zintegrowanych stacków dostawcy.
- **[[2026-09-16 Eskalacja do cięższego panelu LLM na podstawie kwantyfikowanej pewności modelu|Eskalacja do cięższego panelu LLM na podstawie kwantyfikowanej pewności modelu]]** — Autor podważa narrację o skoku jakościowym nowego modelu, twierdząc, że własne ewaluacje dostawcy wskazują na poprawę głównie w efektywności. Sporne wobec konsensusu branżowego („nowszy model = lepszy wynik”): realna wartość migracji może leżeć w koszcie/latency, a nie w zdolnościach — co zmienia strategię adopcji z „wymień model” na „użyj go jako taniej warstwy pierwszego rzutu z eskalacją”.
- **[[2026-09-17 32k tokenów okna kontekstu jako wystarczające dla większości praktycznych zastos|32k tokenów okna kontekstu jako wystarczające dla większości praktycznych zastosowań]]** — Teza stoi w opozycji do dominującego trendu branżowego, w którym dostawcy modeli prześcigają się w oferowaniu okien kontekstu rzędu 128k, 200k, a nawet 1M tokenów, sugerując, że 'więcej kontekstu = lepiej'. Autor twierdzi, że 32k jest w praktyce wystarczające. Do rozstrzygnięcia: dla jakich klas zadań (RAG, analiza długich dokumentów, agenty z długą historią) 32k przestaje wystarczać, a kiedy argument 'mniej kontekstu = lepsza jakość i niższy koszt' jest słuszny.
- **[[2026-09-17 Architektura hybrydowa zamiast pętli agentowej kod deterministyczny + lekki mode|Architektura hybrydowa zamiast pętli agentowej: kod deterministyczny + lekki model decyzyjny + okazjonalny LLM]]** — Teza stoi w opozycji do dominującego konsensusu branżowego („agent-first”), w którym zakłada się, że rdzeniem nowych aplikacji powinny być autonomiczne pętle agentowe z LLM podejmującym decyzje na każdym kroku. Autor twierdzi, że dla wielu zastosowań LLM jest nadmiarowym i kosztownym rdzeniem decyzyjnym, a wystarczająca jest kombinacja kodu deterministycznego i lekkiego modelu decyzyjnego, z LLM używanym jedynie do generowania treści. Do rozstrzygnięcia pozostaje granica: w jakich klasach zadań lekki model decyzyjny dorównuje LLM pod względem jakości decyzji i generalizacji na przypadki brzegowe, a w jakich przewaga LLM (rozumienie kontekstu, rozumowanie wieloetapowe, obsługa nieznanych przypadków) jest niezbędna i uzasadnia koszt.
- **[[2026-09-17 Krytyka protokołu MCP jako rzekomo „lepszego” standardu integracji narzędzi|Krytyka protokołu MCP jako rzekomo „lepszego” standardu integracji narzędzi]]** — Autor zakłada tezę sprzeczną z dominującym konsensusem branżowym, według którego MCP staje się de facto standardem integracji narzędzi z LLM. Twierdzi, że dopóki istnieje wskazane przez niego alternatywne rozwiązanie (treść linku niedostępna w tym wpisie), MCP nie może rościć sobie prawa do miana „lepszego”. Spór do rozstrzygnięcia: czy wartość MCP wynika z realnej przewagi technicznej (standaryzacja, ekosystem serwerów, separacja procesu), czy jest głównie efektem efektu sieciowego i marketingu Anthropic. Wymaga weryfikacji źródła linkowanego przez autora oraz porównania kosztów: narzut latency/tokenów, złożoność wdrożenia i utrzymania, dojrzałość alternatyw.
- **[[2026-09-17 Zastąpienie rozumowania LLM w routingu zadań wyspecjalizowanym, szybkim klasyfik|Zastąpienie rozumowania LLM w routingu zadań wyspecjalizowanym, szybkim klasyfikatorem (Jev) — architektura hybrydowa orkiestratora]]** — Teza stoi w napięciu z powszechnym konsensusem branżowym, według którego orkiestracja i routing zadań powinny być realizowane przez 'inteligentny' agent LLM z pętlą rozumowania i wywołaniami narzędzi. Autor twierdzi, że dla deterministycznych decyzji routujących LLM jest zbędny i należy go zastąpić wyspecjalizowanym, niemal darmowym klasyfikatorem, redukując rolę LLM do 'małego elementu' architektury. Do rozstrzygnięcia pozostaje: (a) czy parytet decyzji utrzymuje się poza wąskim zbiorem 25 zadań ewaluacyjnych i przy zmianach reguł dispatchu/kwot, (b) czy klasyfikator nie wymaga ciągłej re-dystylacji przy ewolucji polityki routingu, (c) czy oszczędność ~100x liczy się wyłącznie dla zastąpionego fragmentu, a nie całego systemu (dla całości -71% kosztu i -90% wall time).
- **[[2026-09-18 Kompaktowanie kontekstu jako klasyfikacja bezpiecznego punktu, a nie reakcja na|Kompaktowanie kontekstu jako klasyfikacja bezpiecznego punktu, a nie reakcja na próg]]** — Teza stoi w sprzeczności z powszechnym konsensusem branżowym, w którym auto-compaction jest wyzwalane progowo (np. procent zajętości okna kontekstowego) i traktowane jako mechanizm deterministyczny. Autor twierdzi, że jest to zły pomysł i że kompaktowanie wymaga decyzji klasyfikacyjnej o bezpieczeństwie punktu — co do rozstrzygnięcia: czy prosty próg tokenów wystarcza, czy konieczny jest detektor stanu agenta.
- **[[2026-09-18 Krytyka selektywnego usuwania tool calls jako metody kompakcji kontekstu|Krytyka selektywnego usuwania tool calls jako metody kompakcji kontekstu]]** — Autor krytykuje szeroko rozpowszechnioną metodę kompakcji kontekstu polegającą na selektywnym usuwaniu wywołań narzędzi, wskazując na fundamentalne wady: rosnące podsumowanie i wysokie koszty niecache'owanego promptu. Jest to sprzeczne z popularnym trendem stosowania tej techniki.
- **[[2026-09-18 Nie stosuj natychmiastowej kompakcji kontekstu — wykrywaj bezpieczny punkt kompa|Nie stosuj natychmiastowej kompakcji kontekstu — wykrywaj bezpieczny punkt kompakcji]]** — Sprzeczność z powszechnym w branży wzorcem automatycznej kompakcji opartej na progu zajętości kontekstu (np. „compact gdy >80% okna”). Autor twierdzi, że trigger progowy jest anty-wzorcem, a kompakcja powinna być warunkowana klasyfikacją bezpieczeństwa stanu — do rozstrzygnięcia, czy podejście klasyfikacyjne nie wprowadza zbyt dużego opóźnienia i kosztu dodatkowego wywołania modelu przy każdym kroku.
- **[[2026-09-20 Luka między badaniami a produktem dlaczego opakowanie i użyteczność wygrywają z|Luka między badaniami a produktem: dlaczego opakowanie i użyteczność wygrywają z "opowiadaniem historii"]]** — Autor podważa popularny konsensus, że o sukcesie decyduje marketing i "opowiedzenie własnej historii". Twierdzi, że różnicę robi dopracowanie produktu do stanu gotowego do adopcji, a nie narracja. Spór do rozstrzygnięcia: czy przewaga Jev wynika z lepszego pakietu inżynierskiego, czy jednak z dystrybucji/marketingu — autor przypisuje decydującą rolę pierwszemu czynnikowi.
- **[[2026-09-20 Research vs produkt pakowanie i gotowość do adopcji decydują o przewadze rynkowe|Research vs produkt: pakowanie i gotowość do adopcji decydują o przewadze rynkowej]]** — Autor podważa powszechny konsensus branżowy, że o sukcesie decyduje marketing i narracja ('you gotta tell your story'). Twierdzi, że w tym przypadku różnicę zrobiła inżynieria pakowania i doprowadzenie rozwiązania do stanu gotowego do adopcji, a nie promocja. Teza sporna: czy pierwszeństwo pomysłu (research) ma jakąkolwiek wartość rynkową bez dopracowania produktowego. Do rozstrzygnięcia w bazie wiedzy jako zasada: oceniaj rozwiązania po metrykach gotowości do użycia, nie po nowości koncepcji.
- **[[2026-09-22 Grok 4.7 jakościowe obserwacje z całodniowego użycia jako firstmate|Grok 4.7: jakościowe obserwacje z całodniowego użycia jako firstmate]]** — Autor podważa powszechny konsensus, że publiczne benchmarki i porównania modeli w grach 3D są użytecznym miernikiem jakości. Twierdzi, że są bezużyteczne dla realnej pracy, mogą prowadzić do błędnych wniosków (np. Opus 5 vs. Fable) i służą głównie uwadze w mediach społecznościowych.
- **[[2026-09-22 Obserwacje z użytkowania Grok 4.7 ścisłe trzymanie się promptu systemowego, stab|Obserwacje z użytkowania Grok 4.7: ścisłe trzymanie się promptu systemowego, stabilność i konserwatyzm]]** — Autor twierdzi, że publiczne benchmarki i porównania modeli w grach 3D są bezużyteczne i nie odzwierciedlają rzeczywistej pracy. To stoi w sprzeczności z powszechną praktyką oceny modeli LLM na podstawie tych metod. Wskazuje, że benchmarki mogą dawać mylące wyniki (np. Opus 5 vs Fable) i że prawdziwa ocena wymaga jakościowych obserwacji z rzeczywistego użytkowania.
- **[[2026-09-23 Cached read tokens dominują w realnym użyciu — surowe liczby z benchmarków mylą|Cached read tokens dominują w realnym użyciu — surowe liczby z benchmarków mylą]]** — Sprzeczność z powszechną praktyką branżową, w której porównuje się modele i providery po zagregowanych liczbach z benchmarków (koszt za milion tokenów, średni throughput, średnie TTFT). Autor twierdzi, że te wartości są mylące, bo w rzeczywistym użyciu wolumen zdominowany jest przez cached read tokens, których proporcja nie jest reprezentowana w typowym benchmarku. Do rozstrzygnięcia: czy benchmarki powinny raportować rozbicie per typ tokena i per współczynnik trafień w cache, oraz jak standaryzować takie pomiary.
- **[[2026-09-23 GPT-6 Luna jako „slow mode” model wsadowy do pracy w tle, nie do interakcji|GPT-6 Luna jako „slow mode”: model wsadowy do pracy w tle, nie do interakcji]]** — Autor podważa dominujący trend „fast mode”, w którym modele przyspiesza się kosztem wyższej ceny, i twierdzi, że potrzebny jest także „slow mode” do pracy w tle. Sprzeciwia się też powszechnemu założeniu, że wysokie reasoning jako firstmate/orkiestrator jest zawsze właściwym wyborem: według niego w przypadku Luny taka konfiguracja nie działa z powodu przeciążenia zdarzeniami i braku przepustowości tur.

---

## Spis tematów i notatek

### Architektura agentowa / Routing i dispatch zadań (1)

- [[2026-09-17 Zastąpienie routing'u zadań opartego na LLM dedykowanym, deterministycznym route|Zastąpienie routing'u zadań opartego na LLM dedykowanym, deterministycznym routerem (Jev) w orchestratorze Firstmate]] — [Post na X](https://x.com/kunchenguid/status/2100468943853085061) ([[Harness|Orchestrator]] [[Kaskady Modeli i Routing Pewności|Routing zadań]] [[Harness|Deterministyczny router]] [[Harness|LLM jako router]] [[Harness|Tool calls]] [[Harness|Latencja]] [[Harness|Koszt tokenów]] [[Harness|Agent harness]] [[Harness|Architektura systemów agentowych]] [[Firstmate i Agenci Wykonawczy]])

### Architektura agentów / Zarządzanie kontekstem (1)

- [[2026-09-21 Zarządzanie transkryptami sesji i unikanie wznawiania wygasłego cache w harnessa|Zarządzanie transkryptami sesji i unikanie wznawiania wygasłego cache w harnessach agentowych]] — [Post na X](https://x.com/kunchenguid/status/2101880818142515556) ([[Harness|Agent Harness]] [[Harness|Transkrypt sesji]] [[Context Compaction|Cache kontekstu]] [[Harness|Zarządzanie sesjami agentowymi]] [[Harness|Koszt inferencji]])

### Architektura harnessu / routing modeli (1)

- [[2026-09-17 Routing modeli z uwzględnieniem zapasu kwoty (quota runway)|Routing modeli z uwzględnieniem zapasu kwoty (quota runway)]] — [Post na X](https://x.com/kunchenguid/status/2100487003431477661) ([[Kaskady Modeli i Routing Pewności|Routing modeli]] [[Harness|Quota runway]] [[Harness|Zarządzanie limitami API]] [[Harness|Harness agentowy]] [[Harness|Load balancing modeli]] [[Harness|Failover dostawców LLM]])

### Architektura harnessu / systemy agentowe (1)

- [[2026-09-17 Degradacja harnessu do basha utrata tool search i przewagi nad CLI|Degradacja harnessu do basha: utrata tool search i przewagi nad CLI]] — [Post na X](https://x.com/kunchenguid/status/2100465119897809142) ([[Harness|Tool search]] [[Harness|Architektura harnessu]] [[Harness|Narzędzia agentowe]] [[Harness|Discoverability narzędzi]] [[Harness|Bash vs ustrukturyzowane narzędzia]] [[Context Compaction|Inżynieria kontekstu]])

### Architektura harnessów / Narzędzia agentowe (1)

- [[2026-09-22 Kompatybilność harnessów Cursor blokuje zewnętrzne harnessy, subskrypcje SuperGr|Kompatybilność harnessów: Cursor blokuje zewnętrzne harnessy, subskrypcje SuperGrok nie]] — [Post na X](https://x.com/kunchenguid/status/2102241720826204224) ([[Harness]] [[Harness|Agent Architecture]] [[Harness|Third-party harness]] [[Harness|Cursor]] [[Harness|SuperGrok]] [[Harness|Agentic Loop]])

### Architektura harnessów / Systemy agentowe (1)

- [[2026-09-22 Konfiguracja per-repo polityki błędów w harnessie agentowym (firstmate)|Konfiguracja per-repo polityki błędów w harnessie agentowym (firstmate)]] — [Post na X](https://x.com/kunchenguid/status/2102239513980608520) ([[Harness|Harness agentowy]] [[Harness|Polityka per-repo]] [[Weryfikacja krokowa|Zewnętrzna weryfikacja]] [[Harness|Tryb no-mistakes]] [[Harness|Konfiguracja agenta]] [[Firstmate i Agenci Wykonawczy]] [[Selektywna weryfikacja kodu]])

### Architektura harnessów / systemy agentowe (1)

- [[2026-09-22 Konfiguracja polityki rygoru per repozytorium w harnessie agentowym (firstmate)|Konfiguracja polityki rygoru per repozytorium w harnessie agentowym (firstmate)]] — [Post na X](https://x.com/kunchenguid/status/2102239513980608520) ([[Harness|Harness agentowy]] [[Harness|Polityka rygoru per repozytorium]] [[Weryfikator|Zewnętrzny weryfikator]] [[Harness|Bramki jakości w CI agenta]] [[Prompt Architecture|Konfiguracja a prompt]] [[Firstmate i Agenci Wykonawczy]] [[Selektywna weryfikacja kodu]])

### Architektura harnessów / weryfikacja kodu (1)

- [[2026-09-22 Heurystyka selektywnego stosowania zewnętrznego recenzenta kodu (no-mistakes)|Heurystyka selektywnego stosowania zewnętrznego recenzenta kodu (no-mistakes)]] — [Post na X](https://x.com/kunchenguid/status/2102239379536433551) ([[Weryfikator|Zewnętrzny weryfikator]] [[Code Review|Agent code review]] [[Harness|Harness agentowy]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Selekcja zadań dla agenta]] [[Selektywna weryfikacja kodu]])

### Architektura harnessów i narzędzi agentowych (1)

- [[2026-09-22 Rozdzielenie harnessu agentowego według dostawcy modelu (pi dla modeli nie-Anthr|Rozdzielenie harnessu agentowego według dostawcy modelu (pi dla modeli nie-Anthropic)]] — [Post na X](https://x.com/kunchenguid/status/2102239083678650816) ([[Harness|Harness agentowy]] [[Harness|Model-agnostic harness]] [[Harness|Tool calling]] [[Prompt Architecture|Prompt cache]] [[Kaskady Modeli i Routing Pewności|Routing modeli]] [[Harness|Benchmarking modeli]])

### Architektura harnessów i narzędzia agentowe (1)

- [[2026-09-22 Ograniczenia integracji zewnętrznych harnessów w Cursorze vs subskrypcje SuperGr|Ograniczenia integracji zewnętrznych harnessów w Cursorze vs subskrypcje SuperGrok]] — [Post na X](https://x.com/kunchenguid/status/2102241720826204224) ([[Harness]] [[Harness|Vendor Lock-in]] [[Harness|Cursor]] [[Harness|SuperGrok]] [[Harness|Subskrypcja modelu vs warstwa orkiestracji]] [[Firstmate i Agenci Wykonawczy]])

### Architektura harnessów i polityka danych dostawców modeli (1)

- [[2026-09-12 Transparentne subsydiowanie danych treningowych zamiast wymuszania własnego harn|Transparentne subsydiowanie danych treningowych zamiast wymuszania własnego harnessu]] — [Post na X](https://x.com/kunchenguid/status/2098854862788440308) ([[Harness]] [[Harness|Vendor lock-in]] [[Harness|Zbieranie danych treningowych]] [[Harness|Subsydiowanie cenowe modeli]] [[Harness|Model-agnostic tooling]] [[Harness|Polityka prywatności w AI]] [[Harness|Architektura systemów agentowych]])

### Architektura harnessów i routing modeli (2)

- [[2026-09-16 Eskalacja do cięższego panelu LLM na podstawie kwantyfikowanej pewności modelu|Eskalacja do cięższego panelu LLM na podstawie kwantyfikowanej pewności modelu]] — [Post na X](https://x.com/kunchenguid/status/2100090575106310498) ([[Kaskady Modeli i Routing Pewności|Routing modeli według pewności]] [[Kaskady Modeli i Routing Pewności|Kaskada modeli]] [[Harness|Mixture of Agents]] [[Harness|Kalibracja pewności modelu]] [[Harness|Ewaluacje modeli]] [[Harness|Koszt vs jakość inferencji]])
- [[2026-09-17 Routing modeli z uwzględnieniem pozostałego limitu kwot (quota runway)|Routing modeli z uwzględnieniem pozostałego limitu kwot (quota runway)]] — [Post na X](https://x.com/kunchenguid/status/2100487003431477661) ([[Kaskady Modeli i Routing Pewności|Model Routing]] [[Harness|Quota Management]] [[Harness|Rate Limiting]] [[Harness|Agent Harness]] [[Harness|Load Balancing Modeli]] [[Harness|429 Too Many Requests]])

### Architektura harnessów i systemów agentowych (1)

- [[2026-09-17 Tool calling przez bash degraduje harness do gorszej wersji CLI|Tool calling przez bash degraduje harness do gorszej wersji CLI]] — [Post na X](https://x.com/kunchenguid/status/2100465119897809142) ([[Harness|Tool calling]] [[Harness|Tool search]] [[Harness|Harness agentowy]] [[Harness|Bash]] [[Harness|CLI]] [[Context Compaction|Inżynieria kontekstu]])

### Architektura systemów agentowych (1)

- [[2026-09-17 Jev nie zastępuje LLM-ów — wymaga nowego paradygmatu budowy oprogramowania|Jev nie zastępuje LLM-ów — wymaga nowego paradygmatu budowy oprogramowania]] — [Post na X](https://x.com/kunchenguid/status/2100471365912707312) ([[Harness|Systemy agentowe]] [[Harness|LLM jako komponent systemu]] [[Harness]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Paradygmat wytwarzania oprogramowania z LLM]])

### Architektura systemów agentowych / Ekonomia tokenów (1)

- [[2026-09-16 Model kosztowy agenta AI zatrudnienie „CTO|Model kosztowy agenta AI: zatrudnienie „CTO]] — [Post na X](https://x.com/kunchenguid/status/2100262459282239910) ([[Harness|Systemy agentowe]] [[Harness|Ekonomia tokenów]] [[Harness|Koszt a skalowanie]] [[Context Compaction|Inżynieria kontekstu]])

### Architektura systemów agentowych / Ewaluacja i metryki (1)

- [[2026-09-22 Ewaluacja agentów przez wynik i wskaźnik reworku, nie przez jakość promptu|Ewaluacja agentów przez wynik i wskaźnik reworku, nie przez jakość promptu]] — [Post na X](https://x.com/kunchenguid/status/2102294506062385364) ([[Harness|Ewaluacja agentów]] [[Firstmate Agent|Architektura firstmate]] [[Harness|Skalowanie agentów]] [[Harness|Koszt iteracji]] [[Rework Rate|Metryki reworku]] [[Firstmate i Agenci Wykonawczy]])

### Architektura systemów agentowych / Inżynieria kontekstu (3)

- [[2026-09-17 Brief zadania jako obowiązkowy element kontekstu wejściowego przy delegacji do a|Brief zadania jako obowiązkowy element kontekstu wejściowego przy delegacji do agenta]] — [Post na X](https://x.com/kunchenguid/status/2100494796687340001) ([[Context Compaction|Inżynieria kontekstu]] [[Harness|Systemy multi-agentowe]] [[Harness|Task Brief]] [[Harness|Orkiestracja agentów]] [[Kaskady Modeli i Routing Pewności|Routing modeli]] [[Harness|Zarządzanie budżetem tokenowym]] [[Harness|Audytowalność decyzji agenta]] [[Firstmate i Agenci Wykonawczy]])
- [[2026-09-17 Dlaczego klasyfikatory tradycyjne nie działają dla kategorii definiowanych przez|Dlaczego klasyfikatory tradycyjne nie działają dla kategorii definiowanych przez użytkownika]] — [Post na X](https://x.com/kunchenguid/status/2100609623531421915) ([[Harness|Dynamiczna klasyfikacja in-context]] [[Harness|Open-label classification]] [[Harness|Zero-shot i few-shot klasyfikacja LLM]] [[Harness|Kategorie definiowane przez użytkownika]] [[Harness|Kiedy LLM zamiast klasyfikatora ML]])
- [[2026-09-17 Dynamiczna kompozycja kontekstu przy dyspozycji agenta task brief + reguły dyspo|Dynamiczna kompozycja kontekstu przy dyspozycji agenta: task brief + reguły dyspozycji + dane o kwotach]] — [Post na X](https://x.com/kunchenguid/status/2100494796687340001) ([[Context Compaction|Inżynieria kontekstu]] [[Harness|Orkiracja agentów]] [[Harness|Task Brief]] [[Prompt Architecture|Dynamiczna kompozycja promptu]] [[Harness|Zarządzanie budżetem tokenów]] [[Harness|Reguły dyspozycji użytkownika]] [[Harness|Recykling artefaktów pośrednich]] [[Firstmate i Agenci Wykonawczy]])

### Architektura systemów agentowych / Inżynieria kosztów (1)

- [[2026-09-17 Architektura hybrydowa logika deterministyczna + Jev + LLM zamiast pętli agentow|Architektura hybrydowa: logika deterministyczna + Jev + LLM zamiast pętli agentowych]] — [Post na X](https://x.com/kunchenguid/status/2100476218512748616) ([[Harness|Pętla agentowa]] [[Harness|Architektura hybrydowa]] [[Harness|Redukcja kosztów LLM]] [[Harness|Logika deterministyczna vs LLM]] [[Harness|Inżynieria systemów agentowych]])

### Architektura systemów agentowych / Inżynieria kosztów i opóźnień (1)

- [[2026-09-16 Selektywne stosowanie LLM routing modeli, eskalacja i triage zamiast LLM-do-wszy|Selektywne stosowanie LLM: routing modeli, eskalacja i triage zamiast LLM-do-wszystkiego]] — [Post na X](https://x.com/kunchenguid/status/2100052440343294172) ([[Kaskady Modeli i Routing Pewności|Model routing]] [[Harness|Eskalacja modeli]] [[Code Review|Triage code review]] [[Harness|LLM-do-wszystkiego (anty-wzorzec)]] [[Harness|Zużycie tokenów]] [[Harness|Latencja]] [[Harness|Harness agentowy]])

### Architektura systemów agentowych / Inżynieria kosztów wnioskowania (1)

- [[2026-09-17 Architektura hybrydowa zamiast pętli agentowej kod deterministyczny + lekki mode|Architektura hybrydowa zamiast pętli agentowej: kod deterministyczny + lekki model decyzyjny + okazjonalny LLM]] — [Post na X](https://x.com/kunchenguid/status/2100476218512748616) ([[Harness|Architektura hybrydowa]] [[Harness|Pętla agentowa]] [[Harness|Agent-first by default (anty-wzorzec)]] [[Kaskady Modeli i Routing Pewności|Routing modeli]] [[Harness|Redukcja kosztów inferencji]] [[Harness|Logika deterministyczna]] [[Harness|Małe modele decyzyjne]] [[Kaskady Modeli i Routing Pewności|Kaskadowanie modeli]] [[Harness|Testowalność systemów LLM]])

### Architektura systemów agentowych / Klasyfikacja z LLM (1)

- [[2026-09-17 Klasyfikacja kategorii definiowanych przez użytkownika — dlaczego klasyczny klas|Klasyfikacja kategorii definiowanych przez użytkownika — dlaczego klasyczny klasyfikator nie działa]] — [Post na X](https://x.com/kunchenguid/status/2100609623531421915) ([[Harness|In-context classification]] [[Harness|LLM jako klasyfikator]] [[Prompt Architecture|Few-shot prompting]] [[Harness|Dynamiczne przestrzenie etykiet]] [[Harness|User-defined taxonomy]] [[Kaskady Modeli i Routing Pewności|Embedding-based routing]] [[Prompt Architecture|Prompt engineering]])

### Architektura systemów agentowych / Optymalizacja kosztów (1)

- [[2026-09-16 Orkiestracja tanim modelem z eskalacją do modelu najwyższej klasy|Orkiestracja tanim modelem z eskalacją do modelu najwyższej klasy]] — [Post na X](https://x.com/kunchenguid/status/2100089760475930830) ([[Harness|Orkiestracja agentów]] [[Harness|Model tiering]] [[Harness|Eskalacja decyzji]] [[Harness|Optymalizacja kosztów LLM]] [[Kaskady Modeli i Routing Pewności|Routing modeli]] [[Harness|Multi-agent systemy]] [[Firstmate i Agenci Wykonawczy]])

### Architektura systemów agentowych / Optymalizacja kosztów i latencji (1)

- [[2026-09-16 Unikanie wzorca LLM do wszystkiego — routing, eskalacja i triage jako zadania kl|Unikanie wzorca "LLM do wszystkiego" — routing, eskalacja i triage jako zadania klasyfikacyjne]] — [Post na X](https://x.com/kunchenguid/status/2100052440343294172)

### Architektura systemów agentowych / Protokoły integracji narzędzi (1)

- [[2026-09-17 Krytyka protokołu MCP jako rzekomo „lepszego” standardu integracji narzędzi|Krytyka protokołu MCP jako rzekomo „lepszego” standardu integracji narzędzi]] — [Post na X](https://x.com/kunchenguid/status/2100461539316920716) ([[Harness|MCP - Model Context Protocol]] [[Harness|Function calling]] [[Harness|Warstwa narzędzi agenta]] [[Harness|Benchmark protokołów integracji]] [[Harness|Anty-wzorce w systemach agentowych]])

### Architektura systemów agentowych / Routing modeli i koszty (1)

- [[2026-09-16 Tani model jako orkiestrator z eskalacją do modelu top-tier (fable tier)|Tani model jako orkiestrator z eskalacją do modelu top-tier (fable tier)]] — [Post na X](https://x.com/kunchenguid/status/2100089760475930830) ([[Kaskady Modeli i Routing Pewności|Tiered model routing]] [[Harness|Model escalation pattern]] [[Harness|Tan i model jako orkiestrator]] [[Harness|Koszty systemów agentowych]] [[Prompt Architecture|Prompt steering]] [[Harness|System agentowy]] [[Firstmate i Agenci Wykonawczy]])

### Architektura systemów agentowych / Routing zadań (1)

- [[2026-09-21 Jev jako dedykowany router w orkiestratorze typu chief-of-staff|Jev jako dedykowany router w orkiestratorze typu chief-of-staff]] — [Post na X](https://x.com/kunchenguid/status/2101898514523730033) ([[Kaskady Modeli i Routing Pewności|Routing zadań do subagentów]] [[Harness|Orkiestrator chief-of-staff]] [[Harness|Dedykowany router zamiast decyzji LLM]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Koszt tokenów i latencja]] [[Firstmate i Agenci Wykonawczy]])

### Architektura systemów agentowych / Routing zadań / Optymalizacja kosztów i latencji (1)

- [[2026-09-17 Zastąpienie rozumowania LLM w routingu zadań wyspecjalizowanym, szybkim klasyfik|Zastąpienie rozumowania LLM w routingu zadań wyspecjalizowanym, szybkim klasyfikatorem (Jev) — architektura hybrydowa orkiestratora]] — [Post na X](https://x.com/kunchenguid/status/2100468943853085061) ([[Kaskady Modeli i Routing Pewności|Routing zadań agentowych]] [[Harness|Orkiestrator agentów]] [[Test-Time Compute i Reasoning Tokens|Reasoning effort]] [[Harness|Model harness]] [[Harness|Dystylacja decyzji do klasyfikatora]] [[Harness|Optymalizacja kosztów LLM]] [[Harness|Latencja i wall time]] [[Harness|Hybrydowa architektura agentowa]] [[Firstmate i Agenci Wykonawczy]])

### Architektura systemów agentowych / obserwacje zachowania modeli (1)

- [[2026-09-23 GPT-6 Luna jako „slow mode” model wsadowy do pracy w tle, nie do interakcji|GPT-6 Luna jako „slow mode”: model wsadowy do pracy w tle, nie do interakcji]] — [Post na X](https://x.com/kunchenguid/status/2102787931178176588) ([[Harness|Systemy agentowe]] [[Firstmate Agent|Firstmate]] [[Harness|Przepustowość tur]] [[Harness|Latencja end-to-end]] [[Harness|Koszt tokenów]] [[Harness|Tryb rozumowania]] [[Harness|Benchmarking modeli]])

### Architektura systemów agentowych / routing modeli (1)

- [[2026-09-16 Kaskadowa inferencja oparta na kwantyfikacji pewności modelu|Kaskadowa inferencja oparta na kwantyfikacji pewności modelu]] — [Post na X](https://x.com/kunchenguid/status/2100090575106310498) ([[Harness|Kwantyfikacja pewności modelu]] [[Kaskady Modeli i Routing Pewności|Inferencja kaskadowa]] [[Kaskady Modeli i Routing Pewności|Confidence-based routing]] [[Harness|Panel LLM / ensemble weryfikujący]] [[Weryfikator|Zewnętrzny weryfikator]] [[Eval Set z realnych sesji|Ewaluacje modeli (evals)]] [[Harness|Anty-wzorzec: slepe zaufanie do benchmarków dostawcy]])

### Architektura systemów agentowych i ewaluacja (1)

- [[2026-09-22 Ewaluacja agentów przez wynik i wskaźnik reworku zamiast jakości promptu|Ewaluacja agentów przez wynik i wskaźnik reworku zamiast jakości promptu]] — [Post na X](https://x.com/kunchenguid/status/2102294506062385364) ([[Harness|Ewaluacja agentów oparta na wyniku]] [[Rework Rate|Rework jako metryka]] [[Harness|Skalowanie nadzoru agentowego]] [[Harness|Agent-liść vs orkiestrator]] [[Firstmate i Agenci Wykonawczy]])

### Benchmarking / limity API i zarządzanie kwotami (1)

- [[2026-09-16 Szacowanie limitu tygodniowego kwoty przez próbkowanie 5% budżetu|Szacowanie limitu tygodniowego kwoty przez próbkowanie 5% budżetu]] — [Post na X](https://x.com/kunchenguid/status/2100323574791962644) ([[Harness|Benchmarking]] [[Harness|Limity API i kwoty]] [[Harness|Ekstrapolacja przez próbkowanie]] [[Test-Time Compute i Reasoning Tokens|Token Throughput]] [[Prompt Architecture|Cache i rozliczanie tokenów]])

### Benchmarking i ekonomika tokenów / Cache (1)

- [[2026-09-23 Cached read tokens dominują w realnym użyciu — surowe liczby z benchmarków mylą|Cached read tokens dominują w realnym użyciu — surowe liczby z benchmarków mylą]] — [Post na X](https://x.com/kunchenguid/status/2102626499748938117) ([[Prompt Architecture|Prompt Caching]] [[Prompt Architecture|Cached Read Tokens]] [[Harness|Benchmarkowanie LLM]] [[Harness|Ekonomika tokenów]] [[Context Compaction|Inżynieria kontekstu]] [[Test-Time Compute i Reasoning Tokens|Token Throughput]] [[Harness|Latencja TTFT]])

### Benchmarking i zarządzanie limitami API (1)

- [[2026-09-16 Szacowanie pełnego limitu tygodniowego (quota) przez ekstrapolację z 5% próbki|Szacowanie pełnego limitu tygodniowego (quota) przez ekstrapolację z 5% próbki]] — [Post na X](https://x.com/kunchenguid/status/2100323574791962644) ([[Harness|Benchmarking]] [[Harness|Limity API (quota)]] [[Harness|Ekstrapolacja z próbki]] [[Test-Time Compute i Reasoning Tokens|Token Throughput]] [[Harness|Harness ewaluacyjny]] [[Harness|Inżynieria kosztów LLM]])

### Benchmarking modeli agentowych / Debugowanie incydentów CI-CD (1)

- [[2026-09-12 Routing modeli w debugowaniu operacyjnym Grok 4.5 vs Opus 4.8 na zapchanych runn|Routing modeli w debugowaniu operacyjnym: Grok 4.5 vs Opus 4.8 na zapchanych runnerach GitHub Actions]] — [Post na X](https://x.com/kunchenguid/status/2098814897354137710) ([[Kaskady Modeli i Routing Pewności|Routing modeli]] [[Harness|Benchmarking modeli agentowych]] [[Harness|GitHub Actions]] [[Harness|Limity runnerów]] [[Harness|Debugowanie incydentów CI-CD]] [[Harness|Koszt tokenów a skuteczność]] [[Harness|Pułapka potwierdzenia w agentach]] [[Harness|Anegdotalna ocena modeli]] [[Firstmate i Agenci Wykonawczy]])

### Dobór modeli i koszt/efektywność w zadaniach agentowych (1)

- [[2026-09-12 Dobór modelu do debugowania Grok 4.5 vs Opus 4.8 w diagnozie awarii GitHub Actio|Dobór modelu do debugowania: Grok 4.5 vs Opus 4.8 w diagnozie awarii GitHub Actions]] — [Post na X](https://x.com/kunchenguid/status/2098814897354137710) ([[Harness|Dobór modelu]] [[Harness|Debugowanie agentowe]] [[Harness|GitHub Actions]] [[Harness|Analiza przyczyny źródłowej]] [[Harness|Koszt tokenów]] [[Harness|Współdzielone runnery CI]] [[Firstmate i Agenci Wykonawczy]])

### Ekonomia API / Inżynieria kontekstu i cache (1)

- [[2026-09-23 Ekonomia długiego kontekstu i cache Anthropic vs OpenAI vs xAI — płaski cennik i|Ekonomia długiego kontekstu i cache: Anthropic vs OpenAI vs xAI — płaski cennik i tani cache read]] — [Post na X](https://x.com/kunchenguid/status/2102615836242678094) ([[Prompt Architecture|Cache promptu]] [[Prompt Architecture|Cached read]] [[Harness|Long context]] [[Harness|Koszt inferencji]] [[Prompt Architecture|Cache hit rate]] [[Harness|Anthropic Claude]] [[Harness|OpenAI]] [[Harness|xAI Grok]] [[Harness|Harness agentowy]])

### Ekonomia i strategia dostawców modeli / Architektura harnessów (1)

- [[2026-09-12 Przejrzyste subsydiowanie modeli a harnessy dostawcy jako dług techniczny|Przejrzyste subsydiowanie modeli a harnessy dostawcy jako dług techniczny]] — [Post na X](https://x.com/kunchenguid/status/2098854862788440308) ([[Harness]] [[Harness|Model-agnostic harness]] [[Harness|Vendor lock-in]] [[Harness|Zbieranie danych treningowych]] [[Harness|Przejrzystość subsydiowania modeli]] [[Context Compaction|Inżynieria kontekstu]])

### Ekonomia systemów agentowych / Inżynieria kontekstu (1)

- [[2026-09-16 Koszt agenta AI jako koszt zatrudnienia CTO — model mentalny zwrotu z tokenów|Koszt agenta AI jako koszt zatrudnienia CTO — model mentalny zwrotu z tokenów]] — [Post na X](https://x.com/kunchenguid/status/2100262459282239910) ([[Harness|Systemy agentowe]] [[Harness|Ekonomia tokenów]] [[Context Compaction|Zarządzanie kontekstem]] [[Harness|Koszt inferencji]] [[Harness|Delegacja zadań do agenta]])

### Ewaluacja modeli / zachowanie agentów (1)

- [[2026-09-22 Grok 4.7 jakościowe obserwacje z całodniowego użycia jako firstmate|Grok 4.7: jakościowe obserwacje z całodniowego użycia jako firstmate]] — [Post na X](https://x.com/kunchenguid/status/2102234191639257399) ([[Harness|Ewaluacja jakościowa modeli]] [[Harness|Benchmarki publiczne]] [[Stabilność modeli i przestrzeganie promptu|Przestrzeganie system promptu]] [[Stabilność modeli i przestrzeganie promptu|Stabilność modelu]] [[Harness|Konserwatywne zachowanie agenta]] [[Harness|Koszt i opóźnienie modelu]] [[Harness|Harness agentowy]] [[CI Check Bypass Confirmation]] [[Firstmate i Agenci Wykonawczy]])

### Inżynieria AI (1)

- [[2026-09-18 Ręczne etykietowanie „bezpiecznych|Ręczne etykietowanie „bezpiecznych]] — [Post na X](https://x.com/kunchenguid/status/2101044924301156365) ([[Bezpieczny punkt kompaktowania]])

### Inżynieria kontekstu (2)

- [[2026-09-18 Krytyka selektywnego usuwania tool calls jako metody kompakcji kontekstu|Krytyka selektywnego usuwania tool calls jako metody kompakcji kontekstu]] — [Post na X](https://x.com/kunchenguid/status/2100800776620900454) ([[Context Compaction|Kompakcja kontekstu]] [[Context Compaction|Zarządzanie oknem kontekstowym]] [[Prompt Architecture|Cache promptów]] [[Harness|Ewaluacja agentów]] [[Harness|DeepSWE]] [[Harness|ProgramBench]])
- [[2026-09-18 Krytyka selektywnej kompakcji kontekstu rosnące podsumowanie i wysokie koszty|Krytyka selektywnej kompakcji kontekstu: rosnące podsumowanie i wysokie koszty]] — [Post na X](https://x.com/kunchenguid/status/2100800776620900454) ([[Context Compaction|Kompakcja kontekstu]] [[Context Compaction|Zarządzanie oknem kontekstowym]] [[Prompt Architecture|Pamięć podręczna promptów]] [[Harness|Ewaluacja modeli]])

### Inżynieria kontekstu / Cache i koszty inferencji (1)

- [[2026-09-18 Kompakcja sesji a cache promptów pełny prefiks vs cache miss|Kompakcja sesji a cache promptów: pełny prefiks vs cache miss]] — [Post na X](https://x.com/kunchenguid/status/2100816020932096060) ([[Prompt Architecture|Prompt Caching]] [[Context Compaction|Kompakcja kontekstu]] [[Prompt Architecture|Cache Miss]] [[Harness|Zarządzanie historią sesji]] [[Harness|Koszty inferencji]] [[Context Compaction|Append-only kontekst]])

### Inżynieria kontekstu / Prompt Caching / Ekonomia tokenów (1)

- [[2026-09-18 Kompakcja kontekstu a cache promptu nie modyfikuj historii przed kompakcją|Kompakcja kontekstu a cache promptu: nie modyfikuj historii przed kompakcją]] — [Post na X](https://x.com/kunchenguid/status/2100816020932096060) ([[Prompt Architecture|Prompt Caching]] [[Context Compaction|Kompakcja kontekstu]] [[Context Compaction|Inżynieria kontekstu]] [[Prompt Architecture|Cache Miss]] [[Harness|Ekonomia tokenów]] [[Harness|Zarządzanie historią sesji]])

### Inżynieria kontekstu / Rozmiar okna kontekstowego (1)

- [[2026-09-17 32k tokenów kontekstu jako wystarczający rozmiar dla większości zastosowań|32k tokenów kontekstu jako wystarczający rozmiar dla większości zastosowań]] — [Post na X](https://x.com/kunchenguid/status/2100475721294782575) ([[Context Compaction|Inżynieria kontekstu]] [[Context Compaction|Okno kontekstowe]] [[Context Compaction|Kompresja kontekstu]])

### Inżynieria kontekstu / Rozmiar okna kontekstu (1)

- [[2026-09-17 32k tokenów okna kontekstu jako wystarczające dla większości praktycznych zastos|32k tokenów okna kontekstu jako wystarczające dla większości praktycznych zastosowań]] — [Post na X](https://x.com/kunchenguid/status/2100475721294782575) ([[Context Compaction|Inżynieria kontekstu]] [[Context Compaction|Okno kontekstu]] [[Harness|Attention dilution]] [[Harness|Zarządzanie budżetem tokenów]])

### Inżynieria kontekstu / Zarządzanie kosztami i cache (1)

- [[2026-09-21 Koszt niezacache'owanego promptu przy 500k kontekstu — kiedy uruchamiać compact|Koszt niezacache'owanego promptu przy 500k kontekstu — kiedy uruchamiać /compact]] — [Post na X](https://x.com/kunchenguid/status/2101872626968969713) ([[Prompt Architecture|Prompt Caching]] [[Prompt Architecture|TTL cache promptu]] [[Context Compaction|Kompresja kontekstu /compact]] [[Context Compaction|Zarządzanie oknem kontekstu]] [[Harness|Koszty tokenów]] [[Harness|Długotrwałe sesje agentowe]] [[Harness|Transkrypt sesji jako pamięć zewnętrzna]] [[Persistencja stanu agenta]])

### Inżynieria kontekstu / Zarządzanie pamięcią agenta (2)

- [[2026-09-18 Auto-compact vs. ręczne mikro-optymalizacje kontekstu w erze szybkiego osądu mod|Auto-compact vs. ręczne mikro-optymalizacje kontekstu w erze szybkiego osądu modeli]] — [Post na X](https://x.com/kunchenguid/status/2101075672747970901) ([[Harness|Auto-compact]] [[Context Compaction|Zarządzanie oknem kontekstowym]] [[Harness|Koszt i latencja osądu modelu]] [[Prompt Architecture|Mikro-optymalizacja promptu]] [[Context Compaction|Inżynieria kontekstu]])
- [[2026-09-21 Delegowanie decyzji o kompakcji kontekstu do zewnętrznego sygnału|Delegowanie decyzji o kompakcji kontekstu do zewnętrznego sygnału]] — [Post na X](https://x.com/kunchenguid/status/2101877657927655730) ([[Context Compaction|Inżynieria kontekstu]] [[Context Compaction|Kompakcja kontekstu]] [[Harness|Zarządzanie pamięcią agenta]] [[Harness|Zewnętrzny sygnał / trigger]] [[Harness|Uwaga modelu (attention)]] [[Persistencja stanu agenta]])

### Inżynieria kontekstu / pamięć agentów / cache (1)

- [[2026-09-21 Nie wznawiaj długiej sesji po wygaśnięciu cache — użyj transkryptu w nowej sesji|Nie wznawiaj długiej sesji po wygaśnięciu cache — użyj transkryptu w nowej sesji]] — [Post na X](https://x.com/kunchenguid/status/2101880818142515556) ([[Harness|Agent harness]] [[Harness|Transkrypt sesji]] [[Context Compaction|Cache kontekstu]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Zarządzanie pamięcią agenta]] [[Harness|Koszt tokenów]] [[Prompt Architecture|Cache miss]])

### Inżynieria kontekstu / zarządzanie cache i kosztami (1)

- [[2026-09-21 Koszty niecache'owanego kontekstu i kolejność operacji compact|Koszty niecache'owanego kontekstu i kolejność operacji /compact]] — [Post na X](https://x.com/kunchenguid/status/2101872626968969713) ([[Prompt Architecture|Prompt Cache]] [[Prompt Architecture|TTL cache'u promptu]] [[Context Compaction|Kompakcja kontekstu]] [[Context Compaction|Zarządzanie oknem kontekstu]] [[Harness|Koszty tokenów]] [[Harness|Sesje agentowe]] [[Harness|Transkrypt sesji]])

### Inżynieria kontekstu / zarządzanie pamięcią agenta (7)

- [[2026-09-18 Auto-compact vs. ręczne zarządzanie kontekstem — kiedy mikro-optymalizacja przes|Auto-compact vs. ręczne zarządzanie kontekstem — kiedy mikro-optymalizacja przestaje się opłacać]] — [Post na X](https://x.com/kunchenguid/status/2101075672747970901) ([[Harness|Auto-compact]] [[Context Compaction|Zarządzanie oknem kontekstowym]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Koszt i latencja osądu modelu]] [[Harness|Mikro-optymalizacja vs. decyzje wysokopoziomowe]] [[Harness|Systemy agentowe]])
- [[2026-09-18 Bezpieczne checkpointy kontekstu kryterium braku zależności od nieutrwalonego st|Bezpieczne checkpointy kontekstu: kryterium braku zależności od nieutrwalonego stanu]] — [Post na X](https://x.com/kunchenguid/status/2101044924301156365) ([[Context Compaction|Inżynieria kontekstu]] [[Context Compaction|Checkpoint kontekstu]] [[Context Compaction|Kompakcja kontekstu]] [[Harness|Zarządzanie pamięcią agenta]] [[Harness|Utrwalanie stanu sesji]] [[Eval Set z realnych sesji|Ground truth]] [[Harness|Harness agentowy]] [[Bezpieczny punkt kompaktowania]] [[Checkpointing sesji agenta]])
- [[2026-09-18 compact-adviser dynamiczna strategia kompakcji kontekstu z przesunięciem precisi|compact-adviser: dynamiczna strategia kompakcji kontekstu z przesunięciem precision → recall]] — [Post na X](https://x.com/kunchenguid/status/2101032677940117875) ([[Context Compaction|Inżynieria kontekstu]] [[Context Compaction|Kompakcja kontekstu]] [[Harness|Zarządzanie pamięcią agenta]] [[Harness|Klasyfikator granic zadań]] [[Context Compaction|Precision vs Recall w kompakcji]] [[Prompt Architecture|Prompt hillclimbing]] [[Eval Set z realnych sesji|Eval set z realnych sesji]] [[Harness|Harness agentowy]] [[Harness|Auto vs Hint mode]] [[Bezpieczny punkt kompaktowania]] [[Checkpointing sesji agenta]])
- [[2026-09-18 compact-adviser klasyfikator bezpiecznego momentu kompakcji kontekstu z adaptacy|compact-adviser: klasyfikator bezpiecznego momentu kompakcji kontekstu z adaptacyjnym progiem precision/recall]] — [Post na X](https://x.com/kunchenguid/status/2101032677940117875) ([[Context Compaction|Inżynieria kontekstu]] [[Context Compaction|Kompakcja kontekstu]] [[Harness|Zarządzanie pamięcią agenta]] [[Harness|Klasyfikator decyzyjny]] [[Eval Set z realnych sesji|Eval set]] [[Prompt Architecture|Prompt hillclimbing]] [[Harness|Precision vs Recall]] [[Harness|Harness agentowy]] [[Bezpieczny punkt kompaktowania]] [[Checkpointing sesji agenta]])
- [[2026-09-18 Kompaktowanie kontekstu jako klasyfikacja bezpiecznego punktu, a nie reakcja na|Kompaktowanie kontekstu jako klasyfikacja bezpiecznego punktu, a nie reakcja na próg]] — [Post na X](https://x.com/kunchenguid/status/2101036854925779291) ([[Context Compaction|Compaction kontekstu]] [[Context Compaction|Zarządzanie oknem kontekstowym]] [[Harness|Harness agentowy]] [[Harness|Safe point / punkty bezpiecznego kompaktowania]] [[Harness|Antywzorce agentowe]] [[Context Compaction|Inżynieria kontekstu]] [[Bezpieczny punkt kompaktowania]])
- [[2026-09-18 Nie stosuj natychmiastowej kompakcji kontekstu — wykrywaj bezpieczny punkt kompa|Nie stosuj natychmiastowej kompakcji kontekstu — wykrywaj bezpieczny punkt kompakcji]] — [Post na X](https://x.com/kunchenguid/status/2101036854925779291) ([[Context Compaction|Kompakcja kontekstu]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Zarządzanie pamięcią agenta]] [[Context Compaction|Okno kontekstowe]] [[Harness|Harness agentowy]] [[Harness|Klasyfikacja stanu agenta]] [[Bezpieczny punkt kompaktowania]])
- [[2026-09-21 Kompakcja kontekstu sterowana sygnałem agenta zamiast ręcznego triggera|Kompakcja kontekstu sterowana sygnałem agenta zamiast ręcznego triggera]] — [Post na X](https://x.com/kunchenguid/status/2101877657927655730) ([[Context Compaction]] [[Context Compaction|Zarządzanie kontekstem agenta]] [[Harness|Harness agentowy]] [[Harness|Event-driven triggers w agentach]] [[Harness|Degradacja jakości przy przepełnionym kontekście]])

### Inżynieria produktu / Architektura agentowa (1)

- [[2026-09-20 Luka między badaniami a produktem dlaczego opakowanie i użyteczność wygrywają z|Luka między badaniami a produktem: dlaczego opakowanie i użyteczność wygrywają z "opowiadaniem historii"]] — [Post na X](https://x.com/kunchenguid/status/2101534610710761923) ([[Harness|Luka research-to-product]] [[Context Compaction|Okno kontekstu]] [[Harness|Fine-tuning vs out-of-the-box]] [[Harness|Productizacja modeli AI]] [[Harness|Adopcja narzędzi agentowych]])

### Inżynieria produktu / Strategia wdrożeń AI (1)

- [[2026-09-20 Research vs produkt pakowanie i gotowość do adopcji decydują o przewadze rynkowe|Research vs produkt: pakowanie i gotowość do adopcji decydują o przewadze rynkowej]] — [Post na X](https://x.com/kunchenguid/status/2101534610710761923) ([[Harness|Inżynieria produktu AI]] [[Harness|Gotowość do adopcji]] [[Context Compaction|Okno kontekstowe]] [[Harness|Fine-tuning]] [[Harness|Ewaluacja modeli]] [[Harness|Research vs produkt]])

### Inżynieria systemów agentowych / Zarządzanie niepewnością (1)

- [[2026-09-17 Wykorzystanie kwantyfikacji pewności do filtrowania odpowiedzi modelu|Wykorzystanie kwantyfikacji pewności do filtrowania odpowiedzi modelu]] — [Post na X](https://x.com/kunchenguid/status/2100608000042127434) ([[Harness|Kwantyfikacja pewności]] [[Harness|Zarządzanie niepewnością w LLM]] [[Harness|Filtrowanie odpowiedzi modelu]] [[Harness|Inżynieria wymagań]])

### Proces weryfikacji / Code Review AI (1)

- [[2026-09-22 Selektywne code review kiedy NIE uruchamiać automatycznej weryfikacji zmian|Selektywne code review: kiedy NIE uruchamiać automatycznej weryfikacji zmian]] — [Post na X](https://x.com/kunchenguid/status/2102239379536433551) ([[Code Review]] [[Weryfikacja krokowa|Automatyczna weryfikacja zmian]] [[Weryfikator|Zewnętrzny weryfikator]] [[Harness|Pętla feedbacku agenta]] [[Harness|Koszt tokenów]] [[Harness|Anty-wzorce w systemach agentowych]] [[Selektywna weryfikacja kodu]])

### Weryfikacja agentów i inżynieria wymagań (1)

- [[2026-09-17 Kwantyfikacja pewności w weryfikatorach pozwala odrzucać niepewne odpowiedzi|Kwantyfikacja pewności w weryfikatorach pozwala odrzucać niepewne odpowiedzi]] — [Post na X](https://x.com/kunchenguid/status/2100608000042127434) ([[Harness|LLM-as-a-judge]] [[Weryfikator|Zewnętrzny weryfikator]] [[Harness|Kalibracja pewności modelu]] [[Harness|Próg pewności]] [[Harness|Inżynieria wymagań]] [[Harness|Systemy agentowe]])

### Zachowanie modeli i ocena (1)

- [[2026-09-22 Obserwacje z użytkowania Grok 4.7 ścisłe trzymanie się promptu systemowego, stab|Obserwacje z użytkowania Grok 4.7: ścisłe trzymanie się promptu systemowego, stabilność i konserwatyzm]] — [Post na X](https://x.com/kunchenguid/status/2102234191639257399) ([[Prompt Architecture|Prompt systemowy]] [[Harness|Zachowanie modelu]] [[Harness|Benchmarkowanie LLM]] [[Stabilność modeli i przestrzeganie promptu|Stabilność modelu]] [[Harness|Konserwatyzm modelu]] [[Harness|Koszt tokenów]] [[Harness|Opóźnienie modelu]] [[CI Check Bypass Confirmation]] [[Firstmate i Agenci Wykonawczy]])
