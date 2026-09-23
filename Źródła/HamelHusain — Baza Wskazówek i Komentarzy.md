---
autor: "@HamelHusain"
źródło: "https://x.com/HamelHusain"
wygenerowano: "2026-09-23 02:30"
typ: synteza-wiedzy
tagi:
  - hamelhusain
  - ai-engineering
  - prompt-engineering
  - twitter-extract
---

# @HamelHusain — Baza Wskazówek i Komentarzy

> Destylacja praktycznych porad, heurystyk inżynierskich i komentarzy technicznych z profilu @HamelHusain na platformie X. Wyciągnięto 5 wartościowych wpisów.

## ⚠️ Kwestie sporne i rozbieżności do rozstrzygnięcia

> Wpisy, w których autor podważa powszechne przekonania branżowe lub prezentuje tezy stojące w sprzeczności z innymi praktykami:

- **[Kaskada modeli (model cascade) nie zakłada kalibracji log-prob — wymaga najpierw analizy statystycznej progu](https://x.com/HamelHusain/status/2088689040027775300):** Sprzeczność z szeroko powtarzanym konsensusem branżowym, że kaskady modeli i routing oparty na log-prob są zawodne, bo modele LLM są źle skalibrowane. Hamel Husain twierdzi, że to zarzut nieistotny: metoda nie zakłada kalibracji, lecz wymaga uprzedniej analizy statystycznej sygnału na konkretnym datasecie, a brak znalezienia progu jest akceptowalnym, przewidzianym w pracy wynikiem. Do rozstrzygnięcia: w jakim zakresie niekalibrowane log-prob rzeczywiście dyskwalifikują kaskadę, a w jakim wystarczy empiryczna walidacja progu (szczególnie dla zadań klasyfikacyjnych, gdzie test jest tani i weryfikowalny).

---

## Spis kategorii

- [Inżynieria agentowa / Ewaluacja i iteracja](#inżynieria-agentowa--ewaluacja-i-iteracja) (1)
- [Architektura agentów i protokoły kontekstu (MCP / WebMCP)](#architektura-agentów-i-protokoły-kontekstu-(mcp--webmcp)) (1)
- [Ewaluacja AI / Metodologia eksperymentów](#ewaluacja-ai--metodologia-eksperymentów) (1)
- [Architektura systemów ML / routing i kaskady modeli](#architektura-systemów-ml--routing-i-kaskady-modeli) (1)
- [Ewaluacja i systemy agentowe](#ewaluacja-i-systemy-agentowe) (1)

---

## Inżynieria agentowa / Ewaluacja i iteracja

### Zbieranie ~10 przykładów pozytywnych/negatywnych jako paliwo do hill-climbingu agenta

- **Data:** `Wed Sep 02 04:18:52 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2095003500992503835)
- **Rodzaj:** Komentarz w dyskusji (@petergyang)
- **Powiązane pojęcia:** [[Harness|Hill climbing agenta]] [[Eval Set z realnych sesji|Zbiór ewaluacyjny (eval set)]] [[Harness|Przykłady pozytywne i negatywne]] [[Prompt Architecture|Iteracyjna optymalizacja promptu]] [[Harness|Few-shot examples]]

**Kontekst / Problem:**
Odpowiedź w dyskusji pod wpisem @petergyang. Autor odpowiada na wcześniejszą wymianę zdań i przechodzi do konkretnej rady praktycznej: gdy chce się iteracyjnie poprawiać (hill climb) zachowanie agenta, kluczowe jest szybkie zebranie niewielkiego, ale reprezentatywnego zestawu przykładów — zarówno pozytywnych (poprawne zachowanie), jak i negatywnych (błędy). Taki zbiór stanowi sygnał doboru dla kolejnych iteracji promptu, narzędzi i logiki agenta.

**Rada inżynierska:**
Zbierz możliwie szybko około 10 przykładów pozytywnych i negatywnych (pos/neg) — to wystarczający startowy sygnał, by agent mógł 'hill climbować', czyli iteracyjnie poprawiać swoje wyniki. Więcej przykładów jest lepsze, ale ich liczba powinna być proporcjonalna do krytyczności zadania: im bardziej krytyczny przypadek użycia, tym większy i staranniejszy zbiór przykładów należy zgromadzić przed dalszą optymalizacją.

**Uwaga / Anty-wzorzec:**
Czekanie z iteracją na 'idealny' lub bardzo duży zbiór danych zamiast wystartować z ~10 przykładami — opóźnia pętlę sprzężenia zwrotnego. Z drugiej strony bagatelizowanie krytyczności zadania i poprzestanie na zbyt małej próbce przy zastosowaniach wysokiego ryzyka.

> **Cytat:** *"@petergyang I’m just giving you a hard time.  If you can collect ~10 pos/neg examples quickly it will help your agent hill climb it 

The more the better but depends how critical it is"*

---

## Architektura agentów i protokoły kontekstu (MCP / WebMCP)

### WebMCP: współpraca agentów i ludzi w interfejsie UI oraz notatniki oparte na plikach Markdown

- **Data:** `Wed Aug 26 15:03:00 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2092628886572200169)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|WebMCP]] [[Harness|Model Context Protocol (MCP)]] [[Harness|Agent kodujący]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Ewaluacja modeli foundation]] [[Harness|Runbook]] [[Harness|Markdown jako format artefaktów]] [[Harness|Współpraca człowiek-agent]]

**Kontekst / Problem:**
Omówienie nowego wpisu OpenAI o budowaniu z WebMCP — protokołem, w którym narzędzia są eksponowane bezpośrednio przez przeglądarkę, a nie przez API lub klasyczne serwery MCP. Główny scenariusz to sytuacje, w których agent i człowiek muszą współpracować nad tym samym interfejsem (np. wspólna edycja komórek notatnika). Autorzy pokazują też nowy typ notatnika zgodny z WebMCP, nastawiony na 'spotkanie użytkownika tam, gdzie jest': użytkownik przynosi własnego agenta kodującego, a artefakty to zwykłe pliki Markdown. Notatnik służy do kuratorowania runbooków i wysokiej jakości przykładów uruchamiania ewaluacji modeli foundation na własnej infrastrukturze, bo wymaga interaktywnego majstrowania przy stanie długotrwałych zadań z jednoczesnym notowaniem. Projekt jest open source.

**Rada inżynierska:**
Gdy zadanie wymaga interaktywnej, wspólnej pracy człowieka i agenta nad żywym stanem (komórki notatnika, długotrwałe joby, runbooki ewaluacyjne), rozważ wystawienie narzędzi przez WebMCP bezpośrednio w przeglądarce zamiast przez API lub MCP — ale najpierw przeanalizuj tradeoffy opisane we wpisie. Utrzymuj artefakty jako czyste pliki Markdown i pozwól użytkownikowi podłączyć własnego agenta kodującego: obniża to koszt integracji i pozwala agentowi działać na tym samym interfejsie, którego używa człowiek.

**Uwaga / Anty-wzorzec:**
Traktowanie WebMCP jako zamiennika API lub klasycznych serwerów MCP. To inny kanał ekspozycji narzędzi (przeglądarka), z własnym zestawem kompromisów — nie jest domyślnym wyborem dla każdego przypadku integracji. Drugi anty-wzorzec: budowanie interfejsów wymuszających migrację użytkownika zamiast 'meet people where they are' (własny agent, własne pliki).

> **Cytat:** *"1) Shows an example of building with WebMCP, meant for when you want agents and and humans to collaborate on using a UI (like co-editing notebook cells). It's different than MCPs or APIs in that its exposed directly through the browser. Read the post for discussion of the tradeoffs. 2) They created a new kind of notebook which works with WebMCP that prioritizes meeting people where they are: you bring your own coding agent and files are just markdown. The author uses it to curate runbooks or high quality examples of how to run foundation model evals on their infrastructure."*

---

## Ewaluacja AI / Metodologia eksperymentów

### Ewaluacja produktów AI wymaga metodologii data science, nie deterministycznych testów

- **Data:** `Sat Aug 29 20:20:55 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2093796057063006529)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Ewaluacja modeli AI]] [[Harness|Stochastyczność wyjść modeli]] [[Harness|Projektowanie eksperymentów]] [[Harness|Testowanie hipotez]] [[Harness|Data Science w AI]]

**Kontekst / Problem:**
Hamel odpowiada na narzekania („rage bait”), że data science rzekomo nie jest potrzebne w erze LLM. Argumentuje, że właśnie DS — statystyka, projektowanie eksperymentów, testowanie hipotez — jest niezbędne, gdyż wyjścia modeli AI są tekstowe, zaszumione i stochastyczne. Problem: jak mierzyć, czy produkt AI działa, skoro nie ma deterministycznych, binarnych wyników.

**Rada inżynierska:**
Ewaluację produktów AI należy prowadzić metodami Data Science: projektować eksperymenty i testować hipotezy odporne na szum oraz stochastyczność wyjść. Nie oceniaj modelu na podstawie pojedynczych wyjść — mierz rozkłady, kontroluj wariancję i buduj metryki odporne na szum. Umiejętność wnioskowania statystycznego (DS) jest kluczowa przy ocenie produktów AI, gdzie wyjściem jest tekst.

**Uwaga / Anty-wzorzec:**
Ocenianie produktu AI na podstawie pojedynczych, przykładowych wyjść tekstowych bez uwzględnienia wariancji i szumu — prowadzi do fałszywych wniosków o działaniu systemu.

> **Cytat:** *"Don't fall for this rage bait 😅

DS gives you the tools and judgement to make sense of noisy signals and stochastic outputs 

For AI -> lets you measure if an AI product is working even though the outputs are text. 

You have to design experiments and test hypothesis that account for noisy signals."*

---

## Architektura systemów ML / routing i kaskady modeli

### Kaskada modeli (model cascade) nie zakłada kalibracji log-prob — wymaga najpierw analizy statystycznej progu

- **Data:** `Sat Aug 15 18:07:27 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2088689040027775300)
- **Rodzaj:** Komentarz w dyskusji (@ThePeshwa)
- **Powiązane pojęcia:** [[Kaskady Modeli i Routing Pewności|Model cascade]] [[Harness|Kalibracja log-probabilities]] [[Harness|Proxy score]] [[Harness|Threshold tuning]] [[Kaskady Modeli i Routing Pewności|Routing modeli]] [[Harness|Ewaluacja na własnym datasecie]] [[Harness|LLM-as-a-judge]]

**Kontekst / Problem:**
Wymiana zdań pod wpisem @ThePeshwa, który zarzucił technice kaskady modeli, że opiera się na (zwykle błędnym) założeniu o kalibracji log-prawdopodobieństw modelu. Hamel Husain odpiera zarzut: kaskada nie zakłada niczego o kalibracji, lecz zakłada wykonanie analizy statystycznej na własnym datasecie PRZED ustaleniem progu decyzyjnego. Problem praktyczny: jak tanio routować ruch między tanim i drogim modelem (lub między klasyfikatorem a LLM) i jak zweryfikować, czy sygnał proxy w ogóle nadaje się do wyznaczenia progu.

**Rada inżynierska:**
Traktuj kaskadę modeli jako procedurę eksperymentalną, nie jako gotowy wzór: (1) najpierw zmierz rozkład proxy score (np. log-prob, pewność klasyfikatora, score z mniejszego modelu) na własnym, reprezentatywnym datasecie; (2) dopiero potem szukaj progu, przy którym tani model przejmuje większość przypadków bez utraty jakości; (3) jeśli proxy score jest zbyt szumny, poprawnym wynikiem eksperymentu jest brak progu — odrzucenie techniki i przejście dalej. Dla zadań klasyfikacyjnych próba jest tania i łatwo weryfikowalna nawet przy szumie, więc próg opłaca się sprawdzić empirycznie zamiast dyskutować o założeniach teoretycznych. Zawsze zadaj pytanie: czy ten konkretny sygnał jest godny zaufania dla tego konkretnego datasetu?

**Uwaga / Anty-wzorzec:**
Dwie symetryczne pułapki: (a) odrzucanie kaskady „na papierze” argumentem o niekalibrowanych log-prob, bez przeprowadzenia własnej analizy statystycznej; (b) wdrożenie kaskady z arbitralnie przyjętym progiem (np. 0.9) bez walidacji na własnych danych — przy szumym proxy score prowadzi to do cichej utraty jakości na przypadkach przekazanych tanemu modelowi.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Sprzeczność z szeroko powtarzanym konsensusem branżowym, że kaskady modeli i routing oparty na log-prob są zawodne, bo modele LLM są źle skalibrowane. Hamel Husain twierdzi, że to zarzut nieistotny: metoda nie zakłada kalibracji, lecz wymaga uprzedniej analizy statystycznej sygnału na konkretnym datasecie, a brak znalezienia progu jest akceptowalnym, przewidzianym w pracy wynikiem. Do rozstrzygnięcia: w jakim zakresie niekalibrowane log-prob rzeczywiście dyskwalifikują kaskadę, a w jakim wystarczy empiryczna walidacja progu (szczególnie dla zadań klasyfikacyjnych, gdzie test jest tani i weryfikowalny).

> **Cytat:** *"The model cascade technique doesn't assume anything about the calibration of log probabilities! Quite the opposite, the technique relies upon you doing statistical analysis **first** before committing to a threshold. The paper even discusses the possibility that you may not find a threshold if the proxy score is too noisy. You have to put your machine learning hat on. Can you trust the signal for this specific dataset? Great! If not, also great, and move on. However, for classification the technique is cheap to try and easy to verify, even in the presence of noise."*

---

## Ewaluacja i systemy agentowe

### Plugin eval skills: skill odkrywania błędów i inteligentne próbkowanie trace'ów

- **Data:** `Mon Aug 17 19:47:25 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2089438973714440196)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Ewaluacja modeli]] [[Harness|Failure modes]] [[Harness|Inteligentne próbkowanie]] [[Harness|Adnotacja danych]] [[Harness|Systemy agentowe]] [[Harness|Trace'y]] [[Kaskady Modeli i Routing Pewności|Routing workflow]]

**Kontekst / Problem:**
Autor wraz z @sh_reya rozwijają plugin 'eval skills' dla agentów kodujących. Problem: ręczna analiza dużych zbiorów wyjść modelu lub trace'ów jest kosztowna i nieustrukturyzowana. Nowa wersja wprowadza skill odkrywania błędów (error-discovery), który na podstawie pliku z wyjściami AI lub trace'ami buduje dedykowaną aplikację do przeglądu z inteligentnym próbkowaniem, oraz skill startowy (start), który rozpoznaje sytuację użytkownika i kieruje agenta do właściwego workflow (znajdowanie błędów w trace'ach lub audyt istniejącego pipeline'u ewaluacji).

**Rada inżynierska:**
Zamiast ręcznie przeglądać całe zbiory trace'ów, deleguj agentowi budowę dedykowanej aplikacji do adnotacji z inteligentnym próbkowaniem: podczas gdy człowiek annotuje próbkę, agent grupuje notatki w tryby awarii (failure modes) i automatycznie wyszukuje powiązane przykłady. Dodaj też warstwę routingu (skill startowy), która na podstawie kontekstu użytkownika wybiera właściwy workflow — odkrywanie błędów vs. audyt istniejącego pipeline'u ewaluacji.

**Uwaga / Anty-wzorzec:**
Analiza wyjść modelu bez strukturyzacji: brak inteligentnego próbkowania i grupowania w failure modes prowadzi do przeglądania przypadków losowo, pomijania klas błędów i marnowania czasu na adnotację nieinformacyjnych przykładów.

> **Cytat:** *"The biggest change is a new error-discovery skill. Give your coding agent a file of AI outputs or traces, and it builds a custom review app w/intelligent sampling. As you annotate the sample, the agent groups your notes into failure modes and finds related examples. We also added a start skill, which looks at your situation and routes your agent to the right workflow. It can help you find errors in a set of traces or audit an eval pipeline you already have."*

---
