---
autor: @teortaxesTex
źródło: https://x.com/teortaxesTex
wygenerowano: 2026-09-23 02:10
typ: synteza-wiedzy
tagi: [teortaxestex, ai-engineering, prompt-engineering, twitter-extract]
---

# @teortaxesTex — Baza Wskazówek i Komentarzy

> Destylacja praktycznych porad, heurystyk inżynierskich i komentarzy technicznych z profilu @teortaxesTex na platformie X. Wyciągnięto 7 wartościowych wpisów.

## ⚠️ Kwestie sporne i rozbieżności do rozstrzygnięcia

> Wpisy, w których autor podważa powszechne przekonania branżowe lub prezentuje tezy stojące w sprzeczności z innymi praktykami:

- **[Kompakcja treningowa redukuje znaczenie rozmiaru KV cache przy długim kontekście](https://x.com/teortaxesTex/status/2102545198199038197):** Teza stoi w sprzeczności z dominującym konsensusem, że rozmiar KV cache / pamięci kontekstu jest krytycznym wąskim gardłem długiego kontekstu i wymaga agresywnych technik kompresji (pruning, sliding window, summarization). Autor twierdzi, że kompakcja treningowa czyni ten problem w dużej mierze nieaktualnym. Do rozstrzygnięcia: czy 890 MB/1M to realny, powszechnie osiągalny poziom, czy wartość specyficzna dla konkretnej architektury/modelu, oraz czy 'reasoning with outputs' faktycznie zastępuje potrzebę zarządzania cache.
- **[Temporalna dysagregacja jako źródło ground truth do treningu modeli predykcyjnych](https://x.com/teortaxesTex/status/2102173977879757153):** Autor przeciwstawia się rozpowszechnionemu przekonaniu, że prognozowanie przyszłości jest fundamentalnie trudniejsze od modelowania danych historycznych z powodu braku ground truth. Twierdzi, że to 'actually easy', ponieważ ground truth dla przeszłości istnieje w formie temporalnie rozproszonej. Sporne pozostaje, czy rekonstrukcja pominiętych danych historycznych rzeczywiście uczy ekstrapolacji w warunkach niestacjonarności i zmiany reżimu — krytycy wskazują, że inter-/ekstrapolacja to nie to samo zadanie.
- **[Brak ground truth blokuje rzetelną ocenę online; weryfikowalność domen kluczem do ewaluacji](https://x.com/teortaxesTex/status/2102172327232385279):** Autor podważa powszechną praktykę używania LLM jako sędziów (LLM-as-judge) do oceny zadań otwartych, wskazując na brak ground truth i ryzyko niewiarygodnych ocen. Do rozstrzygnięcia: czy LLM-as-judge może być wystarczający przy braku weryfikowalnych sygnałów, czy konieczne są hybrydowe metody z formalną weryfikacją.

---

## Spis kategorii

- [Inżynieria kontekstu / zarządzanie pamięcią](#inżynieria-kontekstu--zarządzanie-pamięcią) (1)
- [Architektura modeli / Teoria treningu i mechanistyczna interpretowalność](#architektura-modeli--teoria-treningu-i-mechanistyczna-interpretowalność) (1)
- [Architektura modeli / Rozumowanie latentne i inżynieria kontekstu](#architektura-modeli--rozumowanie-latentne-i-inżynieria-kontekstu) (1)
- [Trening modeli / Transfer i generalizacja](#trening-modeli--transfer-i-generalizacja) (1)
- [Trening modeli / Inżynieria danych](#trening-modeli--inżynieria-danych) (1)
- [Prompt Architecture / Inżynieria promptów](#prompt-architecture--inżynieria-promptów) (1)
- [Ewaluacja modeli i weryfikacja](#ewaluacja-modeli-i-weryfikacja) (1)

---

## Inżynieria kontekstu / zarządzanie pamięcią

### Kompakcja treningowa redukuje znaczenie rozmiaru KV cache przy długim kontekście

- **Data:** `Tue Sep 22 23:46:53 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102545198199038197)
- **Rodzaj:** Komentarz w dyskusji (@awesome_ruler_)
- **Powiązane pojęcia:** [[Harness|KV cache]] [[Context Compaction|Kompakcja kontekstu]] [[Harness|Long-context]] [[Harness|Zarządzanie pamięcią agenta]] [[Stabilność modeli i przestrzeganie promptu|Reasoning przez outputy]]

**Kontekst / Problem:**
Dyskusja w wątku o ograniczeniach pamięciowych długiego kontekstu i rozmiarze cache. Autor odpowiada na argument, że mniejszy cache to problem, i twierdzi, że znaczenie rozmiaru cache spada dzięki postępom w kompakcji treningowej — przy ~890 MB na 1M tokenów kontekstu można po prostu kontynuować rozumowanie na wyjściach (reasoning carried through outputs) bez agresywnego zarządzania pamięcią.

**Rada inżynierska:**
Nie projektuj harnessu ani pipeline'u wokół przedwczesnej optymalizacji rozmiaru cache/KV. Wraz z dojrzałą kompakcją treningową (training compaction) ślad pamięciowy kontekstu maleje do poziomu rzędu ~890 MB na 1M tokenów, co sprawia, że wąskim gardłem przestaje być sam cache, a strategia 'utrzymuj rozumowanie w outputach' (persist reasoning w wyjściach, nie w cache) staje się praktyczna i wystarczająca.

**Uwaga / Anty-wzorzec:**
Traktowanie rozmiaru cache/KV jako głównego ograniczenia i budowanie architektury wokół agresywnego przycinania/kompresji kontekstu — to przedwczesna optymalizacja, gdy kompakcja na poziomie treningu i tak redukuje footprint.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Teza stoi w sprzeczności z dominującym konsensusem, że rozmiar KV cache / pamięci kontekstu jest krytycznym wąskim gardłem długiego kontekstu i wymaga agresywnych technik kompresji (pruning, sliding window, summarization). Autor twierdzi, że kompakcja treningowa czyni ten problem w dużej mierze nieaktualnym. Do rozstrzygnięcia: czy 890 MB/1M to realny, powszechnie osiągalny poziom, czy wartość specyficzna dla konkretnej architektury/modelu, oraz czy 'reasoning with outputs' faktycznie zastępuje potrzebę zarządzania cache.

> **Cytat:** *"@awesome_ruler_ @industriaalist @jayden_teoh_ Well, smaller cache doesn't matter much now
we're starting to have good training compaction, and at 890 Mb/1M context, you can just keep reasoning with outputs"*

---

## Architektura modeli / Teoria treningu i mechanistyczna interpretowalność

### MTP to red herring — pojedyncza predykcja tokenu wystarcza dla look-ahead w aktywacjach; liczy się efektywna głębokość obwodu

- **Data:** `Tue Sep 22 22:59:28 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102533265265500175)
- **Rodzaj:** Komentarz w dyskusji (@rudzinskimaciej)
- **Powiązane pojęcia:** [[Harness|Multi-Token Prediction]] [[Harness|Next-Token Prediction]] [[Harness|Effective Circuit Depth]] [[Harness|Look-ahead w aktywacjach]] [[Harness|Mechanistic Interpretability]] [[Harness|Residual Stream]] [[Harness|Ablacja warstw]]

**Kontekst / Problem:**
Dyskusja w wątku o tym, czy wielotokenowa predykcja (MTP, Multi-Token Prediction) jest niezbędna, aby model wykazywał zdolność 'patrzenia w przyszłość' (look-ahead) i planowania. Autor odrzuca tezę, że MTP jest źródłem tych zdolności, argumentując, że sam cel przewidywania pojedynczego następnego tokenu już wymusza na aktywacjach reprezentacje wyprzedzające. Przesuwa pytanie badawcze z celu treningowego na *efektywną* głębokość obwodu obliczeniowego (effective circuit depth) — ile warstw transformacji faktycznie uczestniczy w wyliczeniu danego wyniku.

**Rada inżynierska:**
Nie zakładaj, że MTP (lub inny dodatkowy cel treningowy) jest konieczny do uzyskania zachowań look-ahead/planowania — samo autoregresyjne przewidywanie następnego tokenu już indukuje w aktywacjach reprezentacje wyprzedzające. Zamiast debatować nad celem treningowym, mierz *efektywną* głębokość obwodu: ile warstw realnie wnosi wkład do danego wyniku (np. przez ablacje warstw, patching aktywacji, analizę residual stream). To rozdziela 'co model optymalizuje' od 'jak głęboko faktycznie liczy'.

**Uwaga / Anty-wzorzec:**
Traktowanie MTP jako wyjaśnienia zdolności look-ahead — to red herring, który odwraca uwagę od właściwego pytania. Anty-wzorzec: mylenie celu treningowego (objective) z efektywną głębokością obliczeniową (circuit depth) i wyciąganie wniosków o architekturze z samej obecności dodatkowego celu.

> **Cytat:** *"MTP is a red herring. Single token prediction objective is sufficient for activations to already "look ahead"
my question is about *effective* circuit depth"*

---

## Architektura modeli / Rozumowanie latentne i inżynieria kontekstu

### KV cache jako rozszerzenie efektywnej głębokości serialnej w modelach rozumujących

- **Data:** `Tue Sep 22 22:18:48 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102523033499877448)
- **Rodzaj:** Komentarz w dyskusji (@industriaalist)
- **Powiązane pojęcia:** [[Harness|KV cache]] [[Harness|Rozumowanie latentne]] [[Harness|Filler tokens]] [[Harness|Efektywna głębokość serialna]] [[Harness|Scratchpad]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Modele rozumujące po RL]]

**Kontekst / Problem:**
Autor odpowiada na tezę, że większość rozumowania można wykonać w przestrzeni latentnej, lepiej niż w języku naturalnym, z wyjątkiem wywołań narzędzi. Podnosi problem: jaka część tego efektu wynika z samego skalowania reprezentacji latentnej przez KV cache, niezależnie od treści znaczącej w sekwencji. Powołuje się na eksperymenty Astra z filler tokens. Twierdzi, że duże modele rozumujące po RL są bardziej 'patrzące w przyszłość' i przechowują częściowe obliczenia, co daje większą efektywną głębokość serialną niż stała głębokość pojedynczego forward pass.

**Rada inżynierska:**
Projektując prompty i systemy agentowe, traktuj kontekst oraz KV cache nie tylko jako bierną pamięć treści, lecz także jako pamięć roboczą/scratchpad dla częściowych obliczeń. U modeli rozumujących po RL kolejne tokeny mogą zwiększać efektywną głębokość serialną ponad ograniczenie wynikające ze stałej liczby warstw. Warto świadomie zarządzać długością kontekstu, zostawiać miejsce na tokeny robocze i testować, czy wydłużenie reprezentacji latentnej — nawet przez filler tokens — poprawia wyniki. Pamiętaj jednak, że tokeny znaczące dają większy zysk niż wypełniacze.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: zakładanie, że model wyłącznie 'przewiduje następny token', a kontekst służy tylko jako bierna pamięć informacji. Drugi anty-wzorzec: wnioskowanie, że filler tokens lub sama długość KV cache zastąpią wartościową treść — autor zaznacza, że tokeny znaczące pomagają bardziej, a efekt filler tokens może być mylący bez kontroli eksperymentalnej.

> **Cytat:** *"> most of the reasoning can be done in latent space (except like tool calls) and in fact, much better than in nat lang
Yes. no dispute. The issue: how much of that is afforded just by scaling the latent representation via KV cache, even modulo the meaningful sequence content? See Astra's scaling with filler tokens. Meaningful tokens, ofc, help more. I think there's a popular underestimation where "it just outputs the next token". I think large reasoning models after a lot of RL are more forward-looking, and basically store partial computations that add up to longer effective serial depth of fixed-depth forward passes. Does this make sense?"*

---

## Trening modeli / Transfer i generalizacja

### Ustrukturyzowany sygnał treningowy (kod, matematyka) generalizuje rozumowanie lepiej niż styl

- **Data:** `Mon Sep 21 23:13:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102174532547080559)
- **Rodzaj:** Komentarz w dyskusji (@phl43)
- **Powiązane pojęcia:** [[Harness|Sygnał treningowy]] [[Harness|Generalizacja rozumowania]] [[Harness|Pretraining vs RL]] [[Harness|Transfer umiejętności]] [[Harness|Dane treningowe: kod i matematyka]] [[Harness|Czynnik g modelu]]

**Kontekst / Problem:**
Dyskusja o tym, jaki rodzaj danych treningowych (pretraining i RL) prowadzi do transferu umiejętności rozumowania na inne dziedziny. Autor przeciwstawia sygnał logicznie ustrukturyzowany (kod, matematyka) względem sygnału stylistycznego, argumentując empirycznie: modele pretrenowane na kodzie poprawiły się niemal we wszystkich zadaniach, a DeepSeek-R1 trenowany RL na matematyce i kodzie stał się znacznie lepszym pisarzem niż bazowy V3.

**Rada inżynierska:**
Do budowy zdolności rozumowania inwestuj w sygnał treningowy o ścisłej strukturze logicznej — kod i matematyka — zarówno na etapie pretreningu, jak i RL. Taki sygnał generalizuje: podnosi wyniki na zadaniach odległych od dziedziny treningu (np. pisanie, ogólne rozumowanie). Wniosek inżynierski: jeśli celem jest ogólna kompetencja modelu (wysokie 'g'), dobieraj dane treningowe według kryterium gęstości logicznej struktury, a nie według atrakcyjności stylistycznej.

**Uwaga / Anty-wzorzec:**
Optymalizowanie pod styl (np. 'ładne pisanie', ton, forma) jako główny sygnał treningowy nie podnosi ogólnej zdolności rozumowania — styl nie jest silnie skorelowany z czynnikiem g (general intelligence). Trenowanie wyłącznie na danych stylistycznych daje model, który dobrze 'brzmi', ale słabo rozumuje i słabo transferuje.

> **Cytat:** *"We see that logically structured training signal (both in pretraining and in RL) generalizes reasoning. First models pretrained on coding got better at ≈all tasks, R1 was RL'd for mafs&coding and became a vastly better writer than V3. but style, it seems, is not very g-loaded"*

---

## Trening modeli / Inżynieria danych

### Temporalna dysagregacja jako źródło ground truth do treningu modeli predykcyjnych

- **Data:** `Mon Sep 21 23:11:47 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102173977879757153)
- **Rodzaj:** Komentarz w dyskusji (@hesipullfade)
- **Powiązane pojęcia:** [[Harness|Self-supervised learning]] [[Harness|Temporalna dysagregacja]] [[Eval Set z realnych sesji|Ground truth]] [[Harness|Szeregi czasowe]] [[Harness|Masked modeling]] [[Harness|Ekstrapolacja vs interpolacja]] [[Harness|Distribution shift]]

**Kontekst / Problem:**
Dyskusja dotyczy zarzutu, że nie da się wytrenować modelu prognozującego przyszłość, bo nie istnieje ground truth dla zdarzeń, które jeszcze nie nastąpiły. Autor odpowiada, że ground truth dla danych historycznych istnieje — jest tylko temporalnie rozproszony (temporally disaggregated), czyli rozbity na mniejsze przedziały czasowe i częściowo pominięty w danych wejściowych. Problem sprowadza się więc do zadania rekonstrukcji brakujących obserwacji historycznych.

**Rada inżynierska:**
Traktuj prognozowanie przyszłości jako zadanie rekonstrukcji pominiętych danych historycznych. Jeśli model potrafi odtworzyć usunięte/maskowane fragmenty przeszłego szeregu czasowego (dla których ground truth faktycznie posiadasz), to nabywa tę samą umiejętność ekstrapolacji potrzebną do przewidywania przyszłości. Praktycznie: buduj zbiory treningowe przez celowe maskowanie, agregowanie lub usuwanie okien czasowych z danych historycznych i ucz model ich odtworzenia — to daje niemal nieograniczony, samo-nadzorowany sygnał treningowy bez konieczności czekania na przyszłe etykiety.

**Uwaga / Anty-wzorzec:**
Błędne założenie, że brak etykiet dla przyszłości uniemożliwia trening predykcyjny. Anty-wzorzec: zbieranie danych wyłącznie w układzie 'cecha teraz → cel w przyszłości' i rezygnacja z ogromnego korpusu historycznego, który można przekonwertować na zadania rekonstrukcji. Uwaga jednak: ekstrapolacja w przyszłość obciążona jest przesunięciem rozkładu (non-stationarity), którego rekonstrukcja przeszłości nie ujawnia w pełni.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor przeciwstawia się rozpowszechnionemu przekonaniu, że prognozowanie przyszłości jest fundamentalnie trudniejsze od modelowania danych historycznych z powodu braku ground truth. Twierdzi, że to 'actually easy', ponieważ ground truth dla przeszłości istnieje w formie temporalnie rozproszonej. Sporne pozostaje, czy rekonstrukcja pominiętych danych historycznych rzeczywiście uczy ekstrapolacji w warunkach niestacjonarności i zmiany reżimu — krytycy wskazują, że inter-/ekstrapolacja to nie to samo zadanie.

> **Cytat:** *"@hesipullfade @phl43 you have ground truth for those, just temporally disaggregated
this is actually easy. If it can learn to predict omitted historical data, it learns to predict future data"*

---

## Prompt Architecture / Inżynieria promptów

### Podejście rubryka + przykłady + bootstrap przy pracy z LLM

- **Data:** `Mon Sep 21 23:06:12 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102172573517701416)
- **Rodzaj:** Komentarz w dyskusji (@teortaxesTex)
- **Powiązane pojęcia:** [[Prompt Architecture]] [[Harness|Rubryki oceny]] [[Harness|Few-shot prompting]] [[Context Compaction|Bootstrap kontekstu]] [[Context Compaction|Inżynieria kontekstu]]

**Kontekst / Problem:**
Autor odpowiada na pytanie innego użytkownika, czy da się zrealizować jakieś zadanie przy pomocy modeli LLM (potocznie 'clankers'). Odpowiedź brzmi: tak, ale wymaga to dostarczenia modelowi rubryk oceny, przykładów oraz stopniowego prowadzenia przez proces (bootstrap). Autor zaznacza, że takie podejście jest czasochłonne ('slow going').

**Rada inżynierska:**
Aby skutecznie wymusić na modelu LLM wykonanie złożonego zadania, należy: (1) dostarczyć rubryki (jawne kryteria oceny/sukcesu), (2) podać przykłady wzorcowe (few-shot), (3) prowadzić model krok po kroku w trybie bootstrap, budując kontekst inkrementalnie. Nie jest to jednak szybka ścieżka — proces jest żmudny i wymaga iteracji.

**Uwaga / Anty-wzorzec:**
Oczekiwanie, że model samodzielnie wykona złożone zadanie bez rubryk, przykładów i stopniowego prowadzenia. Brak cierpliwości do iteracyjnego bootstrapu prowadzi do porzucenia podejścia mimo jego skuteczności.

> **Cytat:** *"btw the answer is "yes, with clankers damn it, you give them rubrics, examples, and bootstrap step by step" but it's a slow going"*

---

## Ewaluacja modeli i weryfikacja

### Brak ground truth blokuje rzetelną ocenę online; weryfikowalność domen kluczem do ewaluacji

- **Data:** `Mon Sep 21 23:05:13 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102172327232385279)
- **Rodzaj:** Komentarz w dyskusji (@phl43)
- **Powiązane pojęcia:** [[Eval Set z realnych sesji|Ground truth]] [[Harness|LLM-as-judge]] [[Harness|Ewaluacja modeli]] [[Harness|Weryfikacja formalna]] [[Harness|Lean]] [[Harness|Testy jednostkowe]] [[Stabilność modeli i przestrzeganie promptu|Benchmarking]]

**Kontekst / Problem:**
Dyskusja dotyczy oceny wyników modeli w zadaniach online/open-ended. Autor wskazuje, że próby naprawy problemu są punktowe i nie stanowią priorytetu, ponieważ brakuje ground truth. W domenach z automatyczną weryfikacją (testy kodu, natychmiastowe sprawdzanie obliczeń, Lean dla matematyki) ocena jest wykonalna; w zadaniach otwartych pozostaje problem, a użycie LLM jako sędziego („clankers”) jest wątpliwe.

**Rada inżynierska:**
Projektuj ewaluację w oparciu o weryfikowalne sygnały: testy jednostkowe, natychmiastowe sprawdzanie obliczeń, formalne dowody (Lean). Dla zadań bez ground truth nie używaj LLM-as-judge jako jedynego źródła prawdy; traktuj je jako heurystykę i jawnie oznaczaj niepewność oceny.

**Uwaga / Anty-wzorzec:**
Poleganie na LLM jako sędzim (LLM-as-judge) w zadaniach otwartych bez ground truth prowadzi do niezweryfikowanych, podatnych na halucynacje ocen. Brak ground truth uniemożliwia rzetelny scoring online i może maskować rzeczywiste błędy modelu.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor podważa powszechną praktykę używania LLM jako sędziów (LLM-as-judge) do oceny zadań otwartych, wskazując na brak ground truth i ryzyko niewiarygodnych ocen. Do rozstrzygnięcia: czy LLM-as-judge może być wystarczający przy braku weryfikowalnych sygnałów, czy konieczne są hybrydowe metody z formalną weryfikacją.

> **Cytat:** *"@phl43 There have been attempts to fix this in a targeted fashion, but yes, not a priority, and it's genuinely hard because you don't have ground truth. Literally how do you score online? With clankers? Coding has tests, calculation has instant checking, Lean makes math verifiable."*

---
