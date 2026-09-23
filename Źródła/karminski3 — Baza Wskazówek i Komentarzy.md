---
autor: @karminski3
źródło: https://x.com/karminski3
wygenerowano: 2026-09-23 02:09
typ: synteza-wiedzy
tagi: [karminski3, ai-engineering, prompt-engineering, twitter-extract]
---

# @karminski3 — Baza Wskazówek i Komentarzy

> Destylacja praktycznych porad, heurystyk inżynierskich i komentarzy technicznych z profilu @karminski3 na platformie X. Wyciągnięto 27 wartościowych wpisów.

## ⚠️ Kwestie sporne i rozbieżności do rozstrzygnięcia

> Wpisy, w których autor podważa powszechne przekonania branżowe lub prezentuje tezy stojące w sprzeczności z innymi praktykami:

- **[Claude Opus 5.5 podejrzany o kwantyzowaną destylację — stabilność 6/6 vs. zapadanie się rozumowania (overthinking)](https://x.com/karminski3/status/2102479290420048093):** Teza kontrowersyjna wobec narracji producenta: autor utrzymuje, że Claude Opus 5.5 nie jest nowym modelem, lecz skwantyzowaną lub wewnętrznie destylowaną wersją innego modelu ('fable 5.1') — argumentem jest brak dostrzegalnych różnic w szczegółach implementacyjnych przy 6/6 powtórzeń. Do rozstrzygnięcia: (1) czy 'niższe koszty przy tej samej jakości' wynika z kwantyzacji/destylacji, czy z realnej zmiany architektury (np. MoE o mniejszej liczbie aktywnych parametrów); (2) czy zwiększone zużycie thinking-tokenów jest dowodem na mniejszy model, czy tylko efektem zmiany polityki rozumowania (dłuższy CoT bez zmiany rozmiaru); (3) czy występujące zawieszenia rozumowania to defekt modelu, czy artefakt konkretnego harnessu/limitów. Wpis nie zawiera niezależnych pomiarów parametrów ani logów, więc obie tezy pozostają hipotezami do weryfikacji eksperymentalnej.
- **[reasoning_effort jako narzędzie marketingowe — pułapki benchmarkowania i przenoszenie kosztów na użytkownika](https://x.com/karminski3/status/2099767043155218568):** Autor podważa powszechny konsensus branżowy, że reasoning_effort to pożyteczna funkcja oddająca kontrolę nad trade-offem compute/accuracy użytkownikowi. Teza kontrowersyjna: to w istocie narzędzie marketingowe, które (a) maskuje słabość post-trainingu (effort ≠ performance), (b) przenosi ryzyko kosztowe na użytkownika, (c) przez niejawne deklaracje ('benchmarki robione na max', 'sweet spot w high') wprowadza użytkowników w błąd, sugerując że 'high = najlepszy'. Do rozstrzygnięcia: czy post-training da się doprowadzić do stanu, w którym wyższy effort rzeczywiście monotonicznie = wyższa jakość (postulat autora), czy effort pozostanie na stałe parametrem regulacji kosztu/opóźnienia, a nie jakości. Warto zweryfikować to empirycznie — jeśli monotoniczność nie zachodzi, benchmarkowanie z dowolnym pojedynczym effortem jest metodologicznie wadliwe.
- **[reasoning_effort jako narzędzie marketingowe: pułapki metodologii benchmarków i transfer ryzyka kosztowego na użytkownika](https://x.com/karminski3/status/2099767018279084387):** Teza kontrowersyjna wobec konsensusu branżowego: autor twierdzi, że reasoning_effort to głównie narzędzie marketingowe służące transferowi kosztów compute i ryzyka rozliczeniowego na użytkownika, a nie rzetelny parametr sterujący jakością. Podważa też powszechne przekonanie, że tryb 'high' jest optymalny. Do rozstrzygnięcia: czy reasoning_effort powinien być traktowany jako parametr inżynierski (do kalibracji pod zadanie) czy jako mechanizm różnicowania cenowego; oraz czy rozbieżność 'thinking effort ≠ performance' wynika z braków post-trainingu (teza autora), czy jest nieusuwalną cechą architektury. Dodatkowo sygnalizowana niespójność w komunikacji producenta (benchmarki na 'max' + rekomendacja 'high') wymaga weryfikacji na poziomie transparentności raportowania.
- **[System Scaling: pętla prób i błędów w środowisku oraz współpraca wielu agentów jako klucz do wdrożeń AI w inżynierii](https://x.com/karminski3/status/2092894849619874210):** Autor przeciwstawia się dominującemu w branży paradygmatowi 'scaling laws' opartemu na liczbie parametrów i mocy obliczeniowej, twierdząc że o realnym wdrożeniu AI w inżynierii decyduje skalowanie systemowe (System Scaling): ujednolicenie pętli prób i błędów ze środowiskiem oraz współpracy wielu agentów. Do rozstrzygnięcia: czy przyrost zdolności systemowych może trwale kompensować niedostatki pojedynczego modelu, czy też jest od niego zależny i nie da się go generalizować na dowolne domeny inżynierskie. Brak tu twardych danych porównawczych (tylko pojedynczy case: ~10 minut do konfiguracji firewalla), więc tezę należy traktować jako hipotezę wymagającą benchmarku na wielu zadaniach.
- **[SOTA jako kompresor informacji: dlaczego reasoning effort = max psuje wyniki na SWE-bench](https://x.com/karminski3/status/2099426676669366337):** Teza stoi w sprzeczności z dominującym konsensusem branżowym, że skalowanie test-time compute (większy budżet rozumowania, więcej tokenów myślowych) monotonicznie poprawia jakość. Autor twierdzi, że ustawienie 'max' może POWODOWAĆ INWERSJĘ wyników na SWE-bench, a miarą SOTA jest maksymalna kompresja informacji (najmniej tokenów na najtrudniejszy problem), a nie długość rozumowania. Do rozstrzygnięcia: dla jakich klas zadań i modeli inwersja występuje, gdzie leży optymalny punkt reasoning effortu oraz jak zdefiniować i egzekwować 'poprawne zatrzymanie' rozumowania – brak tu twardych liczb i metodologii, poleganie na samych linkach do prac.
- **[Kompresja informacji jako metryka SOTA: dlaczego 'max' reasoning tokens psuje SWE i kiedy model powinien przestać myśleć](https://x.com/karminski3/status/2099421138069950509):** Teza kontrowersyjna wobec dominującego w branży podejścia 'scale reasoning at inference time' (test-time compute scaling), gdzie zakłada się, że więcej kroków rozumowania ≈ lepsze wyniki i gdzie dostawcy eksponują parametr 'reasoning effort = high/max'. Autor twierdzi, że dla benchmarków agentowych (SWE) maksymalizacja budżetu rozumowania może DZIWAĆ WYNIKI (inwersja rankingu) i że prawdziwą miarą SOTA jest KOMPRESJA informacji (minimalny koszt tokenowy przy najtrudniejszym zadaniu), a nie objętość analizy. Wniosek: długość rozumowania to hiperparametr wymagający walidacji per-model i per-benchmark, a nie uniwersalne 'więcej = lepiej'.
- **[Intensywność rozumowania jako realny lewar wydajności — dowody z DeepSeek-R1-Zero (AIME24: 15% → 71%)](https://x.com/karminski3/status/2099396323942547519):** Spór z rozpowszechnioną w społeczności praktyką rekomendowania poziomu 'high' zamiast 'max' oraz z tezą, że przełącznik intensywności myślenia nie przekłada się na jakość modelu. Autor twierdzi, że jest odwrotnie i popiera to wynikami DeepSeek-R1-Zero (15% → 71% na AIME24 przy wzroście długości rozumowania, bez dopływu nowej wiedzy). Do rozstrzygnięcia pozostaje: czy w modelach nowszej generacji (np. deepseek-v4.1-flash) obowiązuje ta sama monotoniczna zależność, czy występuje punkt nasycenia/degradacji (overthinking) przy maksymalnym budżecie rozumowania — autor tego nie mierzył osobno, a krytycy nie przedstawili danych.
- **[Skill jako izomorfizm kodu i danych: metaprogramowanie i dynamiczna generacja Micro-Skillów](https://x.com/karminski3/status/2099383433034440811):** Autor podważa dominującą praktykę traktowania skilli/promptów jako statycznych, deklaratywnych szablonów ('skill = dokument'). Proponuje paradygmat dynamiczny, w którym skill jest programem generującym inne skille w czasie wykonania (metaprogramowanie). Spór dotyczy tego, czy skille powinny być deterministyczne i audytowalne (podejście klasyczne, stabilne, ale kruche na nowe formaty), czy generatywne i samoadaptacyjne (elastyczne, ale zależne od jakości modelu i trudniejsze do walidacji). Do rozstrzygnięcia: koszt latencji i tokenów przy generacji Micro-Skilla per-wejście vs. zysk z odporności na nieznane formaty.

---

## Spis kategorii

- [Ewaluacja modeli i benchmarking / zachowanie modeli (reasoning, token throughput)](#ewaluacja-modeli-i-benchmarking--zachowanie-modeli-(reasoning,-token-throughput)) (1)
- [Systemy agentowe / Inżynieria pętli agentowej](#systemy-agentowe--inżynieria-pętli-agentowej) (1)
- [Benchmarki modeli / Agentic Coding / Architektura inferencji](#benchmarki-modeli--agentic-coding--architektura-inferencji) (1)
- [Wydania modeli / Architektura małych modeli dense / Inżynieria kontekstu](#wydania-modeli--architektura-małych-modeli-dense--inżynieria-kontekstu) (1)
- [Benchmarking / Polityka dostawców modeli / Inżynieria ewaluacji](#benchmarking--polityka-dostawców-modeli--inżynieria-ewaluacji) (1)
- [Metodologia benchmarków / Architektura reasoning / Krytyka rynku LLM](#metodologia-benchmarków--architektura-reasoning--krytyka-rynku-llm) (1)
- [Architektura LLM / Inferencja niskolatencyjna](#architektura-llm--inferencja-niskolatencyjna) (1)
- [Architektura modeli / Structured Output / Type-Safe AI](#architektura-modeli--structured-output--type-safe-ai) (1)
- [Architektura systemów agentowych / Agentic Systems Engineering](#architektura-systemów-agentowych--agentic-systems-engineering) (1)
- [Architektura systemów agentowych / Agentic Scaling](#architektura-systemów-agentowych--agentic-scaling) (1)
- [Systemy agentowe / Bezpieczeństwo i analiza logów](#systemy-agentowe--bezpieczeństwo-i-analiza-logów) (1)
- [Architektura systemów agentowych / Planowanie](#architektura-systemów-agentowych--planowanie) (1)
- [Bezpieczeństwo modeli / Alignment / Red Teaming](#bezpieczeństwo-modeli--alignment--red-teaming) (1)
- [Architektura agentów / Edge AI / WebGPU](#architektura-agentów--edge-ai--webgpu) (1)
- [Trening modeli / Reasoning / Dystylacja](#trening-modeli--reasoning--dystylacja) (1)
- [Modele rozumujące / Test-time compute / Dystylacja](#modele-rozumujące--test-time-compute--dystylacja) (1)
- [Inżynieria rozumowania / Test-time compute / Benchmarking](#inżynieria-rozumowania--test-time-compute--benchmarking) (1)
- [Inżynieria rozumowania / Prompt Architecture / Benchmarking agentowy](#inżynieria-rozumowania--prompt-architecture--benchmarking-agentowy) (1)
- [Prompt Architecture / Reasoning Effort & Test-time Compute](#prompt-architecture--reasoning-effort-&-test-time-compute) (1)
- [Inżynieria agentowa / Prompt Architecture](#inżynieria-agentowa--prompt-architecture) (1)
- [Prompt Architecture / Agent Harness / Metaprogramowanie](#prompt-architecture--agent-harness--metaprogramowanie) (1)
- [Benchmarki LLM / Agentic Coding / Inżynieria promptów](#benchmarki-llm--agentic-coding--inżynieria-promptów) (1)
- [Benchmarking i lokalna inferencja małych modeli agentowych](#benchmarking-i-lokalna-inferencja-małych-modeli-agentowych) (1)
- [Benchmarking i ewaluacja modeli](#benchmarking-i-ewaluacja-modeli) (1)
- [Multimodalne modele i architektura harnessów agentowych](#multimodalne-modele-i-architektura-harnessów-agentowych) (1)
- [Inżynieria kontekstu / Analiza wideo w LLM](#inżynieria-kontekstu--analiza-wideo-w-llm) (1)
- [Multimodalność / Przetwarzanie wideo](#multimodalność--przetwarzanie-wideo) (1)

---

## Ewaluacja modeli i benchmarking / zachowanie modeli (reasoning, token throughput)

### Claude Opus 5.5 podejrzany o kwantyzowaną destylację — stabilność 6/6 vs. zapadanie się rozumowania (overthinking)

- **Data:** `Tue Sep 22 19:24:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2102479290420048093)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|Reasoning Token Budget]] [[Harness|Chain-of-Thought]] [[Harness|Overthinking w LLM]] [[Harness|Model Distillation]] [[Harness|Kwantyzacja modeli]] [[Harness|Mixture-of-Experts]] [[Stabilność modeli i przestrzeganie promptu|Benchmarking LLM]] [[Harness|Regresja jakości modelu (降智)]] [[Harness|Koszt vs. wydajność modelu]] [[Harness|Harness agentowy]]

**Kontekst / Problem:**
Autor testuje Claude Opus 5.5 na zadaniach generowania kodu frontendowego i porównuje go z innym modelem (nazwanym 'fable 5.1'). Problem praktyczny: czy nowszy, tańszy model faktycznie jest nową architekturą, czy tylko skwantyzowaną/destylowaną wersją poprzednika — i jakie ma to konsekwencje dla niezawodności oraz kosztu tokenów rozumowania. Wnioski oparte są na wielokrotnym powtórzeniu tego samego promptu (test 'gacha') oraz na obserwacji zużycia thinking-tokenów.

**Rada inżynierska:**
Traktuj zużycie thinking-tokenów jako tani, pośredni sygnał o architekturze i rozmiarze modelu: jeśli nowy model przy tej samej jakości outputu generuje wyraźnie więcej tokenów rozumowania, to najprawdopodobniej jest to model mniejszy, który nadrabia jakość długością łańcucha myślowego (wymiana reasoning length za wydajność). Równolegle stosuj test powtarzalności typu 'gacha' — uruchom ten sam prompt N razy (tu 6/6) i porównuj nie tylko poprawność, ale i szczegóły implementacyjne outputu; brak różnic w detalach między dwoma modelami to mocny sygnał, że jeden jest kwantyzacją/destylacją drugiego. Przy doborze modelu produkcyjnego oceniaj zawsze parę (koszt, stabilność), a nie sam benchmark jednorazowy.

**Uwaga / Anty-wzorzec:**
Zapadanie się rozumowania (overthinking / 'thunder big thinking'): model wchodzi w pętlę reasoning i nie potrafi wygenerować kodu — autor odtworzył to zarówno w terminalu, jak i w interfejsie webowym, kilkukrotnie, więc nie jest to jednorazowy glitch, lecz systemowa wada mniejszego modelu nadrabiającego rozumowaniem. Wniosek inżynierski: dla pipeline'ów agentowych z twardym budżetem tokenów i twardym timeoutem potrzebny jest zewnętrzny limit/breaker na długość CoT oraz fallback do drugiego modelu. Drugie anty-wzorzec: zakładanie stabilności dostawcy — '降智' (ciche degradacje modelu po stronie vendora) jest tu określane jako powtarzalna praktyka Anthropic; bez przypięcia wersji modelu i własnych testów regresyjnych jakość produkcji może spaść bez ostrzeżenia. Teza o tym, że Opus 5.5 to skwantyzowana lub destylowana wersja innego modelu, jest kontrowersyjna — brakuje oficjalnego potwierdzenia, więc nie należy jej traktować jako faktu, dopóki nie zostanie zweryfikowana niezależnymi pomiarami.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Teza kontrowersyjna wobec narracji producenta: autor utrzymuje, że Claude Opus 5.5 nie jest nowym modelem, lecz skwantyzowaną lub wewnętrznie destylowaną wersją innego modelu ('fable 5.1') — argumentem jest brak dostrzegalnych różnic w szczegółach implementacyjnych przy 6/6 powtórzeń. Do rozstrzygnięcia: (1) czy 'niższe koszty przy tej samej jakości' wynika z kwantyzacji/destylacji, czy z realnej zmiany architektury (np. MoE o mniejszej liczbie aktywnych parametrów); (2) czy zwiększone zużycie thinking-tokenów jest dowodem na mniejszy model, czy tylko efektem zmiany polityki rozumowania (dłuższy CoT bez zmiany rozmiaru); (3) czy występujące zawieszenia rozumowania to defekt modelu, czy artefakt konkretnego harnessu/limitów. Wpis nie zawiera niezależnych pomiarów parametrów ani logów, więc obie tezy pozostają hipotezami do weryfikacji eksperymentalnej.

> **Cytat:** *"给大家带来claude opus 5.5 的前端测试结果. 直接说结论, 我怀疑现在opus 5.5就是 fable 5.1 的量化版或者自家蒸馏版, 可以直接看我的视频, 几乎看不出两个模型实现细节上的差别. 而且模型继承了Anthropic一贯的优良特点, 一个字, 稳, 6次抽卡6次全都是这个质量. 除此之外我测试时很明显 opus 5.5 的思考token消耗更多. 这意味着opus5.5模型会更小一些(用reasoning长度换性能). 这同样意味着会有雷霆大思考的情况, 比如最后一个火山喷发测试, 我terminal和网页都测试了好几次, 结果都无法输出代码. 思考卡住了. 当然瑕不掩瑜. 毕竟比fable便宜又能获得差不多的性能, 只要不降智, 就是好模型(但无奈Anthropic降智是祖传艺能...)."*

---

## Systemy agentowe / Inżynieria pętli agentowej

### Problem „early stopping” w AgenticCoding — modele nie wykorzystują pełnego budżetu iteracji

- **Data:** `Tue Sep 22 16:41:16 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2102438087158858212)
- **Rodzaj:** Komentarz w dyskusji (@dreamli60679407)
- **Powiązane pojęcia:** [[Harness|Agentic Coding]] [[Harness|Early Stopping w agentach]] [[Harness|Harness agentowy]] [[Weryfikator|Zewnętrzny weryfikator]] [[Harness|Polityka iteracji i budżet narzędziowy]] [[Stabilność modeli i przestrzeganie promptu|Benchmark / grupa kontrolna modeli]]

**Kontekst / Problem:**
Autor komentuje wpis innego użytkownika i porównuje własne doświadczenia z agentowym kodowaniem (AgenticCoding). Zgłasza konkretną obserwację behawioralną modeli: największym problemem nie jest jakość pojedynczego kroku, lecz przedwczesne zatrzymywanie pętli — model rezygnuje z dalszych prób, zanim wyczerpie dostępne iteracje lub budżet narzędziowy. Jednocześnie sugeruje potrzebę grupy kontrolnej (benchmarku porównawczego), aby ocenić, czy inne modele zachowują się inaczej w tej samej pętli.

**Rada inżynierska:**
Traktuj „early stopping” jako mierzalną metrykę zachowania agenta, a nie cechę modelu. Przy budowie harnessu agentowego: (1) jawnie definiuj kryterium sukcesu i warunek stopu, (2) wymuszaj wyczerpanie budżetu iteracji narzędziowych zanim agent zadeklaruje porażkę — np. przez twardy licznik prób i politykę „nie kończ, dopóki nie wykonasz N podejść lub nie udowodnisz niemożności”, (3) stosuj zewnętrzny weryfikator (testy, kompilacja, linter) jako obiektywny sygnał kontynuacji zamiast polegać na samoocenie modelu, (4) porównuj modele na tym samym harnessie z grupą kontrolną — różnice w „chęci do iterowania” są często artefaktem formatu promptu i agent scaffolding, nie tylko zdolności modelu.

**Uwaga / Anty-wzorzec:**
Poleganie na tym, że model sam zdecyduje, kiedy przestać iterować. Anty-wzorce: brak twardego licznika iteracji, brak zewnętrznego sygnału sukcesu/porażki, brak grupy kontrolnej przy ocenie modeli. Skutek: agent rezygnuje po pierwszym niepowodzeniu i wygląda na „słabszy”, choć problemem jest architektura pętli, a nie możliwości modelu.

> **Cytat:** *"@dreamli60679407 话说有对照组吗? 好奇其他模型能达到什么效果. 我这里AgenticCoding目前遇到最大的问题还是早停, 模型不是很愿意去用尽机会迭代."*

---

## Benchmarki modeli / Agentic Coding / Architektura inferencji

### MiMo-v2.6-pro: 3× skok w AgenticCoding, HNSW + AVX-512, 464 tps i problem wczesnego zatrzymania

- **Data:** `Tue Sep 22 16:00:37 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2102427860585841100)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|HNSW]] [[Harness|AVX-512]] [[Harness|Agentic Coding]] [[Harness|MiMo-v2.6-pro]] [[Harness|Mixture of Experts (MoE)]] [[Harness|Token throughput (tps)]] [[Harness|Early stopping w pętlach agentowych]] [[Weryfikator|Zewnętrzny weryfikator]] [[Harness|Budżet iteracji agenta]] [[Stabilność modeli i przestrzeganie promptu|Reasoning effort control]] [[Harness|Live RL]]

**Kontekst / Problem:**
Raport z testów Xiaomi MiMo-v2.6-pro po treningu RL prowadzonym na żywo (live RL). Model jest oceniany w dwóch osiach: (1) AgenticCoding — zadanie implementacji bazy wektorowej, gdzie wynik wzrósł z 2505 (MiMo-v2.5-Pro) do 7810, czyli ~3×, zbliżając się do Claude Fable-5; wygenerowany algorytm to jednowykresowy HNSW (M=16/M0=28) z dokładnym dystansem AVX-512 i per-wątkowym 'visited stamp'. (2) Frontend — słabsza oś: model potrafi one-shot napisać silnik ray tracingu, ale zawodzi w rozumieniu przestrzeni i symulacji fizyki (kulka nie przebija ściany). Dodatkowo zmierzono przepustowość: wariant ultraspeed osiąga 464 tps, szczytowo ~900 tps, stabilnie ~500 tps przy 1.02T parametrów całkowitych i 42B aktywowanych (MoE), gdy modele o podobnej skali dają zwykle 60–80 tps. Autor podaje też, że 67% korpusu treningu po RL to kod, co tłumaczy profil zdolności.

**Rada inżynierska:**
Do zadań backendowego AgenticCoding MiMo-v2.6-pro jest obecnie mocnym wyborem (algorytmika + jakość generowanego kodu). W praktyce produkcyjnej: (1) ustawiaj duży timeout — model myśli długo i nie ma jeszcze regulacji 'reasoning effort', a endpoint jest przeciążony; (2) licz się z wysoką przepustowością (do ~500 tps stabilnie) przy MoE 42B aktywnych parametrów, co czyni go realnym kandydatem do pętli agentowych; (3) przy benchmarkach iteracyjnych dodaj zewnętrzny kontroler budżetu iteracji, który wymusza kontynuację po plateau, zamiast pozwalać modelowi 'oddać pracę'.

**Uwaga / Anty-wzorzec:**
Przedwczesne zatrzymanie (early stopping) w pętli agentowej: przy limicie 50 iteracji na rundę model w 2 z 3 testów przerywał pracę ok. 30. iteracji, gdy wynik przestał rosnąć, i sam 'składał arkusz', marnując pozostały budżet iteracji i obniżając wynik końcowy. Anty-wzorzec: brak zewnętrznego weryfikatora/kryterium stopu i zdanie się na samodzielną decyzję modelu o zakończeniu. Dodatkowo: brak kontroli głębokości rozumowania utrudnia budżetowanie latencji, a słabe rozumienie przestrzenne i fizyka dyskwalifikują go z zadań frontend/3D.

> **Cytat:** *""给大家带来小米 MiMo-v2.6-pro 的测试速报! 简单来讲, 这次不愧是直播RL带来的效果, AgenticCoding 能力提升明显, 之前的 MiMo-v2.5-Pro 在我的向量数据库测试中得分只有2505, 而这次直接翻了3倍, 得分来到了7810. 与 Claude Fable-5 分数接近了. 而且算法也进化为了单图HNSW分层近邻图(M=16/M0=28) + AVX-512精确距离 + 每线程visited stamp. ... 当然也有值得注意的点, 比如这次测试我发现它还是有早停的问题的, 上面的向量数据库测试, 每轮最大迭代50次, 但是三次测试中, 有两次它迭代到30轮左右就没办法提升分数, 于是选择了直接交卷, 浪费了测试机会. 以及, 模型思考偏长, 而且暂时不支持调整思考强度, 加上普速接口现在异常火爆, 所以最好给大一些超时, 避免无法输出结果.""*

---

## Wydania modeli / Architektura małych modeli dense / Inżynieria kontekstu

### K2-Horizon-7B: mały dense model z pełną uwagą dorównuje 27B, ale koszty kontekstu są wysokie

- **Data:** `Tue Sep 15 22:37:55 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099991128061919596)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|K2-Horizon-7B]] [[Stabilność modeli i przestrzeganie promptu|Qwen3.6-27B]] [[Harness|Dense vs MoE]] [[Context Compaction|Pełna uwaga a koszt kontekstu]] [[Harness|Kwantyzacja 8-bit i 4-bit]] [[Harness|Unsloth]] [[Harness|vLLM]] [[Harness|SGLang]] [[Harness|Thinking budget low/high]] [[Harness|AA Bench]] [[Harness|BrowseComp]] [[Harness|SWEBench Verified]] [[Harness|Terminal Bench]] [[Harness|Open-source recipe i dane treningowe]] [[Harness|MiniCPM5-2B]]

**Kontekst / Problem:**
IFM wydał K2-Horizon-7B — mały, gęsty (dense) model 7B, który na benchmarku AA Bench uzyskuje 21 pkt, zbliżając się do Qwen3.6-27B (22 pkt). Model dodatkowo dominuje nad poprzednimi flagowcami (GPT-5, DeepSeek-V4) w BrowseComp, a w SWEBench Verified i Terminal Bench osiąga mocne wyniki inżynierskie. Cały pipeline (dane treningowe, recipe, kod treningowy, metody ewaluacji) jest w pełni open source. Obsługuje kontekst do 512K i konfigurowalną intensywność rozumowania (low/medium/high, domyślnie i oficjalnie zalecane high).

**Rada inżynierska:**
Małe modele dense (7B) trenowane świadomie mogą osiągać benchmarki zbliżone do większych modeli (27B) i dominować w zadaniach wyszukiwania/agentowych (BrowseComp, SWEBench Verified, Terminal Bench). Jednak K2-Horizon-7B używa PEŁNEJ UWAGI (full attention), a nie MoE ani sliding-window/rzadkiej uwagi — przez co koszt pamięci rośnie liniowo wraz z długością kontekstu. Dla kontekstu 128K w BF16 wymagane ~18 GB VRAM/unified memory. Rekomendacja: poczekać na kwantyzację 8-bit/4-bit (np. od Unsloth) zamiast używać BF16 przy długim kontekście. Do natychmiastowego użycia: vLLM lub SGLang (już wspierają ten model). Przy konfiguracji rozumowania stosować ustawienie 'high', zgodnie z oficjalną rekomendacją autora modelu.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: wdrażanie małego modelu dense z pełną uwagą w trybie BF16 przy długim kontekście (128K+) bez uwzględnienia kosztu pamięci — prowadzi to do szybkiego wyczerpania VRAM (~18 GB dla 128K) i niepotrzebnych kosztów inferencji. Drugi anty-wzorzec: wyciąganie wniosków o wydajności wyłącznie na podstawie liczby parametrów bez patrzenia na architekturę uwagi — model 7B z pełną uwagą może mieć wyższy koszt kontekstu niż większy MoE z rzadką aktywnością. Trzeci: ignorowanie zalecanego trybu 'high' myślenia, co może obniżać jakość na zadaniach agentowych.

> **Cytat:** *"IFM刚放出了个神奇7B Dense小模型 K2-Horizon-7B. 神奇的是这玩意在AA Bench里面有21分, 而Qwen3.6-27B是22分, 也就是说这7B参数量快追平了27B的水平. ... 这个模型现在完全是社区明星了, 它的训练数据, 怎么训练的(recipe), 训练代码以及评估方法全都是开源的. 参数上这个模型最大支持512K上下文, 但是注意, 这玩意虽然参数只有7B, 但是它是全注意力的, 所以上下文成本相当高. 目前还只有原始BF16精度, 如果要用128K上下文, 就要18G显存/统一内存. 所以还是等等8bit/4bit量化版本比较好 ... 以及这个模型同样支持设置思考强度. 分为low/medium/high, 然后默认/官方强烈推荐用high. 如果现在不差显存想直接用可以使用vLLM/SGLang."*

---

## Benchmarking / Polityka dostawców modeli / Inżynieria ewaluacji

### reasoning_effort jako narzędzie marketingowe — pułapki benchmarkowania i przenoszenie kosztów na użytkownika

- **Data:** `Tue Sep 15 07:47:29 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099767043155218568)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|reasoning_effort]] [[Stabilność modeli i przestrzeganie promptu|Benchmark methodology]] [[Harness|cost-performance balance]] [[Harness|Post-training quality]] [[Harness|Model provider incentives]] [[Stabilność modeli i przestrzeganie promptu|DeepSeek v4.1 Flash]]

**Kontekst / Problem:**
Autor prowadzi benchmarki porównawcze modeli i zderza się z metodologicznym problemem: czy wolno testować konkurencyjne modele z różnymi poziomami reasoning_effort, skoro domyślne/„reklamowane” ustawienie bywa inne. Komentarze sugerują, że DeepSeeka należy testować z reasoning_effort=high (bo tam ma być „sweet spot”), podczas gdy inne modele puszczane są z max. Autor kwestionuje sam sens istnienia parametru reasoning_effort jako funkcji produktowej, wskazując na asymetrię informacyjną i transfer ryzyka kosztowego z dostawcy na użytkownika.

**Rada inżynierska:**
Traktuj reasoning_effort jako parametr wpływający na rozkład kosztu/opóźnienia, a nie na 'jakość' — nie zakładaj monotonicznej zależności effort↔accuracy. Przy benchmarkach porównawczych: (1) raportuj jawnie poziom effort dla każdego modelu i (2) jeśli dostawca reklamuje max jako ustawienie benchmarkowe, testuj z max, a wyniki z high traktuj jako osobny slice kosztowo-wydajnościowy (cost–performance balance). Nie uśredniaj różnych effortów w jednej tabeli — rozdziel je. Wymuszaj na dostawcach jawną deklarację: 'jaki effort użyto do liczb w karcie modelu'.

**Uwaga / Anty-wzorzec:**
Testowanie własnego modelu (lub ulubionego) na 'high', gdy konkurencja jest mierzona na 'max' — to zaniża koszt i zawyża efektywność, ale uniemożliwia uczciwe porównanie. Drugi anty-wzorzec: interpretowanie 'high' jako 'najlepszego trybu' tylko dlatego, że dostawca nazywa go sweet spotem w cost–performance balance — to marketing, nie optimum accuracy. Trzeci: traktowanie reasoning_effort jako substytutu jakości — u autora jest to objaw słabego post-trainingu, a nie cecha docelowa.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor podważa powszechny konsensus branżowy, że reasoning_effort to pożyteczna funkcja oddająca kontrolę nad trade-offem compute/accuracy użytkownikowi. Teza kontrowersyjna: to w istocie narzędzie marketingowe, które (a) maskuje słabość post-trainingu (effort ≠ performance), (b) przenosi ryzyko kosztowe na użytkownika, (c) przez niejawne deklaracje ('benchmarki robione na max', 'sweet spot w high') wprowadza użytkowników w błąd, sugerując że 'high = najlepszy'. Do rozstrzygnięcia: czy post-training da się doprowadzić do stanu, w którym wyższy effort rzeczywiście monotonicznie = wyższa jakość (postulat autora), czy effort pozostanie na stałe parametrem regulacji kosztu/opóźnienia, a nie jakości. Warto zweryfikować to empirycznie — jeśli monotoniczność nie zachodzi, benchmarkowanie z dowolnym pojedynczym effortem jest metodologicznie wadliwe.

> **Cytat:** *"问题在于我做的是 benchmark, 不是日常使用. 不能因其他模型都用max然后deepseek high 好单独用high测. 然后评论说应该用high测. 以及, reasoning_effort 在我看来是大模型厂商的营销手段. 把算力与精度的权衡交给了用户, 顺便把算力计费的风险也转移给了用户. 而且巧妙地进行掩饰: 宣称benchmark全是max跑出来的. 最后又说甜区(注意论文里称作cost–performance balance) 在high. 造成的结果就是, 有人认为high就是最好的. 我当然同意 thinking effort 不等价于 performance. 而且我认为之所以不等价是因为后训练拉了. 理想上应该追求让它等价. 但请注意, deepseek-v4-1-flash技术报告里给max评价为: best reserved for the most challenging tasks."*

---

## Metodologia benchmarków / Architektura reasoning / Krytyka rynku LLM

### reasoning_effort jako narzędzie marketingowe: pułapki metodologii benchmarków i transfer ryzyka kosztowego na użytkownika

- **Data:** `Tue Sep 15 07:47:23 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099767018279084387)
- **Rodzaj:** Komentarz w dyskusji (@QuantumTransf)
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|reasoning_effort]] [[Stabilność modeli i przestrzeganie promptu|Metodologia benchmarków]] [[Harness|Cost-performance balance]] [[Harness|Post-training]] [[Stabilność modeli i przestrzeganie promptu|DeepSeek-V4]] [[Harness|Compute billing risk]]

**Kontekst / Problem:**
Autor odpowiada pod wpisem @QuantumTransf, broniąc spójności metodologicznej swoich benchmarków. Problem: przy porównywaniu modeli nie można testować jednego modelu (DeepSeek) w trybie 'high', gdy wszystkie inne uruchamiane są w trybie 'max' — to zaburza porównywalność. Komentujący sugerowali, że należy używać 'high'. Autor podnosi szerszą tezę: parametr reasoning_effort nie jest neutralnym narzędziem technicznym, lecz mechanizmem marketingowo-biznesowym, który przenosi na użytkownika zarówno kompromis dokładność/koszt, jak i ryzyko rozliczeniowe za zużyty compute.

**Rada inżynierska:**
Traktuj reasoning_effort jako wymiar konfiguracji, a nie jakość modelu. Zasady inżynierskie: (1) W benchmarkach porównawczych wszystkie modele muszą być uruchamiane w tym samym, jawnie zadeklarowanym poziomie effort — mieszanie 'max' i 'high' między modelami unieważnia wyniki. (2) Nie zakładaj, że wyższy effort = lepszy wynik — 'thinking effort ≠ performance'. (3) Sweet spot (w paperach: cost-performance balance) zwykle leży w 'high', ale to zależy od zadania — 'max' jest zarezerwowany dla najtrudniejszych przypadków (wg technical report deepseek-v4-1-flash: 'best reserved for the most challenging tasks'). (4) Czytaj deklaracje producenta o benchmarkach krytycznie: deklaracja 'wszystkie benchmarki na max' w połączeniu z rekomendacją 'high jako sweet spot' jest wewnętrznie niespójna i służy ukryciu realnych kosztów. (5) Różnica między effort a performance wynika w dużej mierze z niedostatecznego post-trainingu — docelowo należy dążyć do ich równoważności.

**Uwaga / Anty-wzorzec:**
Anty-wzorce: (1) Uruchamianie modelu w trybie 'high' tylko dlatego, że inni używają 'max' — brak jednolitej metodologii porównawczej. (2) Bezkrytyczne przyjęcie, że 'high to najlepszy tryb', co jest artefaktem marketingu, a nie właściwością modelu. (3) Ignorowanie przeniesienia ryzyka kosztowego: użytkownik płaci za compute, a producent maskuje prawdziwy koszt benchmarków deklarując 'max'. (4) Zakładanie, że reasoning_effort jest neutralnym parametrem, podczas gdy w praktyce jest narzędziem różnicowania cenowego i pozycjonowania.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Teza kontrowersyjna wobec konsensusu branżowego: autor twierdzi, że reasoning_effort to głównie narzędzie marketingowe służące transferowi kosztów compute i ryzyka rozliczeniowego na użytkownika, a nie rzetelny parametr sterujący jakością. Podważa też powszechne przekonanie, że tryb 'high' jest optymalny. Do rozstrzygnięcia: czy reasoning_effort powinien być traktowany jako parametr inżynierski (do kalibracji pod zadanie) czy jako mechanizm różnicowania cenowego; oraz czy rozbieżność 'thinking effort ≠ performance' wynika z braków post-trainingu (teza autora), czy jest nieusuwalną cechą architektury. Dodatkowo sygnalizowana niespójność w komunikacji producenta (benchmarki na 'max' + rekomendacja 'high') wymaga weryfikacji na poziomie transparentności raportowania.

> **Cytat:** *"问题在于我做的是 benchmark, 不是日常使用. 不能因其他模型都用max然后deepseek high 好单独用high测.  

然后评论说应该用high测. 

以及, reasoning_effort 在我看来是大模型厂商的营销手段. 把算力与精度的权衡交给了用户, 顺便把算力计费的风险也转移给了用户. 而且巧妙地进行掩饰: 宣称benchmark全是max跑出来的. 最后又说甜区(注意论文里称作cost–performance balance) 在high. 

造成的结果就是, 有人认为high就是最好的. 

我当然同意 thinking effort 不等价于 performance. 而且我认为之所以不等价是因为后训练拉了. 理想上应该追求让它等价.

但请注意, deepseek-v4-1-flash技术报告里给max评价为: best reserved for the most challenging tasks."*

---

## Architektura LLM / Inferencja niskolatencyjna

### Jev/TypeSafe AI: równoległe próbkowanie schematu i 70 ms inferencji dla decyzji w czasie rzeczywistym

- **Data:** `Thu Sep 17 22:46:03 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2100717948881326224)
- **Rodzaj:** Komentarz w dyskusji (@karminski3)
- **Powiązane pojęcia:** [[Harness|LLM Inference]] [[Harness|Memory Bandwidth]] [[Harness|Parallel Sampling Architecture]] [[Harness|Structured Output]] [[Harness|System One vs System Two]] [[Harness|Latency Budget]] [[Harness|Vercel AI Gateway]] [[Prompt Architecture]]

**Kontekst / Problem:**
Model Jev od TypeSafe AI ma być używany w wysokoczęstotliwościowych scenariuszach produkcyjnych, np. przy bastionie do klasyfikacji ryzykownych komend shell (rm -rf /). Jego przewaga wynika z architektury równoległego próbkowania: zamiast przechodzić przez aktywowane parametry dla każdego tokenu, wykonuje jedną propagację w przód i zwraca dyskretne predykcje oraz prawdopodobieństwa gałęzi dla wszystkich pól zdefiniowanego schematu. Autor podaje cenę $0.042/M input i darmowy output. Ograniczenia: brak lokalnych węzłów => ~120 ms do US West, co daje min. ~200 ms; model jest System One, więc wymaga System Two do strategii i generowania promptu; dostęp przez Vercel AI Gateway.

**Rada inżynierska:**
Projektuj wyjście jako z góry zdefiniowany schemat pól; dla niskich opóźnień wybieraj architektury, które zwracają wszystkie pola w jednym przebiegu, zamiast generować token po tokenie. Mierz SLA end-to-end (inferencja + sieć + kolejki), a System One łącz z System Two, który najpierw tworzy strategię/prompt.

**Uwaga / Anty-wzorzec:**
Ignorowanie opóźnienia sieciowego i lokalizacji węzłów: nawet 70 ms inferencji staje się ~200 ms przy dostępie do US West, co może wykluczyć część scenariuszy real-time. Drugi anty-wzorzec: używanie System One do decyzji strategicznych bez warstwy System Two, co obniża jakość wyjścia.

> **Cytat:** *"但天下武功唯快不破, 这玩意从输入到输出最快只需要70ms! 所以完全可以用在高频的生产级场景, 比如接到堡垒机里面实时判断用户输入的shell命令是否存在危险(rm -rf /). 再加上输入每百万token只需要$0.042, 输出不要钱. 妥妥的新一代flash模型斩杀线(有的flash模型会被企业用作决策器). 说完了用途再来看它的架构, 传统大模型有多少token就要把激活参数过多少遍(前向传播)所以特别吃显存带宽, 而这个模型设计了一个特殊的并行采样架构, 只需要一次前向传播, 就能输出所有预设schema字段的离散预测与分支概率. 达成了极低的延迟. 而推出Jev的 TypeSafe AI 这个公司也很有噱头, 它是 Diogo Almeida 一手创办的, 就是他曾经在 OpenAI 的 InstructGPT 和早期 RLHF（基于人类反馈的强化学习) 团队中的贡献才有了如今的ChatGPT. 最后说一下目前模型的限制, 首先由于没有本土节点, 所以虽然它只需要70ms, 但是到美西这海底光缆延迟120ms是躲不掉的, 所以至少还是200ms打底. 另外, 模型被官方称为 System One 模型, 所以理想搭配还需要一个 System Two 模型用来进行战略判断, 然后生成策略当作提示词输入进去, 这样才能提升模型的输出质量. 另外, 官网还在申请使用, 不过vercel的AI Gateway已经能直接用了, 所以想测试的同学直接去vercel用就行."*

---

## Architektura modeli / Structured Output / Type-Safe AI

### Model Jev: decyzyjny model AI z type-safe strukturą zamiast autoregRESji tekstowej

- **Data:** `Thu Sep 17 22:46:02 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2100717944565354595)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Type-Safe AI]] [[Harness|Structured Output]] [[Harness|Decision Slots]] [[Harness|JSON Schema]] [[Harness|Model Autoregresyjny]] [[Harness|Systemy Agentowe]] [[Harness|Kompilacja Schematu]]

**Kontekst / Problem:**
Autor @karminski3 przedstawia model 'Jev' jako alternatywę dla tradycyjnych autoregresyjnych LLM-ów. Model rezygnuje z generowania zwykłego tekstu i zamiast tego działa wyłącznie jako silnik decyzyjny: przyjmuje tekst na wejściu, ale zwraca ustrukturyzowane decyzje (np. JSON) zgodne z wcześniej zdefiniowanym Schema. Problem, który rozwiązuje, to zawodność parsowania swobodnego tekstu LLM-ów (halucynowane pola, niepoprawny JSON, nieprzewidywalny format) oraz potrzeba deterministycznego, typowanego wyjścia w systemach produkcyjnych i agentowych.

**Rada inżynierska:**
Traktuj model jako kompilator decyzji: zdefiniuj Schema wejścia (jak protobuf/GraphQL), która jest kompilowana do konkretnych 'slotów decyzyjnych' (decision slots). Model nie generuje tekstu — wypełnia sloty, dzięki czemu wyjście strukturalne (JSON) jest z założenia poprawne i nie wymaga walidacji ani naprawiania parserem. Dla złożonych zadań (np. gra Slay the Spire, analiza rynku/portfela) sprowadź stan świata do tekstu, zdefiniuj pełny zbiór dozwolonych akcji, a model samodzielnie wybierze decyzję. To podejście eliminuje całą klasę błędów formatowania typową dla swobodnej generacji.

**Uwaga / Anty-wzorzec:**
Ograniczenie wejścia wyłącznie do tekstu — model nie przyjmuje jeszcze innych modalności (obraz, dźwięk, dane binarne), więc każde wejście trzeba najpierw zserializować do tekstu. Dodatkowo sztywna definicja Schema oznacza, że nie da się uzyskać swobodnej odpowiedzi narracyjnej — architektura jest celowo nieelastyczna i wymaga zaprojektowania slotów decyzyjnych z góry. Uwaga: wpis ma charakter wprowadzający/zapowiedzi i kończy się niedokończonym pytaniem retorycznym — brak jeszcze twardych benchmarków porównawczych względem klasycznych LLM-ów.

> **Cytat:** *"给大家写个简单的Jev模型介绍, 这绝对是个需要重点关注的模型. 简单讲, 这个模型放弃了传统自回归架构, 它没有办法直接输出普通文本. 但是他能进行决策! 比如最简单的二分类场景, 输入一条短信, 让它判断是否为垃圾短信, 它就可以输出这样的JSON: {"decision": { "isSpam": true }, "probabilities": { "isSpam": { "true": 0.982, "false": 0.018 } } } 没错, 它只能进行结构化输出, 甚至你输入的时候要定义 Schema (用过protobuf/GraphQL的同学应该能理解), 在送入模型时被编译为特定的决策槽位, 然后按照槽位输出, 所以输出JSON不可能出问题. 而复杂一些的场景, 比如让这个模型玩杀戮尖塔或者看盘, 只需要把内容转换为文本输入进去(没错, 目前模型只支持文本输入), 然后定义好模型能进行哪些动作, 模型就会自主决策了. 到目前为止, 是不是看上去跟普通文本大模型没区别? #jev #TypeSafeAI #DiogoAlmeida #systemone #vercel"*

---

## Architektura systemów agentowych / Agentic Systems Engineering

### System Scaling: pętla prób i błędów w środowisku oraz współpraca wielu agentów jako klucz do wdrożeń AI w inżynierii

- **Data:** `Thu Aug 27 08:39:50 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2092894849619874210)
- **Rodzaj:** Komentarz w dyskusji (@karminski3)
- **Powiązane pojęcia:** [[Harness|System Scaling]] [[Harness|Agentic Systems Engineering]] [[Harness|Environment Feedback Loop]] [[Harness|Multi-Agent Collaboration]] [[Harness|Weryfikacja zewnętrzna]] [[Harness|Harness agentowy]] [[Harness|DeepResearch]] [[Harness|Open Source Framework]] [[Harness|Konfiguracja firewalla przez agenta]]

**Kontekst / Problem:**
Autor komentuje pod wpisem innego użytkownika, podsumowując wynik pracy nad frameworkiem agentowym. Rozwiązywany problem: jak sprawić, by system AI samodzielnie dostarczył realny artefakt inżynierski (konfigurację firewalla w odpowiedzi na zidentyfikowany atak) zamiast jedynie generować tekst. W tle przewija się teza o ograniczeniach strategii skalowania wyłącznie parametrów modelu oraz o open-source'owym frameworku i dostrojonym modelu DeepResearch, które umożliwiły eksperyment.

**Rada inżynierska:**
Traktuj 'System Scaling' jako priorytet nad skalowaniem parametrów modelu: buduj architekturę, w której (1) środowisko zwraca wiarygodny sygnał o powodzeniu/porażce (environment trial-and-error feedback), a (2) wiele agentów współdzieli ten sygnał i koordynuje pracę. Dopiero sprzężenie tych dwóch elementów w jeden spójny system pozwala agentowi dostarczyć działający artefakt (np. reguły firewalla) w realistycznym czasie rzędu minut, a nie tylko szkic odpowiedzi. Konkretny przepływ: agent proponuje zmianę → harness aplikuje ją w środowisku → weryfikator/środowisko zwraca wynik → agent koryguje. Benchmarkuj nie pojedynczy prompt, lecz cały łańcuch decyzyjno-weryfikacyjny.

**Uwaga / Anty-wzorzec:**
Skupianie się wyłącznie na liczbie parametrów i 'wyścigu zbrojeń' modeli (卷模型参数量) przy pomijaniu warstwy systemowej: bez pętli feedbacku ze środowiska i bez orkiestracji wielu agentów nawet mocny model nie domknie zadania inżynierskiego. Drugi anty-wzorzec: ocenianie agenta po jakości pojedynczej odpowiedzi, a nie po czasie i niezawodności dostarczenia zweryfikowanego artefaktu — to zniekształca obraz rzeczywistej użyteczności systemu.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor przeciwstawia się dominującemu w branży paradygmatowi 'scaling laws' opartemu na liczbie parametrów i mocy obliczeniowej, twierdząc że o realnym wdrożeniu AI w inżynierii decyduje skalowanie systemowe (System Scaling): ujednolicenie pętli prób i błędów ze środowiskiem oraz współpracy wielu agentów. Do rozstrzygnięcia: czy przyrost zdolności systemowych może trwale kompensować niedostatki pojedynczego modelu, czy też jest od niego zależny i nie da się go generalizować na dowolne domeny inżynierskie. Brak tu twardych danych porównawczych (tylko pojedynczy case: ~10 minut do konfiguracji firewalla), więc tezę należy traktować jako hipotezę wymagającą benchmarku na wielu zadaniach.

> **Cytat:** *"最后, 在这个架构加持下, 它仅用了10分钟左右就给我交付了针对攻击的防火墙配置. 这真的是 Agentic 系统工程的胜利了. 

未来的 AI 竞争, 不仅是卷模型参数量, 能把环境试错反馈和多 Agent 协同做成统一的系统 (System Scaling), 才是真正让AI在各种工程中落地的关键.

另外, 这个框架还开源了! 这里: https://t.co/n4F2ulrtEc
配套的 DeepResearch 模型也在这里: https://t.co/f8BzbXFh1n (模型之前也给大家测过, 是针对 DeepResearch 特调的, 性能相当不错)"*

---

## Architektura systemów agentowych / Agentic Scaling

### Harness Scaling: skalowanie rusztowania agentów zamiast samych parametrów modelu

- **Data:** `Thu Aug 27 08:39:49 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2092894843429363871)
- **Rodzaj:** Komentarz w dyskusji (@karminski3)
- **Powiązane pojęcia:** [[Harness|Harness Scaling]] [[Harness|Agentic Coordination Scaling]] [[Harness|Environment Scaling]] [[Harness|Agent Team]] [[Harness|Agent Swarm]] [[Harness|AgentOS]] [[Harness|ModSecurity]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Utrata uwagi (Attention Loss)]] [[Harness|Halucynacje modeli]] [[Harness|Sandbox]] [[Harness|Asynchroniczne przetwarzanie agentów]]

**Kontekst / Problem:**
Analiza bezpieczeństwa ok. 1,2 mln logów (260 MB) pod kątem ekstrakcji wskaźników ataku i generowania reguł ModSecurity. Klasyczny liniowy agent nie jest w stanie przetworzyć takiego wolumenu bez utraty uwagi, halucynacji i błędu całego zadania.

**Rada inżynierska:**
Skaluj harness, nie tylko model: 1) Harness Scaling — dokładaj framework, Agent Tools i Agent Team/Swarm, bo parametry dają 'inteligencję', a otoczenie daje zdolność wykonawczą. 2) Agentic Coordination Scaling — dziel zadanie jak zespół SOC: agent wywiadu czyści logi i ekstrahuje złośliwe IP oraz cechy ataku, agent reguł na tej podstawie pisze reguły ModSecurity; uruchamiaj agentów asynchronicznie i równolegle, tak aby pierwsze wyniki wywiadu natychmiast zasilały generator reguł, a nowe wymagania można było dodawać w locie bez przerywania działających zadań. 3) Environment Scaling — nie wrzucaj całych 260 MB logów do kontekstu modelu, bo grozi to eksplozją tokenów; pisz dedykowane skrypty ekstrahujące istotne zdarzenia i uruchamiaj je w izolowanym runtime (AgentOS), który pozwala wykonywać ryzykowny kod bez wpływu na system hosta.

**Uwaga / Anty-wzorzec:**
Antywzorzec: tradycyjny, jednowątkowy agent czytający cały wolumen logów w jednym kontekście. Prowadzi to do utraty uwagi, halucynacji, eksplozji tokenów i awarii zadania. Drugi antywzorzec: przekonanie, że samo zwiększanie parametrów modelu wystarczy do zadań operacyjnych na dużą skalę.

> **Cytat:** *"这个任务最难的点就是, 如果是最传统的Agent系统, 就只能单线思考, 120万条日志(约260MB), 绝对会导致各种注意力丢失或者产生幻觉, 最后整个任务就直接报错.

这次  Apodex 1.1 版本就针对这个场景做了升级. 这里必须要给大家介绍一个概念: Harness Scaling

简单来讲, 光堆模型参数量只能提升模型的"智力", 而堆模型的脚手架(framework), 工具箱(Agent Tools)和团队(Agent Team/Swarm), 就能提升模型干活的能力.

Apodex 1.1 在两个地方发力了:

首先是 Agentic Coordination Scaling（智能体协同扩展）：
它的 Agent Team 像一个真正的 SOC 安全团队一样把任务拆了, 情报 Agent 去清洗几十万条日志提取恶意 IP 和特征, 规则 Agent 根据特征去写 ModSecurity 拦截规则. 注意这些是异步并行的, 速度非常快, 甚至情报 Agent 刚吐出第一批探测到的攻击日志, 规则 Agent 就已经开始写防火墙规则了. 而且如果要改需求, 可以随时在这个过程中添加, 不用担心影响正在跑的任务.

紧接着是 Environment Scaling（环境扩展）：
如果这120万条日志全都让AI去读取, token量肯定直接炸了, 所以有针对性的编写脚本去抽取攻击日志就是工作的主要内容了, 而这些日志全都是运行在 AgentOS 上的, 它是整个 Apodex 系统的运行时承载, 在这个上面模型可以运行各种风险代码而不用担心影响宿主系统."*

---

## Systemy agentowe / Bezpieczeństwo i analiza logów

### Agent Apodex 1.1 analizuje 1,2 mln logów ataku i generuje reguły firewalla end-to-end

- **Data:** `Thu Aug 27 08:39:48 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2092894838492655713)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Systemy agentowe]] [[Context Compaction|Inżynieria kontekstu]] [[Stabilność modeli i przestrzeganie promptu|Benchmarki agentów]] [[Harness|Analiza logów bezpieczeństwa]] [[Harness|Automatyczne generowanie reguł firewalla]] [[Weryfikator|Zewnętrzny weryfikator]] [[Context Compaction|Przetwarzanie danych przekraczających okno kontekstu]] [[Harness|Pętla agentowa analiza-wdrożenie]]

**Kontekst / Problem:**
Autor testuje świeżo wydany system agentowy Apodex 1.1 na realistycznym, wysokowolumenowym zadaniu bezpieczeństwa: pakuje 1,2 mln rekordów logów serwera WWW z publicznego zbioru Zenodo (zawierającego prawdziwe próby ataków privilege escalation) i zleca agentowi dwuetapowe zadanie — (1) zidentyfikowanie techniki atakującego, (2) wygenerowanie reguł firewalla blokujących ten ruch. Agent przechodzi cały łańcuch od surowych danych do artefaktu wdrożeniowego bez ręcznej ingerencji. Wpis jest częściowo promocyjny (nazwy produktów, hashtagi #AgentOS #SystemScaling), ale opisuje konkretny scenariusz testu kompetencyjnego agenta.

**Rada inżynierska:**
Test wartości agenta należy projektować end-to-end na realnym, dużym korpusie: wejście = surowe, nieoczyszczone dane operacyjne (tu 1,2 mln logów), wyjście = artefakt wykonywalny (reguły firewalla), a nie streszczenie. Wolumen danych znacząco przekracza okno kontekstu, więc agent musi opierać się na narzędziach i iteracyjnej agregacji (parsowanie, filtrowanie, grupowanie) oraz utrwalać wyniki pośrednie poza kontekstem — dopiero to pozwala domknąć pętlę analiza → reguła. Wniosek inżynierski: miarą dojrzałości harnessu agentowego jest zdolność do przejścia od nieprzetworzonego szumu do wdrożeniowego artefaktu w jednym przebiegu.

**Uwaga / Anty-wzorzec:**
Anty-wzorce widoczne w takim podejściu: (1) ocenianie agenta po wrażeniu „udało się”, bez metryk — brak precision/recall detekcji, kosztu tokenów, latencji i odsetka fałszywych reguł; (2) brak niezależnego weryfikatora reguł firewalla — wygenerowana reguła może zablokować legalny ruch lub nie pokryć wariantów ataku; (3) próba wrzucenia całego korpusu logów do kontekstu zamiast warstwowego przetwarzania z użyciem narzędzi; (4) brak kontroli nad odtwarzalnością — bez ustalonego ground truth i podziału danych wynik nie jest porównywalny między wersjami modelu.

> **Cytat:** *"劲爆, 我给刚发布的 Apodex 1.1 出了个极其变态的实战难题, 它真的跑通了! 

我直接打包了120万条日志, 里面包含真实的提权攻击的 Web Server 日志(用的是 Zenodo Dataset). 

然后让他帮我把黑客的攻击方式抓出来, 还要给我写防火墙规则拦截攻击. 结果它真的做到了, 从分析到写规则一气呵成"*

---

## Architektura systemów agentowych / Planowanie

### Ograniczenia modeli System-1: porównanie Jev vs czysty losowy w labiryncie

- **Data:** `Mon Sep 21 07:49:04 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2101941770003361893)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|System-1 vs System-2]] [[Harness|Lokalne optimum]] [[Harness|Pólya's random walk theorem]] [[Harness|Planowanie w agentach]] [[Harness|Heurystyka]] [[Harness|Backtracking]] [[Harness|MCTS]]

**Kontekst / Problem:**
Eksperyment porównujący wydajność modelu Jev (szybki, jednokrokowy, strukturalny ewaluator decyzji) z czystym generatorem liczb losowych w zadaniu znajdowania ścieżki w labiryncie. Celem było sprawdzenie, czy model System-1 z heurystyką (odległość Manhattan) poradzi sobie lepiej niż losowe decyzje. Wynik: losowy wygrał, Jev utknął w lokalnym optimum, powtarzając ruchy w kółko. Autor konkluduje, że Jev nie jest plannerem, lecz szybkim jednokrokowym klasyfikatorem i do złożonych zadań potrzebny jest model System-2.

**Rada inżynierska:**
W zadaniach wymagających planowania wielokrokowego, backtrackingu lub gdy lokalna heurystyka jest sprzeczna z globalnym optimum, nie używaj wyłącznie modeli System-1. Nawet podając historię (last_move, visited_count) i reguły drugorzędne, model może je ignorować i wpaść w lokalne optimum. Zapewnij mechanizmy planowania (System-2), takie jak przeszukiwanie drzewa, MCTS lub jawne zarządzanie pamięcią i backtrackingiem.

**Uwaga / Anty-wzorzec:**
Zakładanie, że szybki model System-1 z bogatymi cechami i heurystyką poradzi sobie z zadaniami planistycznymi. Może on przedkładać lokalną heurystykę (np. mniejsza odległość Manhattan) nad reguły unikania zapętleń, co prowadzi do systematycznych porażek. Unikaj go w zadaniach o nieodwracalnych decyzjach, natychmiastowej śmierci (Snake, Tetris, autonomiczna jazda) oraz wymagających audytu (operacje na bazie danych).

> **Cytat:** *"所以, Jev 它只是一个极速的单步结构化判断器, 但绝不是规划器. 最好还是带一个System-2模型才能进行复杂任务. 最后给大家整理慎用 Jev 的场景：需要绕路, 回溯, 多步规划的：迷宫, 装箱, 调度等局部启发和全局最优不一致的图问题. 突然死亡型控制：贪吃蛇, 俄罗斯方块, 自动驾驶等. 一步踏错当场GG. 不可逆高代价决策：删库, 事务操作, 尤其是需要审计的场景."*

---

## Bezpieczeństwo modeli / Alignment / Red Teaming

### Test wpływu języka (hebrajski vs angielski vs chiński) na skuteczność odmów modeli — obalenie mitu o 'low-resource jailbreak'

- **Data:** `Mon Sep 21 00:09:21 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2101826076762857867)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Jailbreak]] [[Harness|Model Alignment]] [[Harness|Refusal Rate]] [[Harness|Low-Resource Language Jailbreak]] [[Harness|Gateway Filtering]] [[Harness|Red Teaming]] [[Harness|Safety Guardrails]] [[Stabilność modeli i przestrzeganie promptu|Benchmarkowanie bezpieczeństwa modeli]]

**Kontekst / Problem:**
W sieci krążyła plotka (post z 1,9 mln wyświetleń), że zgłoszenia odwoławcze w języku hebrajskim rzekomo 'przebijają' warstwy bezpieczeństwa i odblokowują konta oraz modele (m.in. Anthropic). Autor postanowił zweryfikować hipotezę, że hebrajski — jako język o mniejszym udziale w korpusie treningowym — może działać jak wektor jailbreaka. Zbudował framework wykorzystujący publiczne korpusy z HuggingFace i przygotował zestawy promptów w trzech językach (EN/ZH/HE), zawierające zarówno treści szkodliwe (powinny być odrzucone), jak i kontrolne treści neutralne (powinny być zaakceptowane).

**Rada inżynierska:**
Nie zakładaj, że język o niskim udziale w korpusie automatycznie osłabia alignment. Współczesne modele (Fable-5.1, DeepSeek-V4.1-Flash) utrzymują zbliżone wskaźniki odmów niezależnie od języka: Fable-5.1 — EN 95,0%, ZH 94,4%, HE 95,1%; DeepSeek-V4.1-Flash — EN 100%, ZH 100%, HE 99,3%. Warto też rozdzielać warstwy obrony: 32–36% szkodliwych zapytań blokuje gateway (przed dotarciem do modelu), a 54–60% odmawia sam model. Najgroźniejsze treści są odcinane już na poziomie bramy, co oznacza, że pomiar 'refusal rate' samego modelu bez uwzględnienia gateway zaniża realną skuteczność systemu. Przy testach bezpieczeństwa stosuj kontrolę zmiennych — testuj wyłącznie wpływ języka, bez dodatkowych promptów jailbreakowych, aby izolować badaną zmienną.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: opieranie się na przestarzałych wynikach z 2023 r. (praca 'Low-Resource Languages Jailbreak GPT-4'), które wskazywały, że języki takie jak luo, szkocki gaelicki czy hmong omijają zabezpieczenia. Wniosek ten nie jest już aktualny — alignment został wzmocniony i dziś nawet hebrajski (nie aż tak niszowy) nie daje przewagi. Drugi anty-wzorzec: wyciąganie wniosków o 'sile modelu' wyłącznie z refusal rate bez rozdzielenia blokad gateway vs odmowy modelu — prowadzi to do błędnej oceny, gdzie realnie działa obrona.

> **Cytat:** *"测了一波后直接说结论, 没有这回事. 中文, 英文, 希伯来语的拒绝率没太大区别. 对于有害内容, Fable-5.1的拒绝率是英语 95.0%, 中文 94.4%, 希伯来语 95.1%. 其中被网关拦截大约 32–36%，然后模型正文拒绝回答大约 54–60%. 尤其是极其危险的题目, 基本都没到大模型, 直接网关就拦掉了. 而 DeepSeek-V4.1-Flash 甚至表现更好一些, 英语 100%, 中文 100%, 希伯来语 99.3%. 从测试结论来看, 目前大模型的安全对齐已经做得很好了... 在2023年还有论文『Low-Resource Languages Jailbreak GPT-4』指出使用类似鲁语,苏格兰盖尔语或苗语会绕过模型安全机制. 但现在基本都没问题了. 另外需要注意, 为了测试控制变量, 我只测试了语言对模型安全机制的影响, 并没有使用提示词进行越狱."*

---

## Architektura agentów / Edge AI / WebGPU

### Agent kodujący w całości w przeglądarce: MiniCPM5-2B 4bit ONNX + WebGPU (bez Dockera i Node)

- **Data:** `Mon Sep 14 22:55:34 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099633181934907654)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|WebGPU]] [[Harness|ONNX Runtime]] [[Harness|MiniCPM]] [[Harness|Coding Agent]] [[Harness|Tool Calling]] [[Harness|Edge AI]] [[Harness|Kwantyzacja 4-bit]] [[Harness|Inferencja w przeglądarce]] [[Harness|Self-healing UI]]

**Kontekst / Problem:**
Problem: uruchomienie pełnego Coding Agenta (wirtualny terminal, edycja plików, tool_call) zwykle wymaga infrastruktury — Dockera, Node, kluczy API i połączenia z chmurą. Projekt HuggingFace Space 'MiniCPM5-2B-WebGPU-Pi' pokazuje alternatywę: framework Pi opakowuje agenta, a model MiniCPM5-2B w wersji 4bit ONNX (poniżej 2 GB) napędza całość. Zarówno framework, jak i model inferencyjny działają wyłącznie w przeglądarce (WebGPU), bez backendu. Autor raportuje ~25 tps na GPU 3080Ti i zaskakująco dobrą stabilność tool_call jak na model 2B.

**Rada inżynierska:**
Miniaturowe modele (2B) po kwantyzacji 4bit do ONNX potrafią stabilnie prowadzić pętlę agentową (tool_call + edycja plików) w całości po stronie klienta przez WebGPU — bez API KEY i bez sieci. Kluczowa przewaga architektoniczna: agent uruchomiony w kontekście przeglądarki dziedziczy naturalnie sesję logowania i cookies użytkownika, co otwiera scenariusze automatyzacji wewnętrznych/niepublicznych projektów oraz SaaS-ów bez dostępu do publicznego internetu. Drugi wzorzec: wtyczka 'self-healing' nasłuchująca błędów w konsoli przeglądarki i wstrzykująca hot-patch na żywo, bez przeładowania strony.

**Uwaga / Anty-wzorzec:**
Poleganie na odziedziczonym stanie logowania/cookies do automatyzacji cudzych SaaS-ów rodzi ryzyko naruszenia ToS, problemy bezpieczeństwa (ekspozycja sesji) i kruchość względem zmian po stronie serwisu. Dodatkowo model 2B ma ograniczoną głębokość rozumowania — 'dobra stabilność tool_call' nie oznacza niezawodności na poziomie dużych modeli; nie należy zakładać, że mini-model zastąpi większy model w złożonych zadaniach agentowych bez walidacji.

> **Cytat:** *"看到个神奇的 huggingface Space项目, 思路很值得借鉴跟大家说下. Space 叫 MiniCPM5-2B-WebGPU-Pi, 不用起 Docker, 也不用装 Node 啥的, 打开网页就是一个带虚拟终端, 能进行文件编辑和 tool_call 的完整Coding Agent. 这玩意用 Pi 包了个 Coding Agent, 然后使用 MiniCPM5-2B 模型驱动. ... 这里用的是 MiniCPM5-2B 4bit ONNX 封装版本 (不到2G), 所以从框架到推理模型全都运行在了浏览器上. ... 我实测这玩意在我的3080Ti上能跑到25tps, 框架内部模拟了shell环境和提供了最基础的文件编辑tool_call. ... MiniCPM5-2B 的 tool_call 稳定性意外的不错"*

---

## Trening modeli / Reasoning / Dystylacja

### Dystylacja długiego CoT R1 do małych modeli i pułapka budżetu myślenia

- **Data:** `Mon Sep 14 09:52:12 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099436039169536325)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Chain-of-Thought (CoT)]] [[Harness|Dystylacja wiedzy]] [[Harness|Budżet myślenia (thinking budget)]] [[Stabilność modeli i przestrzeganie promptu|DeepSeek R1]] [[Stabilność modeli i przestrzeganie promptu|Reasoning modele]] [[Harness|Ollama]] [[Stabilność modeli i przestrzeganie promptu|Qwen]]

**Kontekst / Problem:**
Autor przypomina kluczowy wątek z pracy DeepSeek R1 (Section 3) dotyczący długiego rozumowania (long CoT). Omawia mechanizm, w którym długie łańcuchy myśli generowane przez duży model R1 są destylowane do małych modeli (Qwen-1.5B, 7B, 14B), oraz zjawisko, w którym wydłużenie budżetu myślenia w czasie inferencji prowadzi do skokowego wzrostu zdolności rozwiązywania zadań (z 71.0% do 86.7%). Zwraca też uwagę na mylącą praktykę dystrybucji modeli destylowanych jako 'DeepSeek'.

**Rada inżynierska:**
Przy pracy z modelami reasoning: (1) długość łańcucha myśli (thinking budget) jest sterowalnym hiperparametrem inferencji — zwiększenie budżetu myślenia daje dodatni zwrot w jakości rozumowania, szczególnie dla modeli destylowanych z długiego CoT; (2) destylacja długich CoT z dużego modelu (R1) do małego (1.5B/7B/14B) przenosi zdolność rozumowania — mały model z wystarczającym budżetem myślenia znacząco zyskuje; (3) zawsze rozróżniaj model bazowy od destylatu: 'deepseek-r1-distilled-qwen-7b' to Qwen dostrojony na danych R1, nie DeepSeek R1.

**Uwaga / Anty-wzorzec:**
Traktowanie modelu destylowanego (np. deepseek-r1-distilled-qwen-7b dystrybuowanego przez ollama) jako oryginalnego DeepSeek R1. To prowadzi do błędnych wniosków o architekturze, wydajności i kosztach. Nazewnictwo 'uruchamiamy DeepSeek' na małym Qwenie jest marketingowym uproszczeniem zacierającym różnicę między modelem nauczycielskim a uczniem.

> **Cytat:** *"请读完了Section 2后继续看Section 3 . 明确写了模型在长思考时的表现. 当时震撼人心的继续从71.0% 飙升到 86.7% 就是这么来的. 然后将 R1 生成的长思维链蒸馏到了小模型（ Qwen-1.5B、7B、14B）。在运行时给足其思考预算，然后解题能力就呈现出与思考长度正相关的暴涨。这不就是去年的新闻嘛....怎么还能记不住呢....然后就ollama把deepseek-r1-distilled-qwen-7b 当deepseek给大家装到电脑上了, 美其名曰运行deepseek. 有印象没? 串起来了吧?"*

---

## Modele rozumujące / Test-time compute / Dystylacja

### Test-time compute i dystylacja długiego CoT: od DeepSeek-R1 do małych modeli Qwen

- **Data:** `Mon Sep 14 09:51:35 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099435885599367551)
- **Rodzaj:** Komentarz w dyskusji (@sosolab13)
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|Test-time compute]] [[Harness|Chain-of-Thought]] [[Harness|Dystylacja wiedzy]] [[Stabilność modeli i przestrzeganie promptu|DeepSeek-R1]] [[Harness|Budżet myślenia]] [[Harness|Modele rozumujące]] [[Harness|MoE]] [[Harness|Ollama]]

**Kontekst / Problem:**
Autor odnosi się do dyskusji o tym, skąd bierze się skok jakości modeli rozumujących. Wyjaśnia, że źródłem spektakularnego wzrostu wyników benchmarków (np. z 71,0% do 86,7%) było skalowanie obliczeń w czasie wnioskowania (dłuższe 'myślenie'), a następnie przeniesienie wygenerowanego przez R1 długiego łańcucha myśli (long CoT) do małych modeli (Qwen-1.5B/7B/14B) w procesie dystylacji. Podkreśla, że przy odpowiednio dużym budżecie myślenia zdolność rozwiązywania zadań rośnie wprost proporcjonalnie do długości rozumowania — to był główny przekaz zeszłorocznych doniesień, który wielu błędnie zapomniało.

**Rada inżynierska:**
Reguła inżynierska: (1) Dla modeli rozumujących traktuj budżet myślenia (thinking budget) jako sterowalny parametr runtime — większa długość CoT przekłada się na wyższą skuteczność rozwiązywania zadań (test-time compute scaling). (2) Długi CoT można dystylować z dużego modelu (np. R1) do małych modeli (Qwen 1.5B/7B/14B), zachowując korzyść skalowania myślenia. (3) Zawsze rozróżniaj model źródłowy od modelu dystylowanego — to kluczowe dla poprawnej oceny możliwości i kosztów inferencji.

**Uwaga / Anty-wzorzec:**
Mylenie modeli dystylowanych z oryginałem: narzędzia typu Ollama instalowały deepseek-r1-distilled-qwen-7b pod szyldem 'DeepSeek', przez co użytkownicy wierzyli, że lokalnie uruchamiają pełny DeepSeek-R1. Prowadzi to do błędnych wniosków o jakości, zdolnościach i zachowaniu oryginalnego modelu (architektura MoE, skala, budżet myślenia) oraz do fałszywych porównań benchmarkowych.

> **Cytat:** *"请读完了Section 2后继续看Section 3 . 明确写了模型在长思考时的表现. 当时震撼人心的继续从71.0% 飙升到 86.7% 就是这么来的. 然后将 R1 生成的长思维链蒸馏到了小模型（ Qwen-1.5B、7B、14B）。在运行时给足其思考预算，然后解题能力就呈现出与思考长度正相关的暴涨。这不就是去年的新闻嘛....怎么还能记不住呢....然后就ollama吧deepseek-r1-distilled-qwen-7b 当deepseek给大家装到电脑上了, 美其名曰运行deepseek. 有印象没? 串起来了吧?"*

---

## Inżynieria rozumowania / Test-time compute / Benchmarking

### SOTA jako kompresor informacji: dlaczego reasoning effort = max psuje wyniki na SWE-bench

- **Data:** `Mon Sep 14 09:14:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099426676669366337)
- **Rodzaj:** Komentarz w dyskusji (@karminski3)
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|Test-time Compute]] [[Stabilność modeli i przestrzeganie promptu|Reasoning Effort]] [[Harness|Overthinking]] [[Harness|SWE-bench]] [[Harness|Kompresja informacji w modelach]] [[Harness|Token Efficiency]] [[Harness|Mechanizmy zatrzymania rozumowania]] [[Stabilność modeli i przestrzeganie promptu|Benchmarkowanie modeli rozumujących]]

**Kontekst / Problem:**
Autor odpowiada pod wpisem innego użytkownika, odsyłając do trzech prac/analiz: (1) dlaczego na SWE-bench wyniki przy ustawieniu 'max' się 'odwracają' (倒挂 – niższy reasoning effort wypada lepiej niż maksymalny), (2) czy ustawienie modelu na 'max' jest w ogóle właściwe, (3) jak sprawić, by model poprawnie ZATRZYMYWAŁ się w trakcie myślenia. Kontekst: trwająca w środowisku dyskusja o test-time compute i 'overthinking' w modelach rozumujących. Autor przekonuje, że więcej myślenia nie znaczy lepiej, i formułuje tezę o modelu SOTA jako idealnym kompresorze informacji.

**Rada inżynierska:**
Traktuj model SOTA jako kompresor informacji: miarą jakości jest rozwiązanie najtrudniejszego problemu przy MINIMALNEJ liczbie tokenów, a nie długość łańcucha myślowego. Nie ustawiaj reasoning effort na 'max' domyślnie – na zadaniach typu SWE-bench maksymalny budżet rozumowania potrafi dać wynik GORSZY niż ustawienie niższe (inwersja wyników), bo model wchodzi w pętle, kwestionuje już poprawne kroki i przepala kontekst. Praktycznie: (a) traktuj reasoning budget jako hiperparametr do walidacji na własnym benchmarku, a nie jako 'im więcej tym lepiej'; (b) testuj co najmniej 2-3 poziomy effortu obok siebie i mierz skuteczność zadaniową, nie liczbę tokenów; (c) wdrażaj mechanizmy poprawnego zatrzymania rozumowania (kryteria stopu, limity kroków, weryfikator zewnętrzny), zamiast liczyć, że model sam wyczuje moment zakończenia. Elegancja i zwięzłość rozwiązania (E = mc²) jest sygnałem kompresji, nie jego długość (42).

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: ślepe skalowanie test-time compute – założenie, że 'max thinking' = maksymalna jakość. Prowadzi to do overthinkingu, dryfu rozumowania, zapychania kontekstu i w efekcie regresji na zadaniach agentowych/inżynieryjnych (SWE-bench). Drugi anty-wzorzec: ocenianie modelu po objętości i 'głębokości' odpowiedzi zamiast po trafności przy minimalnym koszcie tokenowym.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Teza stoi w sprzeczności z dominującym konsensusem branżowym, że skalowanie test-time compute (większy budżet rozumowania, więcej tokenów myślowych) monotonicznie poprawia jakość. Autor twierdzi, że ustawienie 'max' może POWODOWAĆ INWERSJĘ wyników na SWE-bench, a miarą SOTA jest maksymalna kompresja informacji (najmniej tokenów na najtrudniejszy problem), a nie długość rozumowania. Do rozstrzygnięcia: dla jakich klas zadań i modeli inwersja występuje, gdzie leży optymalny punkt reasoning effortu oraz jak zdefiniować i egzekwować 'poprawne zatrzymanie' rozumowania – brak tu twardych liczb i metodologii, poleganie na samych linkach do prac.

> **Cytat:** *"来, 走出民科, 咱们阅读论文.  

为什么max测SWE会倒挂：https://t.co/9cV5oLJLLH

设置为max真的就对吗：https://t.co/7QgZzJws0W

到底怎样才能让模型思考的时候正确的停下来: https://t.co/m1M1t03vJi  

我重申我的观点, SOTA的模型永远是完美的信息压缩器. 用最少的token解决最难的问题. 思考一大堆得出宇宙的最终解是42不是SOTA. E = mc² 才是. 

上次的讨论: https://t.co/HK6fCYvgwu"*

---

## Inżynieria rozumowania / Prompt Architecture / Benchmarking agentowy

### Kompresja informacji jako metryka SOTA: dlaczego 'max' reasoning tokens psuje SWE i kiedy model powinien przestać myśleć

- **Data:** `Mon Sep 14 08:52:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099421138069950509)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|Reasoning Token Budget]] [[Stabilność modeli i przestrzeganie promptu|Over-thinking / Reasoning Saturation]] [[Harness|Stop Condition / Termination Policy]] [[Harness|SWE-bench]] [[Harness|Token Efficiency jako metryka]] [[Harness|Information Compression Hypothesis]] [[Harness|Chain-of-Thought]] [[Stabilność modeli i przestrzeganie promptu|Benchmark Inversion]]

**Kontekst / Problem:**
Autor adresuje trzy konkretne problemy z rzeczywistego prowadzenia modeli rozumujących w zadaniach agentowych/inżynierskich: (1) dlaczego ustawienie budżetu rozumowania na 'max' powoduje ODWRÓCENIE (inwersję) wyników benchmarku SWE — czyli pogorszenie wyników przy maksymalnym wysiłku; (2) czy 'max' jest w ogóle poprawnym ustawieniem; (3) jak zmusić model do poprawnego ZATRZYMANIA rozumowania (stop condition / termination policy). Teza autora: model klasy SOTA to nie taki, który generuje najdłuższą analizę, lecz najlepszy KOMPRESOR INFORMACJI — rozwiązuje najtrudniejsze problemy przy minimalnej liczbie tokenów.

**Rada inżynierska:**
Traktuj długość/rozmiar budżetu rozumowania jako hiperparametr do walidacji, a nie jako 'im więcej, tym lepiej'. Optymalizuj na token-efficiency: najlepszy model to najlepszy kompresor informacji — rozwiązuje najtrudniejszy problem najmniejszą liczbą tokenów. Ustawienie reasoning budget = max może skutkować inwersją (odwróceniem kolejności na leaderboardzie SWE), bo modele zapętlają się, krążą wokół hipotez i gubią sygnał. Mierz jakość rozwiązania względem kosztu tokenowego (np. pass@k / token, resolve rate / reasoning tokens) i dobieraj politykę STOP-u: model musi wiedzieć, KIEDY przestać myśleć, nie tylko jak myśleć.

**Uwaga / Anty-wzorzec:**
Domyślne ustawienie 'reasoning = max' / 'thinking budget = max' jako domniemany optimum. Anty-wzorzec: utożsamianie długości rozumowania z jakością — 'myślenie przez tysiące tokenów i dojście do odpowiedzi-wszechświata = 42' to nie SOTA. Werbalna, egzoteryczna analiza nie jest tym samym co zwięzłe, poprawne rozwiązanie (analogia autora: E = mc² zamiast rozwlekłego wyprowadzenia). Brak jawnej polityki zatrzymania prowadzi do over-thinkingu, zużycia kontekstu i degradacji wyników na benchmarkach agentowych typu SWE.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Teza kontrowersyjna wobec dominującego w branży podejścia 'scale reasoning at inference time' (test-time compute scaling), gdzie zakłada się, że więcej kroków rozumowania ≈ lepsze wyniki i gdzie dostawcy eksponują parametr 'reasoning effort = high/max'. Autor twierdzi, że dla benchmarków agentowych (SWE) maksymalizacja budżetu rozumowania może DZIWAĆ WYNIKI (inwersja rankingu) i że prawdziwą miarą SOTA jest KOMPRESJA informacji (minimalny koszt tokenowy przy najtrudniejszym zadaniu), a nie objętość analizy. Wniosek: długość rozumowania to hiperparametr wymagający walidacji per-model i per-benchmark, a nie uniwersalne 'więcej = lepiej'.

> **Cytat:** *"来, 走出民科, 咱们阅读论文. 为什么max测SWE会倒挂：[link] 设置为max真的就对吗：[link] 到底怎样才能让模型思考的时候正确的停下来：[link] 我重申我的观点, SOTA的模型永远是完美的信息压缩器. 用最少的token解决最难的问题. 思考一大堆得出宇宙的最终解是42不是SOTA. E = mc² 才是."*

---

## Prompt Architecture / Reasoning Effort & Test-time Compute

### Intensywność rozumowania jako realny lewar wydajności — dowody z DeepSeek-R1-Zero (AIME24: 15% → 71%)

- **Data:** `Mon Sep 14 07:14:23 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099396323942547519)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|Reasoning Effort]] [[Stabilność modeli i przestrzeganie promptu|Test-time Compute]] [[Stabilność modeli i przestrzeganie promptu|DeepSeek-R1-Zero]] [[Harness|Zero-SFT RL]] [[Harness|Chain-of-Thought]] [[Harness|AIME24]] [[Stabilność modeli i przestrzeganie promptu|Benchmarkowanie konfiguracji modelu]] [[Harness|Latency vs. Token Throughput]]

**Kontekst / Problem:**
Autor przetestował model deepseek-v4.1-flash z ustawieniem maksymalnej intensywności rozumowania (max). W komentarzach społeczność zakwestionowała ten wybór, twierdząc, że należy używać poziomu 'high', a sam przełącznik intensywności myślenia rzekomo nie ma związku z jakością/ wydajnością modelu. Autor odpiera tę tezę, przywołując własną pracę DeepSeek-R1-Zero, która empirycznie wiąże długość rozumowania z wynikami benchmarków.

**Rada inżynierska:**
Poziom intensywności rozumowania (thinking effort / reasoning budget) jest bezpośrednim lewarem jakości, a nie kosmetycznym ustawieniem UI. W DeepSeek-R1-Zero zastosowano czysty RL bez SFT (Zero-SFT RL), nie dodając żadnej nowej wiedzy do modelu — a mimo to wraz ze wzrostem długości łańcucha rozumowania wynik AIME24 wzrósł z 15% do 71%. Wniosek inżynierski: przy zadaniach wymagających rozumowania należy jawnie konfigurować i testować maksymalny budżet rozumowania, mierząc go na benchmarku, zamiast przyjmować domyślny lub 'bezpieczny' niższy poziom. Konfigurację reasoning effort traktuj jako parametr podlegający benchmarkowaniu (accuracy vs. token throughput vs. latency), a nie jako stałą.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: argumentowanie za obniżeniem intensywności rozumowania na podstawie intuicji lub potocznego konsensusu ('high jest lepsze niż max', 'to tylko przełącznik, nie wpływa na wyniki') bez weryfikacji źródłowej — w tym wypadku bez znajomości własnej publikacji dostawcy modelu. Kolejna pułapka: mylenie kosztu inferencji (więcej tokenów, wyższa latencja) z brakiem korzyści jakościowej — wyższy koszt jest realny, ale nie oznacza, że efektu nie ma. Zalecenie: przed krytyką ustawienia sprawdź dokumentację/paper i wykonaj własny pomiar na reprezentatywnym zbiorze zadań.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Spór z rozpowszechnioną w społeczności praktyką rekomendowania poziomu 'high' zamiast 'max' oraz z tezą, że przełącznik intensywności myślenia nie przekłada się na jakość modelu. Autor twierdzi, że jest odwrotnie i popiera to wynikami DeepSeek-R1-Zero (15% → 71% na AIME24 przy wzroście długości rozumowania, bez dopływu nowej wiedzy). Do rozstrzygnięcia pozostaje: czy w modelach nowszej generacji (np. deepseek-v4.1-flash) obowiązuje ta sama monotoniczna zależność, czy występuje punkt nasycenia/degradacji (overthinking) przy maksymalnym budżecie rozumowania — autor tego nie mierzył osobno, a krytycy nie przedstawili danych.

> **Cytat:** *"DS民科怎么这么多, 我测完了 deepseek-v4.1-flash, 开 max, 然后评论跟我说应该开high, 不应该开max. 〇的我买法拉利然后你跟我说挂一档比挂二挡快是吧? 然后跟我说这只是思考强度开关, 跟性能没关系. 干你〇怎么就没关系..... 去年 deepseek 自家发的 DeepSeek-R1-Zero 论文怎么都忘了 ... 就这个论文证明了思考强度越强模型能力越强的. 论文里Zero-SFT RL了一波, 没有增加任何新知识, 随着思考长度增加, AIME24 跑分就从 15% 魔法般的飙到了 71%. 然后震撼业界的雷霆大思考就如同雨后春笋般普及了..... 劝D小鬼对线前看看论文, 大水冲了自家龙王庙了."*

---

## Inżynieria agentowa / Prompt Architecture

### Skill jako izomorfizm kodu i danych: metaprogramowanie i dynamiczna generacja Micro-Skillów

- **Data:** `Mon Sep 14 06:23:09 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099383433034440811)
- **Rodzaj:** Komentarz w dyskusji (@kalasoo)
- **Powiązane pojęcia:** [[Harness|Skill jako izomorfizm kodu i danych]] [[Harness|Metaprogramowanie skilli]] [[Harness|Micro-Skill]] [[Harness|Hybrydowa ekstrakcja regex + LLM]] [[Harness|Pydantic jako harness walidacyjny]] [[Prompt Architecture]] [[Weryfikator|Zewnętrzny weryfikator]] [[Harness|Anty-wzorzec: skill jako dokument]]

**Kontekst / Problem:**
Autor odpowiada pod wpisem o koncepcji 'skill' w systemach agentowych. Rozróżnia statyczne dokumenty (które są albo kodem, albo danymi) od skilla, który pozwala na jednoczesne współistnienie obu warstw (izomorfizm). Problem: większość inżynierów pisze skille jak dokumenty — wpisuje na sztywno konkretny format (np. ekstrakcji faktury) i traci możliwość adaptacji, gdy pojawi się nowy, nieprzewidziany układ danych. Rozwiązanie: traktować skill jako program, który sam generuje wyspecjalizowane pod-zadania (Micro-Skille) dopasowane do konkretnego wejścia.

**Rada inżynierska:**
Traktuj skill jak program, nie jak dokument — wykorzystaj izomorfizm kodu i danych do metaprogramowania. Zamiast wpisywać na sztywno format ekstrakcji, zleć modelowi najpierw analizę topologii układu i konwencji nazewniczych wejścia, a następnie dynamiczną generację wyspecjalizowanego Micro-Skilla, który: (1) rozdziela pola deterministyczne (ekstrahowalne regexem) i kompiluje je do klasycznego kodu, (2) dla pól niejednoznacznych generuje ultra-zwięzły prompt (<=50 znaków) dla LLM, (3) tworzy klasę walidacyjną Pydantic jako prosty harness sprawdzający spójność semantyczną (np. kwota z podatkiem == kwota netto + VAT). Dzięki temu skill staje się odporny na nieznane formaty i działa tak długo, jak model jest wystarczająco inteligentny — nie trzeba go ręcznie rozbudowywać o każdy nowy przypadek.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: 'skill jako dokument' — zapisanie w skillu sztywnego szablonu promptu typu 'wyciągnij datę i kwotę według poniższego formatu'. Taki skill pęka natychmiast po napotkaniu formatu spoza jego zakresu i wymaga ciągłej ręcznej konserwacji. Drugi anty-wzorzec: bezpośrednie generowanie wynikowego JSON-a przez LLM bez wyodrębnienia pól deterministycznych (regex) i bez harnessu walidacyjnego — marnuje tokeny i wprowadza halucynacje tam, gdzie wystarczyłaby deterministyczna ekstrakcja.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor podważa dominującą praktykę traktowania skilli/promptów jako statycznych, deklaratywnych szablonów ('skill = dokument'). Proponuje paradygmat dynamiczny, w którym skill jest programem generującym inne skille w czasie wykonania (metaprogramowanie). Spór dotyczy tego, czy skille powinny być deterministyczne i audytowalne (podejście klasyczne, stabilne, ale kruche na nowe formaty), czy generatywne i samoadaptacyjne (elastyczne, ale zależne od jakości modelu i trudniejsze do walidacji). Do rozstrzygnięcia: koszt latencji i tokenów przy generacji Micro-Skilla per-wejście vs. zysk z odporności na nieznane formaty.

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

## Prompt Architecture / Agent Harness / Metaprogramowanie

### Izomorfizm kodu i danych w skillach: metaprogramowanie Micro-Skill zamiast statycznych promptów

- **Data:** `Mon Sep 14 06:22:54 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099383368999965122)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Izomorfizm kodu i danych]] [[Harness|Metaprogramowanie promptów]] [[Harness|Micro-Skill]] [[Harness|Agent Harness]] [[Harness|Walidacja Pydantic]] [[Harness|Ekstrakcja deterministyczna vs LLM]] [[Prompt Architecture]] [[Context Compaction|Kontekst inżynieria]]

**Kontekst / Problem:**
Autor krytykuje dominujący anty-wzorzec traktowania 'skilla' (definicji zadania agenta) jak zwykłej dokumentacji: sztywnego opisu typu 'wyciągnij datę i kwotę w tym formacie'. Tak zbudowany skill działa tylko na formatach przewidzianych przez autora i 'wybucha' (zawodzi) przy każdej nieznanej odmianie dokumentu. Problem wynika z nierozumienia, że skill może być jednocześnie kodem i danymi (izomorfizm), co otwiera drogę do metaprogramowania.

**Rada inżynierska:**
Traktuj skill jako program, który sam generuje wyspecjalizowany program wykonawczy. Zamiast z góry zakodowanego promptu ekstrakcji, zleć modelowi zadanie metapoznawcze: (1) przeanalizuj topologię układu dokumentu i konwencje nazewnicze, (2) NIE zwracaj od razu wyniku JSON, lecz dynamicznie wygeneruj dedykowany Micro-Skill, który: rozdziela pola deterministyczne (wyciągane regexem, kompilowane do klasycznego kodu) od pól niejednoznacznych (wymagających LLM + ultra-zwięzłego promptu ≤50 znaków), oraz (3) generuje ścisłą klasę walidacyjną Pydantic jako lekki, zewnętrzny harness weryfikujący spójność (np. kwota_z_podatkiem == kwota_bez_podatku + podatek). Dzięki temu skill jest samoadaptujący i nie wymaga ręcznej aktualizacji, o ile model jest wystarczająco zdolny.

**Uwaga / Anty-wzorzec:**
Zapisywanie skilla jako statycznej dokumentacji/szablonu promptu pod konkretny format — brak generalizacji powoduje awarię na nieznanych layoutach. Drugi błąd: wymuszanie natychmiastowego wyjścia JSON zamiast najpierw zbudowania deterministyczno-LLM-owego pipeline'u i walidatora.

> **Cytat:** *"传统文档大多数时间只是【代码】或【数据】其中的一种. 而skill能实现代码与数据同构的特性... 理解了skill的同构性就能玩元编程: "分析这张发票的排版拓扑和命名惯例, 不要直接输出 JSON 结果, 动态生成一个专用的skill(Micro-Skill)并运行它来提取配置, 包括: 哪些字段可以通过正则表达式确定性提取(编译为传统代码). 哪些歧义字段需要 LLM 提取, 并生成一份不超过 50 字的超精简 Prompt. 生成严格验证该格式的 Pydantic 校验类(简单harness, 类似含税金额 == 不含税金额 + 税额)." 这样这个skill只要模型够聪明就不用管了."*

---

## Benchmarki LLM / Agentic Coding / Inżynieria promptów

### Benchmark modeli do agentowego kodowania backendu: stabilność vs szczytowa jakość

- **Data:** `Mon Sep 14 05:50:26 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099375198986461418)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Agentic Coding]] [[Stabilność modeli i przestrzeganie promptu|Benchmarkowanie modeli LLM]] [[Harness|Wariancja wyników modeli]] [[Harness|Inżynieria promptów]] [[Harness|Koszt tokenów]] [[Harness|Bazy wektorowe]] [[Harness|Post-training]] [[Harness|GPT6-Astra]] [[Harness|Fable-5.1]] [[Stabilność modeli i przestrzeganie promptu|DeepSeek-V4.1-Flash]] [[Harness|Kimi-K3]] [[Harness|Hy4-dev]]

**Kontekst / Problem:**
Autor porównuje modele w scenariuszu AgenticCoding: implementacja bazy wektorowej od zera, oceniana wynikiem wydajności bazy danych. Test obejmuje trzy powtórzenia, co pozwala mierzyć nie tylko szczytową jakość, ale też wariancję między próbami i realny koszt tokenowy wynikający z konieczności ponawiania generacji.

**Rada inżynierska:**
Nie oceniaj modelu wyłącznie po pojedynczym najlepszym wyniku. Dla produkcyjnego agentowego kodowania backendu kluczowa jest wariancja Δ między próbami. Model o niższym szczycie, ale stabilny (np. GPT6-Astra, Δ ok. 10–20%) jest w praktyce tańszy, bo nie wymaga wielokrotnego „losowania” i przepalania tokenów. Model SOTA o wysokiej zmienności (np. Fable-5.1, Δ > 50%) stosuj tylko z dopracowanym promptem i budżetem na retry. Do prostych zadań wybieraj najtańszy model o niskiej wariancji (np. DeepSeek-V4.1-Flash), a do złożonych — modele o wysokim szczycie jakości po starannym prompt engineeringu.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: wybór modelu na podstawie jednorazowego benchmarku lub tylko najlepszego wyniku, bez analizy odchylenia między próbami. Wysoka wariancja prowadzi do niestabilnych pipeline’ów agentowych, konieczności wielokrotnego generowania i nieprzewidywalnego zużycia tokenów. Drugi antywzorzec: używanie modelu SOTA o wysokiej zmienności bez dopracowanego promptu — wtedy często wypada gorzej niż stabilny model średniej klasy.

> **Cytat:** *"同步一波大模型写后端代码排行榜

GPT6-Astra 和 Fable-5.1 没来得及做视频, 直接给大家同步图文了.

就结论来说, 单纯后端 AgenticCoding 场景(注意我只说我这个测试, 用大模型从0实现向量数据库, 使用数据库性能计分. 别的我不知道). 目前Fable-5.1 还是SOTA. 写出来的向量数据库直接是第二名的2x.

不过Fable的表现反而跟GPT 完全反过来了, 之前测Anthropic的模型(opus/sonnet) 系列, 反而是最稳的, 三次测试中最高分和最低分差距不超过10%. 而这次 GPT6-Astra 三次得分反而很接近(12985.28, 12134.83, 10676.74), 这证明这个模型的后训练极其稳定, 而 Fable-5.1 则是  21191.51, 11915.19, 7998.93. Δ超过50%. 

所以从省token的角度, 其实更推荐使用 GPT6-Astra. 因为发挥稳定, 不需要重复抽卡. 而 Fable-5.1 更适合经验丰富的工程师好好写提示词后再使用.

国产模型正好也是这个局面, Hy4-dev 虽然分数高, 但是三次得分差距巨大, 10778.51, 6011.78, 4915.22. 而 Kimi-K3 则相对稳定. 另外最具性价比无疑是 DeepSeek-V4.1-Flash. 得分几乎跟 kimi-k3没区别了. 而且Δ<20%. 所以只要不是复杂的代码任务, 直接无脑 DeepSeek-V4.1-Flash最划算. 而复杂的尝试使用GPT6-Astra 和 Fable-5.1.

> #gpt6astra #fable51 #deepseekv41flash"*

---

## Benchmarking i lokalna inferencja małych modeli agentowych

### Dobór reasoning_effort wg typu zadania dla małych modeli agentowych oraz wybór backendu inferencji (llama.cpp vs MLX) na Macu

- **Data:** `Mon Aug 31 08:26:49 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2094341123124985991)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|reasoning_effort]] [[Małe modele agentowe]] [[Harness|llama.cpp]] [[Harness|MLX]] [[Harness|MTP (Multi-Token Prediction)]] [[Stabilność modeli i przestrzeganie promptu|Qwen3]] [[Harness|Kwantyzacja Q4_K_XL]] [[Harness|H100 NVL]] [[Stabilność modeli i przestrzeganie promptu|Benchmark agentowy]] [[Harness|Latencja i przepustowość tokenów]]

**Kontekst / Problem:**
Autor publikuje ranking (ladder) zdolności agentowych małych modeli LLM, testowanych na jednolitym stanowisku: pojedyncza karta H100 NVL + najnowsza wersja llama.cpp. Celem jest wskazanie praktycznie najlepszego modelu i konfiguracji do zadań agentowych oraz korekta domyślnego wyboru runtime'u dla użytkowników Apple Silicon.

**Rada inżynierska:**
1) Dla zadań agentowych na małych modelach ustawiaj reasoning_effort = low — nadmiar rozumowania zwiększa latencję i zużycie tokenów bez poprawy jakości pętli agentowej. 2) Dopiero przy generowaniu kodu podnoś reasoning_effort do medium / high, bo tam głębsze rozumowanie realnie przekłada się na poprawność. 3) Testuj modele na jednorodnym stosie (jedna karta H100 NVL + aktualny llama.cpp), aby wyniki były porównywalne między modelami. 4) Na Macach (Apple Silicon) preferuj MLX zamiast llama.cpp — w pomiarach MLX z włączonym MTP (Multi-Token Prediction) wypada szybciej niż llama.cpp z MTP na tym samym sprzęcie. 5) Kandydat o najlepszym stosunku jakości do kosztu w testach: Qwen3.8-27B-UD-Q4_K_XL (kwantyzacja Q4_K_XL).

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: stosowanie jednego, wysokiego poziomu reasoning_effort do wszystkich zadań (marnowanie tokenów i latencji w pętli agenta) oraz bezrefleksyjne używanie llama.cpp na macOS — pomimo że MLX z MTP jest tam szybszy. Drugi anty-wzorzec: porównywanie modeli na różnych runtime'ach/kwantyzacjach, co unieważnia wnioski z benchmarku.

> **Cytat:** *"小模型 Agent 能力测试的天梯在这里~ (希望图不要被压得太狠....)

目前来看最值得使用是我测试的 Qwen3.8-27B-UD-Q4_K_XL 版本,  Agent 用使用 reasoning_effort = low, 然后写代码开到 medium / high.

另外文中是统一使用单卡 H100 NVL+llama.cpp 最新版本测试的. 如果是Mac用户还是建议优先使用MLX, 实测 MLX 开 MTP 会比 llama.cpp 放在 Mac 上开MTP要快一些.

最后老铁们还想看什么模型的评测欢迎留言~ 我赶紧肝哈哈

#qwen38"*

---

## Benchmarking i ewaluacja modeli

### Metodyka benchmarku małych modeli: macierz kwantyzacji × MTP × poziom rozumowania

- **Data:** `Mon Aug 31 06:27:32 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2094311103987581033)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|pass@k]] [[Harness|Kwantyzacja modeli LLM]] [[Harness|Multi-Token Prediction (MTP)]] [[Stabilność modeli i przestrzeganie promptu|Thinking budget / reasoning effort]] [[Harness|Mixture of Experts (MoE) - modele A3B i A4B]] [[Stabilność modeli i przestrzeganie promptu|Benchmark agentowy]] [[Harness|Open-weights small models]] [[Harness|Przepustowość tokenów vs jakość generacji]]

**Kontekst / Problem:**
Autor przeprowadził kompleksowy benchmark 8 małych modeli open-weights (Qwen3.8-27B, Qwen3.6-27B, Qwen3.6-35B-A3B, Ornith-1.5-35B-A3B, Gemma-4-31B, Gemma-4-26B-A4B, Gemma-4-12B, GPT-OSS-20B) w kontekście zastosowań inżynierskich: generowanie frontendu, Python oraz zdolności agentowe. Celem było wyłonienie najlepszego modelu open-source do pracy, przy jednoczesnym zbadaniu wpływu trzech zmiennych niezależnych: stopnia kwantyzacji (4 warianty na model), włączenia/wyłączenia MTP (Multi-Token Prediction) oraz poziomu rozumowania (low/medium/xhigh).

**Rada inżynierska:**
Projektując ewaluację modeli, nie traktuj ich jako pojedynczych punktów – testuj je jako macierz konfiguracji: kwantyzacja × MTP on/off × poziom myślenia (low/medium/xhigh). Metryka pass@3 (3 przebiegi, brany najlepszy wynik) redukuje wariancję próbkowania i odzwierciedla realne użycie agentowe, gdzie kluczowa jest zdolność modelu do sukcesu w którymkolwiek podejściu. Kluczowa obserwacja kosztowa: dobór GPU (H100) wpływa wyłącznie na przepustowość i czas generacji, a nie na jakość generowanego wyniku – mimo przyspieszenia pełny przebieg macierzy zajął 48 godzin i kosztował 148 USD. Oznacza to, że w planowaniu benchmarków wąskim gardłem jest szerokość macierzy konfiguracji, nie sprzęt.

**Uwaga / Anty-wzorzec:**
Błąd: ocenianie modeli wyłącznie w jednej konfiguracji kwantyzacji lub przy jednym poziomie rozumowania – prowadzi to do błędnych wniosków o 'sile' modelu, gdyż tryb MTP i poziom thinking drastycznie zmieniają kompromis jakość/latencja/koszt. Drugi anty-wzorzec: mylenie wpływu sprzętu (GPU) z wpływem na jakość outputu – szybszy GPU skraca czas benchmarku, ale nie zmienia rozkładu poprawności odpowiedzi. Trzeci: używanie pojedynczego przebiegu (pass@1) do porównań małych modeli, gdzie wariancja jest wysoka.

> **Cytat:** *"终于搞完了! 给大家带来小模型竞技场, 这次测试了8款模型, 包括: Qwen3.8-27B, Qwen3.6-27B, Qwen3.6-35B-A3B, Ornith-1.5-35B-A3B, Gemma-4-31B, Gemma-4-26B-A4B, Gemma-4-12B, GPT-OSS-20B。每个模型4个量化版本, 还测试了 MTP 开启和关闭, 以及 low, medium, xhigh 三档思考强度, 做了个全面横评。测试主要集中在前端, python, Agent 能力上, 每个测试运行3次取最佳结果(pass@3)。测试使用H100显卡(注意用H100是为了生成快, 就这还跑了48小时, 显卡不影响生成效果, 只影响生成速度), 总成本148刀。"*

---

## Multimodalne modele i architektura harnessów agentowych

### Qwen3.8-Omni-Flash: multimodalny harness, plugins do agentów CLI i omni-skill-creator (uczenie przez demonstrację)

- **Data:** `Fri Sep 18 00:57:36 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2100751056104026497)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Multimodalne modele językowe]] [[Harness|Harness agentowy]] [[Harness|Agent CLI]] [[Harness|Plugin architektura agentów]] [[Harness|Teach-by-demonstration]] [[Harness|Omni-skill-creator]] [[Harness|Realtime voice pipeline]] [[Harness|Koszt tokenów multimodalnych]] [[Harness|Kanban task tracking w agentach]] [[Stabilność modeli i przestrzeganie promptu|Qwen3.8-Omni-Flash]]

**Kontekst / Problem:**
Qwen wypuścił Qwen3.8-Omni-Flash (następcę Omni-Flash 3.5) wraz z dwoma frameworkami towarzyszącymi: Qwen-Live-Harness (interfejs typu 'floating ball' z monitorowaniem środowiska i tablicą zadań/kanban do śledzenia długotrwałych zadań) oraz Qwen-MM-Plugins (biblioteka pluginów multimodalnych dla lokalnych agentów CLI: Claude Code, Gemini CLI, Codex, OpenClaw). Model rozwiązuje problemy: słabego rozumienia nakładających się głosów w spotkaniach, ograniczonego kontekstu audio-wideo oraz wysokich kosztów API multimodalnego. Nowa generacja daje +25% średniego wyniku, skok 88%→3% błędu ASR w nakładających się rozmowach, natywne wejście ciągłe A/V do 1 godziny i spadek kosztu audio z 18 RMB do 0,8 RMB za mln tokenów (−98%). Wersja Realtime osiąga opóźnienie ~981 ms dla 20 s audio (słyszy pytanie → krótko myśli → zaczyna mówić).

**Rada inżynierska:**
Traktuj 'harness' i 'plugins' jako warstwę integracyjną, nie tylko model. (1) Aby dodać multimodalność do istniejących lokalnych agentów tekstowych (Claude Code, Codex, Gemini CLI, OpenClaw), instaluj plugin bridge (Qwen-MM-Plugins) zamiast przepisywać agenta — uzupełnia wizję, pamięć długich wideo oraz pozwala agentowi sterować narzędziami graficznymi (Blender, CAD) przez wywołania multimodalne. (2) Do budowy nowych umiejętności używaj podejścia teach-by-demonstration (omni-skill-creator): nagraj wideo z operacji na oprogramowaniu i dołącz narrację głosową wyjaśniającą 'dlaczego' — model uczący się na pełnym modalu (obraz + głos + intencja) tworzy dokładniejsze skille niż sam zapis akcji. To odpowiednik programowania przez demonstrację manipulatora. (3) Dla asystentów długotrwałych zadań używaj harnessu z tablicą zadań (kanban) i pętlą monitoringu środowiska, aby utrzymać stan między turami (np. 'gdy skończysz, zawołaj mnie').

**Uwaga / Anty-wzorzec:**
Pomijanie warstwy głosowej przy tworzeniu skilli — nagrywanie samego wideo operacji bez narracji 'dlaczego' znacząco pogarsza generalizację tworzonego skilla. Drugi anty-wzorzec: traktowanie modelu jako wyłącznie tekstowego i ręczne doklejanie wizji/pamięci w każdym agencie zamiast użycia wspólnej warstwy pluginów multimodalnych.

> **Cytat:** *"Qwen 刚刚发布了 Qwen3.8-Omni-Flash! 同时还发布了两个配套框架, Qwen-Live-Harness, Qwen-MM-Plugins... 多人重叠会议语音识别的错误率直接从上一代的88%降低到了3%... 原生支持最长 1 小时的完整连续音视频输入, 并且API费用降低了98%... 之前音频输入每百万token是18块, 现在是0.8元!... Qwen3.8-Omni-Flash-Realtime... 20s音频约981ms... omni-skill-creator, 只需要录一段操作软件的视频, 然后丢给它, 他就能帮你形成操作这个软件的skill!... 录视频的时候还可以把自己的语音一起录进去, 告诉模型为什么这么做, 加深模型的理解, 创建出来的skill更准确."*

---

## Inżynieria kontekstu / Analiza wideo w LLM

### Dwupoziomowa ekstrakcja klatek wideo do analizy multimodalnej (image_url)

- **Data:** `Fri Aug 21 17:49:35 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2090858868989706352)
- **Rodzaj:** Komentarz w dyskusji (@karminski3)
- **Powiązane pojęcia:** [[Harness|Multimodalne modele LLM]] [[Harness|image_url w promptcie]] [[Harness|Ekstrakcja klatek wideo]] [[Harness|Dwupoziomowe próbkowanie wideo]] [[Harness|Timecode w promptcie]] [[Context Compaction|Inżynieria kontekstu wizyjnego]]

**Kontekst / Problem:**
Problem: analiza wideo przez modele multimodalne jest niedokładna, gdy klatki są wrzucane chaotycznie lub gdy stosuje się jednorodne próbkowanie całego materiału. Autor pokazuje sprawdzony sposób reprezentacji wideo jako sekwencji obrazów przekazywanych przez pole `image_url` wraz z jawnym opisem czasu w promptcie.

**Rada inżynierska:**
Aby uzyskać dokładną analizę wideo: (1) wyekstrahuj klatki jako JPEG/PNG i podaj je w porządku chronologicznym jako wiele wpisów `image_url` w jednym zapytaniu; (2) w promptcie jawnie zadeklaruj sampling rate oraz mapowanie klatek na os czasu (timecode/timeline); (3) zamiast równomiernego próbkowania całego materiału stosuj strategię DWUPOZIOMOWĄ: 'makro 1 fps cała klatka' (kontekst globalny) + 'okno zdarzenia z wysokim FPS i przycięciem/zoomem do centrum' (detale akcji). Taka kompozycja znacząco poprawia rozpoznawanie scen dynamicznych (testowane na CS2 — szybkie akcje).

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: jednorodne (uniform) próbkowanie całego wideo ze stałym FPS bez rozróżnienia na kontekst globalny i okna zdarzeń. Powoduje to albo utratę detali szybkich akcji (zbyt niski FPS globalnie), albo eksplozję liczby klatek (zbyt wysoki FPS globalnie) i degradację kontekstu przez szum.

> **Cytat:** *"把视频抽成 JPEG/PNG, 按时间顺序作为多个 `image_url` 传入, 并在 prompt 里写明采样率和时间轴. 这样分析会更准确. 我使用了一个猫和老鼠的片段进行分析, 这样做模型识别很准确. 另外, 我还用了一段 CS2 录像来验证分析快速动作时的最佳方案, 结论是不要匀速抽全片, 用「宏观 1fps 全图 + 事件窗口高帧率中心放大」两级采样。效果会更好."*

---

## Multimodalność / Przetwarzanie wideo

### Obsługa wideo w deepseek-v4-flash-vision-exp przez ekstrakcję klatek

- **Data:** `Fri Aug 21 17:49:34 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2090858863679750280)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Model multimodalny]] [[Harness|Ekstrakcja klatek]] [[Stabilność modeli i przestrzeganie promptu|deepseek-v4-flash-vision-exp]] [[Harness|Przetwarzanie wideo]] [[Harness|Frame sampling]] [[Harness|Weryfikacja empiryczna zachowania modelu]] [[Harness|Ograniczenia wejścia API]]

**Kontekst / Problem:**
deepseek wypuścił deepseek-v4-flash-vision-exp — swój pierwszy duży model multimodalny, na poziomie możliwości v4-flash. Model nie przyjmuje jednak wejścia audio, a co za tym idzie oficjalna strona i API deepseek nie obsługują wejścia wideo. Powstaje pytanie, jak praktycznie przetwarzać wideo tym modelem, skoro natywny pipeline tego nie wspiera.

**Rada inżynierska:**
Wideo podawaj do modelu przez bezpośrednią ekstrakcję klatek (frame sampling) i wysyłanie ich jako osobnych obrazów. Nie używaj GIF-a jako kontenera na wideo: mimo że model deklaruje obsługę wejścia GIF, faktycznie rozpoznaje wyłącznie pierwszą klatkę animacji (autor zweryfikował to empirycznie kodem). Konwersja wideo → GIF jest więc ślepą uliczką i trzeba zaimplementować własny ekstraktor klatek (z dobranym FPS / progami zmian scen).

**Uwaga / Anty-wzorzec:**
Błędne założenie, że „multimodalny” oznacza pełne zrozumienie wideo i audio. Konkretne pułapki: (1) konwersja wideo do GIF-a — model widzi tylko pierwszą klatkę, reszta materiału jest cicho tracona; (2) oczekiwanie natywnej obsługi wideo/audio w API tylko dlatego, że model jest multimodalny; (3) brak weryfikacji zachowania modelu na formacie, który deklaratywnie „jest wspierany” — deklaracja wsparcia ≠ faktyczna semantyka wejścia.

> **Cytat:** *"给大家写了个 deepseek-v4-flash-vision-exp 输入视频教程

deepseek 最近真的是高产, 刚刚又发了 deepseek-v4-flash-vision-exp, 首个多模态【大】模型. 而且是 v4-flash 能力级别的. 但是! 虽然不是瞎子了, 但是还是听力有问题, 不支持音频输入. 所以默认 deepseek 官网和API都不支持视频输入, 于是给大家写了个小教程, 如何使用这个模型处理视频.

简单来讲, 方法就是直接把视频抽帧. 而且需要注意, 虽然模型支持gif输入, 但是它只识别 gif 的第一帧(我写代码验证了). 所以把视频转换为gif是行不通的.

抽帧的最佳实践也给大家:

#deepseekv4flashvisionexp #deepseek多模态 #deepseek多模态模型"*

---
