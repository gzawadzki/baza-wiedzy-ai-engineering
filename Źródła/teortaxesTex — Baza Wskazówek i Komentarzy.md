---
autor: "@teortaxesTex"
źródło: "https://x.com/teortaxesTex"
wygenerowano: "2026-09-23 02:25"
typ: synteza-wiedzy
tagi:
  - teortaxestex
  - ai-engineering
  - prompt-engineering
  - twitter-extract
---

# @teortaxesTex — Baza Wskazówek i Komentarzy

> Destylacja praktycznych porad, heurystyk inżynierskich i komentarzy technicznych z profilu @teortaxesTex na platformie X. Wyciągnięto 7 wartościowych wpisów.

## ⚠️ Kwestie sporne i rozbieżności do rozstrzygnięcia

> Wpisy, w których autor podważa powszechne przekonania branżowe lub prezentuje tezy stojące w sprzeczności z innymi praktykami:

- **[Kompresja treningowa redukuje znaczenie małego KV cache — długi kontekst staje się praktyczny](https://x.com/teortaxesTex/status/2102545198199038197):** Autor kwestionuje powszechny konsensus, że rozmiar KV cache / okna kontekstowego jest kluczowym ograniczeniem wymagającym agresywnej kompresji, przycinania czy RAG. Teza: dzięki kompresji na etapie treningu i niskiemu narzutowi pamięciowemu (~890 MB/1M tokenów) można pozwolić modelowi na ciągłe rozumowanie z zachowaniem wyjść. Do rozstrzygnięcia: czy podany współczynnik pamięciowy jest reprezentatywny dla realnych wdrożeń, oraz czy 'training compaction' faktycznie eliminuje potrzebę zarządzania kontekstem w produkcji.
- **[Rozumowanie latentne a efektywna głębokość szeregowa po RL i KV cache](https://x.com/teortaxesTex/status/2102523033499877448):** Autor podważa popularny pogląd, że modele autoregresyjne jedynie przewidują następny token. Twierdzi, że duże modele rozumujące po długim RL zachowują się bardziej forward-looking i przechowują częściowe obliczenia, zwiększając efektywną głębokość szeregową. Spór dotyczy tego, ile rozumowania pochodzi z treści tokenów, a ile z samej pojemności reprezentacji latentnej i KV cache.
- **[Logicznie ustrukturyzowany sygnał treningowy generalizuje rozumowanie, ale styl nie jest g-loaded](https://x.com/teortaxesTex/status/2102174532547080559):** Teza podważa dwa popularne przekonania branżowe: (1) że RL jest wąski i domenowo ograniczony — autor pokazuje szeroki transfer z matematyki/kodu na pisanie; (2) że wszystkie zdolności modelu są ze sobą skorelowane (jeden czynnik g) — autor twierdzi, że styl jest słabo g-loaded i nie transferuje razem z rozumowaniem. Do rozstrzygnięcia: czy obserwowany transfer R1 (math/coding RL → lepszy writer niż V3) wynika z generalizacji rozumowania, czy z efektów ubocznych treningu (np. zmiany dystrybucji, RLHF, długości CoT), które przypadkowo poprawiają styl.

---

## Spis kategorii

- [Inżynieria kontekstu / KV cache i pamięć](#inżynieria-kontekstu--kv-cache-i-pamięć) (1)
- [Architektura modeli / Trening](#architektura-modeli--trening) (1)
- [Architektura modeli / Rozumowanie](#architektura-modeli--rozumowanie) (1)
- [Architektura modeli / rozumowanie / Chain-of-Thought](#architektura-modeli--rozumowanie--chain-of-thought) (1)
- [Trening modeli / RL / Generalizacja zdolności](#trening-modeli--rl--generalizacja-zdolności) (1)
- [Inżynieria promptów / Systemy agentowe](#inżynieria-promptów--systemy-agentowe) (1)
- [Benchmarking i weryfikacja / sygnały treningowe](#benchmarking-i-weryfikacja--sygnały-treningowe) (1)

---

## Inżynieria kontekstu / KV cache i pamięć

### Kompresja treningowa redukuje znaczenie małego KV cache — długi kontekst staje się praktyczny

- **Data:** `Tue Sep 22 23:46:53 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102545198199038197)
- **Rodzaj:** Komentarz w dyskusji (@awesome_ruler_)
- **Powiązane pojęcia:** [[Architektura KV Cache i Rozumowanie Latentne|KV cache]] [[Context Compaction|Kompresja kontekstu / training compaction]] [[Context Compaction|Inżynieria kontekstu]] [[Context Compaction|Długi kontekst]] [[Harness|Chain-of-thought]] [[Harness|Zarządzanie pamięcią modelu]]

**Kontekst / Problem:**
Dyskusja w wątku o zarządzaniu kontekstem i pamięcią cache w modelach LLM. Autor odpowiada na argument, że mniejszy cache jest kluczowy, i twierdzi, że dzięki postępom w kompresji na etapie treningu (training compaction) oraz niskiemu narzutowi pamięciowemu (~890 MB na 1M tokenów kontekstu) agresywna optymalizacja rozmiaru cache przestaje być wąskim gardłem — model może po prostu kontynuować rozumowanie wraz z wyjściami.

**Rada inżynierska:**
Nie optymalizuj przedwcześnie rozmiaru KV cache ani nie sięgaj od razu po agresywne strategie przycinania/kompresji kontekstu. Wraz z dojrzewaniem technik kompresji treningowej narzut pamięciowy kontekstu spada (ok. 890 MB / 1M tokenów), więc bardziej opłacalne bywa utrzymywanie długiego, ciągłego rozumowania z zachowaniem wyjść (chain-of-thought + outputs) niż walka o każdy bajt cache. Projektuj harness tak, by pozwalał modelowi 'po prostu dalej rozumować', zamiast forsować radykalne skracanie kontekstu.

**Uwaga / Anty-wzorzec:**
Traktowanie rozmiaru cache jako nadrzędnego ograniczenia i wymuszanie agresywnej kompresji/RAG-owego przycinania kontekstu, gdy model i tak poradziłby sobie z dłuższym kontekstem dzięki lepszej kompresji treningowej — prowadzi to do utraty informacji i gorszego rozumowania bez realnej korzyści pamięciowej.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor kwestionuje powszechny konsensus, że rozmiar KV cache / okna kontekstowego jest kluczowym ograniczeniem wymagającym agresywnej kompresji, przycinania czy RAG. Teza: dzięki kompresji na etapie treningu i niskiemu narzutowi pamięciowemu (~890 MB/1M tokenów) można pozwolić modelowi na ciągłe rozumowanie z zachowaniem wyjść. Do rozstrzygnięcia: czy podany współczynnik pamięciowy jest reprezentatywny dla realnych wdrożeń, oraz czy 'training compaction' faktycznie eliminuje potrzebę zarządzania kontekstem w produkcji.

> **Cytat:** *"@awesome_ruler_ @industriaalist @jayden_teoh_ Well, smaller cache doesn't matter much now
we're starting to have good training compaction, and at 890 Mb/1M context, you can just keep reasoning with outputs"*

---

## Architektura modeli / Trening

### MTP to fałszywy trop — efektywna głębokość obwodu jest kluczowa

- **Data:** `Tue Sep 22 22:59:28 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102533265265500175)
- **Rodzaj:** Komentarz w dyskusji (@rudzinskimaciej)
- **Powiązane pojęcia:** [[Architektura KV Cache i Rozumowanie Latentne|Multi-Token Prediction]] [[Harness|Effective Circuit Depth]] [[Harness|Look-ahead w aktywacjach]] [[Harness|Predykcja pojedynczego tokena]] [[Harness|Głębokość obwodu obliczeniowego]]

**Kontekst / Problem:**
Dyskusja dotyczy tego, czy wielotokenowa predykcja (Multi-Token Prediction, MTP) jest niezbędna, aby model wykazywał zdolność 'patrzenia w przyszłość' (look-ahead) w swoich aktywacjach. Autor argumentuje, że sam cel predykcji pojedynczego tokena wystarcza, by aktywacje już zawierały informację o przyszłych tokenach, a prawdziwym problemem inżynierskim jest efektywna głębokość obwodu obliczeniowego (effective circuit depth), a nie sam cel treningowy.

**Rada inżynierska:**
Nie zakładaj, że MTP (Multi-Token Prediction) jest konieczne do uzyskania zdolności look-ahead w aktywacjach. Cel predykcji pojedynczego tokena już wymusza na modelu kodowanie informacji o przyszłych tokenach w aktywacjach. Zamiast tego skup się na pomiarze i optymalizacji *efektywnej* głębokości obwodu (effective circuit depth) — czyli ile warstw obliczeń jest faktycznie wykorzystywanych do przetwarzania danego tokena. To jest właściwa metryka do analizy zdolności modelu do planowania i rozumowania.

**Uwaga / Anty-wzorzec:**
Traktowanie MTP jako głównego czynnika umożliwiającego modelowi 'patrzenie w przyszłość' — to fałszywy trop (red herring). Również mylenie nominalnej liczby warstw z efektywną głębokością obwodu, która może być znacznie mniejsza ze względu na rezydualne połączenia i równoległe ścieżki.

> **Cytat:** *"MTP is a red herring. Single token prediction objective is sufficient for activations to already "look ahead" my question is about *effective* circuit depth"*

---

## Architektura modeli / Rozumowanie

### Rozumowanie latentne a efektywna głębokość szeregowa po RL i KV cache

- **Data:** `Tue Sep 22 22:18:48 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102523033499877448)
- **Rodzaj:** Komentarz w dyskusji (@industriaalist)
- **Powiązane pojęcia:** [[Architektura KV Cache i Rozumowanie Latentne|KV cache]] [[Test-Time Compute i Reasoning Tokens|Latent reasoning]] [[Harness|Filler tokens]] [[Harness|Efektywna głębokość szeregowa]] [[Harness|Modele rozumujące]] [[Harness|Reinforcement Learning]] [[Harness|Chain-of-thought]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Transformer]]

**Kontekst / Problem:**
Dyskusja pod wpisem o tym, że większość rozumowania modelu może odbywać się w przestrzeni latentnej, lepiej niż w języku naturalnym. Autor zgadza się z tezą, ale pyta, jaka część tego efektu wynika wyłącznie ze skalowania reprezentacji latentnej przez KV cache, nawet po odjęciu wkładu znaczącej treści sekwencji. Przywołuje eksperymenty Astra ze skalowaniem filler tokenów. Twierdzi, że duże modele rozumujące po długim RL są bardziej wybiegające w przyszłość i przechowują częściowe obliczenia, które składają się na dłuższą efektywną głębokość szeregową forward passów o stałej głębokości.

**Rada inżynierska:**
W ewaluacji i projektowaniu harnessów rozdzielaj wkład znaczących tokenów od samej pojemności kontekstu: KV cache, filler tokeny i inne nośniki obliczeń latentnych mogą zwiększać efektywną głębokość szeregową modelu. Nie interpretuj modelu wyłącznie przez pryzmat predykcji następnego tokenu; po intensywnym RL model może odkładać częściowe obliczenia w reprezentacji latentnej, co przypomina forward-looking computation. Testuj ablacje: filler tokeny vs tokeny znaczące, długość kontekstu, obecność KV cache, oraz mierz wpływ na rozumowanie.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: redukowanie działania modelu do „to tylko przewidywanie następnego tokenu”. Ignorowanie latentnej pojemności KV cache, filler tokenów i RL-owego przechowywania częściowych obliczeń prowadzi do błędnych wniosków o skalowaniu, głębokości rozumowania i roli języka naturalnego w CoT.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Autor podważa popularny pogląd, że modele autoregresyjne jedynie przewidują następny token. Twierdzi, że duże modele rozumujące po długim RL zachowują się bardziej forward-looking i przechowują częściowe obliczenia, zwiększając efektywną głębokość szeregową. Spór dotyczy tego, ile rozumowania pochodzi z treści tokenów, a ile z samej pojemności reprezentacji latentnej i KV cache.

> **Cytat:** *"> most of the reasoning can be done in latent space (except like tool calls) and in fact, much better than in nat lang
Yes. no dispute. The issue: how much of that is afforded just by scaling the latent representation via KV cache, even modulo the meaningful sequence content? See Astra's scaling with filler tokens. Meaningful tokens, ofc, help more. I think there's a popular underestimation where "it just outputs the next token". I think large reasoning models after a lot of RL are more forward-looking, and basically store partial computations that add up to longer effective serial depth of fixed-depth forward passes. Does this make sense?"*

---

## Architektura modeli / rozumowanie / Chain-of-Thought

### Długość CoT a efektywna głębokość obwodu w modelach płytkich

- **Data:** `Tue Sep 22 21:54:16 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102516859874759155)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Chain-of-Thought]] [[Harness|Efektywna głębokość obliczeniowa]] [[Harness|Głębokość modelu vs rozumowanie]] [[Prompt Architecture|Kompresja promptu]] [[Harness|Agent harness]]

**Kontekst / Problem:**
Autor rozważa, że pewien efekt architektoniczny — prawdopodobnie korzyść z głębokości lub zdolności obliczeniowych — jest silny przy predykcji kolejnego tokenu na sekwencji N tokenów, ale mocno osłabiony przy rozumowaniu. Chce ustalić najlepszy możliwy związek między długością Chain-of-Thought a efektywną głębokością obwodu transformerowego. Podkreśla, że modele płytkie są znacznie tańsze, więc pytanie ma bezpośrednie znaczenie dla doboru modelu i projektowania harnessu.

**Rada inżynierska:**
Traktuj długość CoT jako przybliżenie dodatkowej głębokości obliczeniowej, ale nie zakładaj liniowej równoważności między liczbą kroków CoT a warstwami modelu. Przy kompilacji promptów i benchmarkingu porównuj koszt/jakość w układzie: płytki model + długi CoT versus głęboki model + krótki CoT. Dla zadań wymagających rozumowania efekt kompensacji może być znacznie słabszy niż dla predykcji kolejnego tokenu, więc waliduj empirycznie zamiast opierać się na intuicji.

**Uwaga / Anty-wzorzec:**
Optymistyczne założenie, że wydłużanie CoT w płytkim modelu w pełni skompensuje brak głębokości. Autor sugeruje, że efekt jest masywnie osłabiony dla rozumowania, co oznacza, że tani model płytki z długim CoT może nie dorównać głębszemu modelowi w zadaniach reasoningowych.

> **Cytat:** *"I strongly suspect that this effect is powerful for next token prediction over N tokens, but massively attenuated for reasoning. What I want to know is the best-case relation between CoT length and effective circuit depth. And given how much cheaper shallow models are… https://t.co/alkoyPXIME"*

---

## Trening modeli / RL / Generalizacja zdolności

### Logicznie ustrukturyzowany sygnał treningowy generalizuje rozumowanie, ale styl nie jest g-loaded

- **Data:** `Mon Sep 21 23:13:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102174532547080559)
- **Rodzaj:** Komentarz w dyskusji (@phl43)
- **Powiązane pojęcia:** [[Harness|Generalizacja rozumowania]] [[Harness|g-loaded capabilities]] [[Harness|RL na kodzie i matematyce]] [[Harness|Transfer umiejętności w LLM]] [[Harness|Pretraining sygnał]] [[Harness|DeepSeek R1]] [[Harness|Styl vs rozumowanie]]

**Kontekst / Problem:**
Dyskusja o tym, jak rodzaj sygnału treningowego wpływa na transfer umiejętności między domenami. Autor odpowiada na tezę, że trening w jednej domenie nie poprawia ogólnych zdolności modelu, argumentując empirycznie, że logicznie ustrukturyzowane sygnały (kod, matematyka) generalizują rozumowanie na niemal wszystkie zadania.

**Rada inżynierska:**
Traktuj kod i matematykę jako uniwersalny nośnik sygnału rozumowania: (1) pretraining na kodzie podnosi wyniki niemal na wszystkich zadaniach, (2) RL na matematyce i kodzie (np. DeepSeek R1) czyni model znacznie lepszym także w zadaniach niewymagających logiki, np. w pisaniu (R1 > V3 jako writer). Wniosek inżynierski: inwestuj w logicznie ustrukturyzowany sygnał treningowy, bo transferuje szerzej niż sygnał stylistyczny. Jednocześnie nie zakładaj transferu cech stylistycznych — styl nie koreluje silnie z ogólną inteligencją (g), więc nie licz na to, że trening rozumowania poprawi jakość prozy czy formatowania i odwrotnie.

**Uwaga / Anty-wzorzec:**
Błąd projektowy: oczekiwanie, że poprawa jednego wymiaru (rozumowanie z RL na kodzie/matmie) automatycznie podniesie wszystkie wymiary, w tym styl. Styl okazuje się słabo 'g-loaded' — nie transferuje się razem z logiką. Odwrotnie, trening wyłącznie na zadaniach stylistycznych nie uogólni rozumowania. Nie mieszaj tych dwóch osi w jednym punkcie pomiaru.

**⚡ Kwestia sporna / do rozstrzygnięcia:**
Teza podważa dwa popularne przekonania branżowe: (1) że RL jest wąski i domenowo ograniczony — autor pokazuje szeroki transfer z matematyki/kodu na pisanie; (2) że wszystkie zdolności modelu są ze sobą skorelowane (jeden czynnik g) — autor twierdzi, że styl jest słabo g-loaded i nie transferuje razem z rozumowaniem. Do rozstrzygnięcia: czy obserwowany transfer R1 (math/coding RL → lepszy writer niż V3) wynika z generalizacji rozumowania, czy z efektów ubocznych treningu (np. zmiany dystrybucji, RLHF, długości CoT), które przypadkowo poprawiają styl.

> **Cytat:** *"@phl43 We see that logically structured training signal (both in pretraining and in RL) generalizes reasoning. First models pretrained on coding got better at ≈all tasks, R1 was RL'd for mafs&coding and became a vastly better writer than V3. but style, it seems, is not very g-loaded"*

---

## Inżynieria promptów / Systemy agentowe

### Praca z agentami LLM: rubryki, przykłady i stopniowy bootstrap

- **Data:** `Mon Sep 21 23:06:12 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102172573517701416)
- **Rodzaj:** Komentarz w dyskusji (@teortaxesTex)
- **Powiązane pojęcia:** [[Prompt Architecture|Prompt Engineering]] [[Harness|Agent harness]] [[Harness|Rubryki oceny]] [[Harness|Bootstrap agenta]] [[Context Compaction|Inżynieria kontekstu]]

**Kontekst / Problem:**
Odpowiedź na pytanie innego użytkownika, czy modele/agenci LLM (slangowo 'clankers') nadają się do wykonania jakiegoś zadania. Autor potwierdza, że tak, ale wymaga to dostarczenia rubryk oceny, przykładów oraz stopniowego bootstrapowania, a cały proces jest powolny.

**Rada inżynierska:**
Przy pracy z agentami LLM dostarczaj im jawne rubryki oceny, konkretne przykłady oraz prowadź je krok po kroku przez bootstrap zadania. Nie oczekuj, że模型 samodzielnie odgadnie kryteria sukcesu — inżynieria kontekstu i stopniowe wprowadzanie są kluczowe, choć spowalniają pracę.

**Uwaga / Anty-wzorzec:**
Brak rubryk, przykładów i stopniowego bootstrapu prowadzi do nieefektywnej pracy agenta; jednocześnie założenie, że proces będzie szybki, jest błędne — to żmudne i powolne zajęcie.

> **Cytat:** *"@phl43 btw the answer is "yes, with clankers damn it, you give them rubrics, examples, and bootstrap step by step"
but it's a slow going"*

---

## Benchmarking i weryfikacja / sygnały treningowe

### Brak ground truth jako bariera scoringu: weryfikowalność domeny decyduje o możliwości treningu

- **Data:** `Mon Sep 21 23:05:13 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102172327232385279)
- **Rodzaj:** Komentarz w dyskusji (@phl43)
- **Powiązane pojęcia:** [[Eval Set z realnych sesji|Ground truth]] [[Harness|Weryfikowalne nagrody (verifiable rewards)]] [[Harness|LLM-as-a-Judge]] [[Harness|Reward hacking]] [[Weryfikator|Lean jako weryfikator dowodów]] [[Harness|Testy jednostkowe jako sygnał treningowy]] [[Weryfikator|Zewnętrzny weryfikator]]

**Kontekst / Problem:**
Dyskusja dotyczy oceniania (scoringu) wyników modeli w domenach otwartych, gdzie nie istnieje obiektywna prawda odniesienia (ground truth). Autor zestawia domeny łatwo weryfikowalne — kod (testy), obliczenia (natychmiastowe sprawdzenie wyniku), matematyka (Lean czyni dowody weryfikowalnymi) — z domenami, w których scoring jest fundamentalnie trudny. Odpowiedź sugeruje, że podejmowano punktowe próby naprawy tego problemu, ale nie są one priorytetem, bo sam problem jest trudny z natury, a nie z braku wysiłku.

**Rada inżynierska:**
Traktuj weryfikowalność domeny jako pierwszorzędne kryterium przy projektowaniu pętli treningowych i benchmarków: buduj sygnały nagrody tam, gdzie istnieje tani, deterministyczny i niezależny od modelu weryfikator (testy jednostkowe, sprawdzarka wyniku liczbowego, kompilator/Lean). W domenach bez ground truth nie da się 'naprawić' scoringu inżynierią promptu — brak prawdy odniesienia jest ograniczeniem strukturalnym, więc albo znajdź zewnętrzny, deterministyczny weryfikator, albo świadomie zaakceptuj niższą wiarygodność sygnału.

**Uwaga / Anty-wzorzec:**
Ocenianie domen bez ground truth przy pomocy innych modeli ('clankers', LLM-as-a-Judge) jako substytutu prawdy odniesienia — prowadzi do zapętlenia oceny w modelu oceniającym, niespójnych sygnałów między uruchomieniami i podatności na reward hacking. Próby 'punktowej naprawy' takiego scoringu nie skalują się, bo brakuje niezależnego, obiektywnego punktu odniesienia.

> **Cytat:** *"There have been attempts to fix this in a targeted fashion, but yes, not a priority, and it's genuinely hard because you don't have ground truth. Literally how do you score online? With clankers? Coding has tests, calculation has instant checking, Lean makes math verifiable."*

---
