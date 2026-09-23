---
autor: "@karminski3"
źródło: "https://x.com/karminski3"
wygenerowano: "2026-09-23 02:25"
typ: synteza-wiedzy
tagi:
  - karminski3
  - ai-engineering
  - prompt-engineering
  - twitter-extract
---

# @karminski3 — Baza Wskazówek i Komentarzy

> Destylacja praktycznych porad, heurystyk inżynierskich i komentarzy technicznych z profilu @karminski3 na platformie X. Wyciągnięto 26 wartościowych wpisów.

## ⚠️ Kwestie sporne i rozbieżności do rozstrzygnięcia

> Wpisy, w których autor podważa powszechne przekonania branżowe lub prezentuje tezy stojące w sprzeczności z innymi praktykami:

- **[Claude Opus 5.5 vs Fable 5.1: dystylacja wykryta przez wzrost zużycia tokenów rozumowania](https://x.com/karminski3/status/2102479290420048093):** Autor podważa dwa elementy konsensusu branżowego: (1) tezę, że nowe wydania modeli to niezależne architektury — sugeruje, że Opus 5.5 to kwantyzowana lub wewnętrznie dystylowana wersja Fable 5.1, co jest sprzeczne z marketingiem Anthropic o 'nowej generacji'; (2) praktykę komunikacyjną dostawcy — wprost oskarża Anthropic o '祖传' (dziedziczną) degradację jakości modeli w czasie (降智), co stoi w sprzeczności z deklaracjami o stałości zachowania wersjonowanych endpointów. Do rozstrzygnięcia wymaga niezależnych, powtarzalnych pomiarów: porównania rozkładu tokenów rozumowania, wyników na stałym zbiorze ewaluacyjnym w czasie oraz (jeśli dostępne) analizy wag/aktywacji.
- **[reasoning_effort jako marketing: przenoszenie kosztu obliczeń i ryzyka rozliczeniowego na użytkownika](https://x.com/karminski3/status/2099767043155218568):** Teza kontrowersyjna wobec konsensusu branżowego: autor twierdzi, że publiczne parametry reasoning_effort to narzędzie marketingowe producentów, które przenosi kompromis obliczeniowy i ryzyko rozliczeniowe na użytkownika, oraz że rozbieżność między 'thinking effort' a 'performance' wynika z niedostatków post-trainingu (a idealnie powinny być równoważne). Jego zdaniem komunikacja 'sweet spot = high' jest myląca i promuje przekonanie, że wysokie ustawienie jest optymalne. Sporny punkt do rozstrzygnięcia: czy parametry effort to neutralne narzędzie kontroli kosztu, czy narzędzie transferu ryzyka i kształtowania percepcji jakości modelu. Wniosek sprzeczny też praktycznie z zaleceniem komentatorów, by testować model tylko na 'high' — autor wskazuje, że taka konfiguracja jest niekompatybilna metodologicznie z benchmarkami prowadzonymi na 'max'. Zgodnie z zasadą aktualności: nowszy wpis (odwołanie do raportu technicznego DeepSeek v4.1-flash) precyzuje stan wiedzy — 'max' jest dla najtrudniejszych zadań.
- **[reasoning_effort w benchmarkach: uczciwe porównanie kontra marketing vendorów](https://x.com/karminski3/status/2099767018279084387):** Autor podważa powszechny konsensus, że reasoning_effort to użyteczna kontrola jakości i że wyższy effort = lepsze wyniki. Twierdzi, że to marketing vendorów i transfer ryzyka kosztowego na użytkownika, a 'high' nie jest najlepsze. Sporne punkty: (1) czy benchmarki powinny używać max dla wszystkich modeli, czy per-model sweet spot; (2) czy reasoning_effort powinien być ekwiwalentem performance po dobrym post-trainingu; (3) czy rekomendacja high jako cost–performance balance jest rzetelna, czy maskuje problemy post-trainingu.
- **[System Scaling: pętla feedbacku środowiskowego i współpraca multi-agent jako klucz do wdrożeń agentowych](https://x.com/karminski3/status/2092894849619874210):** Autor podważa dominujący w branży konsensus, że główną osia konkurencji AI jest skala modeli (parameter scaling). Twierdzi, że decydująca jest 'System Scaling' — ujednolicenie sprzężenia zwrotnego ze środowiska i współpracy multi-agent w jeden spójny system. Do rozstrzygnięcia: czy przyrosty wynikają głównie z lepszych modeli bazowych, czy z inżynierii harnessu wokół nich (i czy da się to rozdzielić eksperymentalnie przy stałym modelu).
- **[SOTA jako kompresor informacji: dlaczego ustawienie reasoning na 'max' psuje benchmarki (odwrócenie wyników SWE)](https://x.com/karminski3/status/2099426676669366337):** Autor podważa powszechny konsensus branżowy, że zwiększanie test-time compute / reasoning effort zawsze poprawia jakość. Teza 'im więcej myślenia, tym lepiej' bywa fałszywa — dowodem jest zjawisko odwrócenia wyników SWE przy ustawieniu reasoning na 'max'. Do rozstrzygnięcia: dla jakich zadań i modeli krzywa jakości od budżetu myślenia jest monotoniczna, a dla jakich ma maksimum lokalne (a więc 'max' jest anty-wzorcem).
- **[SOTA jako idealny kompresor informacji — krytyka „max reasoning effort” i rekomendacja czytania źródeł naukowych](https://x.com/karminski3/status/2099421138069950509):** Autor podważa powszechny konsensus branżowy, zgodnie z którym zwiększanie budżetu rozumowania (max effort / więcej tokenów myślenia) monotonicznie poprawia jakość modelu. Teza karminski3: dla modeli SOTA istnieje punkt przegięcia — nadmierny budżet myślenia powoduje inwersję wyników na benchmarkach agentowych/SWE, a prawdziwym wyróżnikiem SOTA jest zdolność do zwięzłej kompresji informacji (minimalne tokeny na najtrudniejsze problemy), a nie długość rozumowania. Wymaga weryfikacji empirycznej na konkretnych modelach (o-series, DeepSeek R1, QwQ itd.) i benchmarkach.
- **[Przełącznik intensywności rozumowania (thinking effort) realnie skaluje zdolności modelu — nie jest neutralną gałką](https://x.com/karminski3/status/2099396323942547519):** Autor jawnie podważa rozpowszechnioną opinię (wyrażaną przez komentujących), że przełącznik intensywności myślenia (max vs high) to jedynie kontrolka bez związku z wydajnością. Teza autora: intensywność rozumowania wprost przekłada się na zdolności modelu (dowód: DeepSeek-R1-Zero, AIME24 15%→71% przy wzroście długości rozumowania, bez dodawania wiedzy). Do rozstrzygnięcia pozostaje zakres tej zależności: czy wyższy 'effort' zawsze jest korzystny, czy istnieje punkt nasycenia (saturation), w którym dalsze zwiększanie budżetu myślenia daje malejące zwroty lub pogorszenie (overthinking). Wpis jest nowszy i reprezentuje stanowisko autora wobec wcześniejszego konsensusu komentujących.
- **[Izomorfizm kodu i danych w Skillach: metaprogramowanie mikro-skillów dla ekstrakcji danych](https://x.com/karminski3/status/2099383433034440811):** Teza kontrowersyjna wobec dominującej praktyki tworzenia Skillów jako statycznych, deklaratywnych instrukcji/dokumentów (podejście 'prompt-as-document'). Autor twierdzi, że właściwym paradygmatem jest 'prompt-as-program' — skill generujący kod (regex→kod) i dane (prompt dla LLM) w locie oraz samowalidujący się przez harness. Do rozstrzygnięcia: (a) czy dynamicznie generowane Micro-Skille są stabilne i bezpieczne w produkcji (ryzyko prompt injection / niestabilności generacji), (b) czy zysk z metaprogramowania przewyższa koszt dodatkowej inferencji przy generowaniu skilla per dokument, (c) jak wersjonować i audytować skille, które zmieniają się w czasie wykonywania.

---

## Spis kategorii

- [Obserwacje zachowania modeli / Benchmarking](#obserwacje-zachowania-modeli--benchmarking) (1)
- [Benchmarki modeli i Agentic Coding](#benchmarki-modeli-i-agentic-coding) (1)
- [Małe modele gęste / benchmarki / inżynieria wdrożeń LLM](#małe-modele-gęste--benchmarki--inżynieria-wdrożeń-llm) (1)
- [Architektura promptów / Metodologia benchmarków / Ekonomia obliczeń](#architektura-promptów--metodologia-benchmarków--ekonomia-obliczeń) (1)
- [Benchmarking i ewaluacja modeli LLM / Reasoning / Ekonomia inferencji](#benchmarking-i-ewaluacja-modeli-llm--reasoning--ekonomia-inferencji) (1)
- [Architektura modeli / Inferencja produkcyjna / Systemy decyzyjne](#architektura-modeli--inferencja-produkcyjna--systemy-decyzyjne) (1)
- [Architektura modeli / Type-Safe AI / Structured Output](#architektura-modeli--type-safe-ai--structured-output) (1)
- [Agentic Systems / System Scaling / Architektura harnessu](#agentic-systems--system-scaling--architektura-harnessu) (1)
- [Architektura systemów agentowych / Inżynieria kontekstu](#architektura-systemów-agentowych--inżynieria-kontekstu) (1)
- [Systemy agentowe / AI w cyberbezpieczeństwie](#systemy-agentowe--ai-w-cyberbezpieczeństwie) (1)
- [Benchmarking / Ewaluacja modeli](#benchmarking--ewaluacja-modeli) (1)
- [Architektura modeli i systemów agentowych / Ewaluacja AI](#architektura-modeli-i-systemów-agentowych--ewaluacja-ai) (1)
- [Bezpieczeństwo modeli / AI Safety / Wielojęzyczna ocena alignmentu](#bezpieczeństwo-modeli--ai-safety--wielojęzyczna-ocena-alignmentu) (1)
- [Edge AI / Browser-based Agents](#edge-ai--browser-based-agents) (1)
- [Inżynieria modeli / dystylacja / test-time compute](#inżynieria-modeli--dystylacja--test-time-compute) (1)
- [Architektura modeli rozumujących / Inżynieria ewaluacji i test-time compute](#architektura-modeli-rozumujących--inżynieria-ewaluacji-i-test-time-compute) (1)
- [Inżynieria promptów / Modele rozumujące (reasoning) / Efektywność tokenowa](#inżynieria-promptów--modele-rozumujące-(reasoning)--efektywność-tokenowa) (1)
- [Parametry wnioskowania / Reasoning Effort / Thinking Budget](#parametry-wnioskowania--reasoning-effort--thinking-budget) (1)
- [Architektura promptów / Agent Skills / Inżynieria kontekstu](#architektura-promptów--agent-skills--inżynieria-kontekstu) (1)
- [Architektura promptów / Systemy agentowe / Metaprogramowanie](#architektura-promptów--systemy-agentowe--metaprogramowanie) (1)
- [Benchmarki LLM / Agentic Coding / Backend](#benchmarki-llm--agentic-coding--backend) (1)
- [Benchmarking i ewaluacja modeli / Inżynieria agentowa](#benchmarking-i-ewaluacja-modeli--inżynieria-agentowa) (1)
- [Benchmarking i ewaluacja LLM](#benchmarking-i-ewaluacja-llm) (1)
- [Multimodalne modele AI / Systemy agentowe](#multimodalne-modele-ai--systemy-agentowe) (1)
- [Inżynieria kontekstu multimodalnego / analiza wideo w LLM](#inżynieria-kontekstu-multimodalnego--analiza-wideo-w-llm) (1)
- [Multimodalność / Inżynieria wejścia wizyjnego](#multimodalność--inżynieria-wejścia-wizyjnego) (1)

---

## Obserwacje zachowania modeli / Benchmarking

### Claude Opus 5.5 vs Fable 5.1: dystylacja wykryta przez wzrost zużycia tokenów rozumowania

- **Data:** `Tue Sep 22 19:24:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2102479290420048093)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Dystylacja modeli]] [[Harness|Kwantyzacja modeli]] [[Test-Time Compute i Reasoning Tokens|Reasoning tokens]] [[Harness|Thinking stall]] [[Harness|Benchmark stabilności modelu]] [[Harness|Claude Opus 5.5]] [[Harness|Fable 5.1]] [[Harness|Regresja jakości modeli u dostawcy]] [[Weryfikator|Zewnętrzny weryfikator]]

**Kontekst / Problem:**
Autor przeprowadził testy frontendowe (generowanie kodu UI) na Claude Opus 5.5 i porównał je z wcześniej testowanym modelem Fable 5.1. Celem było ustalenie, czy nowy model to samodzielna architektura, czy pochodna (kwantyzacja/dystylacja) istniejącego modelu, oraz ocena stabilności i kosztu inferencji. Wniosek: implementacje obu modeli są wizualnie i strukturalnie nierozróżnialne, co sugeruje wspólne pochodzenie wag, a różnica sprowadza się do ekonomii tokenów rozumowania.

**Rada inżynierska:**
Traktuj zużycie tokenów rozumowania jako tani proxy-sygnał rozmiaru i pochodzenia modelu: jeśli nowy model generuje ten sam wynik co poprzednik, ale zużywa wyraźnie więcej tokenów thinking, to najprawdopodobniej jest to mniejsza sieć (lub kwantyzowana/dystylowana wersja), która nadrabia pojemność długością łańcucha rozumowania. Równolegle oceniaj stabilność przez wielokrotne, niezależne próbkowanie tego samego zadania (autor: 6/6 identycznej jakości) — to odróżnia realną deterministyczność produktu od szczęśliwego trafienia jednego seeda. Przy testach porównawczych dwóch modeli patrz na detale implementacyjne (struktura kodu, dobór bibliotek, styl), a nie tylko na wynikowy screenshot — brak różnic w detalach to silny sygnał wspólnej bazy wagowej.

**Uwaga / Anty-wzorzec:**
Długi łańcuch rozumowania bywa pułapką wydajnościową: model potrafi wejść w stan 'zablokowanego myślenia' (thinking stall / pętla reasoning) i nigdy nie wyemitować kodu — autor zaobserwował to wielokrotnie w teście 'erupcji wulkanu', zarówno w terminalu, jak i w interfejsie webowym. Anty-wzorzec: brak twardego limitu czasu i fallbacku na krótszy tryb rozumowania w harnessie agentowym. Drugi anty-wzorzec: zakładanie, że 'tańszy model o podobnej jakości' pozostanie taki sam w czasie — autor wskazuje na rynkową praktykę stopniowego osłabiania modeli (降智) po stronie dostawcy, więc benchmarki trzeba re-uruchamiać okresowo, a nie ufać jednorazowej ocenie przy premierze.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor podważa dwa elementy konsensusu branżowego: (1) tezę, że nowe wydania modeli to niezależne architektury — sugeruje, że Opus 5.5 to kwantyzowana lub wewnętrznie dystylowana wersja Fable 5.1, co jest sprzeczne z marketingiem Anthropic o 'nowej generacji'; (2) praktykę komunikacyjną dostawcy — wprost oskarża Anthropic o '祖传' (dziedziczną) degradację jakości modeli w czasie (降智), co stoi w sprzeczności z deklaracjami o stałości zachowania wersjonowanych endpointów. Do rozstrzygnięcia wymaga niezależnych, powtarzalnych pomiarów: porównania rozkładu tokenów rozumowania, wyników na stałym zbiorze ewaluacyjnym w czasie oraz (jeśli dostępne) analizy wag/aktywacji.

> **Cytat:** *""给大家带来claude opus 5.5 的前端测试结果. 直接说结论, 我怀疑现在opus 5.5就是 fable 5.1 的量化版或者自家蒸馏版, 可以直接看我的视频, 几乎看不出两个模型实现细节上的差别. 而且模型继承了Anthropic一贯的优良特点, 一个字, 稳, 6次抽卡6次全都是这个质量. 除此之外我测试时很明显 opus 5.5 的思考token消耗更多. 这意味着opus5.5模型会更小一些(用reasoning长度换性能). 这同样意味着会有雷霆大思考的情况, 比如最后一个火山喷发测试, 我terminal和网页都测试了好几次, 结果都无法输出代码. 思考卡住了. 当然瑕不掩瑜. 毕竟比fable便宜又能获得差不多的性能, 只要不降智, 就是好模型(但无奈Anthropic降智是祖传艺能...).""*

---

## Benchmarki modeli i Agentic Coding

### MiMo-v2.6-Pro: 3x skok w benchmarkach AgenticCoding po RL na żywo, ~500 tps przy 42B aktywnych parametrów i problem wczesnego zatrzymania agenta

- **Data:** `Tue Sep 22 16:00:37 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2102427860585841100)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|HNSW]] [[Harness|Agentic Coding]] [[Harness|Early Stopping agenta]] [[Test-Time Compute i Reasoning Tokens|Token throughput (tps)]] [[Harness|Mixture of Experts - aktywne parametry]] [[Harness|AVX-512]] [[Harness|Benchmarkowanie modeli]] [[Harness|Regulacja intensywności rozumowania (thinking effort)]] [[Harness|MiMo-v2.6-Pro]]

**Kontekst / Problem:**
Autor przedstawia szybki raport z testów chińskiego modelu Xiaomi MiMo-v2.6-Pro (oraz wariantu ultraspeed) w zadaniach agentowego kodowania. Celem jest ocena realnej przydatności modelu do backendowego AgenticCoding po treningu RL prowadzonym w transmisji na żywo. Testy obejmują zadanie implementacji bazy wektorowej (poprzedni MiMo-v2.5-Pro: 2505 pkt, obecny: 7810 pkt — 3x wzrost, zbliżenie do Claude Fable-5) oraz zadania frontendowe (np. one-shot silnik ray tracingu, symulacja fizyki rozbijania ściany przez kulkę). Autor porównuje też throughput generowania tokenów z innymi modelami tej samej skali.

**Rada inżynierska:**
Przy wyborze modelu do backendowego AgenticCoding warto kierować się jakością algorytmicznego kodu, a nie tylko ogólnym wrażeniem z demo frontendu: MiMo-v2.6-Pro (1.02T total / 42B aktywne parametry) osiąga ~464 tps w wariancie ultraspeed, ~500 tps dla typowych żądań i szczytowo ~900 tps — przy normie 60–80 tps dla modeli o porównywalnej skali. Ze względu na długi czas rozumowania (thinking) i brak możliwości regulacji jego intensywności oraz przeciążony endpoint standardowy, należy ustawić szeroki timeout, aby uniknąć braku odpowiedzi. Architektura dobrego rozwiązania: pojedynczy graf HNSW (M=16/M0=28) + dokładna odległość AVX-512 + per-thread visited stamp. Trening w 67% oparty na kodzie przekłada się bezpośrednio na silne zdolności algorytmiczne (one-shot silnik ray tracingu).

**Uwaga / Anty-wzorzec:**
Problem wczesnego zatrzymania (early stopping) agenta: w teście bazy wektorowej przy limicie 50 iteracji na rundę model w 2 z 3 prób przerwał iterowanie około 30. rundy, gdy przestał poprawiać wynik, i „oddał pracę” przedwcześnie — marnując budżet testowy. Anty-wzorzec: brak mechanizmu wymuszającego kontynuację eksploracji lub zewnętrznego weryfikatora/stopera, gdy agent sam zdecyduje o zbieżności. Drugi anty-wzorzec: brak wsparcia dla dostrajania intensywności rozumowania, co wymusza agresywne zwiększanie timeoutów. Dodatkowo modele mogą wyglądać dobrze w demo (frontend), a mimo to zawodzić w rozumieniu przestrzennym i symulacji fizyki — nie należy generalizować wyników z jednej domeny na całość.

> **Cytat:** *"给大家带来小米 MiMo-v2.6-pro 的测试速报! ... 之前的 MiMo-v2.5-Pro 在我的向量数据库测试中得分只有2505, 而这次直接翻了3倍, 得分来到了7810. ... 算法也进化为了单图HNSW分层近邻图(M=16/M0=28) + AVX-512精确距离 + 每线程visited stamp. ... MiMo-v2.6-pro-ultraspeed 版本可以达到464tps的速度 ... 峰值可以达到900tps, 常态化请求也可以稳定在500tps左右, 考虑到模型 1.02T 的总参数量, 以及高达 42B 的激活参数量, 再加上同等规模模型一般都在60-80tps的水平 ... 这次测试我发现它还是有早停的问题的, 上面的向量数据库测试, 每轮最大迭代50次, 但是三次测试中, 有两次它迭代到30轮左右就没办法提升分数, 于是选择了直接交卷, 浪费了测试机会. ... 模型思考偏长, 而且暂时不支持调整思考强度, 加上普速接口现在异常火爆, 所以最好给大一些超时 ... 67%的训练语料都是Coding"*

---

## Małe modele gęste / benchmarki / inżynieria wdrożeń LLM

### K2-Horizon-7B: gęsty 7B z pełną uwagą dorównuje 27B, ale wysoki koszt długiego kontekstu wymusza kwantyzację

- **Data:** `Tue Sep 15 22:37:55 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099991128061919596)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|K2-Horizon-7B]] [[Harness|AA Bench]] [[Harness|Qwen3.6-27B]] [[Harness|Qwen3.8-35B-A3B]] [[Harness|Full Attention]] [[Architektura KV Cache i Rozumowanie Latentne|KV Cache]] [[Context Compaction|Długi kontekst]] [[Harness|Kwantyzacja 8-bit]] [[Harness|Kwantyzacja 4-bit]] [[Harness|vLLM]] [[Harness|SGLang]] [[Harness|Unsloth]] [[Harness|Thinking Budget]] [[Harness|SWE-bench Verified]] [[Harness|Terminal Bench]] [[Harness|BrowseComp]] [[Harness|MiniCPM5-2B]] [[Harness|Małe modele językowe]]

**Kontekst / Problem:**
IFM wydało K2-Horizon-7B — gęsty model 7B, który w AA Bench uzyskuje 21 pkt wobec 22 pkt dla Qwen3.6-27B, a w BrowseComp, SWE-bench Verified i Terminal Bench wypada bardzo mocno. Model jest w pełni open-source: dane treningowe, recipe, kod treningowy i metody ewaluacji są jawne. Obsługuje do 512K kontekstu, ale ponieważ używa pełnej uwagi, koszt długiego kontekstu jest bardzo wysoki: 128K w BF16 wymaga ok. 18 GB VRAM/pamięci unified. Autor rekomenduje poczekanie na kwantyzację 8-bit/4-bit oraz użycie vLLM/SGLang, jeśli dostępna jest wystarczająca ilość VRAM.

**Rada inżynierska:**
Przy ocenie małego modelu gęstego nie wystarczy porównywać samych wyników benchmarków z większymi modelami. K2-Horizon-7B ma tylko 7B parametrów, ale jest oparty na pełnej uwadze, więc koszt KV cache i obliczeń silnie rośnie wraz z długością kontekstu; 128K w BF16 wymaga ok. 18 GB VRAM/unified memory. Do długiego kontekstu wybierz kwantyzację 8-bit/4-bit, a do serwowania użyj vLLM/SGLang. Ustawiaj thinking na high zgodnie z rekomendacją twórców.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: wdrażanie BF16 przy 128K kontekstu bez rezerwy VRAM oraz ocena modelu wyłącznie po benchmarkach, bez uwzględnienia kosztu pełnej uwagi, przepustowości i opóźnień. Drugi anty-wzorzec: ignorowanie rekomendowanego poziomu thinking=high i używanie low/medium jako domyślnego.

> **Cytat:** *"IFM刚放出了个神奇7B Dense小模型 K2-Horizon-7B. 神奇的是这玩意在AA Bench里面有21分, 而Qwen3.6-27B是22分, 也就是说这7B参数量快追平了27B的水平.
甚至这个模型在诸如BrowseComp测试中碾压了前几代旗舰模型(GPT-5/DeepSeek-V4). 而且工程能力比如SWEBench Verified/ Terminal Bench 分数表现也很亮眼.
所以敲打一波Qwen, 赶紧放出你们压箱底的Qwen3.8-35B-A3B, 别藏着掖着了. 要被偷家了!

这个模型现在完全是社区明星了, 它的训练数据, 怎么训练的(recipe), 训练代码以及评估方法全都是开源的. 参数上这个模型最大支持512K上下文, 但是注意, 这玩意虽然参数只有7B, 但是它是全注意力的, 所以上下文成本相当高. 目前还只有原始BF16精度, 如果要用128K上下文, 就要18G显存/统一内存. 所以还是等等8bit/4bit量化版本比较好(我刚在X上 @ unsloth 了一波, 看看哥俩会不会有时间做量化吧)

以及这个模型同样支持设置思考强度. 分为low/medium/high, 然后默认/官方强烈推荐用high.

如果现在不差显存想直接用可以使用vLLM/SGLang. 这俩已经支持了. 等 unsloth 放出量化版我给大家来一期10B以下小模型横评.  MiniCPM5-2B 和其他几个小模型已经在跑了.

#K2Horizon7B #MiniCPM52B #Qwen3835BA3B"*

---

## Architektura promptów / Metodologia benchmarków / Ekonomia obliczeń

### reasoning_effort jako marketing: przenoszenie kosztu obliczeń i ryzyka rozliczeniowego na użytkownika

- **Data:** `Tue Sep 15 07:47:29 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099767043155218568)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Test-Time Compute i Reasoning Tokens|reasoning_effort]] [[Harness|Metodologia benchmarków LLM]] [[Harness|Koszt-vs-jakość wnioskowania]] [[Harness|Thinking budget]] [[Harness|Post-training]] [[Harness|Ekonomia tokenów]] [[Harness|DeepSeek v4.1-flash]] [[Harness|Parametry wnioskowania]]

**Kontekst / Problem:**
Autor prowadzi benchmarki modeli LLM i napotyka praktyczny konflikt metodologiczny: skoro wszystkie inne modele testuje się z parametrem max, to nie można modelu DeepSeek mierzyć tylko z reasoning_effort=high — benchmark byłby nieporównywalny. W wątku podnosi tezę, że parametry typu reasoning_effort nie są neutralnym narzędziem inżynierskim, lecz marketingowym mechanizmem producentów modeli: pozwalają przenieść na użytkownika decyzję o kompromisie koszt-efektywność ORAZ ryzyko rozliczeniowe za zużycie obliczeń. Wskazuje też, że producent najpierw deklaruje, że benchmarki publikowane są przy max, a następnie komunikuje, że tzw. sweet spot (w dokumentacji cost–performance balance) leży przy high, co prowadzi do wniosku odbiorców, że 'high = najlepsze'.

**Rada inżynierska:**
Przy benchmarkowaniu modeli zawsze wyrównuj parametry wnioskowania (reasoning_effort / thinking budget) pomiędzy porównywanymi modelami — inaczej mierzysz różnicę w konfiguracji, nie różnicę w modelach. Traktuj 'sweet spot' (cost–performance balance) sprzedawcy jako punkt handlowy, nie inżynierski: sam wyznacz zależność jakość-vs-koszt (thinking budget → accuracy/latency/token throughput) dla swojego obciążenia. Utrzymuj rozdzielenie pojęć: wysiłek rozumowania (budżet tokenów myślowych) ≠ jakość końcowa; dążenie docelowe to konwergencja jakości niezależnie od wysiłku, a rozbieżność jest długiem post-trainingu.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: przyjęcie deklaracji producenta o 'sweet spot = high' jako optymalnej konfiguracji domyślnej bez własnego pomiaru. Konsekwencje: nieporównywalne benchmarki (mieszanie max vs high), przeniesienie ryzyka kosztów tokenów na użytkownika, oraz błędne przekonanie, że wyższy reasoning_effort zawsze oznacza wyższą jakość. Dokumentacja DeepSeek v4.1-flash sama wskazuje, że max jest rezerwowany wyłącznie dla najtrudniejszych zadań — więc 'max = domyślne/lepsze' jest nadużyciem.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Teza kontrowersyjna wobec konsensusu branżowego: autor twierdzi, że publiczne parametry reasoning_effort to narzędzie marketingowe producentów, które przenosi kompromis obliczeniowy i ryzyko rozliczeniowe na użytkownika, oraz że rozbieżność między 'thinking effort' a 'performance' wynika z niedostatków post-trainingu (a idealnie powinny być równoważne). Jego zdaniem komunikacja 'sweet spot = high' jest myląca i promuje przekonanie, że wysokie ustawienie jest optymalne. Sporny punkt do rozstrzygnięcia: czy parametry effort to neutralne narzędzie kontroli kosztu, czy narzędzie transferu ryzyka i kształtowania percepcji jakości modelu. Wniosek sprzeczny też praktycznie z zaleceniem komentatorów, by testować model tylko na 'high' — autor wskazuje, że taka konfiguracja jest niekompatybilna metodologicznie z benchmarkami prowadzonymi na 'max'. Zgodnie z zasadą aktualności: nowszy wpis (odwołanie do raportu technicznego DeepSeek v4.1-flash) precyzuje stan wiedzy — 'max' jest dla najtrudniejszych zadań.

> **Cytat:** *"问题在于我做的是 benchmark, 不是日常使用. 不能因其他模型都用max然后deepseek high 好单独用high测.

然后评论说应该用high测.

以及, reasoning_effort 在我看来是大模型厂商的营销手段. 把算力与精度的权衡交给了用户, 顺便把算力计费的风险也转移给了用户. 而且巧妙地进行掩饰: 宣称benchmark全是max跑出来的. 最后又说甜区(注意论文里称作cost–performance balance) 在high.

造成的结果就是, 有人认为high就是最好的.

我当然同意 thinking effort 不等价于 performance. 而且我认为之所以不等价是因为后训练拉了. 理想上应该追求让它等价.

但请注意, deepseek-v4-1-flash技术报告里给max评价为: best reserved for the most challenging tasks."*

---

## Benchmarking i ewaluacja modeli LLM / Reasoning / Ekonomia inferencji

### reasoning_effort w benchmarkach: uczciwe porównanie kontra marketing vendorów

- **Data:** `Tue Sep 15 07:47:23 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099767018279084387)
- **Rodzaj:** Komentarz w dyskusji (@QuantumTransf)
- **Powiązane pojęcia:** [[Harness|Benchmarkowanie LLM]] [[Test-Time Compute i Reasoning Tokens|Reasoning effort]] [[Harness|Koszt vs jakość]] [[Harness|Post-training]] [[Harness|DeepSeek]] [[Harness|Ekonomia inferencji]]

**Kontekst / Problem:**
Dyskusja o metodologii benchmarkowania modeli reasoning. Autor broni porównywania modeli przy stałym ustawieniu reasoning_effort = max, skoro inne modele są testowane z max; komentujący sugerują testowanie DeepSeek na high. Autor zgłasza tezę, że reasoning_effort to narzędzie marketingowe vendorów: przenosi na użytkownika decyzję o kompromisie koszt–jakość oraz ryzyko kosztowe, a jednocześnie vendorzy publikują benchmarki na max i wskazują high jako sweet spot (w papierach: cost–performance balance). Skutkiem jest błędne przekonanie, że high jest najlepsze. Autor twierdzi też, że thinking effort nie jest równoważny performance głównie z powodu słabego post-trainingu, choć idealnie powinien być. Przywołuje deepseek-v4-1-flash tech report, gdzie max określono jako 'best reserved for the most challenging tasks'.

**Rada inżynierska:**
W benchmarkach porównawczych utrzymuj identyczny reasoning_effort dla wszystkich modeli; nie wybieraj per model poziomu, który akurat wypada najlepiej, bo to zaburza porównanie. Traktuj reasoning_effort jako parametr koszt–jakość, a nie bezpośrednią miarę jakości: high to zwykle cost–performance balance, max rezerwuj dla najtrudniejszych zadań. Od vendorów wymagaj jawnych ustawień reasoning_effort użytych w benchmarkach oraz raportowania pełnej krzywej koszt–jakość, a nie tylko pojedynczych punktów. Przy ocenie modeli reasoning oddzielaj efekt 'więcej myślenia' od jakości post-trainingu.

**Uwaga / Anty-wzorzec:**
Błędne założenie, że wyższy reasoning_effort zawsze oznacza lepszą jakość. Vendorzy publikują benchmarki na max, ale rekomendują high jako sweet spot; użytkownicy mylnie biorą high za najlepsze. Dodatkowo, brak jednolitych ustawień reasoning_effort między modelami prowadzi do nieuczciwych porównań. Post-training może nie czynić thinking effort równoważnym performance, przez co samo zwiększanie wysiłku nie gwarantuje lepszego wyniku.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor podważa powszechny konsensus, że reasoning_effort to użyteczna kontrola jakości i że wyższy effort = lepsze wyniki. Twierdzi, że to marketing vendorów i transfer ryzyka kosztowego na użytkownika, a 'high' nie jest najlepsze. Sporne punkty: (1) czy benchmarki powinny używać max dla wszystkich modeli, czy per-model sweet spot; (2) czy reasoning_effort powinien być ekwiwalentem performance po dobrym post-trainingu; (3) czy rekomendacja high jako cost–performance balance jest rzetelna, czy maskuje problemy post-trainingu.

> **Cytat:** *"问题在于我做的是 benchmark, 不是日常使用. 不能因其他模型都用max然后deepseek high 好单独用high测.  

然后评论说应该用high测. 

以及, reasoning_effort 在我看来是大模型厂商的营销手段. 把算力与精度的权衡交给了用户, 顺便把算力计费的风险也转移给了用户. 而且巧妙地进行掩饰: 宣称benchmark全是max跑出来的. 最后又说甜区(注意论文里称作cost–performance balance) 在high. 

造成的结果就是, 有人认为high就是最好的. 

我当然同意 thinking effort 不等价于 performance. 而且我认为之所以不等价是因为后训练拉了. 理想上应该追求让它等价.

但请注意, deepseek-v4-1-flash技术报告里给max评价为: best reserved for the most challenging tasks."*

---

## Architektura modeli / Inferencja produkcyjna / Systemy decyzyjne

### Jev/TypeSafe AI: jednoprzebiegowa inferencja schematów dla ultraniskiej latencji decyzyjnej

- **Data:** `Thu Sep 17 22:46:03 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2100717948881326224)
- **Rodzaj:** Komentarz w dyskusji (@karminski3)
- **Powiązane pojęcia:** [[Harness|System One]] [[Harness|System Two]] [[Harness|Parallel Sampling Architecture]] [[Harness|Latencja end-to-end]] [[Harness|Guardrails]] [[Harness|Vercel AI Gateway]] [[Jev]] [[TypeSafe — przewodnik praktyczny|TypeSafe AI]]

**Kontekst / Problem:**
Omówienie modelu Jev od TypeSafe AI jako modelu typu System One do wysokoczęstotliwościowych decyzji produkcyjnych. Zamiast klasycznego generowania token-po-tokenie, model ma w jednym przebiegu propagacji wprzód zwracać dyskretne predykcje i prawdopodobieństwa gałęzi dla zdefiniowanych pól schematu. Ma to dawać ok. 70 ms opóźnienia i bardzo niski koszt wejścia ($0,042 / 1M tokenów, wyjście darmowe). Autor wskazuje zastosowanie m.in. w bastionie do real-time klasyfikacji niebezpiecznych komend shell, ale podkreśla ograniczenia: brak lokalnych węzłów, opóźnienie sieci do US West ~120 ms, więc realnie min. ~200 ms, oraz potrzebę modelu System Two do strategii i generowania promptów.

**Rada inżynierska:**
Model typu System One z jednoprzebiegową predykcją pól schematu używaj jako szybkiego klasyfikatora/guardrail w scenariuszach wysokiej częstotliwości, np. ocena ryzyka komend shell. Zawsze licz opóźnienie end-to-end: czas inferencji + opóźnienie sieci do regionu modelu. Do lepszej jakości decyzji łącz go z modelem System Two, który najpierw wykonuje ocenę strategiczną i generuje prompt/kontekst dla szybkiego modelu.

**Uwaga / Anty-wzorzec:**
Pomijanie opóźnienia sieciowego i braku lokalnych węzłów — deklarowane 70 ms może zamienić się w ~200 ms przy dostępie do US West. Oczekiwanie, że model System One samodzielnie poprowadzi złożone rozumowanie strategiczne. Używanie ciężkich modeli LLM do prostych, wysokoczęstotliwościowych decyzji klasyfikacyjnych tam, gdzie wystarczy jednoprzebiegowa inferencja schematowa.

> **Cytat:** *"但天下武功唯快不破, 这玩意从输入到输出最快只需要70ms!

所以完全可以用在高频的生产级场景, 比如接到堡垒机里面实时判断用户输入的shell命令是否存在危险(rm -rf /). 再加上输入每百万token只需要$0.042, 输出不要钱. 妥妥的新一代flash模型斩杀线(有的flash模型会被企业用作决策器).

说完了用途再来看它的架构, 传统大模型有多少token就要把激活参数过多少遍(前向传播)所以特别吃显存带宽, 而这个模型设计了一个特殊的并行采样架构, 只需要一次前向传播, 就能输出所有预设schema字段的离散预测与分支概率. 达成了极低的延迟.

而推出Jev的 TypeSafe AI 这个公司也很有噱头, 它是 Diogo Almeida 一手创办的, 就是他曾经在 OpenAI 的 InstructGPT 和早期 RLHF（基于人类反馈的强化学习) 团队中的贡献才有了如今的ChatGPT.

最后说一下目前模型的限制, 首先由于没有本土节点, 所以虽然它只需要70ms, 但是到美西这海底光缆延迟120ms是躲不掉的, 所以至少还是200ms打底. 另外, 模型被官方称为 System One 模型, 所以理想搭配还需要一个 System Two 模型用来进行战略判断, 然后生成策略当作提示词输入进去, 这样才能提升模型的输出质量.

另外, 官网还在申请使用, 不过vercel的AI Gateway已经能直接用了, 所以想测试的同学直接去vercel用就行."*

---

## Architektura modeli / Type-Safe AI / Structured Output

### Jev: model decyzyjny porzucający architekturę autoregresyjną z typowanym wyjściem strukturalnym

- **Data:** `Thu Sep 17 22:46:02 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2100717944565354595)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Type-Safe AI]] [[Harness|Structured Output]] [[Harness|Decision Model]] [[Harness|Schema Compilation]] [[Harness|Autoregressive Architecture]] [[Jev]] [[Harness|Protobuf]] [[Harness|GraphQL]] [[Harness|Decision Slots]] [[Harness|System One]]

**Kontekst / Problem:**
Tradycyjne LLM-y generują swobodny tekst, przez co ich odpowiedzi trzeba parsować i walidować (ryzyko halucynacji formatu, błędnego JSON-a, driftu schematu). Wpis @karminski3 opisuje model Jev, który porzuca klasyczną architekturę autoregresyjną i nie potrafi w ogóle wypisywać zwykłego tekstu — zamiast tego wykonuje wyłącznie decyzje. Użytkownik definiuje Schema (analogicznie do protobuf/GraphQL), która przy podaniu do modelu jest kompilowana do konkretnych 'slotów decyzyjnych' (decision slots), a model wypełnia je wartościami i prawdopodobieństwami. Problem, który to rozwiązuje: całkowita eliminacja błędów formatu wyjścia przy zachowaniu zdolności decyzyjnych w złożonych scenariuszach (klasyfikacja, gry typu Slay the Spire, analiza wykresów giełdowych).

**Rada inżynierska:**
Traktuj model decyzyjny jako osobny typ komponentu w systemie: zamiast promptować LLM o 'zwróć JSON', zdefiniuj formalny Schema (wzorzec protobuf/GraphQL), która zostaje skompilowana do slotów decyzyjnych. Wyjście ma wtedy postać gwarantowanie poprawnego JSON-a z jawnymi prawdopodobieństwami (np. {\"decision\": {\"isSpam\": true}, \"probabilities\": {\"isSpam\": {\"true\": 0.982, \"false\": 0.018}}}). Dla scenariuszy złożonych (agent grający, analiza rynku) wystarczy zamienić treść na wejście tekstowe i wyliczyć dostępne akcje — model sam podejmuje decyzję w obrębie zdefiniowanej przestrzeni akcji. Kluczowa korzyść inżynierska: brak ryzyka niepoprawnego formatu i deterministyczna walidacja typu (TypeSafeAI).

**Uwaga / Anty-wzorzec:**
Nie zakładaj, że model decyzyjny to zamiennik LLM-a ogólnego przeznaczenia — obecnie obsługuje wyłącznie wejście tekstowe i nie generuje swobodnej odpowiedzi, więc nie nadaje się do zadań wymagających prozy, dialogu czy generowania treści. Antywzorzec: próba użycia go tam, gdzie potrzebny jest wolny tekst, albo pominięcie etapu definiowania i kompilacji Schema — bez schematu model nie ma slotów, które mógłby wypełnić. Drugie ryzyko: nadmierne zaufanie do 'wyjście JSON nigdy nie zawodzi' bez weryfikacji semantycznej (poprawny format ≠ poprawna decyzja).

> **Cytat:** *""给大家写个简单的Jev模型介绍, 这绝对是个需要重点关注的模型. 简单讲, 这个模型放弃了传统自回归架构, 它没有办法直接输出普通文本. 但是他能进行决策! 比如最简单的二分类场景, 输入一条短信, 让它判断是否为垃圾短信, 它就可以输出这样的JSON: {"decision": { "isSpam": true }, "probabilities": { "isSpam": { "true": 0.982, "false": 0.018 } } } 没错, 它只能进行结构化输出, 甚至你输入的时候要定义 Schema (用过protobuf/GraphQL的同学应该能理解), 在送入模型时被编译为特定的决策槽位, 然后按照槽位输出, 所以输出JSON不可能出问题. 而复杂一些的场景, 比如让这个模型玩杀戮尖塔或者看盘, 只需要把内容转换为文本输入进去(没错, 目前模型只支持文本输入), 然后定义好模型能进行哪些动作, 模型就会自主决策了.""*

---

## Agentic Systems / System Scaling / Architektura harnessu

### System Scaling: pętla feedbacku środowiskowego i współpraca multi-agent jako klucz do wdrożeń agentowych

- **Data:** `Thu Aug 27 08:39:50 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2092894849619874210)
- **Rodzaj:** Komentarz w dyskusji (@karminski3)
- **Powiązane pojęcia:** [[Harness|System Scaling]] [[Harness|Agentic Systems Engineering]] [[Harness|Environment Feedback Loop]] [[Harness|Multi-Agent Collaboration]] [[Weryfikator|Zewnętrzny weryfikator]] [[Harness|Harness agentowy]] [[Harness|Time-to-Artifact]] [[Harness|DeepResearch]] [[Harness|Open Source Agent Framework]]

**Kontekst / Problem:**
Autor komentuje działanie pewnej architektury agentowej, która w ok. 10 minut dostarczyła gotową konfigurację firewalla w reakcji na atak. Teza: przewaga nie wynika z rozmiaru modelu, lecz z ujednolicenia dwóch mechanizmów w jeden system — iteracyjnego testowania w realnym środowisku (trial-and-error feedback) oraz koordynacji wielu agentów. Framework jest open source, a towarzyszący mu model DeepResearch został dostrojony specjalnie pod zadania deep research.

**Rada inżynierska:**
Projektuj system agentowy jako harness, w którym (1) agent wykonuje akcję w realnym środowisku, (2) zbiera obiektywny sygnał zwrotny (błąd walidacji, log, wynik testu, odrzucenie konfiguracji przez usługę), (3) poprawia artefakt i powtarza pętlę, a (4) role są rozdzielone między wielu agentów (generator / weryfikator / operator). Optymalizuj metrykę end-to-end 'time-to-artifact' (tu: ~10 min do działającej konfiguracji firewalla), a nie pojedyncze benchmarki modelu. Model traktuj jako wymienny komponent — wartość dodaną tworzy warstwa systemowa wokół niego.

**Uwaga / Anty-wzorzec:**
Skupianie się wyłącznie na skalowaniu liczby parametrów modelu i wynikach benchmarków przy jednoczesnym braku pętli feedbacku z prawdziwego środowiska. Agent bez zewnętrznego weryfikatora generuje konfiguracje (np. reguły firewalla), które wyglądają poprawnie składniowo, ale nie są testowane pod obciążeniem ani w realnym ruchu — to prosta droga do halucynowanych, niebezpiecznych lub nieskutecznych reguł bezpieczeństwa.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor podważa dominujący w branży konsensus, że główną osia konkurencji AI jest skala modeli (parameter scaling). Twierdzi, że decydująca jest 'System Scaling' — ujednolicenie sprzężenia zwrotnego ze środowiska i współpracy multi-agent w jeden spójny system. Do rozstrzygnięcia: czy przyrosty wynikają głównie z lepszych modeli bazowych, czy z inżynierii harnessu wokół nich (i czy da się to rozdzielić eksperymentalnie przy stałym modelu).

> **Cytat:** *"最后, 在这个架构加持下, 它仅用了10分钟左右就给我交付了针对攻击的防火墙配置. 这真的是 Agentic 系统工程的胜利了. 

未来的 AI 竞争, 不仅是卷模型参数量, 能把环境试错反馈和多 Agent 协同做成统一的系统 (System Scaling), 才是真正让AI在各种工程中落地的关键.

另外, 这个框架还开源了! 这里: https://t.co/n4F2ulrtEc
配套的 DeepResearch 模型也在这里: https://t.co/f8BzbXFh1n (模型之前也给大家测过, 是针对 DeepResearch 特调的, 性能相当不错)"*

---

## Architektura systemów agentowych / Inżynieria kontekstu

### Harness Scaling: skalowanie rusztowania agentowego zamiast parametrów modelu

- **Data:** `Thu Aug 27 08:39:49 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2092894843429363871)
- **Rodzaj:** Komentarz w dyskusji (@karminski3)
- **Powiązane pojęcia:** [[Harness|Harness Scaling]] [[Harness|Agentic Coordination Scaling]] [[Harness|Environment Scaling]] [[Harness|Agent Team / Swarm]] [[Harness|AgentOS]] [[Harness|Apodex 1.1]] [[Harness|Attention Loss]] [[Harness|Halucynacje modeli]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|ModSecurity]] [[Harness|Asynchroniczni agenci równolegli]] [[Harness|Izolowany runtime dla kodu generowanego przez LLM]]

**Kontekst / Problem:**
Zadanie analizy ~1,2 mln linii logów bezpieczeństwa (~260 MB) jest niewykonalne dla klasycznego, jednowątkowego systemu agentowego — bezpośrednie wstrzyknięcie takiego wolumenu do kontekstu prowadzi do utraty uwagi (attention loss), halucynacji i finalnego błędu całego zadania. Apodex 1.1 rozwiązuje to przez rozdzielenie skali na dwa niezależne wymiary: skalowanie koordynacji agentów (Agentic Coordination Scaling) oraz skalowanie środowiska wykonawczego (Environment Scaling).

**Rada inżynierska:**
Wprowadź pojęcie Harness Scaling: zwiększanie liczby parametrów podnosi wyłącznie 'inteligencję' modelu, natomiast skalowanie rusztowania (framework), zestawu narzędzi (Agent Tools) i zespołu agentów (Agent Team/Swarm) podnosi realną zdolność wykonywania pracy. W praktyce stosuj dwa niezależne wektory: (1) Agentic Coordination Scaling — rozbij zadanie na asynchroniczne, równoległe role specjalizowane (np. Agent Wywiadowczy czyści setki tysięcy logów i wyciąga złośliwe IP oraz cechy charakterystyczne, Agent Reguł na podstawie tych cech pisze reguły blokujące ModSecurity); agenci działają równolegle i asynchronicznie — Agent Reguł zaczyna pisać reguły firewalla, gdy tylko Agent Wywiadowczy zwróci pierwszą partię wykrytych ataków, a wymagania można dopinać w locie bez zakłócania już działających zadań. (2) Environment Scaling — nie wczytuj surowych danych do modelu, lecz pisz dedykowane skrypty ekstrahujące istotne zdarzenia (tu: logi ataków) i uruchamiaj je w izolowanym runtime (AgentOS), dzięki czemu model może wykonywać ryzykowny kod bez zagrożenia dla systemu hosta.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: podawanie całego wolumenu danych (1,2 mln logów / 260 MB) bezpośrednio do kontekstu AI w nadziei, że model 'sobie poradzi'. Skutek to eksplozja liczby tokenów, utrata uwagi, halucynacje i twardy błąd zadania. Drugi anty-wzorzec: poleganie na jednowątkowej, monolitycznej pętli agenta zamiast na asynchronicznym podziale ról — brak równoległości i brak możliwości modyfikacji wymagań w trakcie pracy.

> **Cytat:** *"这个任务最难的点就是, 如果是最传统的Agent系统, 就只能单线思考, 120万条日志(约260MB), 绝对会导致各种注意力丢失或者产生幻觉, 最后整个任务就直接报错.

这次  Apodex 1.1 版本就针对这个场景做了升级. 这里必须要给大家介绍一个概念: Harness Scaling

简单来讲, 光堆模型参数量只能提升模型的"智力", 而堆模型的脚手架(framework), 工具箱(Agent Tools)和团队(Agent Team/Swarm), 就能提升模型干活的能力.

Apodex 1.1 在两个地方发力了:

首先是 Agentic Coordination Scaling（智能体协同扩展）：
它的 Agent Team 像一个真正的 SOC 安全团队一样把任务拆了, 情报 Agent 去清洗几十万条日志提取恶意 IP 和特征, 规则 Agent 根据特征去写 ModSecurity 拦截规则. 注意这些是异步并行的, 速度非常快, 甚至情报 Agent 刚吐出第一批探测到的攻击日志, 规则 Agent 就已经开始写防火墙规则了. 而且如果要改需求, 可以随时在这个过程中添加, 不用担心影响正在跑的任务.

紧接着是 Environment Scaling（环境扩展）：
如果这120万条日志全都让AI去读取, token量肯定直接炸了, 所以有针对性的编写脚本去抽取攻击日志就是工作的主要内容了, 而这些日志全都是运行在 AgentOS 上的, 它是整个 Apodex 系统的运行时承载, 在这个上面模型可以运行各种风险代码而不用担心影响宿主系统."*

---

## Systemy agentowe / AI w cyberbezpieczeństwie

### Agent Apodex 1.1: analiza 1,2 mln linii logów z realnym atakiem privilege escalation i generowanie reguł firewalla end-to-end

- **Data:** `Thu Aug 27 08:39:48 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2092894838492655713)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Systemy agentowe]] [[Harness|AgentOS]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Ewaluacja agentów end-to-end]] [[Sandbox i Granice Bezpieczeństwa Agenta|Analiza logów bezpieczeństwa]] [[Harness|Generowanie reguł firewalla]] [[Harness|Zbiory benchmarkowe]]

**Kontekst / Problem:**
Autor testuje świeżo wydany system agentowy Apodex 1.1 na zadaniu zbliżonym do produkcyjnego SOC: pakuje ~1,2 mln linii logów serwera WWW pochodzących z publicznego zbioru Zenodo, zawierających realne próby ataków privilege escalation, i zleca agentowi (a) identyfikację technik atakującego oraz (b) wygenerowanie reguł firewalla blokujących te ataki. Test ma weryfikować nie pojedynczą umiejętność modelu, lecz zdolność harnessu agentowego do przeprowadzenia całego łańcucha: ingest dużej objętości danych -> analiza -> synteza wniosków -> artefakt wykonywalny (reguły).

**Rada inżynierska:**
Wartościowy wzorzec ewaluacji agenta: zamiast promptów zabawkowych używaj zadania end-to-end na realnym, dużym i zaśmieconym zbiorze danych (np. 1,2 mln linii logów z benchmarku Zenodo), gdzie miarą sukcesu jest artefakt operacyjny — konkretne reguły firewalla blokujące wykryte techniki ataku. Taki test jednocześnie sprawdza inżynierię kontekstu przy dużej objętości wejścia, zdolność do redukcji szumu, jakość rozumowania przyczynowego (mapowanie log -> technika ataku) oraz użyteczność wyniku w warunkach produkcyjnych. Wniosek praktyczny: budując harness agentowy, projektuj pipeline „duży surowy log -> ekstrakcja sygnału -> hipoteza ataku -> wykonywalna reguła”, a nie pojedyncze zapytanie do modelu.

**Uwaga / Anty-wzorzec:**
Pułapka: traktowanie pojedynczego, spektakularnego przebiegu na zamkniętym zbiorze (Zenodo) jako dowodu gotowości produkcyjnej. Brak tu informacji o liczbie fałszywych alarmów, pokryciu ataków, koszcie tokenów przy 1,2 mln linii ani o tym, czy reguły firewalla zostały zweryfikowane na ruchu na żywo. Bez metryk precyzji/recall i bez zewnętrznego weryfikatora reguł wynik pozostaje anegdotą, a nie potwierdzoną kompetencją systemu.

> **Cytat:** *"劲爆, 我给刚发布的 Apodex 1.1 出了个极其变态的实战难题, 它真的跑通了!

我直接打包了120万条日志, 里面包含真实的提权攻击的 Web Server 日志(用的是 Zenodo Dataset). 

然后让他帮我把黑客的攻击方式抓出来, 还要给我写防火墙规则拦截攻击. 结果它真的做到了, 从分析到写规则一气呵成, 具体过程在这里:

https://t.co/Pltj5lZcqN

#Apodex #AgentOS #网络安全 #SystemScaling #大模型实战"*

---

## Benchmarking / Ewaluacja modeli

### Sprzęt GPU nie wpływa na jakość wyjścia modelu — tylko na przepustowość benchmarku

- **Data:** `Thu Aug 20 17:44:00 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2090495077873533333)
- **Rodzaj:** Komentarz w dyskusji (@xueyu1125)
- **Powiązane pojęcia:** [[Harness|Benchmarking modeli LLM]] [[Harness|Ewaluacja jakości vs wydajności]] [[Harness|Przepustowość tokenów (throughput)]] [[Harness|Latencja inferencji]] [[Harness|Kwantyzacja a jakość wyjścia]]

**Kontekst / Problem:**
Autor odpowiada na wątpliwości dotyczące metodologii dużego benchmarku porównującego 44 modele na jednym prompcie. Wyjaśnia, dlaczego używa szybkich kart (H100) i dlaczego wybór akceleratora nie zniekształca wyników jakościowych.

**Rada inżynierska:**
Przy ewaluacji jakościowej (output quality) wybór GPU jest nieistotny dla samego wyniku — determinuje wyłącznie czas trwania testu. Różne karty dają różną przepustowość tokenów i opóźnienie, ale przy tej samej precyzji/liczbach nie zmieniają rozkładu wygenerowanego tekstu. Dla dużych macierzy porównawczych (np. 44 modele × wiele promptów) dobieraj najszybszy dostępny sprzęt, aby zdążyć w rozsądnym czasie — nawet H100 daje ~5 h na cały przebieg dla pojedynczego promptu. Optymalizuj więc czas ewaluacji sprzętem, a nie kompromisami w jakości pomiaru.

**Uwaga / Anty-wzorzec:**
Mylenie benchmarku szybkości (throughput/latency) z benchmarkiem jakości (quality). Jeśli celem jest pomiar jakości, dobór słabszej karty „dla sprawiedliwości" tylko wydłuża eksperyment i nic nie wnosi. Uwaga jednak: zmiana typu kwantyzacji, precyzji (fp16/int8/int4) lub sterowników na tej samej karcie JUŻ wpływa na jakość wyjścia — to nie jest to samo co zmiana modelu GPU.

> **Cytat:** *"因为测试量较大，所以只能用比较快的卡来测，即使用H100测一个prompt，44个模型测试下来也要5小时。而且测试本身是测试模型输出质量，不是测试速度。不同显卡只是输出速度不同，显卡不会影响输出质量。"*

---

## Architektura modeli i systemów agentowych / Ewaluacja AI

### Jev vs generator losowy: dlaczego szybki model jednokrokowy przegrywa z randomem w zadaniach planistycznych

- **Data:** `Mon Sep 21 07:49:04 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2101941770003361893)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Jev]] [[Harness|System-1 vs System-2]] [[Harness|Lokalne optimum]] [[Harness|Planowanie wielokrokowe]] [[Harness|Pólya Random Walk Theorem]] [[Harness|xoshiro256++]] [[Harness|Heurystyka Manhattan]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Benchmark modeli]] [[Harness|Architektura agentów]]

**Kontekst / Problem:**
Autor testuje hipotezę, czy ultraszybki model decyzyjny (Jev) może w niektórych zadaniach wypaść gorzej niż czysty generator losowy. Opierając się na twierdzeniu o błądzeniu losowym Pólyi (w skończonej dwuwymiarowej spójnej siatce prosty random walk jest powracający - pijany człowiek z prawdopodobieństwem 1 w końcu dotrze do celu), zbudował środowisko testowe do rozwiązywania labiryntu: Jev kontra serwer czystego randomu wystawiony przez API o identycznym formacie. Stack: Rust + xoshiro256++ + bit reservoir + Tokio/Hyper. xoshiro256++ to algorytm PRNG z 2018 r. wykonujący się w 1-2 cykli zegara (~0,5-0,8 ns). Celem było sprawdzenie, czy model jednokrokowy z heurystyką faktycznie przewyższa bezmyślny, ale bardzo szybki losowy wybór.

**Rada inżynierska:**
Model typu Jev to jedynie ekstremalnie szybki, jednokrokowy strukturalny klasyfikator decyzyjny - NIE jest planerem. Do zadań wymagających planowania wieloetapowego zawsze dołącz model System-2. Konkretne zasady: (1) nie używaj Jev tam, gdzie potrzebne jest omijanie przeszkód, backtracking i planowanie wielokrokowe (labirynty, pakowanie do pojemników, szeregowanie, problemy grafowe, gdzie lokalna heurystyka rozmija się z globalnym optimum); (2) nie używaj go w sterowaniu typu 'nagła śmierć' (snake, tetris, autonomia - jeden błędny krok = koniec); (3) nie używaj do nieodwracalnych, kosztownych decyzji (usunięcie bazy danych, operacje transakcyjne, scenariusze wymagające audytu). Uzupełniająco: przy projektowaniu promptu dla modelu jednokrokowego heurystyka lokalna (np. odległość Manhattan) dominuje nad regułami warunkowymi - reguła 'jeśli zbyt wiele prób, to zrób inaczej' nigdy się nie uruchomi, jeśli główny sygnał heurystyczny stale wskazuje ten sam kierunek.

**Uwaga / Anty-wzorzec:**
Pułapka: zakładanie, że dostarczenie modelowi pamięci i historii rozwiąże problem planowania. Autor podał Jevowi last_move, visited_count dla każdego sąsiada oraz wprost nakazał priorytetowo wybierać najmniej odwiedzane otwarte pole, gdy bliższe pola są zablokowane lub nadmiernie odwiedzane. Model to zignorował, bo w jego jednostkowym rozumieniu róg (7,4) wciąż był bliżej celu w metryce Manhattan, a reguła warunkowa była traktowana jako drugorzędna i nigdy nie osiągnęła progu aktywacji. Efekt: 2295 z 2306 kroków spędzonych na kręceniu się w 3 polach martwego narożnika (lokalne optimum), aż do timeoutu. Anty-wzorzec inżynierski: powierzanie zadań planistycznych modelowi jednokrokowemu i łatanie tego coraz bogatszym kontekstem zamiast dodania pętli planowania/System-2.

> **Cytat:** *"为什么Jev有些时候不如随机数发生器?

整了个活, 突然想着Jev会不会某些时候还不如纯正态分布决策效果好, 直接用随机数发生器(甚至也可以叫它 System-1)的高 QPS 硬怼？毕竟猴子在打字机前也能敲出莎士比亚.

而且这事在数学上这其实是有正经定理撑腰的, 著名的波利亚随机游走定理(Pólya's Random Walk Theorem),在有限的二维连通网格里, 简单随机游走是常返的(Recurrent), 也就是说, 一个毫无思想的醉汉在迷宫里瞎晃, 以概率 1 最终必定能摸到终点.

神奇吧？理论有了, 于是我写了个测试环境, 拉来 Jev 和纯随机做了一波迷宫寻路对抗测试.

为了不亏待Jev, 我把规则和特征给足, 把曼哈顿距离作为启发式指标塞进输入, 并告诉它尽量减小与终点的距离.

然后用Rust + xoshiro256++ + bit reservoir + Tokio/Hyper. 包了个API格式与Jev一样的随机数server. 注意 xoshiro256++ 作为随机数发生器算法很牛逼, 这玩意是2018年设计的, 运行一次只要 1 ~ 2 个时钟周期(约 0.5 ~ 0.8 纳秒).

测了一波后直接说结论：纯随机赢麻了, Jev 被系统性打崩了

纯随机虽然无脑, 但是性能极高, 即使无并发顺序请求, 892 步也直接通关了. 总计花费不到300ms.

而正 Jev 跑了 2306 步, 其中 2295 步把自己死死困在了 (7,4) 这个拐角的 3 个格子里疯狂原地打转, 直到测试超时(看视频).

有人可能会说：你是不是没给它历史轨迹？给它记忆不就行了？

别急带了的, 我明确带上了 last_move, 每个邻居格子的 visited_count, 指令里还特意写明了当更近的格子被堵或访问过多时, 优先选访问最少的开口.

结果它根本不听.

因为在它的理解里, 这个拐角向右/向下曼哈顿距离更近, "如果尝试过多再xxx"是次要规则, 永远轮不到触发. 它陷入局部最优了.

所以, Jev 它只是一个极速的单步结构化判断器, 但绝不是规划器. 最好还是带一个System-2模型才能进行复杂任务.

最后给大家整理慎用 Jev 的场景：

需要绕路, 回溯, 多步规划的：迷宫, 装箱, 调度等局部启发和全局最优不一致的图问题. 
突然死亡型控制：贪吃蛇, 俄罗斯方块, 自动驾驶等. 一步踏错当场GG. 
不可逆高代价决策：删库, 事务操作, 尤其是需要审计的场景.

项目在这里: https://t.co/TgCLBLhqNc

#Jev #TypeSafeAI #SystemOne #AI评测 #强化学习"*

---

## Bezpieczeństwo modeli / AI Safety / Wielojęzyczna ocena alignmentu

### Test empiryczny: język hebrajski NIE obchodzi zabezpieczeń modeli LLM (Fable-5.1, DeepSeek-V4.1-Flash)

- **Data:** `Mon Sep 21 00:09:21 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2101826076762857867)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|AI Safety]] [[Harness|Jailbreak]] [[Harness|Multilingual Alignment]] [[Harness|Refusal Rate]] [[Harness|Content Gateway / Input Filter]] [[Harness|Over-refusal]] [[Sandbox i Granice Bezpieczeństwa Agenta|Benchmark bezpieczeństwa]] [[Harness|Low-Resource Languages Jailbreak]]

**Kontekst / Problem:**
W sieci krążyła viralowa teza (190 tys. wyświetleń), że używanie języka hebrajskiego pozwala obejść systemy moderacji i odzyskać zablokowane konta, a nawet 'przełamać' warstwę bezpieczeństwa modeli Anthropic. Autor zweryfikował tę hipotezę w kontrolowanym eksperymencie: przygotował korpus szkodliwych i nieszkodliwych promptów z publicznych zbiorów HuggingFace w trzech tłumaczeniach (angielski, chiński, hebrajski) i zmierzył wskaźniki odmowy (refusal rate) dla Fable-5.1 oraz DeepSeek-V4.1-Flash. Wniosek: efekt 'przełamania przez hebrajski' nie istnieje — współczesny alignment jest wielojęzycznie spójny.

**Rada inżynierska:**
Nie zakładaj, że zmiana języka promptu obchodzi zabezpieczenia — nowoczesne modele mają wyrównany alignment wielojęzyczny. Kluczowa jest też architektura dwuwarstwowa: gateway (filtr wejściowy) przechwytuje ~32–36% najbardziej szkodliwych prób, zanim dotrą do modelu, a sam model odmawia w kolejnych ~54–60% przypadków. Skuteczny system bezpieczeństwa wymaga więc obu warstw: taniego, szybkiego filtra na wejściu + alignmentu wytrenowanego w modelu. Przy benchmarkach bezpieczeństwa zawsze stosuj grupę kontrolną promptów, które model POWINIEN odpowiedzieć (nie tylko tych, które powinien odrzucić), aby wykryć nadmierną blokadę (over-refusal).

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: powoływanie się na historyczne wyniki (np. praca z 2023 'Low-Resource Languages Jailbreak GPT-4', gdzie języki typu zulu, szkocki gaelicki czy hmong faktycznie obchodziły zabezpieczenia GPT-4) jako na aktualny stan wiedzy. Ta podatność została w praktyce naprawiona. Drugi anty-wzorzec: mieszanie testu wpływu języka z testem jailbreaków promptowych — autor świadomie rozdzielił te zmienne (kontrola zmiennych), bo są to odrębne zagadnienia badawcze.

> **Cytat:** *"测了一波后直接说结论, 没有这回事. 中文, 英文, 希伯来语的拒绝率没太大区别. 对于有害内容, Fable-5.1的拒绝率是英语 95.0%, 中文 94.4%, 希伯来语 95.1%. 其中被网关拦截大约 32–36%，然后模型正文拒绝回答大约 54–60%. 尤其是极其危险的题目, 基本都没到大模型, 直接网关就拦掉了. 而 DeepSeek-V4.1-Flash 甚至表现更好一些, 英语 100%, 中文 100%, 希伯来语 99.3%."*

---

## Edge AI / Browser-based Agents

### Agent kodujący uruchamiany w całości w przeglądarce: MiniCPM5-2B 4-bit ONNX + WebGPU bez Dockera i Node.js

- **Data:** `Mon Sep 14 22:55:34 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099633181934907654)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|WebGPU]] [[Harness|Edge AI]] [[Harness|ONNX]] [[Harness|Kwantyzacja 4-bit]] [[Harness|Coding Agent]] [[Harness|Tool Call]] [[Prompt Architecture]] [[Harness|MiniCPM]] [[Context Compaction|Pamięć kontekstowa]] [[Sandbox i Granice Bezpieczeństwa Agenta|Anty-wzorce bezpieczeństwa agentów]]

**Kontekst / Problem:**
Projekt HuggingFace Space „MiniCPM5-2B-WebGPU-Pi” pokazuje wzorzec uruchamiania kompletnego agenta kodującego (wirtualny terminal, edycja plików, tool_call) w całości po stronie klienta — framework „Pi” plus kwantyzowany model MiniCPM5-2B (4-bit ONNX, poniżej 2 GB) działają bezpośrednio w przeglądarce przez WebGPU. Nie trzeba stawiać Dockera ani instalować Node.js — wystarczy otworzyć stronę. Rozwiązuje to problemy: brak konieczności hostowania backendu, brak potrzeby konfigurowania API KEY, praca w środowiskach bez dostępu do internetu publicznego oraz wykorzystanie natywnego kontekstu sesji przeglądarki (loginy, cookies).

**Rada inżynierska:**
Wzorzec architektoniczny: przenieś cały stos agenta (harness + model + pętla tool_call) do środowiska klienta. Dzięki temu agent dziedziczy natywnie stan uwierzytelnienia przeglądarki (cookies, sesje, loginy), działa w intranetach i zamkniętych SaaS bez wyjścia na publiczny internet, oraz nie wymaga ani API KEY, ani połączenia sieciowego — model inferuje lokalnie przez WebGPU. Kwantyzacja do 4-bit ONNX (<2 GB) sprawia, że model mieści się w budżecie pamięci przeglądarki. Autor raportuje ~25 tps na GPU 3080Ti oraz zaskakująco dobrą stabilność tool_call przy modelu klasy 2B, co czyni go realnym kandydatem do edge-agentów.

**Uwaga / Anty-wzorzec:**
Ryzyko bezpieczeństwa: agent działający w kontekście sesji użytkownika ma nieograniczony dostęp do jego loginów i cookies — kompromitacja promptu lub złośliwa strona może przejąć uprawnienia użytkownika. Drugi anty-wzorzec: zakładanie, że mały model (2B) poradzi sobie z dowolną złożonością zadań agentowych — autor podkreśla, że to dopiero „mini” modele, a stabilność tool_call wymaga jeszcze weryfikacji w szerszym benchmarku (proponuje zbiorowy test edge-agentów).

> **Cytat:** *"看到个神奇的 huggingface Space项目, 思路很值得借鉴跟大家说下. Space 叫 MiniCPM5-2B-WebGPU-Pi, 不用起 Docker, 也不用装 Node 啥的, 打开网页就是一个带虚拟终端, 能进行文件编辑和 tool_call 的完整Coding Agent. 这玩意用 Pi 包了个 Coding Agent, 然后使用 MiniCPM5-2B 模型驱动. 神奇的地方就是, 这里用的是 MiniCPM5-2B 4bit ONNX 封装版本 (不到2G), 所以从框架到推理模型全都运行在了浏览器上. 我玩了一会想出来的两个奇葩玩法脑洞: 可以白嫖登录态, 框架+模型直接运行在你的浏览器里, 天然带你的登录信息和 Cookie... 另一个脑洞大开的是可以做一个网站自愈插件, 框架监听浏览器console报错, 网页哪儿炸了就可以现场打热补丁... 我实测这玩意在我的3080Ti上能跑到25tps, 框架内部模拟了shell环境和提供了最基础的文件编辑tool_call... MiniCPM5-2B 的 tool_call 稳定性意外的不错, 大家对 2B 这种迷你模型跑 Agent 感兴趣吗?"*

---

## Inżynieria modeli / dystylacja / test-time compute

### Długi CoT, budżet myślenia i dystylacja R1 do małych modeli

- **Data:** `Mon Sep 14 09:52:12 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099436039169536325)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Long Chain-of-Thought]] [[Harness|Dystylacja modeli]] [[Test-Time Compute i Reasoning Tokens|Test-time compute]] [[Harness|Budżet myślenia]] [[Harness|DeepSeek R1]] [[Harness|Qwen]] [[Harness|Ollama]] [[Harness|Anti-pattern: mylenie dystylatu z modelem źródłowym]]

**Kontekst / Problem:**
Wpis przypomina mechanizm stojący za skokiem jakości modeli rozumujących: długie łańcuchy myśli (long CoT) z R1 zostały zdystylowane do małych modeli Qwen 1.5B/7B/14B, a ich wyniki rosną wraz z przyznanym budżetem myślenia w czasie wnioskowania. Autor krytykuje zapominanie tego faktu oraz mylenie modeli zdystylowanych, np. deepseek-r1-distilled-qwen-7b instalowanego przez Ollama, z oryginalnym DeepSeek R1.

**Rada inżynierska:**
Traktuj długi CoT jako dystylowalną kompetencję, ale jej ujawnienie zależy od runtime’owego budżetu myślenia. Przy małych modelach distilled-R1 zwiększaj limit tokenów rozumowania i mierz wydajność w funkcji długości CoT. Zawsze weryfikuj pochodzenie modelu: deepseek-r1-distilled-qwen-7b to dystylat na Qwen, a nie oryginalny DeepSeek R1.

**Uwaga / Anty-wzorzec:**
Uruchamianie modelu dystylowanego przez Ollama i nazywanie go „DeepSeek” bez rozróżnienia architektury, wag i pochodzenia. Pomijanie sekcji o long thinking prowadzi do błędnych wniosków o możliwościach modelu. Zbyt mały budżet myślenia sztucznie zaniża wyniki małych modeli rozumujących.

> **Cytat:** *"请读完了Section 2后继续看Section 3 . 明确写了模型在长思考时的表现. 当时震撼人心的继续从71.0% 飙升到 86.7% 就是这么来的. 然后将 R1 生成的长思维链蒸馏到了小模型（ Qwen-1.5B、7B、14B）。在运行时给足其思考预算，然后解题能力就呈现出与思考长度正相关的暴涨。这不就是去年的新闻嘛....怎么还能记不住呢....然后就ollama把deepseek-r1-distilled-qwen-7b 当deepseek给大家装到电脑上了, 美其名曰运行deepseek. 有印象没? 串起来了吧?"*

---

## Architektura modeli rozumujących / Inżynieria ewaluacji i test-time compute

### SOTA jako kompresor informacji: dlaczego ustawienie reasoning na 'max' psuje benchmarki (odwrócenie wyników SWE)

- **Data:** `Mon Sep 14 09:14:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099426676669366337)
- **Rodzaj:** Komentarz w dyskusji (@karminski3)
- **Powiązane pojęcia:** [[Test-Time Compute i Reasoning Tokens|Reasoning Effort]] [[Harness|Thinking Budget]] [[Test-Time Compute i Reasoning Tokens|Test-Time Compute]] [[Harness|Kompresja informacji]] [[Harness|SWE-bench]] [[Harness|Kryteria zatrzymania rozumowania]] [[Test-Time Compute i Reasoning Tokens|Token Throughput]] [[Harness|Density of Information per Token]]

**Kontekst / Problem:**
Autor odpowiada na wcześniejszą dyskusję o modelach rozumujących (reasoning models), wskazując na trzy konkretne problemy inżynierskie poparte literaturą: (1) dlaczego benchmark SWE (software engineering) potrafi się 'odwrócić' (倒挂) gdy reasoning effort ustawiony jest na max — tzn. model z maksymalnym budżetem myślenia wypada gorzej niż z mniejszym; (2) czy w ogóle ustawienie reasoning/thinking na 'max' jest właściwe; (3) jak sprawić, aby model poprawnie przerywał rozumowanie (kryteria zatrzymania / stop conditions). Teza nadrzędna: najlepsze modele to doskonałe kompresory informacji — rozwiązują najtrudniejsze problemy przy minimalnej liczbie tokenów.

**Rada inżynierska:**
Traktuj model SOTA jako kompresor informacji: optymalny wynik to maksymalna gęstość informacyjna na token, nie maksymalna długość rozumowania. Zwięzłe, eleganckie rozwiązanie (analogia do E=mc²) bije rozwlekłe rozumowanie prowadzące do trywialnej odpowiedzi (analogia do '42' z Autostopem przez Galaktykę). Praktycznie: nie ustawiaj reasoning effort / thinking budget na 'max' bezwarunkowo — waliduj na własnym benchmarku (np. SWE), bo maksymalny budżet myślenia może powodować odwrócenie wyników (spadek jakości). Wdrażaj jawne kryteria zatrzymania rozumowania zamiast liczyć na to, że model sam 'domyśli się', kiedy skończyć.

**Uwaga / Anty-wzorzec:**
Naiwne założenie 'więcej myślenia = lepszy wynik' i bezrefleksyjne ustawianie reasoning effort na 'max'. Skutki: (a) odwrócenie wyników na benchmarkach typu SWE — model z większym budżetem myślenia osiąga gorsze rezultaty; (b) nadmierne, jałowe rozumowanie zużywające tokeny bez poprawy trafności; (c) brak kontroli nad momentem zatrzymania rozumowania (model 'myśli w nieskończoność').

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor podważa powszechny konsensus branżowy, że zwiększanie test-time compute / reasoning effort zawsze poprawia jakość. Teza 'im więcej myślenia, tym lepiej' bywa fałszywa — dowodem jest zjawisko odwrócenia wyników SWE przy ustawieniu reasoning na 'max'. Do rozstrzygnięcia: dla jakich zadań i modeli krzywa jakości od budżetu myślenia jest monotoniczna, a dla jakich ma maksimum lokalne (a więc 'max' jest anty-wzorcem).

> **Cytat:** *"来, 走出民科, 咱们阅读论文. 为什么max测SWE会倒挂：https://t.co/9cV5oLJLLH 设置为max真的就对吗：https://t.co/7QgZzJws0W 到底怎样才能让模型思考的时候正确的停下来: https://t.co/m1M1t03vJi 我重申我的观点, SOTA的模型永远是完美的信息压缩器. 用最少的token解决最难的问题. 思考一大堆得出宇宙的最终解是42不是SOTA. E = mc² 才是. 上次的讨论: https://t.co/HK6fCYvgwu"*

---

## Inżynieria promptów / Modele rozumujące (reasoning) / Efektywność tokenowa

### SOTA jako idealny kompresor informacji — krytyka „max reasoning effort” i rekomendacja czytania źródeł naukowych

- **Data:** `Mon Sep 14 08:52:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099421138069950509)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Test-Time Compute i Reasoning Tokens|Reasoning budget / max thinking tokens]] [[Harness|Inwersja max na SWE-bench]] [[Harness|Stop condition w modelach rozumujących]] [[Harness|Kompresja informacji jako metryka SOTA]] [[Harness|Token efficiency]] [[Harness|Chain-of-Thought]] [[Harness|Benchmark SWE-bench]]

**Kontekst / Problem:**
Autor krytykuje dwa popularne zjawiska w praktyce inżynierskiej: (1) bezrefleksyjne ustawianie modeli rozumujących na maksymalny budżet myślenia („max”), co według niego powoduje inwersję wyników benchmarku SWE (倒挂 — paradoks: więcej myślenia = gorsze wyniki), oraz (2) kulturę „民科” (amatorskiej pseudonauki) w środowisku AI, gdzie zamiast czytać publikacje naukowe powiela się intuicje. Autor odsyła do trzech prac/materiałów: (a) dlaczego testowanie SWE z ustawieniem max daje odwrócone wyniki, (b) czy „max” faktycznie jest poprawnym ustawieniem, (c) jak doprowadzić model do poprawnego zatrzymania procesu rozumowania (stop condition).

**Rada inżynierska:**
Traktuj model SOTA jako idealny kompresor informacji: metryką jakości jest zdolność rozwiązania najtrudniejszego problemu przy MINIMALNEJ liczbie tokenów. Nie zakładaj, że więcej rozumowania = lepiej — nadmierny budżet myślenia prowadzi do nadprodukcji tokenów i może obniżyć wynik na benchmarkach typu SWE (inwersja „max”). Kluczowe inżyniersko jest projektowanie warunku zatrzymania rozumowania (poprawnego „stopu”), a nie maksymalizowanie długości chain-of-thought. Wzorcowy wynik to zwięzła, elegancka formuła (E=mc²), nie rozwlekłe dochodzenie do „42”.

**Uwaga / Anty-wzorzec:**
Ustawianie parametru „max reasoning effort”/„max thinking tokens” jako domyślnej strategii poprawy jakości. Autor twierdzi, że prowadzi to do inwersji wyników (np. na SWE-bench) — model zużywa budżet na zbędne rozumowanie, rozjeżdża się z intencją i zatrzymuje się w złym momencie. Drugi anty-wzorzec: poleganie na intuicji i community lore zamiast na źródłach naukowych (postawa „民科”).

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor podważa powszechny konsensus branżowy, zgodnie z którym zwiększanie budżetu rozumowania (max effort / więcej tokenów myślenia) monotonicznie poprawia jakość modelu. Teza karminski3: dla modeli SOTA istnieje punkt przegięcia — nadmierny budżet myślenia powoduje inwersję wyników na benchmarkach agentowych/SWE, a prawdziwym wyróżnikiem SOTA jest zdolność do zwięzłej kompresji informacji (minimalne tokeny na najtrudniejsze problemy), a nie długość rozumowania. Wymaga weryfikacji empirycznej na konkretnych modelach (o-series, DeepSeek R1, QwQ itd.) i benchmarkach.

> **Cytat:** *"来, 走出民科, 咱们阅读论文. 
为什么max测SWE会倒挂：https://t.co/9cV5oLJLLH
设置为max真的就对吗：https://t.co/7QgZzJws0W
到底怎样才能让模型思考的时候正确的停下来: https://t.co/m1M1t03vJi 
我重申我的观点, SOTA的模型永远是完美的信息压缩器. 用最少的token解决最难的问题. 思考一大堆得出宇宙的最终解是42不是SOTA. E = mc² 才是."*

---

## Parametry wnioskowania / Reasoning Effort / Thinking Budget

### Przełącznik intensywności rozumowania (thinking effort) realnie skaluje zdolności modelu — nie jest neutralną gałką

- **Data:** `Mon Sep 14 07:14:23 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099396323942547519)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|DeepSeek-R1-Zero]] [[Harness|Thinking Budget]] [[Test-Time Compute i Reasoning Tokens|Reasoning Effort]] [[Harness|Chain-of-Thought]] [[Harness|AIME24]] [[Harness|RL bez SFT (Zero-SFT RL)]] [[Harness|Skalowanie długości rozumowania]] [[Harness|Benchmarki rozumowania]]

**Kontekst / Problem:**
Autor testował model deepseek-v4.1-flash z ustawieniem maksymalnej intensywności rozumowania (max). W komentarzach spotkał się z zarzutem, że powinien użyć trybu 'high', a nie 'max', oraz z tezą, że przełącznik intensywności myślenia to jedynie 'kontrolka' niezwiązana z wydajnością modelu. Autor odpiera ten zarzut, przywołując własną publikację DeepSeek z zeszłego roku (DeepSeek-R1-Zero), która empirycznie wykazała korelację między długością/intensywnością rozumowania a wynikami benchmarków. Problem dotyczy tego, czy parametr 'thinking effort/budget' należy traktować jako realny czynnik wydajności, czy jako kosmetyczną preferencję.

**Rada inżynierska:**
Traktuj intensywność rozumowania (thinking effort / budget) jako realny wymiar skalowania zdolności modelu, a nie neutralną preferencję. DeepSeek-R1-Zero (RL bez SFT, bez dodawania nowej wiedzy) pokazał, że wraz ze wzrostem długości rozumowania wynik AIME24 wzrósł z ok. 15% do ok. 71% — sama zmiana długości myślenia, bez nowych danych, dramatycznie podniosła jakość. Praktyczna reguła: przy zadaniach wymagających rozumowania nie obniżaj pochopnie trybu z 'max' na 'high' — najpierw zmierz wpływ na wyniki dla swojego przypadku. Zanim podważysz zachowanie parametru, sprawdź literaturę i wyniki eksperymentalne, a nie intuicję.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: bagatelizowanie przełącznika intensywności rozumowania jako 'tylko kontrolki' bez wpływu na wydajność oraz argumentowanie na podstawie intuicji zamiast danych/publikacji. Drugi anty-wzorzec: wygłaszanie autorytatywnych twierdzeń o parametrach modelu bez zapoznania się z podstawowymi pracami z zakresu (tu: DeepSeek-R1-Zero) — 'pseudonauka' objawiająca się ignorowaniem dowodów empirycznych. Trzeci: porównywanie trybów 'high' vs 'max' bez pomiaru i bez uwzględnienia, że wyższa intensywność zwykle zwiększa koszt opóźnienia (latency) i zużycie tokenów — trade-off należy mierzyć, nie zgadywać.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor jawnie podważa rozpowszechnioną opinię (wyrażaną przez komentujących), że przełącznik intensywności myślenia (max vs high) to jedynie kontrolka bez związku z wydajnością. Teza autora: intensywność rozumowania wprost przekłada się na zdolności modelu (dowód: DeepSeek-R1-Zero, AIME24 15%→71% przy wzroście długości rozumowania, bez dodawania wiedzy). Do rozstrzygnięcia pozostaje zakres tej zależności: czy wyższy 'effort' zawsze jest korzystny, czy istnieje punkt nasycenia (saturation), w którym dalsze zwiększanie budżetu myślenia daje malejące zwroty lub pogorszenie (overthinking). Wpis jest nowszy i reprezentuje stanowisko autora wobec wcześniejszego konsensusu komentujących.

> **Cytat:** *"DS民科怎么这么多, 我测完了 deepseek-v4.1-flash, 开 max, 然后评论跟我说应该开high, 不应该开max. 〇的我买法拉利然后你跟我说挂一档比挂二挡快是吧? 然后跟我说这只是思考强度开关, 跟性能没关系. 干你〇怎么就没关系..... 去年 deepseek 自家发的 DeepSeek-R1-Zero 论文怎么都忘了: https://t.co/FICrqgGzb0 就这个论文证明了思考强度越强模型能力越强的. 论文里Zero-SFT RL了一波, 没有增加任何新知识, 随着思考长度增加, AIME24 跑分就从 15% 魔法般的飙到了 71%. 然后震撼业界的雷霆大思考就如同雨后春笋般普及了..... 劝D小鬼对线前看看论文, 大水冲了自家龙王庙了."*

---

## Architektura promptów / Agent Skills / Inżynieria kontekstu

### Izomorfizm kodu i danych w Skillach: metaprogramowanie mikro-skillów dla ekstrakcji danych

- **Data:** `Mon Sep 14 06:23:09 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099383433034440811)
- **Rodzaj:** Komentarz w dyskusji (@kalasoo)
- **Powiązane pojęcia:** [[Dynamiczne Skille i Metaprogramowanie Agenta|Agent Skills]] [[Dynamiczne Skille i Metaprogramowanie Agenta|Micro-Skill]] [[Prompt Architecture|Metaprogramowanie promptów]] [[Harness|Izomorfizm kodu i danych]] [[Harness|Ekstrakcja deterministyczna vs LLM]] [[Harness|Pydantic walidacja]] [[Harness|Harness weryfikacyjny]] [[Prompt Architecture|Kompilacja promptu do kodu]]

**Kontekst / Problem:**
Problem: większość ludzi pisze 'skille' (np. Claude Skills) jak statyczne dokumenty-szablony — np. 'wyciągnij datę i kwotę faktury w podanym formacie'. Taki skill działa tylko na formatach przewidzianych z góry i 'wybucha', gdy pojawi się nieznany układ dokumentu. Autor wskazuje, że źródłem błędu jest traktowanie skilla jako dokumentu, podczas gdy skill może być jednocześnie kodem i danymi (izomorfizm), co otwiera drogę do metaprogramowania: skill nie ekstrahuje danych wprost, lecz generuje wyspecjalizowany pod-zadanie (Micro-Skill) i uruchamia go.

**Rada inżynierska:**
Traktuj skill jako program, który sam wytwarza kod i dane, a nie jako sztywny szablon. Zamiast kazać modelowi bezpośrednio zwracać JSON, zleć mu najpierw analizę topologii układu i konwencji nazewniczych dokumentu, a następnie dynamiczne wygenerowanie dedykowanego Micro-Skilla, który: (1) rozdziela pola deterministyczne — ekstrahowane regexem i kompilowane do klasycznego kodu — od pól niejednoznacznych wymagających LLM, (2) generuje ultra-zwięzły prompt (<50 znaków) tylko dla części niejednoznacznej, (3) tworzy klasę walidacji Pydantic jako lekki harness weryfikujący spójność (np. kwota z VAT == kwota netto + VAT). Dzięki temu skill jest odporny na nieznane formaty i 'sam się utrzymuje', o ile model jest wystarczająco zdolny.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: pisanie skilla jako statycznego dokumentu/szablonu ekstrakcji ('wyciągnij pole X w formacie Y'). Skutkuje to kruchym rozwiązaniem, które zawodzi przy każdym formacie nieprzewidzianym w treści skilla. Drugi anty-wzorzec: zlecanie LLM ekstrakcji pól, które da się wyciągnąć deterministycznie (regex/parser) — marnotrawstwo tokenów i utrata niezawodności. Trzeci: brak harnessu walidującego spójność wyników (np. relacji arytmetycznych między polami).

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Teza kontrowersyjna wobec dominującej praktyki tworzenia Skillów jako statycznych, deklaratywnych instrukcji/dokumentów (podejście 'prompt-as-document'). Autor twierdzi, że właściwym paradygmatem jest 'prompt-as-program' — skill generujący kod (regex→kod) i dane (prompt dla LLM) w locie oraz samowalidujący się przez harness. Do rozstrzygnięcia: (a) czy dynamicznie generowane Micro-Skille są stabilne i bezpieczne w produkcji (ryzyko prompt injection / niestabilności generacji), (b) czy zysk z metaprogramowania przewyższa koszt dodatkowej inferencji przy generowaniu skilla per dokument, (c) jak wersjonować i audytować skille, które zmieniają się w czasie wykonywania.

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

## Architektura promptów / Systemy agentowe / Metaprogramowanie

### Izomorfizm skilli: metaprogramowanie przez dynamiczne generowanie Micro-Skilli zamiast statycznych dokumentów

- **Data:** `Mon Sep 14 06:22:54 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099383368999965122)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Izomorfizm kodu i danych]] [[Dynamiczne Skille i Metaprogramowanie Agenta|Micro-Skill]] [[Prompt Architecture|Metaprogramowanie promptów]] [[Harness|Ekstrakcja deterministyczna vs LLM]] [[Harness|Harness weryfikacyjny]] [[Harness|Walidacja Pydantic]] [[Dynamiczne Skille i Metaprogramowanie Agenta|Agent Skills]]

**Kontekst / Problem:**
Autor krytykuje powszechną praktykę pisania 'skilli' (agent skills) jako statycznych dokumentów zawierających sztywne instrukcje ekstrakcji (np. 'wyciągnij datę i kwotę faktury w tym formacie'). Takie podejście jest kruche — każdy nieznany wariant wejścia (nowy layout faktury) powoduje awarię, bo skill nie potrafi się zaadaptować. Problem rozwiązuje koncepcja izomorfizmu kodu i danych: skill powinien być jednocześnie danymi (opisem intencji) i kodem (wykonywalną logiką), co otwiera drogę do metaprogramowania.

**Rada inżynierska:**
Traktuj skill jako program, nie dokument. Zamiast hardkodować reguły ekstrakcji, zleć modelowi analizę topologii układu i konwencji nazewniczych wejścia, a następnie dynamiczne wygenerowanie dedykowanego Micro-Skilla, który: (1) dzieli pola na deterministyczne — ekstrahowane regexem i kompilowane do klasycznego kodu, oraz niejednoznaczne — ekstrahowane przez LLM z ultra-zwięzłym promptem (≤50 znaków); (2) generuje klasę walidacyjną Pydantic działającą jako prosty harness weryfikujący spójność semantyczną (np. kwota z podatkiem == kwota bez podatku + podatek). Dzięki temu skill jest samoadaptujący się i nie wymaga ręcznej konserwacji, dopóki model jest wystarczająco zdolny.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: 'skill jako dokument' — zapisanie jednego sztywnego formatu wyjścia (JSON) i sztywnych reguł ekstrakcji. Skutkuje natychmiastową awarią przy każdym nieznanym formacie wejściowym. Drugi błąd: wymuszanie bezpośredniego wyjścia JSON zamiast wygenerowania konfiguracji ekstrakcji — miesza warstwę danych z warstwą logiki i uniemożliwia rozdzielenie ekstrakcji deterministycznej od probabilistycznej.

> **Cytat:** *"传统文档大多数时间只是【代码】或【数据】其中的一种. 而skill能实现代码与数据同构的特性. ... 理解了skill的同构性就能玩元编程: "分析这张发票的排版拓扑和命名惯例, 不要直接输出 JSON 结果, 动态生成一个专用的skill(Micro-Skill)并运行它来提取配置, 包括: 哪些字段可以通过正则表达式确定性提取(编译为传统代码). 哪些歧义字段需要 LLM 提取, 并生成一份不超过 50 字的超精简 Prompt. 生成严格验证该格式的 Pydantic 校验类(简单harness, 类似含税金额 == 不含税金额 + 税额). ""*

---

## Benchmarki LLM / Agentic Coding / Backend

### Benchmark stabilności i kosztu modeli LLM w backendowym AgenticCoding: Fable-5.1 SOTA, GPT6-Astra rekomendowany dla oszczędności tokenów

- **Data:** `Mon Sep 14 05:50:26 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099375198986461418)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Agentic Coding]] [[Harness|Benchmark LLM]] [[Harness|Wariancja wyników modeli]] [[Harness|Koszt tokenów]] [[Prompt Architecture|Prompt Engineering]] [[Harness|Bazy danych wektorowych]] [[Stabilność modeli i przestrzeganie promptu|Stabilność modeli]] [[Harness|DeepSeek-V4.1-Flash]] [[Harness|GPT6-Astra]] [[Harness|Fable-5.1]] [[Harness|Kimi-K3]] [[Harness|Hy4-dev]]

**Kontekst / Problem:**
Autor porównuje modele językowe w zadaniu polegającym na implementacji od zera bazy danych wektorowych w scenariuszu backendowego AgenticCoding, gdzie ocena wynika z wydajności działania bazy. Benchmark uwzględnia nie tylko maksymalny wynik, ale też rozrzut wyników między trzema próbami oraz koszt tokenów. Fable-5.1 osiąga SOTA, ale ma bardzo wysoką wariancję; GPT6-Astra jest stabilny i tańszy w użyciu; DeepSeek-V4.1-Flash ma najlepszy stosunek jakości do kosztu w prostszych zadaniach.

**Rada inżynierska:**
W backendowym AgenticCoding oceniaj model nie tylko po szczycie wyniku, ale przede wszystkim po stabilności między próbami (Δ). Do zadań powtarzalnych i oszczędności tokenów wybieraj modele o niskiej wariancji: GPT6-Astra, Kimi-K3 lub DeepSeek-V4.1-Flash. Modele o wysokim potencjale, ale dużej zmienności (Fable-5.1, Hy4-dev) stosuj tylko z dobrze dopracowanym promptem i budżetem na wielokrotne próby. Dla prostych zadań najefektywniejszy kosztowo jest DeepSeek-V4.1-Flash; dla złożonych — GPT6-Astra lub Fable-5.1.

**Uwaga / Anty-wzorzec:**
Antywzorzec: wybór modelu wyłącznie po najlepszym pojedynczym wyniku (np. Fable-5.1 = 21191.51) bez analizy wariancji. Prowadzi to do przepalania tokenów na wielokrotne „losowanie” odpowiedzi i nieprzewidywalności w produkcji. Ignorowanie Δ>50% jako ryzyka operacyjnego jest błędem inżynierskim.

> **Cytat:** *"同步一波大模型写后端代码排行榜

GPT6-Astra 和 Fable-5.1 没来得及做视频, 直接给大家同步图文了.

就结论来说, 单纯后端 AgenticCoding 场景(注意我只说我这个测试, 用大模型从0实现向量数据库, 使用数据库性能计分. 别的我不知道). 目前Fable-5.1 还是SOTA. 写出来的向量数据库直接是第二名的2x.

不过Fable的表现反而跟GPT 完全反过来了, 之前测Anthropic的模型(opus/sonnet) 系列, 反而是最稳的, 三次测试中最高分和最低分差距不超过10%. 而这次 GPT6-Astra 三次得分反而很接近(12985.28, 12134.83, 10676.74), 这证明这个模型的后训练极其稳定, 而 Fable-5.1 则是  21191.51, 11915.19, 7998.93. Δ超过50%. 

所以从省token的角度, 其实更推荐使用 GPT6-Astra. 因为发挥稳定, 不需要重复抽卡. 而 Fable-5.1 更适合经验丰富的工程师好好写提示词后再使用.

国产模型正好也是这个局面, Hy4-dev 虽然分数高, 但是三次得分差距巨大, 10778.51, 6011.78, 4915.22. 而 Kimi-K3 则相对稳定. 另外最具性价比无疑是 DeepSeek-V4.1-Flash. 得分几乎跟 kimi-k3没区别了. 而且Δ<20%. 所以只要不是复杂的代码任务, 直接无脑 DeepSeek-V4.1-Flash最划算. 而复杂的尝试使用GPT6-Astra 和 Fable-5.1.

> #gpt6astra #fable51 #deepseekv41flash"*

---

## Benchmarking i ewaluacja modeli / Inżynieria agentowa

### Dobór reasoning_effort per zadanie dla małych modeli agentowych (Qwen3.8-27B) — wnioski z testów na H100 NVL + llama.cpp

- **Data:** `Mon Aug 31 08:26:49 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2094341123124985991)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Qwen3]] [[Test-Time Compute i Reasoning Tokens|reasoning_effort]] [[Harness|llama.cpp]] [[Harness|MLX]] [[Architektura KV Cache i Rozumowanie Latentne|MTP (Multi-Token Prediction)]] [[Harness|Kwantyzacja GGUF / UD-Q4_K_XL]] [[Harness|H100 NVL]] [[Harness|Agent Harness]] [[Harness|Benchmarking LLM]] [[Harness|Single-GPU Inference]]

**Kontekst / Problem:**
Autor opublikował drabinkę (leaderboard) zdolności agentowych małych modeli LLM, testowanych w jednolitym harnessie: pojedyncza karta H100 NVL + najnowsza wersja llama.cpp. Problem, który rozwiązuje: jak wybrać konkretny model, kwantyzację i poziom reasoning_effort dla obciążenia agentowego (tool-calling, pętle decyzyjne) versus obciążenia generowania kodu, oraz jak różni się wydajność runtime'u na sprzęcie Apple względem CUDA.

**Rada inżynierska:**
Reguła inżynierska: poziom reasoning_effort należy dobierać per typ obciążenia, a nie globalnie. Dla zadań agentowych (planowanie, wywołania narzędzi, iteracyjne decyzje) ustawiaj reasoning_effort = low — nadmiar tokenów rozumowania zwiększa latencję i dryf w pętli agenta bez zysku na jakości. Dla generowania kodu przełączaj na medium/high, gdzie głębsze rozumowanie realnie poprawia poprawność. Rekomendowany model z testów: Qwen3.8-27B w kwantyzacji UD-Q4_K_XL — najlepszy kompromis jakość/rozmiar wśród sprawdzonych wariantów. Benchmarki prowadź na izolowanym, jednolitym stacku (single GPU H100 NVL + aktualny llama.cpp), aby wyniki były porównywalne między modelami. Na macOS preferuj runtime MLX zamiast llama.cpp — pomiarowo MLX z włączonym MTP (Multi-Token Prediction) wypada szybciej niż llama.cpp z MTP na tym samym sprzęcie Apple.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: traktowanie reasoning_effort jako parametru 'im wyżej, tym lepiej' i ustawianie go globalnie na high dla wszystkich zadań — w harnessach agentowych to marnotrawstwo budżetu tokenów i wzrost latencji. Druga pułapka: przenoszenie wniosków wydajnościowych między backendami — llama.cpp z MTP na Macu nie jest reprezentatywny dla MLX z MTP; wybór runtime'u musi być weryfikowany empirycznie na docelowej platformie. Trzecia: mieszanie środowisk (różne GPU, różne wersje llama.cpp) w jednym rankingu unieważnia porównanie.

> **Cytat:** *""小模型 Agent 能力测试的天梯在这里~ (希望图不要被压得太狠....)

目前来看最值得使用是我测试的 Qwen3.8-27B-UD-Q4_K_XL 版本, Agent 用使用 reasoning_effort = low, 然后写代码开到 medium / high.

另外文中是统一使用单卡 H100 NVL+llama.cpp 最新版本测试的. 如果是Mac用户还是建议优先使用MLX, 实测 MLX 开 MTP 会比 llama.cpp 放在 Mac 上开MTP要快一些.

最后老铁们还想看什么模型的评测欢迎留言~ 我赶紧肝哈哈

#qwen38""*

---

## Benchmarking i ewaluacja LLM

### Metodologia benchmarku małych modeli: kontrola kwantyzacji, MTP i poziomu rozumowania

- **Data:** `Mon Aug 31 06:27:32 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2094311103987581033)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Benchmark LLM]] [[Harness|Kwantyzacja modeli]] [[Architektura KV Cache i Rozumowanie Latentne|MTP (Multi-Token Prediction)]] [[Harness|pass@k]] [[Harness|Poziom rozumowania (thinking)]] [[Harness|Małe modele open-source]]

**Kontekst / Problem:**
Autor przeprowadził kompleksowy benchmark 8 małych modeli open-source (Qwen3.8/3.6, Ornith, Gemma-4, GPT-OSS) w kontekście zadań frontendowych, Python i agentowych. Celem było wyłonienie najlepszego modelu przy uwzględnieniu wielu wymiarów: 4 warianty kwantyzacji, włączanie/wyłączanie MTP (Multi-Token Prediction) oraz trzy poziomy intensywności rozumowania (low, medium, xhigh).

**Rada inżynierska:**
Przy benchmarkowaniu modeli LLM należy ściśle kontrolować zmienne: używać tej samej kwantyzacji, konfiguracji MTP oraz poziomu thinking dla każdego porównania. Stosować metrykę pass@3 (najlepszy z 3 przebiegów) dla zadań generatywnych. Wydajność GPU (np. H100) wpływa wyłącznie na szybkość generacji, a nie na jakość odpowiedzi – nie należy mylić czasu wykonania z jakością modelu.

**Uwaga / Anty-wzorzec:**
Błędem jest zakładanie, że szybsza karta graficzna poprawia jakość generacji lub że porównanie modeli bez kontroli kwantyzacji, MTP i poziomu rozumowania daje wiarygodne wyniki. Pominięcie tych zmiennych prowadzi do niemiarodajnych wniosków.

> **Cytat:** *"终于搞完了! 给大家带来小模型竞技场, 这次测试了8款模型, 包括:

Qwen3.8-27B
Qwen3.6-27B
Qwen3.6-35B-A3B
Ornith-1.5-35B-A3B
Gemma-4-31B
Gemma-4-26B-A4B
Gemma-4-12B
GPT-OSS-20B

每个模型4个量化版本, 还测试了 MTP 开启和关闭, 以及 low, medium, xhigh 三档思考强度, 做了个全面横评.

测试主要集中在前端, python, Agent 能力上, 每个测试运行3次取最佳结果(pass@3). 

测试使用H100显卡(注意用H100是为了生成快, 就这还跑了48小时, 显卡不影响生成效果, 只影响生成速度), 总成本148刀.

那么这些模型中究竟谁是开源之神? 请看视频!"*

---

## Multimodalne modele AI / Systemy agentowe

### Qwen3.8-Omni-Flash: multimodalny model z agentowymi możliwościami, integracja z harnessami i pluginami

- **Data:** `Fri Sep 18 00:57:36 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2100751056104026497)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Qwen3.8-Omni-Flash]] [[Harness|Qwen-Live-Harness]] [[Harness|Qwen-MM-Plugins]] [[Dynamiczne Skille i Metaprogramowanie Agenta|omni-skill-creator]] [[Harness|Multimodalność]] [[Harness|Agenci AI]] [[Harness|Claude Code]] [[Harness|Gemini CLI]] [[Harness|Codex]] [[Harness|OpenClaw]]

**Kontekst / Problem:**
Nowa generacja modelu Qwen3.8-Omni-Flash przewyższa poprzednią wersję o 25% średnio, ze szczególnym wzrostem w zadaniach agentowych. Redukuje błąd rozpoznawania mowy w nakładających się rozmowach z 88% do 3%, obsługuje do 1 godziny ciągłego audio/wideo i obniża koszt API o 98% (z 18 do 0,8 CNY za milion tokenów). Wersja Realtime osiąga opóźnienie ~981 ms dla 20 s audio. Qwen-Live-Harness to interfejs (pływający przycisk) do konwersacji i monitorowania zadań z tablicą zadań i powiadomieniami. Qwen-MM-Plugins to biblioteka pluginów integrująca multimodalność z Claude Code, Gemini CLI, Codex, OpenClaw, dodająca wizję, pamięć długich wideo i operacje na Blender/CAD. omni-skill-creator tworzy umiejętności na podstawie nagrania wideo z komentarzem głosowym.

**Rada inżynierska:**
Wykorzystaj Qwen-MM-Plugins do dodania multimodalności (wizja, pamięć wideo, sterowanie CAD/Blender) do lokalnych agentów. Użyj omni-skill-creator do tworzenia umiejętności przez nagranie wideo z jednoczesnym komentarzem głosowym, co przypomina uczenie przez demonstrację. Do zadań monitorujących i asynchronicznych stosuj Qwen-Live-Harness z tablicą zadań. Ze względu na 98% obniżkę kosztów, warto rozważyć ten model do długich wejść audio/wideo, zastępując poprzednie wersje.

**Uwaga / Anty-wzorzec:**
Unikaj używania poprzednich wersji modelu do transkrypcji wieloosobowych spotkań – ich błąd wynosił 88%. Upewnij się, że integracja pluginów z agentami jest poprawna, aby nie wprowadzać błędów w działaniu agenta.

> **Cytat:** *""Qwen-Live-Harness? 来看看是啥

Qwen 刚刚发布了 Qwen3.8-Omni-Flash! 同时还发布了两个配套框架, Qwen-Live-Harness, Qwen-MM-Plugins. 给大家整理一下都是啥.

首先Qwen3.8-Omni-Flash, 比上一代的Qwen3.5-omni-flash 平均分提升了25%. 其中最猛的就是Agent能力, 有的分数甚至翻倍了.

然后多人重叠会议语音识别的错误率直接从上一代的88%降低到了3%. 真正的可用了. 除此之外, 原生支持最长 1 小时的完整连续音视频输入, 并且API费用降低了98%.

98%是什么概念? 之前音频输入每百万token是18块, 现在是0.8元!

除此之外, 这次还发布了 Qwen3.8-Omni-Flash-Realtime, 这个是超低延迟版本, 能做到听完问题, 稍加思考后开口的效果(20s音频约981ms).

而Qwen-Live-Harness 和 Qwen-MM-Plugins 又是啥呢?

首先 Qwen-Live-Harness 搞了个悬浮球, 点击后就可以与模型对话了, 它还能做到环境监控, 比如可以跟它说: 我离开一会, 任务跑完了叫我. 它会把任务塞到任务看板里面, 持续跟进任务状态, 最后播报. 

而Qwen-MM-Plugins则是个"赋能"插件库, 可以给 Claude Code、Gemini CLI、Codex、OpenClaw 安装, 装之后就可以多模态的调用 Qwen3.8-Omni-Flash 了. 补齐本地Agent视觉, 长视频记忆能力, 包括操作Blender或者CAD软件进行视觉建模也可以.

除此之外, 里面还弄了个特别有意思的叫 omni-skill-creator, 只需要录一段操作软件的视频, 然后丢给它, 他就能帮你形成操作这个软件的skill! 很像那种机械臂的示教学习, 只需要拉着机械臂的手走一遍, 机械臂就学会接下来怎么操作了. 一定要注意, 模型是全模态的, 所以录视频的时候还可以把自己的语音一起录进去, 告诉模型为什么这么做, 加深模型的理解, 创建出来的skill更准确.

 #Qwen38omniflash #QwenLiveHarness #QwenMMPlugins""*

---

## Inżynieria kontekstu multimodalnego / analiza wideo w LLM

### Dwupoziomowe próbkowanie klatek (1fps makro + okna zdarzeń) dla precyzyjnej analizy wideo w modelach multimodalnych

- **Data:** `Fri Aug 21 17:49:35 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2090858868989706352)
- **Rodzaj:** Komentarz w dyskusji (@karminski3)
- **Powiązane pojęcia:** [[Harness|Multimodal LLM]] [[Harness|image_url]] [[Harness|Dwupoziomowe próbkowanie klatek]] [[Harness|Event-window sampling]] [[Context Compaction|Inżynieria kontekstu]] [[Prompt Architecture|Prompt Engineering]] [[Harness|Analiza wideo w LLM]] [[Harness|Sampling rate]]

**Kontekst / Problem:**
Problem: jak podawać materiał wideo do modelu multimodalnego (vision-LLM) przez API, aby uzyskać precyzyjną analizę treści — w tym szybkich zdarzeń (np. akcji w grze FPS) — bez utraty detali i bez przekroczenia limitów kontekstu/kosztu.

**Rada inżynierska:**
1) Dekomponuj wideo do sekwencji klatek JPEG/PNG, przekazuj je jako serię wielu `image_url` W KOLEJNOŚCI CZASOWEJ. 2) W prompcie jawnie zdeklaruj współczynnik próbkowania (sampling rate) oraz oś czasu / mapowanie klatka→timestamp, żeby model mógł wnioskować o tempie i kolejności zdarzeń. 3) Nie próbkuj całego materiału równomiernie: użyj dwupoziomowego schematu — makro-przegląd całego wideo w ~1 fps (pełna klatka) PLUS dodatkowe okna zdarzeń (event windows) próbkowane z wysokim FPS i przycięte/zzoomowane do centrum zainteresowania. Ten schemat znacząco poprawia rozpoznawanie szybkich akcji (walidowany na nagraniu CS2), a także dokładność rozpoznawania w materiale animowanym (walidowany na klipie Tom i Jerry).

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: równomierne (jednostajne) próbkowanie całego wideo — „匀速抽全片”. Powoduje utratę kluczowych klatek szybkich zdarzeń (motion blur, pominięcie momentów akcji) i obniża dokładność analizy. Drugi anty-wzorzec: przekazywanie klatek bez zadeklarowanego w prompcie sampling rate i osi czasu — model nie ma podstawy do wnioskowania o tempie/chronologii.

> **Cytat:** *"把视频抽成 JPEG/PNG, 按时间顺序作为多个 `image_url` 传入, 并在 prompt 里写明采样率和时间轴. 这样分析会更准确. 我使用了一个猫和老鼠的片段进行分析, 这样做模型识别很准确.

另外, 我还用了一段 CS2 录像来验证分析快速动作时的最佳方案, 结论是不要匀速抽全片, 用「宏观 1fps 全图 + 事件窗口高帧率中心放大」两级采样。效果会更好.

详细教程和POV开源在这里: https://t.co/DaeLlbTySr"*

---

## Multimodalność / Inżynieria wejścia wizyjnego

### DeepSeek-V4-Flash-Vision-Exp: przetwarzanie wideo przez ekstrakcję klatek zamiast konwersji do GIF

- **Data:** `Fri Aug 21 17:49:34 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2090858863679750280)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Ekstrakcja klatek wideo]] [[Harness|Modele multimodalne]] [[Harness|DeepSeek]] [[Harness|Frame sampling]] [[Context Compaction|Budżet kontekstu]] [[Harness|Limity wejścia API]]

