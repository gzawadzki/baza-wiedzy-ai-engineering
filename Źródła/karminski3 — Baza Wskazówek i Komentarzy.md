---
autor: "@karminski3"
źródło: "https://x.com/karminski3"
wygenerowano: "2026-09-23 02:16"
typ: synteza-wiedzy
tagi:
  - karminski3
  - ai-engineering
  - prompt-engineering
  - twitter-extract
---

# @karminski3 — Baza Wskazówek i Komentarzy

> Destylacja praktycznych porad, heurystyk inżynierskich i komentarzy technicznych z profilu @karminski3 na platformie X. Wyciągnięto 29 wartościowych wpisów.

## ⚠️ Kwestie sporne i rozbieżności do rozstrzygnięcia

> Wpisy, w których autor podważa powszechne przekonania branżowe lub prezentuje tezy stojące w sprzeczności z innymi praktykami:

- **[Identyfikacja kwantyzacji i destylacji modelu przez odcisk zachowania: Claude Opus 5.5 vs fable 5.1](https://x.com/karminski3/status/2102479290420048093):** Autor podważa dwa powszechne założenia branżowe: (1) że nowe wersje modeli (Opus 5.5) to nowe architektury — twierdzi, że to kwantyzacja lub wewnętrzna destylacja fable 5.1, co jest tezą kontrowersyjną i weryfikowalną jedynie przez porównanie wag/odcisków zachowania; (2) odwrócona intuicja skalowania — większe zużycie tokenów rozumowania interpretuje jako dowód na MNIEJSZY model (wymiana długości rozumowania za rozmiar), co stoi w sprzeczności z narracją producentów o 'coraz większych i mądrzejszych' modelach. Dodatkowo teza o 'rodzinnym' (祖传) cichym osłabianiu modeli przez Anthropic jest zarzutem wobec konsensusu, że wersje produkcyjne nie degradują względem wersji testowych.
- **[Krytyka parametru reasoning_effort jako narzędzia przenoszenia ryzyka kosztowego na użytkownika](https://x.com/karminski3/status/2099767043155218568):** Autor podważa powszechny konsensus, że parametr reasoning_effort to użyteczne narzędzie do optymalizacji kosztu. Twierdzi, że jest to głównie mechanizm marketingowy i przenoszenie ryzyka kosztowego na użytkownika. Dodatkowo kwestionuje założenie 'high = optimum' — mimo że dokumentacja DeepSeek-v4-1-flash sama opisuje max jako 'best reserved for the most challenging tasks'. Wnioski te stoją w sprzeczności z dominującą praktyką rekomendowania niższych poziomów effort dla typowych zadań. Do dalszego rozstrzygnięcia: czy przy obecnym stanie post-trainingu wyższy effort rzeczywiście monotonnicznie przekłada się na wyższą jakość, czy też istnieje realne plateau/regresja.
- **[reasoning_effort jako narzędzie marketingowe: pułapka nierównego benchmarku i przenoszenia kosztu obliczeń na użytkownika](https://x.com/karminski3/status/2099767018279084387):** Autor podważa powszechny konsensus branżowy, że reasoning_effort to użyteczna funkcja dająca użytkownikowi kontrolę. Twierdzi, że jest to w istocie marketing i transfer ryzyka kosztowego na użytkownika. Dodatkowo twierdzi, że thinking effort powinien być równoważny z performance, a obecna rozbieżność to wina post-trainingu — co jest tezą kontrowersyjną wobec praktyki traktowania wyższego reasoning_effort jako automatycznie lepszego. Do rozstrzygnięcia: czy reasoning_effort to realna dźwignia jakości, czy mechanizm komercjalizacji kosztu obliczeń.
- **[System Scaling kontra skalowanie parametrów: agentowa pętla feedbacku środowiskowego jako klucz do wdrożeń inżynierskich](https://x.com/karminski3/status/2092894849619874210):** Autor podważa dominujący w branży nacisk na 'scale is all you need' (wyścig o liczbę parametrów) i przekłada akcent na inżynierię systemową (System Scaling). Do rozstrzygnięcia: czy przyrost możliwości wynika głównie z rozmiaru modelu, czy z architektury harnessu i pętli weryfikacji w środowisku — oraz czy pojedynczy, szybki sukces (konfiguracja firewalla w 10 min) jest wystarczającym dowodem przewagi podejścia systemowego.
- **[Harness Scaling: skalowanie orkiestracji agentów zamiast samych parametrów modelu](https://x.com/karminski3/status/2092894843429363871):** Teza kontrowersyjna względem dominującego konsensusu branżowego (scaling laws): autor twierdzi, że zwiększanie liczby parametrów modelu podnosi wyłącznie 'inteligencję', a realną zdolność wykonawczą ('pracę') daje dopiero skalowanie harnessu — frameworku, narzędzi i roju agentów. Do rozstrzygnięcia: czy inwestycja w orkiestrację/sandbox przewyższa inwestycję w scaling modelu dla zadań długokontekstowych oraz czy równoległość async faktycznie eliminuje problem attention dilution, czy tylko go maskuje przez dekompozycję zadań i pre-filtrację danych skryptami.
- **[Agent Apodex 1.1 analizuje 1,2 mln linii logów i generuje reguły firewalla dla realnego ataku](https://x.com/karminski3/status/2092894838492655713):** Teza stoi w napięciu z dominującym konsensusem inżynierskim, że LLM nie nadają się do bezpośredniej analizy surowych logów o dużej objętości — standardem jest deterministyczny parsing, normalizacja i reguły korelacji w SIEM, a model pełni co najwyżej rolę asystenta w triage'u. Autor twierdzi, że agent przeszedł cały łańcuch (1,2 mln linii → identyfikacja technik ataku → reguły firewalla) end-to-end. Do rozstrzygnięcia pozostaje: (a) czy model faktycznie przetwarzał surowe dane, czy tylko wyniki zapytań narzędziowych nad spakowanym zbiorem — co zmienia sens tezy z 'model analizuje logi' na 'harness analizuje logi, model orkiestruje'; (b) jaka była precyzja/recall wykrytych ataków i czy reguły firewalla zostały zweryfikowane na odłożonym zbiorze testowym; (c) brak niezależnej reprodukcji — wpis ma charakter demonstracyjno-promocyjny dla Apodex 1.1 i AgentOS.
- **[Jev (System-1) vs czysty generator liczb losowych w labiryncie: klęska w planowaniu wielokrokowym](https://x.com/karminski3/status/2101941770003361893):** Autor podważa dominujący konsensus branżowy, że wyspecjalizowane modele typu System-1 (jak Jev) można stosować do zadań wymagających planowania wielokrokowego. Teza kontrowersyjna: w zadaniach planistycznych czysty generator liczb losowych (System-1) potrafi systemowo pobić inteligentny model decyzyjny, co stoi w sprzeczności z powszechnym założeniem o wyższości modeli decyzyjnych nad losowymi baseline'ami.
- **[Odwrócone skalowanie wysiłku rozumowania: dlaczego tryb „max” psuje wyniki SWE i czym jest kompresja informacji w modelach SOTA](https://x.com/karminski3/status/2099426676669366337):** Autor podważa dominujący konsensus branżowy, że zwiększanie budżetu rozumowania (reasoning effort = max, dłuższe chain-of-thought) monotonicznie poprawia jakość. Twierdzi, że na SWE-bench występuje inwersja (wyniki przy „max” są gorsze), a prawdziwym wyznacznikiem SOTA jest minimalizacja tokenów przy maksymalnej trudności zadania (model jako „perfekcyjny kompresor informacji”). Do rozstrzygnięcia: (a) czy odwrócenie jest artefaktem konkretnego benchmarku/harnessu i konkretnej rodziny modeli, czy zjawiskiem ogólnym; (b) jaki mechanizm zatrzymywania rozumowania (kryterium stopu, weryfikator zewnętrzny, sygnał pewności) daje najlepszy kompromis jakość/koszt; (c) czy teza o „kompresji informacji” jest falsyfikowalną metryką, czy tylko metaforą.
- **[Dlaczego ustawienie maksymalnego budżetu rozumowania (max effort) psuje wyniki SWE-bench i kiedy model powinien przestać myśleć](https://x.com/karminski3/status/2099421138069950509):** Teza autora stoi w sprzeczności z dominującą narracją branżową o skalowaniu test-time compute ('im dłużej model myśli, tym lepiej'). Autor twierdzi, że maksymalny budżet rozumowania powoduje odwrócenie wyników (regresję) na SWE-bench, a miarą jakości nie jest długość reasoning, lecz kompresja informacji — minimalny koszt tokenowy dla najtrudniejszego problemu. Do rozstrzygnięcia: czy regresja 'max' wynika z przetrenowania/overthinking danego modelu, czy jest to uniwersalne prawo, oraz jaki jest optymalny mechanizm zatrzymania rozumowania.
- **[Intensywność rozumowania (thinking budget) a wyniki modelu — więcej myślenia = wyższa skuteczność](https://x.com/karminski3/status/2099396323942547519):** Spór z tezą części społeczności (tzw. 'DS民科'), że ustawienie intensywności rozumowania na 'high' jest lepsze niż 'max' oraz że przełącznik intensywności myślenia nie wpływa na wydajność. Autor odrzuca ten pogląd, powołując się na DeepSeek-R1-Zero (wzrost AIME24 z 15% do 71% wraz z długością rozumowania). Do rozstrzygnięcia: czy istnieją warunki (np. przesycenie/overthinking, dryf, koszt latencji), w których nadmierny budżet myślenia szkodzi wynikom — warto zweryfikować empirycznie dla konkretnych modeli i zadań.
- **[Stabilność vs SOTA w agentowym kodowaniu backendu: benchmark implementacji bazy wektorowej](https://x.com/karminski3/status/2099375198986461418):** Autor podważa proste podejście „wybieraj model SOTA z leaderboardu”. W jego benchmarku Fable-5.1 ma najwyższy szczytowy wynik, ale jednocześnie bardzo dużą wariancję między próbami, przez co w praktyce bardziej opłacalny bywa stabilniejszy GPT6-Astra lub tańszy DeepSeek-V4.1-Flash. To kontrastuje z typowym optymizmem benchmarkowym, gdzie liczy się głównie maksymalny wynik, a nie powtarzalność.

---

## Spis kategorii

- [Obserwacje zachowania modeli / Benchmarking / Architektura promptów](#obserwacje-zachowania-modeli--benchmarking--architektura-promptów) (1)
- [Systemy agentowe / Inżynieria harnessu](#systemy-agentowe--inżynieria-harnessu) (1)
- [Benchmarking modeli i zachowanie agentów (Agentic Coding)](#benchmarking-modeli-i-zachowanie-agentów-(agentic-coding)) (1)
- [Modele i benchmarki](#modele-i-benchmarki) (1)
- [Benchmarking / Inżynieria promptów / Ekonomia inferencji](#benchmarking--inżynieria-promptów--ekonomia-inferencji) (1)
- [Benchmarking i ewaluacja modeli LLM](#benchmarking-i-ewaluacja-modeli-llm) (1)
- [Architektura modeli i optymalizacja inferencji](#architektura-modeli-i-optymalizacja-inferencji) (1)
- [Architektura modeli / Type-Safe AI](#architektura-modeli--type-safe-ai) (1)
- [Systemy agentowe / Agentic Engineering](#systemy-agentowe--agentic-engineering) (1)
- [Architektura systemów agentowych / Inżynieria kontekstu](#architektura-systemów-agentowych--inżynieria-kontekstu) (1)
- [Systemy agentowe / Bezpieczeństwo / Inżynieria kontekstu](#systemy-agentowe--bezpieczeństwo--inżynieria-kontekstu) (1)
- [Benchmarking / Ewaluacja modeli LLM](#benchmarking--ewaluacja-modeli-llm) (1)
- [Reverse engineering / AI Agent / Embedded (ARM Cortex-M)](#reverse-engineering--ai-agent--embedded-(arm-cortex-m)) (1)
- [Architektura systemów agentowych / Benchmarking i ocena modeli](#architektura-systemów-agentowych--benchmarking-i-ocena-modeli) (1)
- [Inne obserwacje](#inne-obserwacje) (1)
- [Architektura harnessów i systemów agentowych / Edge & Browser AI](#architektura-harnessów-i-systemów-agentowych--edge-&-browser-ai) (1)
- [Rozumowanie LLM / Test-time compute / Destylacja](#rozumowanie-llm--test-time-compute--destylacja) (1)
- [Zachowanie modeli / Test-time compute / Destylacja](#zachowanie-modeli--test-time-compute--destylacja) (1)
- [Inżynieria rozumowania / budżet tokenów / benchmarking agentowy](#inżynieria-rozumowania--budżet-tokenów--benchmarking-agentowy) (1)
- [Inżynieria rozumowania / konfiguracja modeli reasoning](#inżynieria-rozumowania--konfiguracja-modeli-reasoning) (1)
- [Zachowanie modeli / Test-time compute (scaling rozumowania)](#zachowanie-modeli--test-time-compute-(scaling-rozumowania)) (1)
- [Architektura skilli / systemy agentowe / metaprogramowanie](#architektura-skilli--systemy-agentowe--metaprogramowanie) (1)
- [Architektura agentowa / Prompt Architecture](#architektura-agentowa--prompt-architecture) (1)
- [Benchmarki LLM / Agentic Coding / Dobór modeli](#benchmarki-llm--agentic-coding--dobór-modeli) (1)
- [Benchmarking modeli / Systemy agentowe](#benchmarking-modeli--systemy-agentowe) (1)
- [Benchmarking i ewaluacja modeli](#benchmarking-i-ewaluacja-modeli) (1)
- [Multimodalne systemy agentowe / architektura harnessów](#multimodalne-systemy-agentowe--architektura-harnessów) (1)
- [Inżynieria kontekstu / Analiza wideo z LLM](#inżynieria-kontekstu--analiza-wideo-z-llm) (1)
- [Multimodalność / Inżynieria wejścia (Vision-Language)](#multimodalność--inżynieria-wejścia-(vision-language)) (1)

---

## Obserwacje zachowania modeli / Benchmarking / Architektura promptów

### Identyfikacja kwantyzacji i destylacji modelu przez odcisk zachowania: Claude Opus 5.5 vs fable 5.1

- **Data:** `Tue Sep 22 19:24:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2102479290420048093)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Kwantyzacja modeli]] [[Harness|Destylacja wiedzy]] [[Harness|Behavioral fingerprinting modeli]] [[Stabilność modeli i przestrzeganie promptu|Reasoning tokens]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Stabilność generacji / determinizmowość]] [[Harness|Degradacja modelu w produkcji]] [[Stabilność modeli i przestrzeganie promptu|Benchmarking LLM]] [[Harness|Testowanie modeli pod kątem UI/frontend]] [[Harness|Pułapka przeładowanego rozumowania]]

**Kontekst / Problem:**
Autor przeprowadził testy frontendowe (generowanie kodu UI) Claude Opus 5.5, porównując go z fable 5.1. Celem było ustalenie, czy nowy model to realnie nowa architektura, czy tylko skwantyzowana/destylowana wersja poprzednika, oraz ocena stabilności i kosztu rozumowania w warunkach produkcyjnych (terminal + web).

**Rada inżynierska:**
Traktuj zachowanie modelu jako 'odcisk palca' (behavioral fingerprint) do wykrywania kwantyzacji/destylacji: jeśli dwa modele generują niemal identyczne szczegóły implementacyjne przy tym samym prompcie, prawdopodobnie dzielą tę samą bazę wag. Mierz też stabilność przez wielokrotne próbkowanie (tu: 6/6 identyczna jakość = wysoka determinizmowość). Dodatkowo: rosnące zużycie tokenów rozumowania przy podobnej jakości wyjścia to sygnał mniejszego modelu kompensującego rozmiar dłuższym łańcuchem myślowym (reasoning-length-for-scale tradeoff) — przydatne przy szacowaniu kosztu i doborze modelu do zadania.

**Uwaga / Anty-wzorzec:**
Pułapka '雷霆大思考' (przeładowane rozumowanie): przy złożonych zadaniach (test z erupcją wulkanu) model potrafi zapętlić się w rozumowaniu i nie wyprodukować żadnego kodu — w terminalu i w przeglądarce, wielokrotnie. Anty-wzorzec: zakładanie, że więcej tokenów rozumowania = lepszy wynik; w praktyce prowadzi to do timeoutów, braku outputu i marnowania budżetu. Drugi anty-wzorzec: opieranie się wyłącznie na benchmarkach bez testu stabilności (抽卡) i bez monitorowania degradacji modelu w czasie (Anthropic '降智' — ciche osłabianie modeli w produkcji).

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor podważa dwa powszechne założenia branżowe: (1) że nowe wersje modeli (Opus 5.5) to nowe architektury — twierdzi, że to kwantyzacja lub wewnętrzna destylacja fable 5.1, co jest tezą kontrowersyjną i weryfikowalną jedynie przez porównanie wag/odcisków zachowania; (2) odwrócona intuicja skalowania — większe zużycie tokenów rozumowania interpretuje jako dowód na MNIEJSZY model (wymiana długości rozumowania za rozmiar), co stoi w sprzeczności z narracją producentów o 'coraz większych i mądrzejszych' modelach. Dodatkowo teza o 'rodzinnym' (祖传) cichym osłabianiu modeli przez Anthropic jest zarzutem wobec konsensusu, że wersje produkcyjne nie degradują względem wersji testowych.

> **Cytat:** *"我怀疑现在opus 5.5就是 fable 5.1 的量化版或者自家蒸馏版... 几乎看不出两个模型实现细节上的差别... 我测试时很明显 opus 5.5 的思考token消耗更多. 这意味着opus5.5模型会更小一些(用reasoning长度换性能). 这同样意味着会有雷霆大思考的情况... 结果都无法输出代码. 思考卡住了... 只要不降智, 就是好模型(但无奈Anthropic降智是祖传艺能...)."*

---

## Systemy agentowe / Inżynieria harnessu

### Problem przedwczesnego zatrzymania (early stopping) w Agentic Coding

- **Data:** `Tue Sep 22 16:41:16 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2102438087158858212)
- **Rodzaj:** Komentarz w dyskusji (@dreamli60679407)
- **Powiązane pojęcia:** [[Harness|Agentic Coding]] [[Harness|Early Stopping w agentach]] [[Harness|Harness agentowy]] [[Weryfikator|Zewnętrzny weryfikator]] [[Harness|Budżet iteracji]] [[Stabilność modeli i przestrzeganie promptu|Grupa kontrolna / benchmark modeli]]

**Kontekst / Problem:**
Autor komentuje wpis innego użytkownika, pytając o istnienie grupy kontrolnej (benchmarku porównawczego) dla innych modeli. Przy okazji dzieli się kluczową obserwacją z własnej pracy nad Agentic Coding: największym problemem nie jest jakość pojedynczej odpowiedzi, lecz skłonność modelu do przedwczesnego zakończenia pętli agentowej — model nie wykorzystuje dostępnego budżetu iteracji, mimo że mógłby poprawić wynik kolejnymi próbami.

**Rada inżynierska:**
W harnessach agentowych (Agentic Coding) należy jawnie przeciwdziałać przedwczesnemu zatrzymaniu: (1) wymuszać minimalny budżet iteracji w prompcie/system message, (2) stosować zewnętrzny weryfikator, który odrzuca wynik i wymusza kolejną próbę, dopóki kryteria nie są spełnione, (3) rozdzielać 'chęć zakończenia' modelu od faktycznego stanu zadania — decyzja o stopie powinna należeć do harnessu, nie do modelu. Warto też prowadzić grupy kontrolne (A/B) między modelami, aby zmierzyć, który model realnie wykorzystuje iteracje, a nie tylko deklaruje gotowość.

**Uwaga / Anty-wzorzec:**
Poleganie na wewnętrznej 'samoocenie' modelu co do gotowości zadania — modele mają tendencję do deklarowania ukończenia zbyt wcześnie (early stopping), przez co tracą dostępne iteracje i nie osiągają potencjalnie lepszego wyniku. Brak grupy kontrolnej/benchmarku uniemożliwia odróżnienie problemu modelu od problemu harnessu.

> **Cytat:** *"话说有对照组吗? 好奇其他模型能达到什么效果. 我这里AgenticCoding目前遇到最大的问题还是早停, 模型不是很愿意去用尽机会迭代."*

---

## Benchmarking modeli i zachowanie agentów (Agentic Coding)

### Testy MiMo-v2.6-Pro: HNSW M=16/M0=28, AVX-512, 464–900 tps oraz przedwczesne zatrzymanie agenta

- **Data:** `Tue Sep 22 16:00:37 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2102427860585841100)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Agentic Coding]] [[Harness|MiMo-v2.6-Pro]] [[Harness|MoE - Mixture of Experts]] [[Harness|HNSW - Hierarchical Navigable Small World]] [[Harness|AVX-512]] [[Harness|Baza danych wektorowych]] [[Harness|Early stopping w pętli agenta]] [[Harness|Throughput tokenów (tps)]] [[Stabilność modeli i przestrzeganie promptu|Testowanie modeli - benchmarki]] [[Context Compaction|Inżynieria kontekstu - timeouty i limity]] [[Harness|Live-stream RL]]

**Kontekst / Problem:**
Przegląd wyników testów Xiaomi MiMo-v2.6-Pro po treningu RL prowadzonym na żywo (live-stream RL). Autor porównuje go do poprzedniej wersji MiMo-v2.5-Pro i do Claude Fable-5, oceniając zdolność do agentowego kodowania (AgenticCoding) na zadaniach backendowych (implementacja bazy danych wektorowych) oraz frontendowych (ray tracing, symulacja fizyki). Omawia architekturę MoE (1.02T parametrów całkowitych, 42B aktywnych), użyty algorytm wyszukiwania najbliższych sąsiadów oraz osiąganą przepustowość tokenów na sekundę. Wskazuje też na problemy operacyjne: przedwczesne zatrzymanie iteracji, długie rozumowanie i przeciążenie API.

**Rada inżynierska:**
Dobieraj model do domeny zadania: MiMo-v2.6-Pro jest mocny w backendowym AgenticCoding (algorytmy, jakość kodu), ale słabszy w rozumieniu przestrzeni i symulacji fizyki na froncie. Przy testach agenta wieloetapowego licz się z tym, że model może zakończyć iteracje zbyt wcześnie, gdy przez kilka rund nie widzi poprawy wyniku — dlatego warto rozdzielać limit iteracji od warunku zbieżności i wymuszać kontynuację eksploracji (np. losowy restart, inny operator mutacji) zamiast pozwalać agentowi 'oddać pracę' w połowie budżetu. Ponadto ustawiaj duże limity czasu dla wolnego, przeciążonego endpointu oraz bierz pod uwagę, że model długo rozumuje i nie da się jeszcze regulować intensywności myślenia. W zakresie implementacji: nowoczesna wyszukiwarka wektorowa to jednowarstwowy graf HNSW (M=16, M0=28), dokładna odległość liczona instrukcjami AVX-512 i per-wątkowy visited stamp w celu uniknięcia kosztownego czyszczenia zbiorów odwiedzonych węzłów.

**Uwaga / Anty-wzorzec:**
Przedwczesne zatrzymanie (early stopping): mimo budżetu 50 iteracji na rundę, w 2 z 3 testów model przerywał na ~30. iteracji, gdy nie notował poprawy, i kończył zadanie, marnując pozostały budżet obliczeniowy. Dodatkowe pułapki: bardzo długie rozumowanie bez możliwości sterowania jego intensywnością oraz przeciążone API w trybie standardowym, które wymaga wydłużonych timeoutów, aby uniknąć pustej odpowiedzi. Anty-wzorzec: wybór tego modelu do zadań frontendowych opartych na rozumieniu przestrzennym i estetyce, gdzie wypada wyraźnie słabiej niż konkurencja.

> **Cytat:** *"简单来讲, 这次不愧是直播RL带来的效果, AgenticCoding 能力提升明显, 之前的 MiMo-v2.5-Pro 在我的向量数据库测试中得分只有2505, 而这次直接翻了3倍, 得分来到了7810. 与 Claude Fable-5 分数接近了. 而且算法也进化为了单图HNSW分层近邻图(M=16/M0=28) + AVX-512精确距离 + 每线程visited stamp. ... 另外本次还给大家测试了输出速度, MiMo-v2.6-pro-ultraspeed 版本可以达到464tps的速度, 着实恐怖. 而根据MiMo的技术报告, 峰值可以达到900tps, 常态化请求也可以稳定在500tps左右, 考虑到模型 1.02T 的总参数量, 以及高达 42B 的激活参数量, 再加上同等规模模型一般都在60-80tps的水平, 这个成绩相当亮眼. 当然也有值得注意的点, 比如这次测试我发现它还是有早停的问题的, 上面的向量数据库测试, 每轮最大迭代50次, 但是三次测试中, 有两次它迭代到30轮左右就没办法提升分数, 于是选择了直接交卷, 浪费了测试机会. 以及, 模型思考偏长, 而且暂时不支持调整思考强度, 加上普速接口现在异常火爆, 所以最好给大一些超时, 避免无法输出结果. 总结: MiMo-v2.6-Pro 适合搞后端AgenticCoding开发! 要算法有算法要质量有质量. 但是前端空间理解和美学还需要加强. 考虑到直播后训练的时候看到的67%的训练语料都是Coding, 这个结果丝毫不惊讶了."*

---

## Modele i benchmarki

### K2-Horizon-7B: mały model dense z pełną uwagą dorównuje 27B na AA Bench, ale koszt kontekstu jest wysoki

- **Data:** `Tue Sep 15 22:37:55 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099991128061919596)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|K2-Horizon-7B]] [[Harness|AA Bench]] [[Stabilność modeli i przestrzeganie promptu|Qwen3.6-27B]] [[Stabilność modeli i przestrzeganie promptu|Qwen3.8-35B-A3B]] [[Harness|MiniCPM5-2B]] [[Harness|vLLM]] [[Harness|SGLang]] [[Harness|unsloth]] [[Harness|Kwantyzacja 8-bit]] [[Harness|Kwantyzacja 4-bit]] [[Harness|Full Attention]] [[Harness|Thinking Effort]] [[Harness|BrowseComp]] [[Harness|SWEBench Verified]] [[Harness|Terminal Bench]]

**Kontekst / Problem:**
IFM wypuściło 7B model dense o nazwie K2-Horizon-7B, który osiąga 21 punktów w AA Bench, zbliżając się do Qwen3.6-27B (22 punkty). Model przewyższa wcześniejsze flagowce (GPT-5/DeepSeek-V4) w testach takich jak BrowseComp oraz dobrze wypada w SWEBench Verified i Terminal Bench. Jest w pełni otwarty: dane treningowe, przepis (recipe), kod treningowy i metody ewaluacji. Obsługuje kontekst do 512K, ale ze względu na pełną uwagę (full attention) koszt pamięciowy kontekstu jest bardzo wysoki. Autor sugeruje, że Qwen powinno odpowiedzieć modelem Qwen3.8-35B-A3B.

**Rada inżynierska:**
Przy małych modelach dense z pełną uwagą (full attention) pamiętaj, że koszt pamięciowy KV cache rośnie liniowo z długością kontekstu. Dla K2-Horizon-7B w BF16 kontekst 128K wymaga ok. 18 GB VRAM/unified memory. Zalecane jest użycie kwantyzacji 8-bit lub 4-bit (np. od unsloth) przed wdrożeniem długiego kontekstu. Model wspiera ustawienie intensywności myślenia (thinking effort: low/medium/high) – domyślnie i zgodnie z zaleceniem producenta należy używać 'high'. Obsługa w vLLM i SGLang jest już dostępna.

**Uwaga / Anty-wzorzec:**
Używanie modelu w pełnej precyzji BF16 z długim kontekstem (np. 128K) bez kwantyzacji prowadzi do szybkiego wyczerpania VRAM. Nie zakładaj, że mały rozmiar parametrów (7B) oznacza niski koszt pamięciowy – pełna uwaga i długi kontekst to główne źródło zużycia pamięci.

> **Cytat:** *"IFM刚放出了个神奇7B Dense小模型 K2-Horizon-7B. 神奇的是这玩意在AA Bench里面有21分, 而Qwen3.6-27B是22分, 也就是说这7B参数量快追平了27B的水平.
甚至这个模型在诸如BrowseComp测试中碾压了前几代旗舰模型(GPT-5/DeepSeek-V4). 而且工程能力比如SWEBench Verified/ Terminal Bench 分数表现也很亮眼.
所以敲打一波Qwen, 赶紧放出你们压箱底的Qwen3.8-35B-A3B, 别藏着掖着了. 要被偷家了!

这个模型现在完全是社区明星了, 它的训练数据, 怎么训练的(recipe), 训练代码以及评估方法全都是开源的. 参数上这个模型最大支持512K上下文, 但是注意, 这玩意虽然参数只有7B, 但是它是全注意力的, 所以上下文成本相当高. 目前还只有原始BF16精度, 如果要用128K上下文, 就要18G显存/统一内存. 所以还是等等8bit/4bit量化版本比较好(我刚在X上 @ unsloth 了一波, 看看哥俩会不会有时间做量化吧)

以及这个模型同样支持设置思考强度. 分为low/medium/high, 然后默认/官方强烈推荐用high.

如果现在不差显存想直接用可以使用vLLM/SGLang. 这俩已经支持了. 等 unsloth 放出量化版我给大家来一期10B以下小模型横评.  MiniCPM5-2B 和其他几个小模型已经在跑了.

#K2Horizon7B #MiniCPM52B #Qwen3835BA3B"*

---

## Benchmarking / Inżynieria promptów / Ekonomia inferencji

### Krytyka parametru reasoning_effort jako narzędzia przenoszenia ryzyka kosztowego na użytkownika

- **Data:** `Tue Sep 15 07:47:29 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099767043155218568)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|reasoning_effort]] [[Stabilność modeli i przestrzeganie promptu|Benchmarkowanie modeli LLM]] [[Harness|Koszt vs dokładność inferencji]] [[Harness|Post-training]] [[Stabilność modeli i przestrzeganie promptu|DeepSeek V4 Flash]] [[Harness|Cost-performance balance]]

**Kontekst / Problem:**
Autor komentuje praktykę benchmarkowania modeli reasoningowych z parametrem reasoning_effort ustawionym na max (dla porównywalności między modelami), podczas gdy część społeczności sugeruje testowanie z ustawieniem high, argumentując że 'high jest słodkim punktem'. Autor kwestionuje sensowność parametru reasoning_effort w ogóle.

**Rada inżynierska:**
Parametr reasoning_effort traktuj jako przeniesienie odpowiedzialności za trade-off między kosztem obliczeń a dokładnością na użytkownika. Vendor publikuje wyniki benchmarków w trybie max (najdroższym), jednocześnie reklamując 'słodki punkt' w trybie high — to sprawia, że użytkownicy uznają high za optymalny, mimo braku twardego uzasadnienia. Dla uczciwego benchmarku należy ustalić jednolity poziom reasoning_effort dla wszystkich porównywanych modeli (np. max), zamiast dopasowywać poziom per-model, bo inaczej wynik jest niewspółmierny.

**Uwaga / Anty-wzorzec:**
Mieszanie poziomów reasoning_effort między modelami w jednym benchmarku zniekształca porównanie. Dodatkowo przyjmowanie założenia, że 'high = najlepsze' bez weryfikacji — autor explicite twierdzi, że thinking effort NIE jest równoważne z performance, i że ta nierównoważność wynika z wad post-trainingu, a nie jest stanem pożądanym. Idealnie model powinien być trenowany tak, by wyższy effort zawsze dawał wyższą jakość.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor podważa powszechny konsensus, że parametr reasoning_effort to użyteczne narzędzie do optymalizacji kosztu. Twierdzi, że jest to głównie mechanizm marketingowy i przenoszenie ryzyka kosztowego na użytkownika. Dodatkowo kwestionuje założenie 'high = optimum' — mimo że dokumentacja DeepSeek-v4-1-flash sama opisuje max jako 'best reserved for the most challenging tasks'. Wnioski te stoją w sprzeczności z dominującą praktyką rekomendowania niższych poziomów effort dla typowych zadań. Do dalszego rozstrzygnięcia: czy przy obecnym stanie post-trainingu wyższy effort rzeczywiście monotonnicznie przekłada się na wyższą jakość, czy też istnieje realne plateau/regresja.

> **Cytat:** *"问题在于我做的是 benchmark, 不是日常使用. 不能因其他模型都用max然后deepseek high 好单独用high测. 然后评论说应该用high测. 以及, reasoning_effort 在我看来是大模型厂商的营销手段. 把算力与精度的权衡交给了用户, 顺便把算力计费的风险也转移给了用户. 而且巧妙地进行掩饰: 宣称benchmark全是max跑出来的. 最后又说甜区(注意论文里称作cost–performance balance) 在high. 造成的结果就是, 有人认为high就是最好的. 我当然同意 thinking effort 不等价于 performance. 而且我认为之所以不等价是因为后训练拉了. 理想上应该追求让它等价. 但请注意, deepseek-v4-1-flash技术报告里给max评价为: best reserved for the most challenging tasks."*

---

## Benchmarking i ewaluacja modeli LLM

### reasoning_effort jako narzędzie marketingowe: pułapka nierównego benchmarku i przenoszenia kosztu obliczeń na użytkownika

- **Data:** `Tue Sep 15 07:47:23 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099767018279084387)
- **Rodzaj:** Komentarz w dyskusji (@QuantumTransf)
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|reasoning_effort]] [[Stabilność modeli i przestrzeganie promptu|Benchmarking modeli LLM]] [[Harness|Cost-performance balance]] [[Harness|Post-training]] [[Stabilność modeli i przestrzeganie promptu|DeepSeek]] [[Harness|Budget rozumowania]]

**Kontekst / Problem:**
Dyskusja dotyczy metodologii porównywania modeli, które eksponują regulowany poziom wysiłku rozumowania (reasoning_effort). Autor broni swojej decyzji benchmarkowej: skoro inne modele testuje się na 'max', to DeepSeek nie może być mierzony osobno na 'high', bo zaburza to porównywalność. Jednocześnie formułuje tezę, że reasoning_effort to w istocie mechanizm marketingowy producentów modeli — przenosi na użytkownika zarówno trade-off między zużyciem obliczeń a dokładnością, jak i ryzyko kosztowe (billing) oraz odpowiedzialność za wybór progu. Problem pogłębia niejawne pozycjonowanie: benchmarki rzekomo raportowane na 'max', a następnie wskazywanie 'high' jako sweet spot (w publikacjach: cost–performance balance), co prowadzi część odbiorców do błędnego wniosku, że 'high' jest po prostu najlepsze.

**Rada inżynierska:**
Przy porównaniach modeli normalizuj parametr reasoning_effort po stronie wszystkich kandydatów (np. wszyscy na 'max') albo jawnie raportuj pełną krzywą cost–performance zamiast pojedynczego punktu. Nie porównuj 'high' jednego modelu z 'max' innego — to łamie porównywalność benchmarku. Traktuj reasoning_effort jako parametr kosztowy, a nie jakościowy: wyższy poziom nie gwarantuje wyższej jakości, przenosi jedynie większe zużycie obliczeń i koszt na użytkownika. Idealnie dążyć do tego, aby thinking effort był równoważny z performance (autor wskazuje, że obecna rozbieżność wynika z niedostatków post-trainingu, a nie z natury parametru).

**Uwaga / Anty-wzorzec:**
Błędne utożsamianie 'high' z optimum jakości oraz traktowanie sweet spot (cost–performance balance) jako globalnego maksimum jakości. Anty-wzorzec po stronie dostawców: raportowanie benchmarków wyłącznie na 'max', a następnie komunikowanie 'high' jako zalecanego progu — bez ujawnienia, że różnica wynika z kompromisu kosztowego, nie z lepszej jakości. Anty-wzorzec po stronie użytkownika: nierówne ustawienia reasoning_effort między modelami w jednym teście porównawczym.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor podważa powszechny konsensus branżowy, że reasoning_effort to użyteczna funkcja dająca użytkownikowi kontrolę. Twierdzi, że jest to w istocie marketing i transfer ryzyka kosztowego na użytkownika. Dodatkowo twierdzi, że thinking effort powinien być równoważny z performance, a obecna rozbieżność to wina post-trainingu — co jest tezą kontrowersyjną wobec praktyki traktowania wyższego reasoning_effort jako automatycznie lepszego. Do rozstrzygnięcia: czy reasoning_effort to realna dźwignia jakości, czy mechanizm komercjalizacji kosztu obliczeń.

> **Cytat:** *"问题在于我做的是 benchmark, 不是日常使用. 不能因其他模型都用max然后deepseek high 好单独用high测.  

然后评论说应该用high测. 

以及, reasoning_effort 在我看来是大模型厂商的营销手段. 把算力与精度的权衡交给了用户, 顺便把算力计费的风险也转移给了用户. 而且巧妙地进行掩饰: 宣称benchmark全是max跑出来的. 最后又说甜区(注意论文里称作cost–performance balance) 在high. 

造成的结果就是, 有人认为high就是最好的. 

我当然同意 thinking effort 不等价于 performance. 而且我认为之所以不等价是因为后训练拉了. 理想上应该追求让它等价.

但请注意, deepseek-v4-1-flash技术报告里给max评价为: best reserved for the most challenging tasks."*

---

## Architektura modeli i optymalizacja inferencji

### Jev od TypeSafe AI: architektura równoległego próbkowania dla ultraniskich opóźnień w produkcji

- **Data:** `Thu Sep 17 22:46:03 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2100717948881326224)
- **Rodzaj:** Komentarz w dyskusji (@karminski3)
- **Powiązane pojęcia:** [[Jev]] [[TypeSafe — przewodnik praktyczny|TypeSafe AI]] [[Harness|System One]] [[Harness|System Two]] [[Harness|Architektura równoległego próbkowania]] [[Harness|Inferencja LLM]] [[Harness|Opóźnienie sieciowe]] [[Harness|Vercel AI Gateway]]

**Kontekst / Problem:**
Model Jev firmy TypeSafe AI oferuje bardzo niskie opóźnienie (70 ms obliczeń) dzięki architekturze równoległego próbkowania, która w jednym przejściu w przód generuje dyskretne predykcje dla wszystkich pól schematu i prawdopodobieństwa gałęzi. Nadaje się do zastosowań produkcyjnych o wysokiej częstotliwości, np. do sprawdzania bezpieczeństwa poleceń shell w bastionie. Koszt: 0,042 USD za milion tokenów wejściowych, wyjście bezpłatne. Ograniczenia: brak lokalnych węzłów, więc opóźnienie sieci do US West wynosi co najmniej 120 ms, co daje minimum 200 ms całkowitego opóźnienia. Model określany jako System One, wymaga uzupełnienia o System Two do podejmowania decyzji strategicznych. Dostępny przez Vercel AI Gateway.

**Rada inżynierska:**
W scenariuszach wymagających wysokiej przepustowości i niskich opóźnień rozważ modele z architekturą równoległego próbkowania, które zwracają wszystkie pola schematu w jednym przejściu w przód, zamiast tradycyjnych modeli autoregresyjnych iterujących po tokenach. Pamiętaj o fizycznym opóźnieniu sieci (np. 120 ms do US West) – nawet ultraszybki model może mieć 200 ms całkowitego czasu odpowiedzi. Do złożonych zadań łącz model System One z modelem System Two generującym strategię jako prompt.

**Uwaga / Anty-wzorzec:**
Poleganie wyłącznie na szybkim modelu System One bez warstwy System Two do oceny strategicznej może prowadzić do błędnych decyzji. Ignorowanie opóźnień sieciowych przy projektowaniu systemów czasu rzeczywistego – samo niskie opóźnienie obliczeń (70 ms) nie gwarantuje niskiego opóźnienia end-to-end.

> **Cytat:** *"但天下武功唯快不破, 这玩意从输入到输出最快只需要70ms!

所以完全可以用在高频的生产级场景, 比如接到堡垒机里面实时判断用户输入的shell命令是否存在危险(rm -rf /). 再加上输入每百万token只需要$0.042, 输出不要钱. 妥妥的新一代flash模型斩杀线(有的flash模型会被企业用作决策器).

说完了用途再来看它的架构, 传统大模型有多少token就要把激活参数过多少遍(前向传播)所以特别吃显存带宽, 而这个模型设计了一个特殊的并行采样架构, 只需要一次前向传播, 就能输出所有预设schema字段的离散预测与分支概率. 达成了极低的延迟.

而推出Jev的 TypeSafe AI 这个公司也很有噱头, 它是 Diogo Almeida 一手创办的, 就是他曾经在 OpenAI 的 InstructGPT 和早期 RLHF（基于人类反馈的强化学习) 团队中的贡献才有了如今的ChatGPT.

最后说一下目前模型的限制, 首先由于没有本土节点, 所以虽然它只需要70ms, 但是到美西这海底光缆延迟120ms是躲不掉的, 所以至少还是200ms打底. 另外, 模型被官方称为 System One 模型, 所以理想搭配还需要一个 System Two 模型用来进行战略判断, 然后生成策略当作提示词输入进去, 这样才能提升模型的输出质量.

另外, 官网还在申请使用, 不过vercel的AI Gateway已经能直接用了, 所以想测试的同学直接去vercel用就行."*

---

## Architektura modeli / Type-Safe AI

### Model Jev: rezygnacja z architektury autoregresyjnej na rzecz decyzyjnych slotów ze schemą typowaną

- **Data:** `Thu Sep 17 22:46:02 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2100717944565354595)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Jev|Jev Model]] [[Harness|Type-Safe AI]] [[Harness|Structured Output]] [[Harness|Decision Slots]] [[Harness|Schema-based Prompting]] [[Harness|Autoregressive vs Decision Models]] [[Harness|System One]] [[Harness|Diogo Almeida]]

**Kontekst / Problem:**
Wprowadzenie do modelu Jev, który porzuca tradycyjną architekturę autoregresyjną (nie potrafi generować zwykłego tekstu), a zamiast tego wykonuje decyzje. Rozwiązuje problem nieprzewidywalności i halucynacji formatu wyjściowego w klasycznych LLM-ach poprzez wymuszenie strukturalnego wyjścia opartego na zdefiniowanej schemie (analogicznie do protobuf/GraphQL), która jest kompilowana do konkretnych slotów decyzyjnych. Model zwraca JSON w formacie gwarantowanym przez schemę, więc wyjście nie może być niepoprawne składniowo. Autor wskazuje, że model zasługuje na szczególną uwagę i jest powiązany z ekosystemem TypeSafeAI, Diogo Almeida oraz System One.

**Rada inżynierska:**
Przy pracy z modelami decyzyjnymi definiuj schemę wyjścia (np. w stylu protobuf/GraphQL) i pozwól kompilatorowi przekształcić ją w sloty decyzyjne. Model wypełnia jedynie zdefiniowane sloty, co eliminuje ryzyko błędnego lub nieparsowalnego JSON-a. Dla złożonych scenariuszy (np. gra Slay the Spire, analiza rynku/notowań) konwertuj stan wejściowy na tekst, zdefiniuj zamknięty zbiór dostępnych akcji, a model samodzielnie podejmie decyzję. To wzorzec „type-safe decision making” — odpowiednik LLM-a, ale z gwarancją typu i struktury wyjścia.

**Uwaga / Anty-wzorzec:**
Model nie potrafi generować swobodnego tekstu — każde zadanie, które wymaga narracyjnego lub nieustrukturyzowanego wyjścia, wymaga przeprojektowania na decyzje i sloty. Aktualnie obsługiwany jest wyłącznie input tekstowy, więc wszystkie dane wejściowe (stan gry, dane rynkowe, treść SMS-a) trzeba najpierw przekonwertować na tekst. Zakładanie, że model zachowa się jak zwykły LLM (swobodna generacja, brak schemy), prowadzi do błędnego użycia architektury.

> **Cytat:** *"给大家写个简单的Jev模型介绍, 这绝对是个需要重点关注的模型. 简单讲, 这个模型放弃了传统自回归架构, 它没有办法直接输出普通文本. 但是他能进行决策! 比如最简单的二分类场景, 输入一条短信, 让它判断是否为垃圾短信, 它就可以输出这样的JSON: {"decision": { "isSpam": true }, "probabilities": { "isSpam": { "true": 0.982, "false": 0.018 } } } 没错, 它只能进行结构化输出, 甚至你输入的时候要定义 Schema (用过protobuf/GraphQL的同学应该能理解), 在送入模型时被编译为特定的决策槽位, 然后按照槽位输出, 所以输出JSON不可能出问题. 而复杂一些的场景, 比如让这个模型玩杀戮尖塔或者看盘, 只需要把内容转换为文本输入进去(没错, 目前模型只支持文本输入), 然后定义好模型能进行哪些动作, 模型就会自主决策了. 到目前为止, 是不是看上去跟普通文本大模型没区别? #jev #TypeSafeAI #DiogoAlmeida #systemone #vercel"*

---

## Systemy agentowe / Agentic Engineering

### System Scaling kontra skalowanie parametrów: agentowa pętla feedbacku środowiskowego jako klucz do wdrożeń inżynierskich

- **Data:** `Thu Aug 27 08:39:50 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2092894849619874210)
- **Rodzaj:** Komentarz w dyskusji (@karminski3)
- **Powiązane pojęcia:** [[Harness|System Scaling]] [[Harness|Agentic Engineering]] [[Harness|Multi-Agent Collaboration]] [[Harness|Environment Feedback Loop]] [[Harness]] [[Harness|DeepResearch]] [[Harness|Verifier]] [[Harness|Konfiguracja Firewalla przez Agenta]]

**Kontekst / Problem:**
Autor opisuje wynik działania architektury agentowej (framework open source + specjalnie dostrojony model DeepResearch), która w ok. 10 minut dostarczyła konfigurację firewalla skierowaną przeciw konkretnemu wektorowi ataku. Teza: realną dźwignią nie jest liczba parametrów modelu, lecz zbudowanie spójnego systemu łączącego wieloagentową współpracę z pętlą prób i błędów w realnym środowisku (tzw. System Scaling).

**Rada inżynierska:**
Traktuj 'System Scaling' jako główny wektor rozwoju: opakuj model w harness, w którym (1) wielu agentów dzieli role i wymienia wyniki, oraz (2) każda hipoteza jest weryfikowana przez wykonanie w środowisku (np. aplikacja reguł firewalla i test ruchu), a wynik weryfikacji wraca jako feedback do kolejnej iteracji. Budżetuj czas na iteracje weryfikacyjne — konfiguracja dostarczona w ~10 min oznacza, że pętla wykonawcza była tania i szybka, nie że model 'wiedział' wszystko od pierwszego strzału. Wykorzystuj gotowe, otwarte frameworki agentowe i modele dostrojone pod DeepResearch zamiast budować wszystko od zera.

**Uwaga / Anty-wzorzec:**
Skalowanie wyłącznie parametrów modelu bez warstwy systemowej (harness, weryfikatory, pętla feedbacku ze środowiska) — takie modele nie przełożą się na realne wdrożenia inżynierskie. Dodatkowe ryzyko: generowanie konfiguracji bezpieczeństwa (firewall) przez agenta bez niezależnego audytu reguł — szybkość dostarczenia (10 min) nie jest dowodem poprawności ani braku obejść; brak wzmianki o testach regresyjnych i walidacji negatywnej (próba obejścia własnych reguł).

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor podważa dominujący w branży nacisk na 'scale is all you need' (wyścig o liczbę parametrów) i przekłada akcent na inżynierię systemową (System Scaling). Do rozstrzygnięcia: czy przyrost możliwości wynika głównie z rozmiaru modelu, czy z architektury harnessu i pętli weryfikacji w środowisku — oraz czy pojedynczy, szybki sukces (konfiguracja firewalla w 10 min) jest wystarczającym dowodem przewagi podejścia systemowego.

> **Cytat:** *"最后, 在这个架构加持下, 它仅用了10分钟左右就给我交付了针对攻击的防火墙配置. 这真的是 Agentic 系统工程的胜利了. 

未来的 AI 竞争, 不仅是卷模型参数量, 能把环境试错反馈和多 Agent 协同做成统一的系统 (System Scaling), 才是真正让AI在各种工程中落地的关键.

另外, 这个框架还开源了! 这里: https://t.co/n4F2ulrtEc
配套的 DeepResearch 模型也在这里: https://t.co/f8BzbXFh1n (模型之前也给大家测过, 是针对 DeepResearch 特调的, 性能相当不错)"*

---

## Architektura systemów agentowych / Inżynieria kontekstu

### Harness Scaling: skalowanie orkiestracji agentów zamiast samych parametrów modelu

- **Data:** `Thu Aug 27 08:39:49 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2092894843429363871)
- **Rodzaj:** Komentarz w dyskusji (@karminski3)
- **Powiązane pojęcia:** [[Harness|Harness Scaling]] [[Harness|Agentic Coordination Scaling]] [[Harness|Environment Scaling]] [[Harness|Agent Team / Swarm]] [[Harness|Attention Dilution]] [[Harness|Halucynacje modeli LLM]] [[Harness|Token Explosion]] [[Harness|AgentOS]] [[Harness|Sandbox / Runtime izolowany]] [[Harness|ModSecurity]] [[Harness|SOC (Security Operations Center)]] [[Harness|Asynchroniczna orkiestracja agentów]] [[Harness|Long-context engineering]]

**Kontekst / Problem:**
Problem: zadanie analizy ~1,2 mln linii logów (~260 MB) w klasycznym, jednowątkowym systemie agentowym. Sekwencyjne wczytywanie takiego wolumenu do kontekstu prowadzi nieuchronnie do rozproszenia uwagi (attention dilution), halucynacji i w konsekwencji błędu całego zadania. Apodex 1.1 rozwiązuje to przez rozbicie zadania na asynchroniczny zespół agentów oraz ekstrakcję logów skryptami poza modelem, uruchamianymi w izolowanym runtime (AgentOS).

**Rada inżynierska:**
Stosuj wieloskalowe podejście do budowy systemów agentowych: samo zwiększanie liczby parametrów modelu podnosi jedynie jego 'inteligencję', natomiast skalowanie rusztowania (framework), narzędzi (Agent Tools) i zespołu agentów (Agent Team/Swarm) podnosi realną zdolność wykonywania pracy — to tzw. Harness Scaling. W praktyce: (1) Agentic Coordination Scaling — podziel zadanie jak prawdziwy zespół SOC: agent wywiadowczy czyści setki tysięcy logów i ekstrahuje złośliwe IP oraz sygnatury, agent reguł na podstawie tych sygnatur pisze reguły blokujące ModSecurity; wszystko asynchronicznie i równolegle, tak by agent reguł zaczynał pisać reguły firewall już na pierwszej partii logów wyplutej przez agenta wywiadu. Nowe wymagania można wstrzykiwać w trakcie działania bez przerywania bieżących zadań. (2) Environment Scaling — nie wczytuj całego wolumenu logów do modelu (eksplozja tokenów), tylko napisz dedykowane skrypty ekstrahujące logi ataków; uruchamiaj je na AgentOS (runtime całego systemu Apodex), aby model mógł wykonywać ryzykowny kod bez wpływu na system hosta.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: klasyczny liniowy (jednowątkowy) agent wczytujący cały surowy wolumen logów do kontekstu. Skutki: utrata uwagi, halucynacje, przekroczenie budżetu tokenów, awaria całego zadania. Drugi anty-wzorzec: wykonywanie kodu generowanego przez model bezpośrednio na hoście bez sandboxa/runtime'u izolującego.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Teza kontrowersyjna względem dominującego konsensusu branżowego (scaling laws): autor twierdzi, że zwiększanie liczby parametrów modelu podnosi wyłącznie 'inteligencję', a realną zdolność wykonawczą ('pracę') daje dopiero skalowanie harnessu — frameworku, narzędzi i roju agentów. Do rozstrzygnięcia: czy inwestycja w orkiestrację/sandbox przewyższa inwestycję w scaling modelu dla zadań długokontekstowych oraz czy równoległość async faktycznie eliminuje problem attention dilution, czy tylko go maskuje przez dekompozycję zadań i pre-filtrację danych skryptami.

> **Cytat:** *"这个任务最难的点就是, 如果是最传统的Agent系统, 就只能单线思考, 120万条日志(约260MB), 绝对会导致各种注意力丢失或者产生幻觉, 最后整个任务就直接报错.

这次  Apodex 1.1 版本就针对这个场景做了升级. 这里必须要给大家介绍一个概念: Harness Scaling

简单来讲, 光堆模型参数量只能提升模型的"智力", 而堆模型的脚手架(framework), 工具箱(Agent Tools)和团队(Agent Team/Swarm), 就能提升模型干活的能力.

Apodex 1.1 在两个地方发力了:

首先是 Agentic Coordination Scaling（智能体协同扩展）：
它的 Agent Team 像一个真正的 SOC 安全团队一样把任务拆了, 情报 Agent 去清洗几十万条日志提取恶意 IP 和特征, 规则 Agent 根据特征去写 ModSecurity 拦截规则. 注意这些是异步并行的, 速度非常快, 甚至情报 Agent 刚吐出第一批探测到的攻击日志, 规则 Agent 就已经开始写防火墙规则了. 而且如果要改需求, 可以随时在这个过程中添加, 不用担心影响正在跑的任务.

紧接着是 Environment Scaling（环境扩展）：
如果这120万条日志全都让AI去读取, token量肯定直接炸了, 所以有针对性的编写脚本去抽取攻击日志就是工作的主要内容了, 而这些日志全都是运行在 AgentOS 上的, 它是整个 Apodex 系统的运行时承载, 在这个上面模型可以运行各种风险代码而不用担心影响宿主系统."*

---

## Systemy agentowe / Bezpieczeństwo / Inżynieria kontekstu

### Agent Apodex 1.1 analizuje 1,2 mln linii logów i generuje reguły firewalla dla realnego ataku

- **Data:** `Thu Aug 27 08:39:48 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2092894838492655713)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Context Compaction|Inżynieria kontekstu]] [[Harness|Systemy agentowe]] [[Harness|AgentOS]] [[Harness|Apodex]] [[Harness|Analiza logów bezpieczeństwa]] [[Harness|Privilege escalation]] [[Harness|Generowanie reguł firewalla]] [[Harness|Weryfikacja zewnętrzna]] [[Stabilność modeli i przestrzeganie promptu|Benchmark agentów]] [[Harness|Zarządzanie pamięcią agenta]]

**Kontekst / Problem:**
Test praktyczny świeżo wydanego agenta Apodex 1.1 (ekosystem AgentOS) na zadaniu z pogranicza bezpieczeństwa: autor spakował ok. 1,2 mln linii logów serwera WWW pochodzących z publicznego zbioru Zenodo, zawierających realne próby ataków polegających na podniesieniu uprawnień (privilege escalation). Zadanie dla agenta było dwuetapowe i end-to-end: (1) zidentyfikować techniki atakującego na podstawie surowych logów, (2) wygenerować reguły firewalla blokujące te ataki. Wg autora agent wykonał cały łańcuch bez ręcznej ingerencji — od analizy po produkcję reguł. Wpis jest zarazem demonstracją możliwości harnessu agentowego w scenariuszu, który klasycznie rozwiązuje się pipeline'em SIEM + deterministyczne parsery + reguły korelacji, a nie modelem językowym.

**Rada inżynierska:**
Wzorzec 'duży wolumen → artefakt weryfikowalny': nie wrzucaj surowych logów do kontekstu modelu, tylko dostarcz je agentowi jako zewnętrzny zbiór danych i pozwól mu iterować narzędziami (grep/agregacje/filtry po polach), a wynik zamknij w konkretnym, testowalnym artefakcie — tutaj regułach firewalla. Kluczowe jest to, że produkt końcowy da się zweryfikować niezależnie (reguła albo blokuje dany wzorzec ruchu, albo nie), więc halucynacja nie przechodzi przez bramkę walidacji. Skalowanie takich zadań opiera się na oddzieleniu warstwy pamięci/kontekstu od warstwy wykonawczej: agent widzi podsumowania i wyniki zapytań, nie całe 1,2 mln linii.

**Uwaga / Anty-wzorzec:**
Traktowanie LLM jako parsera logów. Przy milionowych wolumenach model nie jest w stanie utrzymać całego zbioru w kontekście — bez deterministycznego preprocessingu, indeksowania i zapytań narzędziowych analiza degeneruje się do halucynowanych wzorców ataku. Drugą pułapką jest publikowanie wygenerowanych reguł firewalla bez testu regresyjnego na ruchu (reguła może być poprawna składniowo, a nie blokować niczego albo blokować legalny ruch). Trzecią — wyciąganie ogólnego wniosku 'model rozwiązuje analizę bezpieczeństwa' z jednego, autopromocyjnego demo bez niezależnego audytu wyników.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Teza stoi w napięciu z dominującym konsensusem inżynierskim, że LLM nie nadają się do bezpośredniej analizy surowych logów o dużej objętości — standardem jest deterministyczny parsing, normalizacja i reguły korelacji w SIEM, a model pełni co najwyżej rolę asystenta w triage'u. Autor twierdzi, że agent przeszedł cały łańcuch (1,2 mln linii → identyfikacja technik ataku → reguły firewalla) end-to-end. Do rozstrzygnięcia pozostaje: (a) czy model faktycznie przetwarzał surowe dane, czy tylko wyniki zapytań narzędziowych nad spakowanym zbiorem — co zmienia sens tezy z 'model analizuje logi' na 'harness analizuje logi, model orkiestruje'; (b) jaka była precyzja/recall wykrytych ataków i czy reguły firewalla zostały zweryfikowane na odłożonym zbiorze testowym; (c) brak niezależnej reprodukcji — wpis ma charakter demonstracyjno-promocyjny dla Apodex 1.1 i AgentOS.

> **Cytat:** *"劲爆, 我给刚发布的 Apodex 1.1 出了个极其变态的实战难题, 它真的跑通了!

我直接打包了120万条日志, 里面包含真实的提权攻击的 Web Server 日志(用的是 Zenodo Dataset). 

然后让他帮我把黑客的攻击方式抓出来, 还要给我写防火墙规则拦截攻击. 结果它真的做到了, 从分析到写规则一气呵成"*

---

## Benchmarking / Ewaluacja modeli LLM

### Dobór GPU do benchmarkowania modeli LLM: moc karty wpływa tylko na szybkość, nie na jakość wyjścia

- **Data:** `Thu Aug 20 17:44:00 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2090495077873533333)
- **Rodzaj:** Komentarz w dyskusji (@xueyu1125)
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|Benchmarking LLM]] [[Harness|Ewaluacja modeli]] [[Harness|Harness testowy]] [[Harness|Inferencja]] [[Harness|H100]] [[Harness|Kwantyzacja]] [[Harness|Throughput vs Latency]] [[Harness|Determinizm generacji]]

**Kontekst / Problem:**
Autor odpowiada na wątpliwości dotyczące użycia szybkich kart GPU (H100) w testach porównawczych 44 modeli LLM na dużym zbiorze promptów. Wyjaśnia, że wybór GPU jest podyktowany wyłącznie przepustowością infrastruktury testowej – nawet na H100 pełny przebieg ewaluacji jednego promptu przez 44 modele zajmuje ~5 godzin. Podkreśla, że testy mierzą jakość generowanego tekstu, a nie szybkość inferencji, więc rodzaj karty nie zniekształca wyników jakościowych.

**Rada inżynierska:**
Przy budowie harnessu ewaluacyjnego rozdziel dwie osie pomiarowe: (1) jakość wyjścia – determinowana przez wagi, kwantyzację, sampling i prompt, ale NIE przez klasę GPU; (2) wydajność inferencji (latency, throughput, tokens/s) – zależna od sprzętu. Skoro GPU nie zmienia rozkładu prawdopodobieństw modelu przy identycznych parametrach generacji, można bezpiecznie używać najszybszych dostępnych akceleratorów (np. H100) wyłącznie w celu skrócenia czasu trwania testów. Planuj budżet czasowy realistycznie: 44 modele × N promptów to n×~5h na pojedynczą próbkę, więc równoległość i batchowanie są krytyczne.

**Uwaga / Anty-wzorzec:**
Błędne założenie, że mocniejsza karta GPU zmienia lub 'poprawia' jakość odpowiedzi modelu. GPU wpływa jedynie na czas wykonania, nie na treść wyjścia – o ile zachowana jest ta sama precyzja obliczeń (nie miesza się np. FP16 vs FP8/INT4 w sposób niekontrolowany). Mieszanie różnych poziomów kwantyzacji między maszynami testowymi jest realnym źródłem rozbieżności jakości.

> **Cytat:** *"因为测试量较大，所以只能用比较快的卡来测，即使用H100测一个prompt，44个模型测试下来也要5小时。而且测试本身是测试模型输出质量，不是测试速度。不同显卡只是输出速度不同，显卡不会影响输出质量。"*

---

## Reverse engineering / AI Agent / Embedded (ARM Cortex-M)

### Agent AI (Fable-5.1) przełamuje firmware'owy DRM drukarki etykiet — iniekcja kodu w Cortex-M0 i remapowanie logiki koncentracji wydruku

- **Data:** `Sat Sep 19 22:02:38 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2101431800920990074)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Reverse engineering firmware'u]] [[Harness|AI Agent jako narzędzie RE]] [[Harness|Iniekcja kodu / code cave]] [[Harness|ARM Cortex-M0]] [[Harness|Hardware lock-in i DRM sprzętowy]] [[Harness|Dekompozycja pracy człowiek–AI]] [[Harness|RFID w materiałach eksploatacyjnych]]

**Kontekst / Problem:**
Autor opisuje projekt, w którym agent AI (Fable-5.1) samodzielnie przeprowadził reverse engineering firmware'u termicznej drukarki etykiet, która wykrywała nieoryginalne nośniki po RFID i w odwecie obniżała prędkość oraz jakość druku (klasyczny hardware lock / vendor lock-in). Problem: obejście sztucznego ograniczenia bez oryginalnego nośnika. Kontekst szerszy: AI radykalnie obniża próg wejścia w reverse engineering sprzętu, czyniąc mechanizmy anty-podróbkowe i DRM-owe projektowane przez producentów sprzętu podatnymi na złamanie przez powszechnie dostępnych agentów kodu.

**Rada inżynierska:**
Agent AI potrafi samodzielnie przejść ścieżkę: (1) wyprowadzenie matematycznego modelu sterowania — w tym wypadku formuła koncentracji wydruku darkness = renderer_input × coefficient; (2) lokalizacja zmiennej sterującej (koncentracji) w pamięci; (3) dynamiczna iniekcja kodu w asemblerze — technika code cave (wykorzystanie nieużywanego obszaru kodu i przeskok) na ARM Cortex-M0, pozwalająca wpiąć nową logikę remapowania wartości bez modyfikowania oryginalnych ścieżek. Podział pracy: AI odpowiada za trudny RE ARM, wyprowadzenia matematyczne i iniekcję asemblera, człowiek — za fizyczne wykonanie (wciśnięcie przycisku zasilania, weryfikację wizualną czarności wydruku). Wnioski: przy projektowaniu własnych systemów traktuj każdą logikę kontrolną klienta jako potencjalnie podlegającą patchowaniu — nie polegaj wyłącznie na obfuskacji ani na pojedynczym punkcie weryfikacji.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec po stronie producenta sprzętu: opieranie modelu biznesowego na tanim hardware locku (RFID w nośniku, obniżanie jakości dla nieoryginalnych materiałów eksploatacyjnych) bez realnego zabezpieczenia logiki sterującej. Takie ograniczenia padają trywialnie przed agentem AI zdolnym do analizy binarnej i iniekcji asemblera. Anty-wzorzec po stronie użytkownika: nieprzemyślane flashowanie firmware'u bez backupu — ryzyko trwałego uszkodzenia (brick) urządzenia.

> **Cytat:** *"看到了个Fable5.1弄的神奇项目, 是一个标签打印机的固件... Fable-5.1成功推导出了控制打印浓度的公式: darkness=renderer_input×coefficient, 然后定位了打印浓度在内存中的位置, 然后甚至利用了 Cortex-M0 汇编代码洞跳转技术把浓度重映射的动态逻辑缝合了进去, 彻底绕过了降速和降质限制. 比较黑色幽默的是整个过程 AI 负责搞定高难度的 ARM 逆向, 数学推导和汇编注入, 而人类由于长了眼睛和手, 于是负责提供物理执行力, 也就是按电源键和看纸上的字够不够黑."*

---

## Architektura systemów agentowych / Benchmarking i ocena modeli

### Jev (System-1) vs czysty generator liczb losowych w labiryncie: klęska w planowaniu wielokrokowym

- **Data:** `Mon Sep 21 07:49:04 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2101941770003361893)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|System-1 vs System-2]] [[Harness|Lokalne optimum w planowaniu]] [[Harness|Twierdzenie o spacerze losowym Pólyi]] [[Harness|xoshiro256++]] [[Stabilność modeli i przestrzeganie promptu|Benchmarking modeli decyzyjnych]] [[Harness|Architektura agentów AI]] [[Harness|Modele planujące a klasyfikatory jednokrokowe]]

**Kontekst / Problem:**
Autor zbudował środowisko testowe (Rust + xoshiro256++ + bit reservoir + Tokio/Hyper) z API zgodnym z Jev i przeprowadził pojedynek w zadaniu nawigacji po labiryncie między modelem decyzyjnym Jev (System-1) a czystym generatorem liczb losowych. Celem było sprawdzenie, czy szybki, jednokrokowy klasyfikator strukturalny może dorównać lub pobić losowe decyzje w zadaniu planistycznym. Wsparciem teoretycznym jest twierdzenie o spacerze losowym Pólyi (Pólya's Random Walk Theorem): w skończonej, spójnej siatce 2D prosty spacer losowy jest powracający (recurrent), więc 'pijany' agent z prawdopodobieństwem 1 dotrze do celu.

**Rada inżynierska:**
Traktuj Jev (System-1) wyłącznie jako ultraszybki, jednokrokowy klasyfikator strukturalny — NIGDY jako planer. Jev nie potrafi wykonać wielokrokowej analizy, nie potrafi wyjść z lokalnego optimum i ignoruje reguły warunkowe ('jeśli za często odwiedzone, to...'), ponieważ jego heurystyka jednokrokowa (np. minimalizacja odległości Manhattan) zawsze wygrywa nad regułami drugorzędnymi. Do zadań wymagających planowania, cofania i unikania lokalnych optimów zawsze dołącz model System-2. Kluczowa reguła: gdy lokalna heurystyka jest niespójna z globalnym optimum, model System-1 zawodzi systematycznie.

**Uwaga / Anty-wzorzec:**
Anty-wzorce: (1) Stosowanie Jev/System-1 do zadań wymagających omijania przeszkód, cofania i planowania wielokrokowego — labirynty, bin packing, scheduling, wszędzie tam gdzie lokalne heurystyki są niespójne z globalnym optimum. (2) Sterowanie z 'nagłą śmiercią' (sudden death): Snake, Tetris, jazda autonomiczna — jeden zły krok = natychmiastowa porażka. (3) Nieodwracalne decyzje o wysokim koszcie: usuwanie bazy danych, operacje transakcyjne, scenariusze wymagające audytu. (4) Błędne założenie, że dostarczenie historii (last_move, visited_count) i instrukcji warunkowych naprawi brak zdolności planistycznych — model System-1 i tak zignoruje reguły drugorzędne na rzecz heurystyki jednokrokowej. Obserwacja: Jev utknął w narożniku (7,4) na 2295 z 2306 kroków, kręcąc się w 3 komórkach, podczas gdy czysty RNG ukończył labirynt w 892 krokach w czasie <300 ms.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor podważa dominujący konsensus branżowy, że wyspecjalizowane modele typu System-1 (jak Jev) można stosować do zadań wymagających planowania wielokrokowego. Teza kontrowersyjna: w zadaniach planistycznych czysty generator liczb losowych (System-1) potrafi systemowo pobić inteligentny model decyzyjny, co stoi w sprzeczności z powszechnym założeniem o wyższości modeli decyzyjnych nad losowymi baseline'ami.

> **Cytat:** *"所以, Jev 它只是一个极速的单步结构化判断器, 但绝不是规划器. 最好还是带一个System-2模型才能进行复杂任务.

最后给大家整理慎用 Jev 的场景：

需要绕路, 回溯, 多步规划的：迷宫, 装箱, 调度等局部启发和全局最优不一致的图问题. 
突然死亡型控制：贪吃蛇, 俄罗斯方块, 自动驾驶等. 一步踏错当场GG. 
不可逆高代价决策：删库, 事务操作, 尤其是需要审计的场景."*

---

## Inne obserwacje

### Empiryczna weryfikacja mitu o „破甲

- **Data:** `Mon Sep 21 00:09:21 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2101826076762857867)
- **Rodzaj:** Wpis autorski
---

## Architektura harnessów i systemów agentowych / Edge & Browser AI

### Agent kodujący w całości w przeglądarce: mini model 2B w formacie ONNX 4bit + framework Pi

- **Data:** `Mon Sep 14 22:55:34 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099633181934907654)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Coding Agent]] [[Harness|ONNX]] [[Harness|Kwantyzacja 4bit]] [[Harness|WebGPU]] [[Harness|Edge AI]] [[Harness|MiniCPM]] [[Harness|tool_call]] [[Harness|Agent w przeglądarce]] [[Harness|Wirtualny terminal]] [[Harness|Inference offline]] [[Harness|Self-healing UI]]

**Kontekst / Problem:**
Problem: klasyczne uruchomienie Coding Agenta wymaga kontenera Docker, Node.js i zewnętrznego API (klucz API, połączenie sieciowe), co blokuje scenariusze w środowiskach zamkniętych (intranet, SaaS bez dostępu do sieci publicznej) oraz uniemożliwia natywne korzystanie z sesji/loginu użytkownika. Autor omawia projekt Hugging Face Space 'MiniCPM5-2B-WebGPU-Pi', który eliminuje te zależności: cały stos (framework agenta + inference modelu) działa w przeglądarce. Model MiniCPM5-2B skwantyzowany do 4bit w formacie ONNX zajmuje poniżej 2 GB, framework 'Pi' opakowuje agenta kodującego z wirtualnym terminalem, edycją plików i obsługą tool_call.

**Rada inżynierska:**
Uruchamiaj cały stos agenta (framework + skwantyzowany model) po stronie przeglądarki zamiast na serwerze, gdy potrzebujesz: (1) natywnego dostępu do stanu logowania i cookies użytkownika bez konfiguracji API KEY, (2) pracy całkowicie offline lub w sieci zamkniętej (intranet, wewnętrzne SaaS), (3) minimalnej infrastruktury (brak Docker/Node). Kluczem jest kompresja modelu do 4bit ONNX <2 GB — MiniCPM5-2B w tej konfiguracji osiąga ~25 tps na GPU 3080Ti, a jego stabilność tool_call okazuje się zaskakująco dobra jak na model 2B. Drugi wzorzec: wtyczka 'self-healing' — harness nasłuchuje błędów w konsoli przeglądarki i nanosi hot-patche na zepsutą stronę bez przeładowania. To sygnał, że mini modele (2B) nadają się już do realnych zadań agentowych na urządzeniu końcowym.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: odruchowe zakładanie, że każdy agent wymaga zewnętrznego API KEY i stałego połączenia z siecią — pomija to całą klasę zastosowań edge (urządzenia końcowe, środowiska air-gapped, operowanie w kontekście sesji użytkownika). Druga pułapka: ignorowanie rozmiaru artefaktu — model musi zmieścić się w rozsądnym budżecie pamięci (tu <2 GB przez kwantyzację 4bit ONNX), inaczej nie odpali się w WebGPU/przeglądarce. Warto też pamiętać, że pomiar 25 tps dotyczy konkretnego GPU (3080Ti) i nie przenosi się wprost na słabszy sprzęt.

> **Cytat:** *"看到个神奇的 huggingface Space项目, 思路很值得借鉴跟大家说下. Space 叫 MiniCPM5-2B-WebGPU-Pi, 不用起 Docker, 也不用装 Node 啥的, 打开网页就是一个带虚拟终端, 能进行文件编辑和 tool_call 的完整Coding Agent. 这玩意用 Pi 包了个 Coding Agent, 然后使用 MiniCPM5-2B 模型驱动. 神奇的地方就是, 这里用的是 MiniCPM5-2B 4bit ONNX 封装版本 (不到2G), 所以从框架到推理模型全都运行在了浏览器上. ... 我实测这玩意在我的3080Ti上能跑到25tps, 框架内部模拟了shell环境和提供了最基础的文件编辑tool_call. ... MiniCPM5-2B 的 tool_call 稳定性意外的不错, 大家对 2B 这种迷你模型跑 Agent 感兴趣吗?"*

---

## Rozumowanie LLM / Test-time compute / Destylacja

### Długi CoT, budżet rozumowania i destylacja DeepSeek-R1 do małych modeli Qwen

- **Data:** `Mon Sep 14 09:52:12 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099436039169536325)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|Test-time compute scaling]] [[Harness|Chain-of-Thought]] [[Harness|Budżet rozumowania]] [[Harness|Destylacja modeli]] [[Stabilność modeli i przestrzeganie promptu|DeepSeek-R1]] [[Harness|Ollama]] [[Stabilność modeli i przestrzeganie promptu|Qwen]]

**Kontekst / Problem:**
Wpis przypomina wnioski z pracy DeepSeek-R1 (sekcje 2–3): długie rozumowanie podnosi wyniki z 71,0% do 86,7%, a destylacja długich łańcuchów myśli z R1 do małych modeli Qwen 1.5B/7B/14B pozwala uzyskać wzrost zdolności rozwiązywania zadań wraz z długością myślenia, jeśli zapewni się odpowiedni budżet rozumowania. Autor krytykuje zbiorową niepamięć oraz mylenie modeli destylowanych z oryginalnym DeepSeek-R1 w Ollama.

**Rada inżynierska:**
Traktuj długość myślenia jako sterowalny budżet obliczeniowy: w modelach rozumujących większa liczba tokenów CoT może przekładać się na wyższą dokładność. Destyluj długie łańcuchy myśli z dużego modelu do małych modeli (Qwen 1.5B/7B/14B) i zawsze raportuj użyty budżet rozumowania, bo bez niego benchmark jest nieporównywalny.

**Uwaga / Anty-wzorzec:**
Mylenie modelu destylowanego (deepseek-r1-distilled-qwen-7b) z oryginalnym DeepSeek-R1 i nazywanie go „DeepSeek” w Ollama. Prowadzi to do błędnych wniosków o skali, architekturze i rzeczywistych zdolnościach modelu źródłowego oraz do porównań bez kontroli budżetu rozumowania.

> **Cytat:** *"请读完了Section 2后继续看Section 3 . 明确写了模型在长思考时的表现. 当时震撼人心的继续从71.0% 飙升到 86.7% 就是这么来的. 然后将 R1 生成的长思维链蒸馏到了小模型（ Qwen-1.5B、7B、14B）。在运行时给足其思考预算，然后解题能力就呈现出与思考长度正相关的暴涨。这不就是去年的新闻嘛....怎么还能记不住呢....然后就ollama把deepseek-r1-distilled-qwen-7b 当deepseek给大家装到电脑上了, 美其名曰运行deepseek. 有印象没? 串起来了吧?"*

---

## Zachowanie modeli / Test-time compute / Destylacja

### Skalowanie test-time compute i destylacja długiego CoT: dlaczego modele distilled ≠ oryginalny R1

- **Data:** `Mon Sep 14 09:51:35 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099435885599367551)
- **Rodzaj:** Komentarz w dyskusji (@sosolab13)
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|Test-time compute]] [[Harness|Chain-of-Thought]] [[Harness|Destylacja wiedzy]] [[Harness|Budżet myślenia (thinking budget)]] [[Stabilność modeli i przestrzeganie promptu|DeepSeek R1]] [[Stabilność modeli i przestrzeganie promptu|Modele rozumujące (reasoning models)]] [[Harness|Ollama]] [[Harness|Rozróżnienie model bazowy vs destylowany]]

**Kontekst / Problem:**
Autor odpowiada pod cudzym wpisem, prostując nieporozumienie dotyczące publikacji DeepSeek R1. Wyjaśnia, że skok wyników z 71,0% do 86,7% (AIME) wziął się wprost z wydłużenia łańcucha myślenia (long thinking) — czyli z mechanizmu skalowania obliczeń w czasie wnioskowania (test-time compute), a nie z samej architektury. Następnie DeepSeek zdestylował wygenerowane przez R1 długie łańcuchy myślenia do małych modeli (Qwen-1.5B/7B/14B). Przy odpowiednio dużym budżecie myślenia (thinking budget) ich zdolność rozwiązywania zadań rosła gwałtownie, wprost proporcjonalnie do długości rozumowania.

**Rada inżynierska:**
Reguła inżynierska: wydajność modelu rozumującego jest funkcją przyznanego budżetu tokenów myślenia (test-time compute), a nie tylko liczby parametrów. (1) Skaluj czas wnioskowania — pozwól modelowi generować długie CoT, zanim wymusisz odpowiedź. (2) Długie CoT nauczyciela (R1) można destylować do małych modeli (1.5B–14B), które przy wystarczającym budżecie myślenia zbliżają się do dużych modeli rozumujących. (3) Przy dystrybucji i benchmarkach zawsze rozróżniaj model bazowy od modelu destylowanego — sprawdzaj nazwę i kartę modelu, nie marketingową etykietę.

**Uwaga / Anty-wzorzec:**
Myślenie, że pobierając przez ollama model 'deepseek-r1-distilled-qwen-7b' uruchamiasz oryginalnego DeepSeek R1. To w rzeczywistości model bazowy Qwen (1.5B/7B/14B) dostrojony na łańcuchach myślenia wygenerowanych przez R1 — zupełnie inny model niż pełny R1. Mieszanie tych pojęć prowadzi do błędnych wniosków o możliwościach i o porównaniach benchmarkowych. Dodatkowo: bez przyznania wystarczającego budżetu myślenia model destylowany traci swoją główną przewagę — efekt 'wzrostu z 71,0% do 86,7%' nie wystąpi, jeśli konfiguracja wnioskowania nie pozwoli na długie rozumowanie.

> **Cytat:** *"请读完了Section 2后继续看Section 3 . 明确写了模型在长思考时的表现. 当时震撼人心的继续从71.0% 飙升到 86.7% 就是这么来的. 然后将 R1 生成的长思维链蒸馏到了小模型（ Qwen-1.5B、7B、14B）。在运行时给足其思考预算，然后解题能力就呈现出与思考长度正相关的暴涨。这不就是去年的新闻嘛....怎么还能记不住呢....然后就ollama吧deepseek-r1-distilled-qwen-7b 当deepseek给大家装到电脑上了, 美其名曰运行deepseek. 有印象没? 串起来了吧?"*

---

## Inżynieria rozumowania / budżet tokenów / benchmarking agentowy

### Odwrócone skalowanie wysiłku rozumowania: dlaczego tryb „max” psuje wyniki SWE i czym jest kompresja informacji w modelach SOTA

- **Data:** `Mon Sep 14 09:14:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099426676669366337)
- **Rodzaj:** Komentarz w dyskusji (@karminski3)
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|Reasoning budget]] [[Harness|Thinking budget]] [[Harness|Inverted scaling]] [[Harness|SWE-bench]] [[Harness|Chain-of-Thought]] [[Harness|Early exit / stop condition]] [[Harness|Information compression as model quality]] [[Harness|Token efficiency]] [[Harness|Agent harness]] [[Stabilność modeli i przestrzeganie promptu|Benchmark contamination]]

**Kontekst / Problem:**
Autor odpowiada pod cudzym wpisem, odsyłając do trzech prac/analiz: (1) dlaczego ustawienie maksymalnego wysiłku rozumowania (reasoning effort / thinking budget = max) prowadzi do ODWRÓCONEGO (倒挂) skalowania na benchmarku SWE — tj. wyniki są gorsze niż przy niższym budżecie; (2) czy „max” jest w ogóle właściwym ustawieniem; (3) jak nauczyć model POPRAWNIE PRZERWAĆ rozumowanie (kiedy przestać myśleć). Kontekst: praktyka agentowa na zadaniach typu SWE-bench, gdzie długie łańcuchy myśli nie przekładają się na rozwiązanie problemu.

**Rada inżynierska:**
Traktuj jakość modelu jako miarę KOMPRESJI INFORMACJI, nie ilości wygenerowanego rozumowania. Reguła inżynierska: optymalizuj metrykę „najtrudniejszy problem rozwiązanym przy minimalnej liczbie tokenów”, a nie „maksymalny budżet myślenia”. W harnessach agentowych NIE ustawiaj reasoning effort/thinking budget na sztywno na max — strojenie budżetu rozumowania jest hiperparametrem zadaniowym, bo przy zbyt dużym budżecie pojawia się odwrócenie wyników (inverted scaling) na zadaniach SWE. Równolegle zainwestuj w mechanizm warunkowego zatrzymania rozumowania (stop condition / early exit), aby model kończył łańcuch myśli dokładnie wtedy, gdy ma już rozwiązanie, a nie po wyczerpaniu budżetu. Referencja do aktualnych badań jest wymagana — autor odrzuca argumentację anegdotyczną („民科”, pseudonauka) na rzecz lektury prac.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: założenie „więcej myślenia = lepszy wynik” i bezrefleksyjne ustawianie reasoning effort/thinking budget na max. Skutek: odwrócone skalowanie na SWE, marnowanie tokenów, wyższa latencja i koszt bez zysku jakościowego. Drugi anty-wzorzec: model, który nie umie samodzielnie przerwać rozumowania i „myśli w nieskończoność”, produkując długi wywód zamiast zwięzłego, poprawnego rozwiązania (autor ironicznie: dojście do „ostatecznej odpowiedzi wszechświata = 42” nie jest SOTA — SOTA to E = mc², czyli maksymalna kompresja).

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor podważa dominujący konsensus branżowy, że zwiększanie budżetu rozumowania (reasoning effort = max, dłuższe chain-of-thought) monotonicznie poprawia jakość. Twierdzi, że na SWE-bench występuje inwersja (wyniki przy „max” są gorsze), a prawdziwym wyznacznikiem SOTA jest minimalizacja tokenów przy maksymalnej trudności zadania (model jako „perfekcyjny kompresor informacji”). Do rozstrzygnięcia: (a) czy odwrócenie jest artefaktem konkretnego benchmarku/harnessu i konkretnej rodziny modeli, czy zjawiskiem ogólnym; (b) jaki mechanizm zatrzymywania rozumowania (kryterium stopu, weryfikator zewnętrzny, sygnał pewności) daje najlepszy kompromis jakość/koszt; (c) czy teza o „kompresji informacji” jest falsyfikowalną metryką, czy tylko metaforą.

> **Cytat:** *"来, 走出民科, 咱们阅读论文.  

为什么max测SWE会倒挂：https://t.co/9cV5oLJLLH

设置为max真的就对吗：https://t.co/7QgZzJws0W

到底怎样才能让模型思考的时候正确的停下来: https://t.co/m1M1t03vJi  

我重申我的观点, SOTA的模型永远是完美的信息压缩器. 用最少的token解决最难的问题. 思考一大堆得出宇宙的最终解是42不是SOTA. E = mc² 才是. 

上次的讨论: https://t.co/HK6fCYvgwu"*

---

## Inżynieria rozumowania / konfiguracja modeli reasoning

### Dlaczego ustawienie maksymalnego budżetu rozumowania (max effort) psuje wyniki SWE-bench i kiedy model powinien przestać myśleć

- **Data:** `Mon Sep 14 08:52:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099421138069950509)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|Reasoning Effort / Thinking Budget]] [[Harness|SWE-bench]] [[Harness|Chain-of-Thought]] [[Stabilność modeli i przestrzeganie promptu|Test-time compute scaling]] [[Harness|Model stop conditions]] [[Harness|Information compression in LLM]]

**Kontekst / Problem:**
Autor odnosi się do zjawiska 'odwrócenia' (倒挂) wyników na benchmarku SWE-bench, gdy model reasoning konfiguruje się z maksymalnym budżetem myślenia / maksymalnym reasoning effort. Zamiast poprawy wyników, dłuższe rozumowanie prowadzi do regresji. Autor podnosi dwa pytania: (1) czy 'max' jest zawsze optymalnym ustawieniem, (2) jak sprawić, aby proces rozumowania modelu zatrzymywał się w odpowiednim momencie, zamiast generować nieskończenie długie, rozwlekłe łańcuchy myśli. Podaje linki do prac naukowych i wzywa do odejścia od 'naukowej amatorszczyzny' na rzecz czytania źródeł.

**Rada inżynierska:**
Nie traktuj 'max reasoning effort' jako domyślnej, bezpiecznej wartości. Budżet myślenia należy kalibrować per zadanie, a mechanizm zatrzymania rozumowania powinien być trenowany/projektowany świadomie (model musi umieć 'przestać myśleć' w momencie uzyskania odpowiedzi). Kluczowa reguła inżynierska: SOTA to model będący doskonałym kompresorem informacji — rozwiązuje najtrudniejszy problem przy minimalnej liczbie tokenów. E = mc² a nie rozwlekła analiza dochodząca do '42'.

**Uwaga / Anty-wzorzec:**
Ślepe ustawianie maksymalnego budżetu rozumowania ('more thinking = better') oraz fetyszyzowanie długich łańcuchów myśli. Anty-wzorzec: ocenianie jakości modelu po liczbie rozumowanych tokenów; rozwlekły reasoning nie jest oznaką jakości, a wręcz koreluje z regresją na zadaniach rzeczywistych (SWE-bench).

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Teza autora stoi w sprzeczności z dominującą narracją branżową o skalowaniu test-time compute ('im dłużej model myśli, tym lepiej'). Autor twierdzi, że maksymalny budżet rozumowania powoduje odwrócenie wyników (regresję) na SWE-bench, a miarą jakości nie jest długość reasoning, lecz kompresja informacji — minimalny koszt tokenowy dla najtrudniejszego problemu. Do rozstrzygnięcia: czy regresja 'max' wynika z przetrenowania/overthinking danego modelu, czy jest to uniwersalne prawo, oraz jaki jest optymalny mechanizm zatrzymania rozumowania.

> **Cytat:** *"来, 走出民科, 咱们阅读论文. 
为什么max测SWE会倒挂：https://t.co/9cV5oLJLLH
设置为max真的就对吗：https://t.co/7QgZzJws0W
到底怎样才能让模型思考的时候正确的停下来: https://t.co/m1M1t03vJi 
我重申我的观点, SOTA的模型永远是完美的信息压缩器. 用最少的token解决最难的问题. 思考一大堆得出宇宙的最终解是42不是SOTA. E = mc² 才是."*

---

## Zachowanie modeli / Test-time compute (scaling rozumowania)

### Intensywność rozumowania (thinking budget) a wyniki modelu — więcej myślenia = wyższa skuteczność

- **Data:** `Mon Sep 14 07:14:23 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099396323942547519)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|Test-time compute]] [[Harness|Chain of Thought]] [[Harness|Long CoT]] [[Stabilność modeli i przestrzeganie promptu|Reasoning budget]] [[Stabilność modeli i przestrzeganie promptu|DeepSeek-R1-Zero]] [[Harness|RL bez SFT]] [[Stabilność modeli i przestrzeganie promptu|AIME24 benchmark]] [[Harness|Model rozumujący]]

**Kontekst / Problem:**
Autor przetestował model deepseek-v4.1-flash z ustawieniem intensywności rozumowania na 'max', po czym spotkał się z zarzutem, że powinien użyć 'high', a nie 'max', oraz z tezą, że przełącznik intensywności myślenia nie ma związku z wydajnością. Problem dotyczy tego, jak parametr thinking budget wpływa na rzeczywistą jakość odpowiedzi modeli rozumujących oraz jak łatwo bagatelizuje się to zjawisko w dyskusjach społecznościowych.

**Rada inżynierska:**
Traktuj intensywność rozumowania (thinking budget / reasoning effort) jako realny czynnik wpływający na jakość, a nie kosmetyczny przełącznik. Wyższy budżet myślenia => dłuższy łańcuch rozumowania (long CoT) => wyższe wyniki na zadaniach wymagających rozumowania. Fundamentem tego jest DeepSeek-R1-Zero: czysty RL bez SFT i bez dodawania nowej wiedzy, gdzie samo wydłużenie rozumowania podniosło wynik AIME24 z ~15% do ~71%. To dowód na test-time compute scaling — moc obliczeniowa inwestowana w czasie inferencji przekłada się na zdolności rozumowania. Przed formułowaniem tez o zachowaniu modelu zawsze weryfikuj oryginalne prace (np. DeepSeek-R1-Zero), zamiast opierać się na anegdotach z komentarzy.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: dyskutowanie o parametrach modelu na podstawie przeczucia lub zasłyszanej opinii ('high jest lepsze niż max') bez znajomości literatury i bez własnych, powtarzalnych pomiarów. Drugi anty-wzorzec: mylenie przełącznika intensywności rozumowania z nieistotnym ustawieniem — prowadzi to do systematycznego niedoszacowania potencjału modelu i błędnych wniosków porównawczych. Autor porównuje to do kupienia Ferrari i rezygnacji z wyższego biegu 'bo tak szybciej'.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Spór z tezą części społeczności (tzw. 'DS民科'), że ustawienie intensywności rozumowania na 'high' jest lepsze niż 'max' oraz że przełącznik intensywności myślenia nie wpływa na wydajność. Autor odrzuca ten pogląd, powołując się na DeepSeek-R1-Zero (wzrost AIME24 z 15% do 71% wraz z długością rozumowania). Do rozstrzygnięcia: czy istnieją warunki (np. przesycenie/overthinking, dryf, koszt latencji), w których nadmierny budżet myślenia szkodzi wynikom — warto zweryfikować empirycznie dla konkretnych modeli i zadań.

> **Cytat:** *"DS民科怎么这么多, 我测完了 deepseek-v4.1-flash, 开 max, 然后评论跟我说应该开high, 不应该开max. ... 就这个论文证明了思考强度越强模型能力越强的. 论文里Zero-SFT RL了一波, 没有增加任何新知识, 随着思考长度增加, AIME24 跑分就从 15% 魔法般的飙到了 71%."*

---

## Architektura skilli / systemy agentowe / metaprogramowanie

### Izomorfizm kodu i danych w skillach: metaprogramowanie Micro-Skills do ekstrakcji danych

- **Data:** `Mon Sep 14 06:23:09 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099383433034440811)
- **Rodzaj:** Komentarz w dyskusji (@kalasoo)
- **Powiązane pojęcia:** [[Harness|Micro-Skill]] [[Harness|Izomorfizm kodu i danych]] [[Harness|Metaprogramowanie agentowe]] [[Harness|Pydantic]] [[Harness|Harness walidacyjny]] [[Harness|Ekstrakcja danych z dokumentów]] [[Harness|Dynamiczne generowanie promptów]]

**Kontekst / Problem:**
Autor odpowiada pod wpisem @kalasoo, rozwijając tezę, że tradycyjne dokumenty są zwykle albo [kodem], albo [danymi] — tylko jednym z dwóch. Skille (agent skills) mają jednak właściwość izomorfizmu kodu i danych: ten sam artefakt może jednocześnie opisywać strukturę danych i logikę przetwarzania. Problem: większość ludzi pisze skille jak dokumenty — wpisuje z góry zdefiniowany format (np. 'wyciągnij datę i kwotę faktury według poniższego wzoru') i taki skill pęka, gdy pojawi się format spoza wzorca. Rozwiązaniem jest potraktowanie skilla jako programu generującego programy (metaprogramowanie): model analizuje konkretny przypadek i dynamicznie tworzy dopasowany Micro-Skill.

**Rada inżynierska:**
Traktuj skill jako metaprogram, a nie statyczny dokument z wklejonym formatem. Zamiast hardkodować reguły ekstrakcji, każ modelowi: (1) przeanalizować topologię układu i konwencje nazewnicze konkretnego dokumentu, (2) NIE zwracać od razu wyniku JSON, lecz dynamicznie wygenerować wyspecjalizowany Micro-Skill i go uruchomić, (3) rozdzielić pracę: pola deterministyczne wyekstrahować regexem skompilowanym do klasycznego kodu, a pola niejednoznaczne zostawić LLM-owi z ultra-zwięzłym promptem (limit znaków, np. ≤50), (4) wygenerować klasę walidacji Pydantic jako lekki harness sprawdzający spójność (np. kwota_z_podatkiem == kwota_bez_podatku + podatek). Dzięki temu skill nie wymaga ręcznej aktualizacji — jego poprawność zależy tylko od inteligencji modelu.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: pisanie skilla jak dokumentu — statyczne wklejenie jednego wzorca formatu i polecenie 'wyciągnij te pola zgodnie z poniższym schematem'. Taki skill działa wyłącznie na znanych formatach i 'wybucha' przy pierwszej niespotykanej strukturze. Drugi błąd: wymuszanie natychmiastowego wyjścia JSON zamiast generowania dopasowanego programu — to marnuje potencjał izomorfizmu kodu i danych i blokuje metaprogramowanie.

> **Cytat:** *"传统文档大多数时间只是【代码】或【数据】其中的一种. 而skill能实现代码与数据同构的特性.

比如写一个处理发票的skill, 大部分人只会写:

"帮我按照下面的格式提取发票日期, 金额"

万一遇到个skill中没有的格式就炸了. 这其实就是把skill写成了文档.

而理解了skill的同构性就能玩元编程:

"分析这张发票的排版拓扑和命名惯例, 不要直接输出 JSON 结果, 动态生成一个专用的skill(Micro-Skill)并运行它来提取配置, 包括:
哪些字段可以通过正则表达式确定性提取(编译为传统代码).
哪些歧义字段需要 LLM 提取, 并生成一份不超过 50 字的超精简 Prompt.
生成严格验证该格式的 Pydantic 校验类(简单harness, 类似含税金额 == 不含税金额 + 税额). "

这样这个skill只要模型够聪明就不用管了."*

---

## Architektura agentowa / Prompt Architecture

### Skill jako kod: izomorfizm kodu i danych oraz dynamiczne mikro-skille

- **Data:** `Mon Sep 14 06:22:54 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099383368999965122)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Skill]] [[Harness|Micro-Skill]] [[Harness|Izomorfizm kodu i danych]] [[Harness|Metaprogramowanie promptów]] [[Harness|Ekstrakcja deterministyczna]] [[Harness|Regex vs LLM]] [[Harness|Pydantic]] [[Harness|Harness weryfikacyjny]] [[Harness|Walidacja semantyczna]] [[Context Compaction|Inżynieria kontekstu]]

**Kontekst / Problem:**
Autor diagnozuje fundamentalny problem projektowania skilli dla agentów LLM: większość ludzi pisze skille jak dokumenty — statyczne instrukcje z wbudowanym z góry założonym formatem wejścia (np. 'wyciągnij datę i kwotę faktury według poniższego schematu'). Takie skille działają wyłącznie dla formatów przewidzianych przez autora, a przy nieznanej strukturze wejścia (inny layout faktury, inna konwencja nazewnictwa) całkowicie zawodzą. Autor proponuje odejście od paradygmatu 'skill = dokument' na rzecz 'skill = kod', wykorzystując izomorfizm kodu i danych: skill może sam siebie generować, kompilować i walidować w czasie wykonania.

**Rada inżynierska:**
Projektuj skille jako programy zdolne do metaprogramowania, a nie jako statyczne dokumenty. Zamiast z góry zakodowanego schematu ekstrakcji, prompt powinien zlecić modelowi najpierw analizę topologii układu i konwencji nazewnictwa wejścia, a następnie dynamiczne wygenerowanie dedykowanego mikro-skilla (Micro-Skill) dla tego konkretnego przypadku. Generowany mikro-skill powinien rozdzielać pracę na trzy warstwy: (1) pola deterministyczne → kompilowane do kodu (regex), (2) pola niejednoznaczne → ultra-zwięzły prompt LLM (limit ~50 znaków/słów), (3) walidacja → klasa Pydantic jako lekki harness sprawdzający spójność semantyczną (np. kwota z VAT == kwota netto + podatek). Taki skill staje się samoregulujący — jego poprawność zależy już tylko od zdolności modelu, a nie od przewidzenia z góry wszystkich formatów wejściowych.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: 'skill pisany jak dokument'. Wbudowanie na sztywno konkretnego formatu wejścia i schematu wyjścia w treść promptu. Objawia się tym, że skill działa świetnie na danych treningowych/przykładowych, ale 'wybucha' (błąd lub halucynacja) przy pierwszym nieprzewidzianym formacie. Drugi antywzorzec: wymuszanie, by LLM wykonywał deterministyczną ekstrakcję, którą trywialnie rozwiązałby regex — marnuje tokeny i wprowadza niedeterminizm tam, gdzie nie jest potrzebny. Brak harnessu walidacyjnego sprawia, że błędnie wyekstrahowane dane przechodzą dalej bez wykrycia niespójności.

> **Cytat:** *"传统文档大多数时间只是【代码】或【数据】其中的一种. 而skill能实现代码与数据同构的特性. 比如写一个处理发票的skill, 大部分人只会写: "帮我按照下面的格式提取发票日期, 金额" 万一遇到个skill中没有的格式就炸了. 这其实就是把skill写成了文档. 而理解了skill的同构性就能玩元编程: "分析这张发票的排版拓扑和命名惯例, 不要直接输出 JSON 结果, 动态生成一个专用的skill(Micro-Skill)并运行它来提取配置, 包括: 哪些字段可以通过正则表达式确定性提取(编译为传统代码). 哪些歧义字段需要 LLM 提取, 并生成一份不超过 50 字的超精简 Prompt. 生成严格验证该格式的 Pydantic 校验类(简单harness, 类似含税金额 == 不含税金额 + 税额). " 这样这个skill只要模型够聪明就不用管了."*

---

## Benchmarki LLM / Agentic Coding / Dobór modeli

### Stabilność vs SOTA w agentowym kodowaniu backendu: benchmark implementacji bazy wektorowej

- **Data:** `Mon Sep 14 05:50:26 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099375198986461418)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|Benchmarkowanie LLM]] [[Harness|Agentic Coding]] [[Harness|Wariancja wyników modeli]] [[Harness|Stabilność post-trainingu]] [[Harness|Koszt tokenów]] [[Harness|Prompt Engineering]] [[Harness|Vector Database]] [[Stabilność modeli i przestrzeganie promptu|DeepSeek-V4.1-Flash]] [[Harness|GPT6-Astra]] [[Harness|Fable-5.1]] [[Harness|Kimi-K3]] [[Harness|Hy4-dev]]

**Kontekst / Problem:**
Autor porównuje modele w wąskim, praktycznym scenariuszu AgenticCoding: implementacja bazy wektorowej od zera i ocena przez wydajność bazy. Wyniki pokazują, że najwyższy szczytowy wynik (Fable-5.1) nie jest jednoznacznie najlepszym wyborem produkcyjnym, bo model ma ogromny rozrzut między próbami, podczas gdy GPT6-Astra jest znacznie bardziej stabilny, a DeepSeek-V4.1-Flash oferuje najlepszy stosunek jakości do kosztu w prostych zadaniach.

**Rada inżynierska:**
Oceniaj modele do agentowego kodowania nie tylko po maksymalnym wyniku, lecz przede wszystkim po wariancji wyników między powtórzeniami. Do prostych zadań backendowych wybieraj stabilny i tani model, np. DeepSeek-V4.1-Flash; do złożonych zadań sięgaj po GPT6-Astra jako stabilny wybór albo po Fable-5.1 tylko wtedy, gdy masz doświadczenie w prompt engineeringu i akceptujesz konieczność wielokrotnego próbkowania. Stabilność modelu przekłada się bezpośrednio na przewidywalność harnessu, zużycie tokenów i koszt iteracji.

**Uwaga / Anty-wzorzec:**
Wybór modelu wyłącznie na podstawie pojedynczego najlepszego wyniku lub pozycji „SOTA” w rankingu. Ignorowanie rozrzutu między próbami prowadzi do przepalania tokenów na repeated sampling, niestabilnych wyników agenta i trudności w reprodukcji zachowania systemu. Wysokowariancyjny model bez dopracowanego promptu może wypaść znacznie poniżej swojego potencjału.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor podważa proste podejście „wybieraj model SOTA z leaderboardu”. W jego benchmarku Fable-5.1 ma najwyższy szczytowy wynik, ale jednocześnie bardzo dużą wariancję między próbami, przez co w praktyce bardziej opłacalny bywa stabilniejszy GPT6-Astra lub tańszy DeepSeek-V4.1-Flash. To kontrastuje z typowym optymizmem benchmarkowym, gdzie liczy się głównie maksymalny wynik, a nie powtarzalność.

> **Cytat:** *"就结论来说, 单纯后端 AgenticCoding 场景(注意我只说我这个测试, 用大模型从0实现向量数据库, 使用数据库性能计分. 别的我不知道). 目前Fable-5.1 还是SOTA. 写出来的向量数据库直接是第二名的2x。... 所以从省token的角度, 其实更推荐使用 GPT6-Astra. 因为发挥稳定, 不需要重复抽卡. 而 Fable-5.1 更适合经验丰富的工程师好好写提示词后再使用。... 另外最具性价比无疑是 DeepSeek-V4.1-Flash. 得分几乎跟 kimi-k3没区别了. 而且Δ<20%. 所以只要不是复杂的代码任务, 直接无脑 DeepSeek-V4.1-Flash最划算. 而复杂的尝试使用GPT6-Astra 和 Fable-5.1."*

---

## Benchmarking modeli / Systemy agentowe

### Dobór reasoning_effort i runtime (llama.cpp vs MLX) dla małych modeli agentowych — wyniki testów na H100 NVL

- **Data:** `Mon Aug 31 08:26:49 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2094341123124985991)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|reasoning_effort]] [[Harness|llama.cpp]] [[Harness|MLX]] [[Harness|MTP (Multi-Token Prediction)]] [[Harness|Kwantyzacja Q4_K_XL]] [[Stabilność modeli i przestrzeganie promptu|Qwen3]] [[Harness|Małe modele agentowe]] [[Stabilność modeli i przestrzeganie promptu|Benchmark LLM]] [[Harness|H100 NVL]]

**Kontekst / Problem:**
Autor opublikował ranking (drabinkę) zdolności agentowych małych modeli LLM, testowanych w jednolitym środowisku: pojedyncza karta H100 NVL + najnowsza wersja llama.cpp. Celem jest wskazanie praktycznie użytecznego modelu i konfiguracji do zadań agentowych oraz kodowania, a także dobór właściwego runtime'u w zależności od platformy sprzętowej.

**Rada inżynierska:**
Reguły inżynierskie wynikające z testów: (1) Najbardziej opłacalny w użyciu okazał się Qwen3.8-27B w wariancie kwantyzacji UD-Q4_K_XL. (2) Poziom reasoning_effort należy różnicować per zadanie — dla pracy agentowej ustawiać low, natomiast dla generowania kodu medium lub high. (3) Runtime dobierać do platformy: na Macach preferować MLX zamiast llama.cpp, ponieważ MLX z włączonym MTP (Multi-Token Prediction) wypada w praktyce szybciej niż llama.cpp z MTP na tym samym sprzęcie. (4) Benchmarki prowadzić na jednolitym stacku (jedna karta H100 NVL + najnowszy llama.cpp), aby wyniki były porównywalne między modelami.

**Uwaga / Anty-wzorzec:**
Stosowanie jednego, globalnego poziomu reasoning_effort do wszystkich zadań — obniża to efektywność agenta (nadmiar rozumowania przy prostych krokach) albo jakość kodu (niedostateczne rozumowanie przy złożonych zmianach). Drugi anty-wzorzec: uruchamianie llama.cpp na macOS bez porównania z MLX+MTP, co skutkuje niepotrzebnie niższym throughputem wnioskowania.

> **Cytat:** *"小模型 Agent 能力测试的天梯在这里~ ... 目前来看最值得使用是我测试的 Qwen3.8-27B-UD-Q4_K_XL 版本, Agent 用使用 reasoning_effort = low, 然后写代码开到 medium / high. 另外文中是统一使用单卡 H100 NVL+llama.cpp 最新版本测试的. 如果是Mac用户还是建议优先使用MLX, 实测 MLX 开 MTP 会比 llama.cpp 放在 Mac 上开MTP要快一些."*

---

## Benchmarking i ewaluacja modeli

### Arena małych modeli: kwantyzacja × MTP × poziom rozumowania w benchmarku pass@3

- **Data:** `Mon Aug 31 06:27:32 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2094311103987581033)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|pass@k]] [[Harness|Kwantyzacja modeli LLM]] [[Harness|MTP (Multi-Token Prediction)]] [[Harness|Thinking budget / poziom rozumowania]] [[Harness|MoE (Mixture of Experts)]] [[Stabilność modeli i przestrzeganie promptu|Benchmarkowanie agentów]] [[Harness|Małe modele open-source]]

**Kontekst / Problem:**
Autor przeprowadził kompleksowy benchmark porównawczy 8 małych modeli open-source (rodziny Qwen3.8/3.6, Gemma-4, Ornith-1.5, GPT-OSS-20B) w konfiguracjach MoE (A3B/A4B) oraz gęstych. Celem było ustalenie, który model jest faktycznie najlepszy w praktycznych zadaniach inżynierskich (frontend, Python, zdolności agentowe), przy jednoczesnej kontroli zmiennych takich jak poziom kwantyzacji, włączony/wyłączony MTP (Multi-Token Prediction) oraz trzy poziomy intensywności rozumowania (low/medium/xhigh).

**Rada inżynierska:**
Przy ewaluacji modeli należy kontrolować jednocześnie kilka osi zmiennych, które istotnie wpływają na wynik: (1) liczbę wariantów kwantyzacji — 4 poziomy na model, (2) MTP on/off, (3) poziom rozumowania low/medium/xhigh. Wynik należy agregować jako pass@3 (3 przebiegi, brany najlepszy), co redukuje wariancję stochastyczną i lepiej odzwierciedla praktyczne użycie. Sam sprzęt (H100) wpływa wyłącznie na szybkość generacji, nie na jakość — dlatego dobiera się go pod przepustowość, nie pod wierność wyników. Realny koszt pełnego, wieloosiowego benchmarku małego modelu to ok. 148 USD i ~48 godzin nawet na H100.

**Uwaga / Anty-wzorzec:**
Częstym błędem jest porównywanie modeli przy niespójnych konfiguracjach: pomijanie różnic w kwantyzacji, w rozumowaniu (thinking budget) lub w MTP on/off prowadzi do fałszywych wniosków o 'lepszym modelu'. Anty-wzorcem jest także raportowanie pojedynczego przebiegu (pass@1) bez uśredniania/pass@3 — wariancja generacji maskuje rzeczywiste różnice zdolności. Dodatkowo: mylenie wpływu sprzętu (GPU) z jakością generacji prowadzi do niepotrzebnych kosztów — H100 skraca czas, ale nie zmienia wyniku.

> **Cytat:** *"终于搞完了! 给大家带来小模型竞技场, 这次测试了8款模型... 每个模型4个量化版本, 还测试了 MTP 开启和关闭, 以及 low, medium, xhigh 三档思考强度, 做了个全面横评. 测试主要集中在前端, python, Agent 能力上, 每个测试运行3次取最佳结果(pass@3). 测试使用H100显卡(注意用H100是为了生成快, 就这还跑了48小时, 显卡不影响生成效果, 只影响生成速度), 总成本148刀."*

---

## Multimodalne systemy agentowe / architektura harnessów

### Qwen3.8-Omni-Flash, Live-Harness i MM-Plugins: multimodalny harness, tanie audio i skill-learning z wideo

- **Data:** `Fri Sep 18 00:57:36 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2100751056104026497)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|Qwen3.8-Omni-Flash]] [[Harness|Qwen-Live-Harness]] [[Stabilność modeli i przestrzeganie promptu|Qwen-MM-Plugins]] [[Harness|Multimodalne modele językowe]] [[Harness|Agent harness]] [[Harness|Skill learning z demonstracji]] [[Harness|omni-skill-creator]] [[Harness|Realtime multimodal API]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Task board dla agentów]]

**Kontekst / Problem:**
Premiera Qwen3.8-Omni-Flash oraz dwóch frameworków: Qwen-Live-Harness i Qwen-MM-Plugins. Model poprawia średnie wyniki o 25% względem Qwen3.5-omni-flash, ze szczególnie dużym wzrostem w Agent abilities. Redukuje WER dla nakładającej się mowy wielu osób z 88% do 3%, wspiera do 1 godziny ciągłego audio-wideo, obniża koszt audio o 98% (18 CNY → 0,8 CNY za 1M tokenów) i oferuje wariant Realtime z latencją ok. 981 ms dla 20 s audio. Harness dodaje悬浮球 do interakcji, monitoring środowiska, task board i śledzenie zadań. MM-Plugins integrują Qwen Omni z Claude Code, Gemini CLI, Codex i OpenClaw, uzupełniając lokalne agenty o wizję, pamięć długich wideo oraz sterowanie Blender/CAD. omni-skill-creator uczy umiejętności z nagrania wideo z narracją głosową.

**Rada inżynierska:**
Projektuj agenta jako trzy warstwy: model omnimodalny, harness orkiestrujący zadania oraz plugin do istniejącego CLI. Do tworzenia skilli używaj demonstracji wideo połączonej z narracją głosową wyjaśniającą intencję, bo model omnimodalny wiąże percepcję, uzasadnienie i akcję. Wariant Realtime stosuj tylko tam, gdzie niska latencja jest krytyczna; w pozostałych przypadkach korzystaj z Flash dla kosztu.

**Uwaga / Anty-wzorzec:**
Nie zakładaj, że automatycznie wygenerowany skill z wideo jest gotowy produkcyjnie. Brak reprezentatywnych nagrań, weryfikatora i sprzężenia zwrotnego grozi kruchymi umiejętnościami w Blender/CAD oraz overfittingiem do jednej demonstracji. Benchmarki producenta dla WER, kosztu i Agent abilities wymagają walidacji na własnej domenie.

> **Cytat:** *"Qwen 刚刚发布了 Qwen3.8-Omni-Flash! 同时还发布了两个配套框架, Qwen-Live-Harness, Qwen-MM-Plugins. ... 原生支持最长 1 小时的完整连续音视频输入, 并且API费用降低了98%. 98%是什么概念? 之前音频输入每百万token是18块, 现在是0.8元! ... Qwen-Live-Harness 搞了个悬浮球, 点击后就可以与模型对话了, 它还能做到环境监控 ... 而Qwen-MM-Plugins则是个"赋能"插件库, 可以给 Claude Code、Gemini CLI、Codex、OpenClaw 安装, 装之后就可以多模态的调用 Qwen3.8-Omni-Flash 了. ... 里面还弄了个特别有意思的叫 omni-skill-creator, 只需要录一段操作软件的视频, 然后丢给它, 他就能帮你形成操作这个软件的skill! ... 模型是全模态的, 所以录视频的时候还可以把自己的语音一起录进去, 告诉模型为什么这么做, 加深模型的理解, 创建出来的skill更准确."*

---

## Inżynieria kontekstu / Analiza wideo z LLM

### Dwupoziomowa strategia próbkowania klatek w analizie wideo przez modele multimodalne

- **Data:** `Fri Aug 21 17:49:35 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2090858868989706352)
- **Rodzaj:** Komentarz w dyskusji (@karminski3)
- **Powiązane pojęcia:** [[Harness|Multimodalne modele językowe]] [[Harness|image_url]] [[Harness|Dekompozycja wideo na klatki]] [[Harness|Dwupoziomowe próbkowanie klatek]] [[Harness|Event window sampling]] [[Context Compaction|Zarządzanie kontekstem]] [[Harness|Vision-LLM]] [[Prompt Architecture|Prompt architecture]]

**Kontekst / Problem:**
Problem: jak skutecznie przekazywać modele multimodalnemu (vision-LLM) treść wideo, aby uzyskać precyzyjną analizę zarówno scen statycznych, jak i szybkich akcji (np. strzelanie w CS2). Autor eksperymentuje z różnymi schematami próbkowania klatek i porównuje jakość rozpoznawania modelu.

**Rada inżynierska:**
Zamiast wysyłać wideo w formacie natywnym, dekomponuj je na klatki JPEG/PNG i przekazuj je sekwencyjnie jako wiele wpisów `image_url` w porządku chronologicznym. W prompcie jawnie deklaruj współczynnik próbkowania (sampling rate) oraz oś czasu (timeline), aby model poprawnie zinterpretował odstępy między klatkami. Dla materiałów z szybką akcją stosuj próbkowanie dwupoziomowe: (1) makro — 1 fps na całym materiale w celu uzyskania kontekstu globalnego oraz (2) mikro — okna zdarzeń (event windows) próbkowane z wysoką częstotliwością i w dodatku przycięte/powiększone do centrum akcji (center zoom). Takie podejście daje lepszą jakość niż jednorodne próbkowanie całego nagrania ze stałą, wysoką częstotliwością.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: jednorodne (uniform) próbkowanie całego wideo ze stałą częstotliwością. Powoduje to albo pominięcie kluczowych momentów szybkiej akcji (przy niskim fps), albo eksplozję liczby klatek i zużycia kontekstu/tokenów bez proporcjonalnego wzrostu jakości (przy wysokim fps). Brak jawnego podania sampling rate i timeline w prompcie prowadzi do błędnej interpretacji przez model — nie wie on, jaki odstęp czasu reprezentują kolejne klatki, co zaburza wnioskowanie o dynamice zdarzeń.

> **Cytat:** *"把视频抽成 JPEG/PNG, 按时间顺序作为多个 `image_url` 传入, 并在 prompt 里写明采样率和时间轴. 这样分析会更准确. 我使用了一个猫和老鼠的片段进行分析, 这样做模型识别很准确. 另外, 我还用了一段 CS2 录像来验证分析快速动作时的最佳方案, 结论是不要匀速抽全片, 用「宏观 1fps 全图 + 事件窗口高帧率中心放大」两级采样。效果会更好. 详细教程和POV开源在这里: https://t.co/DaeLlbTySr"*

---

## Multimodalność / Inżynieria wejścia (Vision-Language)

### Obsługa wideo modelem deepseek-v4-flash-vision-exp przez ekstrakcję klatek (bez wejścia audio)

- **Data:** `Fri Aug 21 17:49:34 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2090858863679750280)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|DeepSeek V4 Flash Vision]] [[Harness|Ekstrakcja klatek]] [[Harness|Modele vision-language]] [[Harness|Multimodalność]] [[Harness|GIF]] [[Harness|ASR]] [[Harness|Pipeline wideo]]

**Kontekst / Problem:**
DeepSeek wypuścił deepseek-v4-flash-vision-exp — swój pierwszy duży model multimodalny na poziomie możliwości v4-flash. Model 'przestał być ślepy', ale nadal nie obsługuje audio (brak wejścia dźwiękowego), a ani oficjalna strona DeepSeek, ani API nie przyjmują wideo. Powstaje więc luka integracyjna: jak przetwarzać materiały wideo, skoro natywny pipeline tego nie wspiera. Autor opisuje obejście oparte na dekodowaniu wideo po stronie aplikacji i podawaniu modelowi pojedynczych klatek jako obrazów.

**Rada inżynierska:**
Wideo podawane do modelu vision należy najpierw zdekodować do sekwencji klatek (frame extraction) i wysyłać jako osobne obrazy — to jedyna działająca ścieżka, dopóki API/strona nie wspierają wideo natywnie. Nie wolno używać GIF-a jako kontenera na wideo: mimo że model formalnie akceptuje wejście GIF, przetwarza wyłącznie pierwszą klatkę (autor potwierdził to empirycznie kodem). Przy projektowaniu pipeline'u multimodalnego trzeba więc rozdzielić kanały: obraz (obsługiwany), wideo (do emulacji przez klatki), audio (nieobsługiwane — wymaga zewnętrznego ASR i doklejenia transkrypcji do kontekstu).

**Uwaga / Anty-wzorzec:**
Konwersja wideo do GIF-a w celu 'oszukania' modelu — kończy się analizą tylko pierwszej klatki i cichą utratą całej treści temporalnej (błąd trudny do wykrycia, bo model zwraca sensowną odpowiedź na podstawie jednego kadru). Drugi anty-wzorzec: założenie, że 'multimodalny' = pełny zestaw modalności — brak audio oznacza konieczność osobnego etapu transkrypcji, inaczej model nie ma dostępu do warstwy dźwiękowej.

> **Cytat:** *"给大家写了个 deepseek-v4-flash-vision-exp 输入视频教程

deepseek 最近真的是高产, 刚刚又发了 deepseek-v4-flash-vision-exp, 首个多模态【大】模型. 而且是 v4-flash 能力级别的. 但是! 虽然不是瞎子了, 但是还是听力有问题, 不支持音频输入. 所以默认 deepseek 官网和API都不支持视频输入, 于是给大家写了个小教程, 如何使用这个模型处理视频.

简单来讲, 方法就是直接把视频抽帧. 而且需要注意, 虽然模型支持gif输入, 但是它只识别 gif 的第一帧(我写代码验证了). 所以把视频转换为gif是行不通的."*

---
