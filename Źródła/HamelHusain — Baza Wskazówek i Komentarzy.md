---
autor: "@HamelHusain"
źródło: "https://x.com/HamelHusain"
wygenerowano: 2026-09-23 01:56
typ: synteza-wiedzy
tagi:
  - hamelhusain
  - ai-engineering
  - prompt-engineering
  - twitter-extract
---

# @HamelHusain — Baza Wskazówek i Komentarzy

> Destylacja praktycznych porad, heurystyk inżynierskich i komentarzy technicznych z profilu @HamelHusain na platformie X. Wyciągnięto 5 wartościowych wpisów.

## Spis kategorii

- [Ewaluacja i doskonalenie agentów](#ewaluacja-i-doskonalenie-agentów) (1)
- [Architektura agentów / Harness i interfejsy](#architektura-agentów--harness-i-interfejsy) (1)
- [Ewaluacja AI / Metodologia](#ewaluacja-ai--metodologia) (1)
- [Architektura modeli / Routing i kaskady](#architektura-modeli--routing-i-kaskady) (1)
- [Ewaluacja i weryfikacja (evals / error discovery)](#ewaluacja-i-weryfikacja-(evals--error-discovery)) (1)

---

## Ewaluacja i doskonalenie agentów

### Szybkie zbieranie ~10 przykładów pos/neg przyspiesza hill climbing agenta

- **Data:** `Wed Sep 02 04:18:52 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2095003500992503835)
- **Rodzaj:** Komentarz w dyskusji (@petergyang)
- **Powiązane pojęcia:** [[Harness|Hill climbing agenta]] [[Harness|Ewaluacja agentów]] [[Harness|Przykłady pozytywne i negatywne]] [[Harness|Iteracyjne doskonalenie promptu]] [[Harness|Few-shot examples]]

**Kontekst / Problem:**
Odpowiedź Kuna Chena w wątku pod wpisem @petergyang; brak treści posta nadrzędnego. Kontekst dotyczy sposobu poprawiania jakości agenta. Kun łagodzi wcześniejszy ton i doradza praktyczne podejście: szybko zebrać kilkanaście przykładów pozytywnych i negatywnych, aby agent mógł iteracyjnie się wspinać (hill climb). Podkreśla, że liczba przykładów zależy od tego, jak krytyczne jest zadanie.

**Rada inżynierska:**
Aby agent skutecznie się poprawiał, zbierz szybko około 10 przykładów pozytywnych i negatywnych — to wystarczy, by uruchomić pętlę hill climbing. Więcej przykładów jest lepsze, ale ich liczbę dobieraj do krytyczności zadania; nie blokuj iteracji brakiem dużego, idealnego zbioru.

**Uwaga / Anty-wzorzec:**
Czekanie na duży, idealnie zbalansowany zbiór danych przed rozpoczęciem iteracyjnego doskonalenia agenta. Traktowanie liczby przykładów jako celu samego w sobie zamiast zależności od krytyczności zadania.

> **Cytat:** *"@petergyang I’m just giving you a hard time.  If you can collect ~10 pos/neg examples quickly it will help your agent hill climb it 

The more the better but depends how critical it is"*

---

## Architektura agentów / Harness i interfejsy

### WebMCP i notebooki agentowe: współpraca człowieka i agenta na wspólnym UI (markdown + BYO coding agent)

- **Data:** `Wed Aug 26 15:03:00 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2092628886572200169)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|WebMCP]] [[Harness|MCP]] [[Harness|Human-in-the-loop]] [[Harness|Markdown jako źródło prawdy]] [[Notebook agentowy]] [[Harness|Runbook]] [[Harness|Ewaluacja modeli foundation]] [[Harness|Long-running jobs]]

**Kontekst / Problem:**
Kun Chen omawia nowy wpis blogowy OpenAI (autor: Jeremy Lewi) pokazujący praktyczne budowanie z WebMCP — protokołem wystawiającym narzędzia bezpośrednio przez przeglądarkę, przeznaczonym do scenariuszy, w których agent i człowiek współpracują na tym samym UI (np. wspólna edycja komórek notebooka). To odróżnia WebMCP od MCP i zwykłych API, które nie są projektowane pod równoległą, interaktywną obecność człowieka w tym samym interfejsie. Drugi wątek to nowy typ notebooka: pliki są po prostu markdownem, a użytkownik przyprowadza własnego coding agenta — co obniża koszt adopcji i pozwala trzymać artefakty w formacie czytelnym dla człowieka i agenta. Zastosowanie: kuratorowanie runbooków i wysokiej jakości przykładów ewaluacji modeli foundation na własnej infrastrukturze, gdzie trzeba interaktywnie dłubać przy stanie długo działających zadań i jednocześnie robić notatki inline.

**Rada inżynierska:**
Gdy agent i człowiek mają pracować nad tym samym artefaktem równolegle, wybieraj warstwę integracji dopasowaną do trybu współpracy: WebMCP (eksponowany wprost przez przeglądarkę) do wspólnej, interaktywnej pracy na UI, MCP/API do wywołań bezstanowych i wsadowych. Projektuj artefakty pracy (notebooki, runbooki) jako czysty markdown i pozwól użytkownikowi przyprowadzić własnego coding agenta — to 'meeting people where they are' redukuje vendor lock-in i utrzymuje kontekst edytowalny zarówno przez człowieka, jak i model. Notebook jest właściwym formatem, gdy trzeba iterować nad stanem długo działających zadań i notować inline; runbooki i przykłady ewaluacji modeli to naturalny zastosowanie.

**Uwaga / Anty-wzorzec:**
Traktowanie MCP/API i WebMCP jako zamienników — pierwsze nie są projektowane pod współdzielony, interaktywny UI z człowiekiem w pętli; wybór złej warstwy kończy się albo nadmiarową złożonością, albo brakiem możliwości współedycji. Drugi anty-wzorzec: zamykanie artefaktów wiedzy (runbooki, evale) w formacie własnościowym zamiast markdownu, co blokuje 'bring your own agent'.

> **Cytat:** *"Shows an example of building with WebMCP, meant for when you want agents and and humans to collaborate on using a UI (like co-editing notebook cells). It's different than MCPs or APIs in that its exposed directly through the browser. ... They created a new kind of notebook which works with WebMCP that prioritizes meeting people where they are: you bring your own coding agent and files are just markdown."*

---

## Ewaluacja AI / Metodologia

### Data Science jako fundament ewaluacji produktów AI o stochastycznych wyjściach

- **Data:** `Sat Aug 29 20:20:55 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2093796057063006529)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Ewaluacja AI]] [[Harness|Stochastyczne wyjścia modeli]] [[Harness|Noisy Signals]] [[Harness|Data Science]] [[Harness|Projektowanie eksperymentów]] [[Harness|Testowanie hipotez]]

**Kontekst / Problem:**
Kun Chen odpowiada na wpis Hamela Husaina, który (jak sugeruje Kun) jest 'rage baitem' deprecjonującym Data Science. Kontekst: dyskusja o tym, czy tradycyjne metody DS mają zastosowanie w erze AI, gdzie wyjścia modeli są tekstowe, zaszumione i niedeterministyczne. Kun prostuje błąd myślenia, że DS jest nieprzydatne dla AI.

**Rada inżynierska:**
Traktuj Data Science jako zestaw narzędzi i osądu do pracy z zaszumionymi sygnałami i stochastycznymi wyjściami. W produktach AI, gdzie output jest tekstem (a więc niedeterministyczny), nie da się ocenić 'czy działa' za pomocą prostych asercji — trzeba projektować eksperymenty i testować hipotezy, które explicite uwzględniają szum w sygnale. To jest właściwa metodologia ewaluacji AI, a nie porzucenie DS.

**Uwaga / Anty-wzorzec:**
Uleganie narracji (rage bait), że Data Science jest zbędna w erze AI. Drugi anty-wzorzec: ocenianie produktu AI tak, jakby jego wyjścia były deterministyczne — bez uwzględnienia wariancji i szumu w wynikach tekstowych.

> **Cytat:** *"Don't fall for this rage bait 😅 DS gives you the tools and judgement to make sense of noisy signals and stochastic outputs. For AI -> lets you measure if an AI product is working even though the outputs are text. You have to design experiments and test hypothesis that account for noisy signals."*

---

## Architektura modeli / Routing i kaskady

### Model cascade nie zakłada kalibracji log-probabilities — wymaga najpierw analizy statystycznej progu

- **Data:** `Sat Aug 15 18:07:27 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2088689040027775300)
- **Rodzaj:** Komentarz w dyskusji (@ThePeshwa)
- **Powiązane pojęcia:** [[Harness|Model Cascade]] [[Harness|Proxy Score]] [[Harness|Kalibracja log-probabilities]] [[Jev|Routing modeli]] [[Harness|Weryfikacja statystyczna sygnału]] [[Harness|Threshold tuning]]

**Kontekst / Problem:**
Kun Chen odpowiada @ThePeshwa, który twierdził, że technika model cascade opiera się na założeniu o kalibracji log-probabilities. Kun prostuje to nieporozumienie: kaskada nie zakłada niczego o kalibracji — wręcz przeciwnie, wymaga przeprowadzenia analizy statystycznej proxy score PRZED ustaleniem progu decyzyjnego. Paper omawia nawet scenariusz, w którym progu nie da się w ogóle znaleźć, jeśli proxy score jest zbyt zaszumiony. Kontekst: routing tanich vs drogich modeli na podstawie sygnału pewności.

**Rada inżynierska:**
Traktuj model cascade jako eksperyment ML, nie jako gotową regułę: (1) najpierw zbierz dane i sprawdź statystycznie, czy proxy score (np. log-prob, confidence) koreluje z poprawnością odpowiedzi na TWOIM datasecie; (2) dopiero potem ustal próg przełączania między tanim a drogim modelem; (3) jeśli sygnał jest zbyt zaszumiony i progu nie da się wyznaczyć — to też jest poprawny wynik, odpuść technikę. Dla zadań klasyfikacyjnych kaskada jest tania w wypróbowaniu i łatwa w weryfikacji nawet przy szumie, więc warto ją testować empirycznie zamiast odrzucać a priori.

**Uwaga / Anty-wzorzec:**
Błędne założenie, że kaskada wymaga idealnie skalibrowanych log-probabilities, prowadzi do przedwczesnego odrzucenia techniki. Odwrotny anty-wzorzec: wdrażanie kaskady bez uprzedniej walidacji statystycznej sygnału na własnym datasecie — kopiowanie progu z papera bez sprawdzenia, czy proxy score w ogóle jest informatywny dla danego rozkładu danych.

> **Cytat:** *"The model cascade technique doesn't assume anything about the calibration of log probabilities! Quite the opposite, the technique relies upon you doing statistical analysis **first** before committing to a threshold. The paper even discusses the possibility that you may not find a threshold if the proxy score is too noisy. You have to put your machine learning hat on. Can you trust the signal for this specific dataset? Great! If not, also great, and move on. However, for classification the technique is cheap to try and easy to verify, even in the presence of noise."*

---

## Ewaluacja i weryfikacja (evals / error discovery)

### Eval skills plugin: skill do odkrywania błędów z inteligentnym próbkowaniem i grupowaniem w tryby awarii

- **Data:** `Mon Aug 17 19:47:25 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2089438973714440196)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Eval Set z realnych sesji|Evals]] [[Harness|Failure modes]] [[Harness|Intelligent sampling]] [[Harness|Error discovery]] [[Harness|Trace analysis]] [[Harness|LLM-as-judge]] [[Agent skills]] [[Harness|Human annotation]]

**Kontekst / Problem:**
Kun Chen wraz z Shreyą Shankar rozwijają plugin 'eval skills' dla agentów kodujących. Po serii iteracji dodali dwa nowe skille: (1) error-discovery — agent dostaje plik z wynikami AI lub trace'ami, buduje dedykowaną aplikację do przeglądu (review app) z inteligentnym próbkowaniem; gdy człowiek annotuje próbkę, agent grupuje notatki w tryby awarii (failure modes) i dociąga powiązane przykłady; (2) start — rozpoznaje sytuację użytkownika i kieruje agenta do właściwego workflow (znajdowanie błędów w zestawie trace'ów albo audyt istniejącego pipeline'u ewaluacyjnego). Problem, który to rozwiązuje: ręczne przeglądanie setek trace'ów i ręczne kategoryzowanie błędów nie skaluje się, a ewaluacje często są budowane bez realnego zrozumienia, jakie błędy faktycznie występują w produkcji.

**Rada inżynierska:**
Nie zaczynaj od metryk ani od pisania sędziów (LLM-as-judge) — zacznij od odkrywania błędów. Wrzuć agentowi plik trace'ów/wyników i pozwól mu zbudować customową aplikację do przeglądu z inteligentnym próbkowaniem, a następnie annotuj próbkę: agent zamieni Twoje notatki na taksonomię failure modes i sam dociągnie podobne przykłady. Dopiero z tej taksonomii wyprowadzaj metryki i weryfikatory. Używaj skilla 'start', żeby agent najpierw rozpoznał Twoją sytuację (szukanie błędów w trace'ach vs. audyt istniejącego pipeline'u eval) i wybrał właściwy workflow, zamiast zgadywać podejście od zera.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: budowanie ewaluacji 'z góry' — wymyślanie metryk i kryteriów bez wcześniejszego przejrzenia realnych trace'ów, co prowadzi do mierzenia rzeczy, które nie mają związku z faktycznymi awariami. Druga pułapka: ręczna, niesystematyczna annotacja bez próbkowania i grupowania — nie skaluje się i nie daje powtarzalnej taksonomii failure modes.

> **Cytat:** *"The biggest change is a new error-discovery skill. Give your coding agent a file of AI outputs or traces, and it builds a custom review app w/intelligent sampling. As you annotate the sample, the agent groups your notes into failure modes and finds related examples. We also added a start skill, which looks at your situation and routes your agent to the right workflow."*

---