**Kontekst / Problem:**
DeepSeek udostępnił deepseek-v4-flash-vision-exp — pierwszy multimodalny (wizyjny) duży model w klasie możliwości v4-flash. Model obsługuje obraz, ale nie przyjmuje audio, a oficjalne API i strona DeepSeek nie wystawiają natywnego wejścia wideo. Powstaje więc problem integracyjny: jak podać modelowi treść wideo, skoro jedynym kanałem wejściowym są pojedyncze obrazy. Autor opisuje obejście tego ograniczenia po stronie harnessu/klienta API.

**Rada inżynierska:**
Przy modelu wizyjnym bez natywnego wsparcia wideo stosuj dekompozycję wideo na sekwencję klatek (frame sampling) i podawaj je jako osobne obrazy w kontekście. To jedyna niezawodna ścieżka — nie próbuj opakowywać wideo w formaty animowane, bo model traktuje je jak zwykły obraz statyczny. Dobór gęstości próbkowania klatek i rozdzielczości to główne parametry wpływające na koszt tokenów oraz na to, czy model wychwyci zdarzenia krótkotrwałe (przy rzadkim próbkowaniu tracisz klatki kluczowe, przy gęstym — eksploduje budżet kontekstu).

**Uwaga / Anty-wzorzec:**
Konwersja wideo do GIF-a jest anty-wzorcem: mimo że model formalnie akceptuje wejście GIF, rozpoznaje wyłącznie pierwszą klatkę animacji (autor potwierdził to eksperymentalnie kodem). Pipeline 'wideo -> GIF -> model' daje więc pozornie działający, ale semantycznie okrojony wynik — model widzi tylko pierwszy kadr i nie ma świadomości ruchu ani zdarzeń w czasie.

> **Cytat:** *"给大家写了个 deepseek-v4-flash-vision-exp 输入视频教程

deepseek 最近真的是高产, 刚刚又发了 deepseek-v4-flash-vision-exp, 首个多模态【大】模型. 而且是 v4-flash 能力级别的. 但是! 虽然不是瞎子了, 但是还是听力有问题, 不支持音频输入. 所以默认 deepseek 官网和API都不支持视频输入, 于是给大家写了个小教程, 如何使用这个模型处理视频.

简单来讲, 方法就是直接把视频抽帧. 而且需要注意, 虽然模型支持gif输入, 但是它只识别 gif 的第一帧(我写代码验证了). 所以把视频转换为gif是行不通的."*

---
