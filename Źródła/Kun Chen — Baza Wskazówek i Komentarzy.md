---
autor: Kun Chen (@kunchenguid)
źródło: "https://x.com/kunchenguid"
wygenerowano: 2026-09-23 01:47
typ: synteza-wiedzy
tagi:
  - kun-chen
  - ai-engineering
  - prompt-engineering
  - twitter-extract
---

# Kun Chen (@kunchenguid) — Baza Wskazówek i Komentarzy

> Destylacja praktycznych porad, heurystyk inżynierskich i komentarzy technicznych Kuna Chena z Twittera/X. Wyciągnięto 32 wartościowych wpisów.

## Spis kategorii

- [Eval / Zarządzanie zasobami](#eval--zarządzanie-zasobami) (1)
- [Ekonomia agentów / koszt kontekstu](#ekonomia-agentów--koszt-kontekstu) (1)
- [Architektura harnessu / Routing modeli](#architektura-harnessu--routing-modeli) (1)
- [Architektura systemów agentowych / Zarządzanie kosztami](#architektura-systemów-agentowych--zarządzanie-kosztami) (1)
- [Architektura systemów AI / Routing i orkiestracja](#architektura-systemów-ai--routing-i-orkiestracja) (1)
- [Ewaluacja agentów / Architektura orkiestracji](#ewaluacja-agentów--architektura-orkiestracji) (1)
- [Harness / Narzędzia i konfiguracja](#harness--narzędzia-i-konfiguracja) (1)
- [Harnessy i weryfikacja krokowa](#harnessy-i-weryfikacja-krokowa) (1)
- [Weryfikacja / Proces inżynierski](#weryfikacja--proces-inżynierski) (1)
- [Wybór harnessu / routing modeli](#wybór-harnessu--routing-modeli) (1)
- [Obserwacje zachowania modeli / Ewaluacja modeli](#obserwacje-zachowania-modeli--ewaluacja-modeli) (1)
- [Architektura systemów / Wybór modelu (LLM vs klasyczne ML)](#architektura-systemów--wybór-modelu-(llm-vs-klasyczne-ml)) (1)
- [Weryfikacja / Agent Harness](#weryfikacja--agent-harness) (1)
- [Orkiestracja agentów / Architektura kontekstu](#orkiestracja-agentów--architektura-kontekstu) (1)
- [Architektura harnessa / Routing i selekcja modeli](#architektura-harnessa--routing-i-selekcja-modeli) (1)
- [Architektura systemów agentowych / Optymalizacja kosztów](#architektura-systemów-agentowych--optymalizacja-kosztów) (1)
- [Paradygmaty budowania oprogramowania z AI](#paradygmaty-budowania-oprogramowania-z-ai) (1)
- [Architektura agentów / Orkiestracja i optymalizacja kosztów](#architektura-agentów--orkiestracja-i-optymalizacja-kosztów) (1)
- [Architektura narzędzi agenta (tool design / harness)](#architektura-narzędzi-agenta-(tool-design--harness)) (1)
- [Harness / Ekosystem narzędzi i strategia vendorowa](#harness--ekosystem-narzędzi-i-strategia-vendorowa) (1)
- [Ewaluacja i wybór modeli](#ewaluacja-i-wybór-modeli) (1)
- [Wybór modelu / debugowanie agentowe](#wybór-modelu--debugowanie-agentowe) (1)
- [Architektura agentów / Orkiestracja](#architektura-agentów--orkiestracja) (1)
- [Harness i zarządzanie kontekstem / koszty](#harness-i-zarządzanie-kontekstem--koszty) (1)
- [Zarządzanie kontekstem / Harness](#zarządzanie-kontekstem--harness) (1)
- [Zarządzanie kontekstem i kosztami](#zarządzanie-kontekstem-i-kosztami) (1)
- [Zarządzanie kontekstem / ewolucja praktyk inżynierskich](#zarządzanie-kontekstem--ewolucja-praktyk-inżynierskich) (1)
- [Zarządzanie kontekstem / Harness agentowy](#zarządzanie-kontekstem--harness-agentowy) (1)
- [Inne obserwacje](#inne-obserwacje) (1)
- [Zarządzanie kontekstem / Harnessy agentowe / Ewaluacja promptów](#zarządzanie-kontekstem--harnessy-agentowe--ewaluacja-promptów) (1)
- [Prompt Caching / Zarządzanie kontekstem](#prompt-caching--zarządzanie-kontekstem) (1)
- [Zarządzanie kontekstem / Compaction w harnessie agenta](#zarządzanie-kontekstem--compaction-w-harnessie-agenta) (1)

---

## Eval / Zarządzanie zasobami

### Ekstrapolacja zużycia kwot z próbki 5% zamiast pełnego przebiegu eval

- **Data:** `Wed Sep 16 20:38:57 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100323574791962644)
- **Rodzaj:** Komentarz w dyskusji (@EthanClinick)
- **Powiązane pojęcia:** [[Harness|Eval]] [[Harness|Zarządzanie quota]] [[Harness|Próbkowanie i ekstrapolacja]] [[TypeSafe — przewodnik praktyczny|Koszt tokenów]]

**Kontekst / Problem:**
Kun Chen odpowiada @EthanClinick w dyskusji o tym, jak mierzyć, ile pełny zestaw eval-i pochłonąłby z tygodniowego quota (limitu tokenów/requestów). Problem: uruchamianie kompletnego evala na 100% budżetu jest kosztowne i niepotrzebne. Rozwiązanie: uruchom eval tylko na 5% tygodniowego quota, zmierz rzeczywiste zużycie tokenów z tej próbki, a następnie przeskaluj liniowo do 100%. Tym samym szacujesz obciążenie produkcyjne bez konieczności wykonywania pełnego przebiegu.

**Rada inżynierska:**
Do szacowania pełnego obciążenia evalem nie uruchamiaj 100% zakresu — wystarczy reprezentatywna próbka (np. 5% tygodniowego quota). Zmierz rzeczywiste zużycie tokenów na próbce i przeskaluj proporcjonalnie, żeby wyliczyć prognozę dla pełnego przebiegu. Oszczędza to kwotę i czas, a wciąż daje praktyczną estymację budżetu.

**Uwaga / Anty-wzorzec:**
Mylenie 'przebiegu evala' z 'przebiegiem pełnego quota' — zakładanie, że trzeba realnie zużyć 100% budżetu, żeby zmierzyć, ile on wynosi. To prowadzi do marnowania kwoty i spowalnia iterację nad evalem.

> **Cytat:** *"@EthanClinick the eval runs through 5 whole % of my weekly quota and count the token value from those runs to calculate what 100% would be. it doesn't need to actually run through 100% of it :)"*

---

## Ekonomia agentów / koszt kontekstu

### Koszt agenta jako koszt zatrudnienia CTO — model mentalny uzasadniający zużycie tokenów

- **Data:** `Wed Sep 16 16:36:05 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100262459282239910)
- **Rodzaj:** Komentarz w dyskusji (@anab7bmessi1)
- **Powiązane pojęcia:** [[Harness|Ekonomia agentów AI]] [[TypeSafe — przewodnik praktyczny|Koszt tokenów a zwrot z pracy inżynierskiej]] [[Harness|Skalowanie projektu a delegacja do agenta]] [[Harness|Model mentalny agent jako współpracownik]] [[Harness|Harness inżynierski]]

**Kontekst / Problem:**
Kun Chen odpowiada użytkownikowi @anab7bmessi1, który najprawdopodobniej zwrócił uwagę, że używanie agenta (np. harnessu do kodowania) wiąże się z realnym kosztem — zużyciem tokenów, czasu, a być może też narzutem poznawczym. Brak treści posta nadrzędnego, więc kontekst odtwarzany z samej odpowiedzi: toczy się dyskusja o tym, czy wysoki koszt pracy agenta jest akceptowalny. Kun nie neguje kosztu — potwierdza go wprost — ale przenosi rozmowę z poziomu 'ile to kosztuje' na poziom 'jaka wartość jest za to kupowana'.

**Rada inżynierska:**
Traktuj agenta AI nie jak darmowe narzędzie, ale jak zatrudnienie CTO: koszt jest realny i nieunikniony, ale staje się opłacalny powyżej pewnego progu skali projektu. Praktyczna reguła: nie optymalizuj zużycia tokenów w izolacji — licz je jako inwestycję w redukcję pracy, którą w przeciwnym razie musiałbyś wykonać samodzielnie (czytanie kodu, research, refaktoryzacja, pisanie boilerplate'u). Jeśli dana iteracja agenta oszczędza Ci realne godziny pracy inżynierskiej, jej koszt jest uzasadniony; jeśli nie — to nie jest problem kosztu tokenów, tylko źle dobranego zadania dla agenta.

**Uwaga / Anty-wzorzec:**
Dwie skrajności, które Kun implicitnie koryguje: (1) oczekiwanie, że agent będzie bez kosztów — prowadzi do rezygnacji z agenta dokładnie wtedy, gdy projekt wchodzi w fazę, w której najbardziej by pomógł; (2) patrzenie wyłącznie na metrykę 'ile tokenów spalił' bez równoległego liczenia 'ile pracy ludzkiej zastąpił', co skutkuje mikro-optymalizacją promptów kosztem jakości wyniku.

> **Cytat:** *"@anab7bmessi1 yes there is absolutely a cost associated

the mental model is that you are hiring a CTO - it’s not free but it’s necessary to help you scale beyond a certain point

most of the tokens it uses are used to reduce work that you would otherwise have to do yourself"*

---

## Architektura harnessu / Routing modeli

### Kwantyfikacja pewności modelu jako trigger do eskalacji na cięższy panel LLM

- **Data:** `Wed Sep 16 05:13:05 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100090575106310498)
- **Rodzaj:** Komentarz w dyskusji (@nicknow)
- **Powiązane pojęcia:** [[Jev|Confidence-based routing]] [[Harness|LLM escalation panel]] [[Harness|Model efficiency vs capability]] [[Harness|Model confidence quantification]] [[Harness|Harness architecture]] [[Harness|Cost-aware inference]]

**Kontekst / Problem:**
Kun Chen odpowiada @nicknow w dyskusji o nowym modelu (oceniając jego możliwości). Twierdzi, że trudno wyobrazić sobie, by model radził sobie znacząco lepiej niż poprzednie — nawet własne eval producenta wskazują, że główna poprawa dotyczy efektywności, a nie realnego wzrostu jakości rozumowania. Zamiast więc liczyć na 'lepszy model', Kun wskazuje inną wartość: zdolność modelu do kwantyfikowania własnej pewności (confidence). To pozwala zaprojektować harness, który tanie/z lekkim modelem obsługuje sprawy pewne, a przy niskiej pewności eskaluje zadanie do droższego, cięższego panelu LLM.

**Rada inżynierska:**
Nie opieraj architektury na założeniu, że kolejny model będzie fundamentalnie mądrzejszy — traktuj wzrosty jako głównie efektywnościowe. Buduj harness warstwowo: używaj sygnału confidence z modelu jako bramki routingu. Jeśli wynik ma niską pewność, przekieruj zadanie do cięższego, wielomodelowego panelu (LLM-powered panel), a jeśli pewność jest wysoka — zaakceptuj tani wynik bez eskalacji. Dzięki temu płacisz za drogie rozumowanie tylko tam, gdzie naprawdę trzeba.

**Uwaga / Anty-wzorzec:**
Oczekiwanie, że sam upgrade modelu rozwiąże problemy produkcyjne. Jeśli eval producenta pokazuje poprawę głównie w efektywności (koszt/latencja), a nie w jakości, to wymiana modelu bez zmiany architektury harnessu nie przyniesie istotnego zysku — trzeba raczej zaprojektować warunkową eskalację opartą na confidence.

> **Cytat:** *"@nicknow it’s hard to imagine it doing better - their own evals also indicate it’s mostly about efficiency

but i like its ability to quantify confidence - i can easily build a system that says “if the result is not confident then let’s run a heavier LLM powered panel”"*

---

## Architektura systemów agentowych / Zarządzanie kosztami

### Tania orkiestracja + eskalacja niejednoznacznych decyzji do modelu top-tier

- **Data:** `Wed Sep 16 05:09:51 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100089760475930830)
- **Rodzaj:** Komentarz w dyskusji (@Steve_Yegge)
- **Powiązane pojęcia:** [[Harness|Multi-agent orchestration]] [[Jev|Model routing]] [[Harness|Cost optimization]] [[Harness|Model escalation]] [[Harness|Task decomposition]] [[Harness|Cheap model for orchestration]]

**Kontekst / Problem:**
Odpowiedź pod wpisem @Steve_Yegge, dotycząca praktyk pracy z systemami multi-agentowymi (odniesienie do 'firstmate' — agenta orkiestrującego). Kun dzieli się obserwacją z miesięcy pracy: systemy agentowe tracą rentowność, gdy wszystkie kroki — w tym rutynową orkiestrację ('task 1 się skończył, uruchom task 2') — wykonuje najdroższy, najmocniejszy model. Rozwiązaniem jest hierarchia modeli: tani model do routingu/orkiestracji, mocny model tylko do decyzji wymagających 'fable level wisdom'.

**Rada inżynierska:**
Rozdziel role według kosztu i trudności: orkiestrację, routowanie i sekwencjonowanie zadań (np. 'zadanie 1 gotowe → odpal zadanie 2') deleguj do taniego modelu, natomiast model top-tier (fable) rezerwuj wyłącznie dla decyzji niejednoznacznych i wymagających głębokiego rozumowania. Kluczowy element: prompt taniego modelu musi być silnie sterowany (heavily steer) tak, aby sam rozpoznawał granice swojej kompetencji i eskalował w górę. Ta eskalacja świadomie ograniczona do przypadków niejednoznacznych daje dużą poprawę jakości systemu bez psucia ogólnej jakości ani budżetu.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: używanie modeli top-tier ('fable tier') do rutynowych zadań orkiestracyjnych, które nie wymagają zaawansowanego rozumowania — to główne źródło niekontrolowanych kosztów w systemach agentowych. Drugą pułapką jest eskalacja wszystkiego (brak selektywności) — eskalować należy tylko decyzje niejednoznaczne.

> **Cytat:** *"having been working with my firstmate for months, i learned one of the biggest traps is that we may put fable tier models on many mundane orchestration-ish tasks (like "oh task 1 finished let me kick off task 2") that really don't need fable level wisdom. that's what makes the cost untenable

i'm having great success with using a cheap model for orchestration and heavily steer it to escalate ambiguous decisions to fable, which makes a surprisingly big difference without compromising the overall quality of the system"*

---

## Architektura systemów AI / Routing i orkiestracja

### Model routing i deterministyczne komponenty zamiast „LLM do wszystkiego”

- **Data:** `Wed Sep 16 02:41:33 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100052440343294172)
- **Rodzaj:** Komentarz w dyskusji (@EthanSDE)
- **Powiązane pojęcia:** [[Jev|Model routing]] [[Harness|Escalation judgment]] [[Code Review|Triage code review]] [[Firstmate Agent|Deterministyczna orkiestracja]] [[Harness|Zużycie tokenów]] [[TypeSafe — przewodnik praktyczny|Latencja agenta]]

**Kontekst / Problem:**
Kun Chen odpowiada @EthanSDE, potwierdzając („yes! many many examples”), że istnieje wiele miejsc w systemach agentowych, gdzie nie trzeba używać LLM. Wymienia konkretne przypadki: routing modeli (model routing), ocena konieczności eskalacji (escalation judgment) oraz triage wyników code review. Kontekst: dyskusja o tym, które elementy harnessu/agenta powinny być deterministyczne, a które oparte na modelu.

**Rada inżynierska:**
Nie wkładaj LLM w każdy krok pipeline'u. Routing między modelami, decyzja o eskalacji do mocniejszego modelu/człowieka oraz triage znalezisk z code review mogą być realizowane regułowo lub deterministycznie — to tańsze i szybsze. Traktuj LLM jako jeden z komponentów orkiestracji, nie jako domyślny mechanizm dla wszystkich decyzji.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec „LLM for everything” — używanie modelu nawet do trywialnych decyzji klasyfikacyjnych/routingowych, co drastycznie pali tokeny i wprowadza ogromne opóźnienia („burns tokens and is super slow”), czyniąc system niepraktycznym w produkcji.

> **Cytat:** *"yes! many many examples - model routing, escalation judgment, triaging code review findings etc etc

right now it’s LLM for everything which burns tokens and is super slow"*

---

## Ewaluacja agentów / Architektura orkiestracji

### Ewaluacja systemów agentowych przez outcome i wskaźnik rework, nie przez jakość promptu

- **Data:** `Tue Sep 22 07:10:43 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102294506062385364)
- **Rodzaj:** Komentarz w dyskusji (@kryptm4n)
- **Powiązane pojęcia:** [[Firstmate Agent|Orkiestracja agentów]] [[Firstmate Agent|Firstmate]] [[Harness|Ewaluacja przez outcome]] [[Rework Rate|Wskaźnik reworku]] [[Firstmate i Agenci Wykonawczy|Leaf node agent]] [[Harness|Skalowalność vs kontrola]] [[Harness|Misalignment agentów]]

**Kontekst / Problem:**
Kun Chen odpowiada @kryptm4n, który prawdopodobnie zapytał o porównanie jakości promptów pisanych ręcznie (bezpośrednio do agenta-liścia) z promptami generowanymi automatycznie przez 'firstmate' (jego system orkiestracji agentów). Problem: jak zmierzyć, czy automatycznie tworzone prompty są równie dobre jak te pisane przez człowieka.

**Rada inżynierska:**
Nie da się rzetelnie porównać jakości promptu pisanego iteracyjnie z człowiekiem do jednorazowego promptu wygenerowanego przez system orkiestracji (firstmate), bo to nie są porównywalne artefakty — rozmowa z agentem-liściem to seria drobnych promptów z bieżącym sterowaniem, a nie jeden 'pełny wymóg'. Zamiast tego ewaluuj OUTCOME i częstość reworku (ile razy trzeba wracać i poprawiać). Praktyczna reguła: mierz skalowalność i koszt korekty, nie elegancję promptu. Świadomy tradeoff: bezpośrednie sterowanie agentem-liściem = lepsza kontrola i szybszy rezultat, ale nie skaluje się (pożera czas); orkiestracja (firstmate) = skaluje się, ale sporadycznie generuje misalignment wymagający późniejszej korekty. To ten sam tradeoff co zarządzanie dużą organizacją ludzką vs robienie wszystkiego samemu.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: ocenianie systemu orkiestracji agentów przez pryzmat 'jakości promptu' — prowadzi to do porównywania nieporównywalnych rzeczy (iteracyjna rozmowa vs jednorazowy wygenerowany prompt) i daje mylące wnioski. Drugi anty-wzorzec: brak kwantyfikacji wskaźnika reworku, przez co decyzja 'ręcznie vs orkiestracja' opiera się wyłącznie na wrażeniach jakościowych.

> **Cytat:** *"this is a very good question and i have not done a dedicated evaluation on just the quality of the prompts

it's tricky because when i talk directly to a leaf node agent i don't attempt to write a full requirement upfront and expect autonomous execution. i typically end up doing it a lot more iteratively, so often times i don't have a single "prompt" that's comparable to what firstmate would write

i think what's more practical is to evaluate the outcome, and how often rework happens. i haven't quantified this but it's a good thing to look into. qualitatively i definitely think whenever i directly talk to a leaf node agent i can steer it more closely and get better results faster - but i end up spending a lot of time and it doesn't scale. firstmate helps me scale but occasionally there will be misalignment and needs correction later on. much like the tradeoff between managing a large human organization vs doing everything myself"*

---

## Harness / Narzędzia i konfiguracja

### Ograniczenia klientów przy podłączaniu własnego harnessu (Cursor vs SuperGrok)

- **Data:** `Tue Sep 22 03:40:58 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102241720826204224)
- **Rodzaj:** Komentarz w dyskusji (@tanishqk)
- **Powiązane pojęcia:** [[Harness]] [[Harness|Third-party harness]] [[Harness|Cursor]] [[Stabilność modeli i przestrzeganie promptu|SuperGrok]] [[Harness|Wybór dostawcy modelu]]

**Kontekst / Problem:**
Kun Chen odpowiada @tanishqk w wątku o używaniu własnego (zewnętrznego) harnessu wokół modeli. Wskazuje praktyczne ograniczenie: klient Cursor nie pozwala na podłączenie trzeciej strony / własnego harnessu (3p harness), natomiast subskrypcje SuperGrok na to pozwalają — sam używa własnego harnessu właśnie przez subskrypcję SuperGrok.

**Rada inżynierska:**
Dobór klienta/subskrypcji jest decyzją architektoniczną, nie tylko kosztową: jeśli chcesz uruchamiać własny harness (własne pętle agentowe, zewnętrzni weryfikatorzy, kontrola nad prompt architecture), wybierz dostawcę, który nie blokuje third-party harnessu. Cursor tego nie umożliwia, a subskrypcje SuperGrok tak — Kun realnie korzysta z tego drugiego kanału.

**Uwaga / Anty-wzorzec:**
Zakładanie, że dowolny popularny klient IDE/agent (np. Cursor) pozwoli podłączyć własny harness lub zewnętrzny model pod własną pętlą — ograniczenia licencyjne i klienckie mogą to uniemożliwić i zablokować całą strategię harnessu po fakcie.

> **Cytat:** *"@tanishqk cursor doesn't allow 3p harness but supergrok subs do. i'm using through my supergrok"*

---

## Harnessy i weryfikacja krokowa

### Per-repo polityka jakości w harnessie Firstmate: brak-mistakes vs no-mistakes

- **Data:** `Tue Sep 22 03:32:12 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102239513980608520)
- **Rodzaj:** Komentarz w dyskusji (@kunchenguid)
- **Powiązane pojęcia:** [[Harness]] [[Weryfikacja krokowa]] [[Weryfikator|Zewnętrzny weryfikator]] [[Harness|Quality gates per-repo]] [[Harness|Polityka jakości agentów]] [[Firstmate Agent|Firstmate]]

**Kontekst / Problem:**
Kun Chen odpowiada @EthanClinick w wątku o narzędziu 'Firstmate' (harness/agent sterujący pracą w wielu repozytoriach). Ethan prawdopodobnie pytał, czy da się zróżnicować poziom rygoru weryfikacji między repo (np. część repo wymaga pełnej weryfikacji 'no-mistakes', część nie). Kun wyjaśnia, że Firstmate pozwala zadeklarować per-repo, które repozytoria mają podlegać trybowi 'no-mistakes', a które nie — i że harness sam potrafi skonfigurować te reguły za użytkownika.

**Rada inżynierska:**
Traktuj politykę jakości jako konfigurację per-repository, nie globalną. W praktyce: część repozytoriów (np. produkcyjne, krytyczne, o wysokim koszcie błędu) powinna działać w trybie 'no-mistakes' — czyli agent musi przejść rygorystyczną, zewnętrzną weryfikację każdego kroku, zanim zmiana zostanie uznana za gotową. Inne repo (prototypy, sandboxy, kod jednorazowy) mogą działać w lżejszym trybie, żeby nie marnować tokenów i czasu na weryfikację tam, gdzie błąd jest tani. Kluczowe: pozwól harnessowi generować i utrzymywać te reguły automatycznie (self-setup), zamiast ręcznie utrzymywać listy w konfiguracji — ręczne listy się rozjeżdżają wraz ze zmianami w repo i zespołu.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: jedna, globalna polityka weryfikacji dla wszystkich repozytoriów. Albo wymuszasz 'no-mistakes' wszędzie (marnujesz czas i budżet na repo, gdzie to nie jest potrzebne), albo nigdzie (wypuszczasz niezweryfikowane zmiany w krytycznych repo). Drugi anty-wzorzec: ręczne, hardkodowane listy repo wymagających weryfikacji — szybko stają się nieaktualne, gdy pojawiają się nowe repo lub zmienia się ich krytyczność.

> **Cytat:** *"@EthanClinick in firstmate, you can also tell firstmate which repos need no-mistakes vs not. it can setup the rules for you"*

---

## Weryfikacja / Proces inżynierski

### Kiedy stosować rygorystyczną weryfikację: test "czy poprosiłbym człowieka o code review?"

- **Data:** `Tue Sep 22 03:31:40 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102239379536433551)
- **Rodzaj:** Komentarz w dyskusji (@EthanClinick)
- **Powiązane pojęcia:** [[Weryfikacja krokowa]] [[Harness|Harness inżynierski]] [[Weryfikator|Zewnętrzny weryfikator]] [[Code Review|Code review]] [[Harness|Selektywna weryfikacja zmian]]

**Kontekst / Problem:**
Kun Chen odpowiada @EthanClinick, który najwyraźniej sugerował, że każdej zmianie w kodzie należy poddawać rygorystyczny proces weryfikacji (prawdopodobnie narzędzie/harness "no-mistakes"). Kun prostuje to założenie: nie każda zmiana wymaga pełnej, kosztownej weryfikacji. Wprowadza prostą heurystykę decyzyjną opartą na analogii do ludzkiego procesu code review, aby uniknąć nadmiernego narzutu na trywialne zmiany.

**Rada inżynierska:**
Przed uruchomieniem kosztownego procesu weryfikacji (harness, zewnętrzny weryfikator, agent sprawdzający) zadaj sobie pytanie: "Czy poprosiłbym innego człowieka o code review tej zmiany?". Jeśli odpowiedź brzmi NIE — najprawdopodobniej nie potrzebujesz pełnego, rygorystycznego trybu weryfikacji. Skaluj intensywność weryfikacji do ryzyka i złożoności zmiany, a nie stosuj maksymalny rygor do wszystkiego.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: bezwarunkowe stosowanie najcięższego trybu weryfikacji (np. "no-mistakes") do KAŻDEJ zmiany, w tym trywialnych (literówki, drobne poprawki). To marnuje czas, tokeny i uwagę, a także zaciera sygnał — gdy wszystko jest weryfikowane rygorystycznie, przestajemy odróżniać zmiany faktycznie ryzykowne od rutynowych.

> **Cytat:** *"no - not every change! i talked about this in more depth in my latest video but tl;dr is you can ask yourself "would i ask another human to do code review for this change" and if the answer is no, then you probably don't need no-mistakes"*

---

## Wybór harnessu / routing modeli

### Używaj Pi dla modeli innych niż Anthropic

- **Data:** `Tue Sep 22 03:30:29 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102239083678650816)
- **Rodzaj:** Komentarz w dyskusji (@tanishqk)
- **Powiązane pojęcia:** [[Harness]] [[Jev|Model routing]] [[Harness|Anthropic]] [[Harness|Claude Code]] [[Harness|Pi]] [[Harness|Tool calling]]

**Kontekst / Problem:**
Odpowiedź Kuna Chena na wpis @tanishqk. Brak treści posta nadrzędnego, ale z odpowiedzi wynika, że rozmowa dotyczyła wyboru harnessu/narzędzia do pracy z modelami. Kun dzieli się regułą: Anthropic obsługuje w swoim ekosystemie, a każdy inny model uruchamia przez Pi.

**Rada inżynierska:**
Dopasuj harness do dostawcy modelu: dla modeli Anthropic używaj narzędzi z ekosystemu Anthropic (np. Claude Code), a dla wszystkich pozostałych modeli używaj Pi. Nie zakładaj, że jeden harness jest optymalny dla każdego modelu — provider-specific tooling ma znaczenie.

**Uwaga / Anty-wzorzec:**
Traktowanie jednego harnessu jako uniwersalnego dla wszystkich modeli. Różnice w tool-callingu, formatowaniu promptów i obsłudze kontekstu między dostawcami mogą powodować gorsze wyniki, jeśli nie dobierzesz narzędzia do modelu.

> **Cytat:** *"@tanishqk i use pi for any model that's not anthropic"*

---

## Obserwacje zachowania modeli / Ewaluacja modeli

### Grok 4.7 jako firstmate: ścisłe trzymanie się system promptu, stabilność i konserwatyzm kosztem szybkości

- **Data:** `Tue Sep 22 03:11:03 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102234191639257399)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|System Prompt]] [[Harness]] [[Firstmate Agent|Firstmate]] [[Harness|Ewaluacja modeli]] [[Stabilność modeli i przestrzeganie promptu|Benchmarki]] [[Harness|Stabilność modelu]] [[Harness|Konserwatyzm agenta]] [[TypeSafe — przewodnik praktyczny|Koszty tokenów]] [[Harness|Zaufanie do agenta]]

**Kontekst / Problem:**
Kun Chen opisuje pierwszy dzień pracy z Grok 4.7 jako swoim 'firstmate' (głównym agentem-harnessem w codziennej pracy inżynierskiej). Kontekst: w sieci pojawiły się raporty 'it's terrible' oparte wyłącznie o publiczne benchmarki oraz porównania modeli przez pryzmat generowania gier 3D. Kun odrzuca oba źródła jako bezwartościowe i proponuje ocenę jakościową z realnej, całodniowej pracy. To wpis ewolucyjny: Kun wprost pomija Grok 4.6 (bo 4.5 działał mu lepiej) i porównuje 4.7 do 4.5, co pokazuje, że jego stan wiedzy o modelach zmienia się wraz z doświadczeniem produkcyjnym, a nie z numeracją wersji.

**Rada inżynierska:**
Oceniaj modele wyłącznie na podstawie realnej, całodniowej pracy w swoim harnessie, nie na podstawie publicznych benchmarków ani dem typu 'model zrobił grę 3D'. Benchmarki są bezużyteczne (przykład: wskazywały Opus 5 jako lepszy od Fable, co nie pokrywa się z praktyką). Najbardziej wartościowy sygnał jakościowy to ścisłość trzymania się system promptu: Grok 4.7 jako pierwszy uwidocznił instrukcje, których żaden inny model wcześniej nie egzekwował (np. żądanie wskazania konkretnych czerwonych checków CI do pominięcia i odmowa prostego 'yolo'). Oznacza to, że warto pisać system prompty z myślą o modelach zdolnych je w pełni egzekwować – dopiero taki model ujawnia, że instrukcje w ogóle działają. Stabilność i przewidywalność (brak 'spikiness') buduje zaufanie szybciej niż pojedyncze momenty geniuszu.

**Uwaga / Anty-wzorzec:**
Dwie pułapki: (1) wyciąganie wniosków o modelu z publicznych benchmarków i viralowych dem (gry 3D) – to nie jest realna praca, a rozbieżność z praktyką bywa dramatyczna; (2) zakładanie, że model z większym numerem wersji jest lepszy – Kun celowo pomija Grok 4.6, bo 4.5 działał mu lepiej, co pokazuje, że numeracja nie implikuje regresji ani progresu. Dodatkowo: model konserwatywny (pytający o zgodę) bywa postrzegany jako spowolnienie, ale w wielu przypadkach brak potwierdzenia prowadziłby do niepożądanych akcji – pozornie oczywiste 'yes i do want that' jest często uzasadnione, bo intencja była rzeczywiście niejednoznaczna.

> **Cytat:** *"it follows system prompt very, very closely ... i traced it and it's indeed how i instructed it in firstmate's system prompt, but none of the other models followed it closely enough to make this behavior visible - grok 4.7 is the first to pick that up ... 2. it's very "stable" ... if you've used astra then you know what a "spiky" model is ... grok 4.7 is the opposite of that ... 3. it's a conservative model ... it doesn't like to take actions without asking, and would explicitly say so ... 4. it's a bit slower and costs more than 4.5, visibly"*

---

## Architektura systemów / Wybór modelu (LLM vs klasyczne ML)

### Dlaczego klasyczny klasyfikator nie zastąpi LLM przy kategoriach definiowanych przez użytkownika

- **Data:** `Thu Sep 17 15:35:36 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100609623531421915)
- **Rodzaj:** Komentarz w dyskusji (@winterspeak)
- **Powiązane pojęcia:** [[Harness|LLM jako klasyfikator]] [[Harness|Zero-shot classification]] [[Harness|User-defined taxonomy]] [[Harness|Kiedy nie trenować klasyfikatora]] [[Harness|Dynamiczne etykiety w promptcie]]

**Kontekst / Problem:**
Kun Chen odpowiada użytkownikowi @winterspeak, który najprawdopodobniej zasugerował, że problem poruszany w jego narzędziu (najpewniej automatyczne kategoryzowanie/etykietowanie treści, np. wpisów czy notatek) to zwykłe zadanie klasyfikacyjne, które można rozwiązać tradycyjnym klasyfikatorem ML. Kun prostuje to założenie, wyjaśniając naturę swojego use case'u.

**Rada inżynierska:**
Gdy kategorie są definiowane przez użytkownika i są w pełni dowolne (freeform), klasyczne podejście ML jest niewykonalne z dwóch powodów: (1) nie da się wytrenować jednego uniwersalnego klasyfikatora pokrywającego nieskończoną przestrzeń etykiet wszystkich użytkowników, (2) nie można wymagać, aby każdy użytkownik trenował własny model. W takich przypadkach właściwym narzędziem jest LLM działający zero-shot/few-shot, ponieważ przyjmuje definicje kategorii jako część promptu (kontekst), a nie jako wagi modelu. Reguła projektowa: zanim sięgniesz po trening klasyfikatora, sprawdź czy przestrzeń etykiet jest zamknięta i stabilna — jeśli jest otwarta i zależna od użytkownika, klasyfikacja musi być promptowana, nie trenowana.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: traktowanie każdego zadania przypisania etykiety jako problemu uczenia nadzorowanego ("to przecież tylko klasyfikacja"). Prowadzi to do projektowania pipeline'u treningowego, którego nie da się utrzymać przy dynamicznych, per-użytkownik etykietach — koszt oznaczonego data setu rośnie liniowo z liczbą użytkowników, a model i tak nie generalizuje na nowe kategorie.

> **Cytat:** *"not exactly - if you think about the use case i have here, the categories are user-defined and completely freeform

there’s no way i can train a traditional classifier that will work for every user, and there’s no way every user will train their own classifier"*

---

## Weryfikacja / Agent Harness

### Kwantyfikacja confidence w Jev jako filtr niepewnych odpowiedzi

- **Data:** `Thu Sep 17 15:29:09 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100608000042127434)
- **Rodzaj:** Komentarz w dyskusji (@PremiumGoblin)
- **Powiązane pojęcia:** [[Harness|Confidence gating]] [[Jev]] [[Harness|Ambiguity in requirements]] [[Harness|Agent Harness]] [[Harness|Low-confidence outputs]]

**Kontekst / Problem:**
Kun Chen odpowiada na wpis @PremiumGoblin, najprawdopodobniej dotyczący tego, czy dobrze zdefiniowane wymagania rozwiązują problem niejednoznaczności w implementacji. Kun zgadza się tylko częściowo: ocena, czy wymagania są wystarczająco dobrze określone i ile niejednoznaczności pozostaje w fazie implementacji, jest trudna. Wskazuje, że narzędzie Jev pomaga, bo kwantyfikuje confidence, co pozwala odrzucać odpowiedzi, gdy model nie jest pewny.

**Rada inżynierska:**
Nie zakładaj, że wymagania zawsze da się w pełni doprecyzować przed implementacją — ocena poziomu niejednoznaczności bywa trudna. Zamiast polegać wyłącznie na ludzkim osądzie, używaj skwantyfikowanego confidence z Jev: jeśli odpowiedź nie ma wystarczającej pewności, odrzuć ją zamiast przyjmować do dalszego przetwarzania.

**Uwaga / Anty-wzorzec:**
Traktowanie „well-defined requirements” jako uniwersalnego rozwiązania problemu niejednoznaczności oraz brak progu odrzucania odpowiedzi o niskim confidence — prowadzi to do przepuszczania niepewnych, potencjalnie błędnych wyników do implementacji.

> **Cytat:** *"not always - but for some cases yes, the judgment on whether requirements are “well defined” enough and how much ambiguity still exists during the implementation phase is not easy to answer

the extra nice thing about jev is that it quantifies the confidence, so i can say “if it’s not confident the i discard its answer”"*

---

## Orkiestracja agentów / Architektura kontekstu

### Kontekst wejściowy dla sub-agenta = task brief + reguły dispatchu + quota data

- **Data:** `Thu Sep 17 07:59:19 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100494796687340001)
- **Rodzaj:** Komentarz w dyskusji (@ArtifexPraxis)
- **Powiązane pojęcia:** [[Harness|Task brief]] [[Harness|Multi-agent orchestration]] [[Harness|Kontekst wejściowy agenta]] [[Harness|Dispatch rules]] [[Harness|Quota i rate limiting w agentach]] [[Harness|Delegacja zadań w harnessie]]

**Kontekst / Problem:**
Kun Chen odpowiada @ArtifexPraxis w wątku o systemie orkiestracji agentów (firstmate → crewmate). Wyjaśnia, jak składa się kontekst wejściowy dla agenta-decydenta o imieniu 'Jev' w momencie podejmowania decyzji o delegowaniu zadania. Zamiast wrzucać surowy prompt użytkownika, system najpierw wymusza wygenerowanie artefaktu pośredniego (task brief), który dopiero razem z politykami i danymi operacyjnymi trafia do modelu.

**Rada inżynierska:**
Buduj kontekst dla agenta delegującego (routera/dyspozytora), a nie tylko dla wykonawcy. Sprawdzony wzorzec: (1) task brief — zwięzły, wygenerowany przez orkiestratora opis zadania wystarczający do samodzielnej realizacji; (2) dispatch rules — reguły użytkownika, kto/co/kiedy ma być zaangażowane; (3) quota data — dane o limitach/zużyciu budżetu lub rate limitach. Ten trójskładnikowy kontekst jest wejściem dopiero do decyzji o delegacji, co oddziela 'co zrobić' (brief) od 'jak dysponować zasobami' (rules + quota). Wymuszenie zapisu task briefu przed dispatchem daje też darmową weryfikację: jeśli briefu nie da się napisać jednoznacznie, zadanie jest źle zdefiniowane i nie należy go delegować.

**Uwaga / Anty-wzorzec:**
Przekazywanie surowego promptu użytkownika bezpośrednio do sub-agenta bez pośredniego task briefu i bez reguł dispatchu/quota — prowadzi do delegacji źle zdefiniowanych zadań, przekroczeń limitów i braku audytowalności decyzji o routingu.

> **Cytat:** *"@ArtifexPraxis when firstmate is about to dispatch a crewmate to do a task, it first has to write a task brief anyway

that task brief + the user's dispatch rules + the user's quota data = input context to Jev here"*

---

## Architektura harnessa / Routing i selekcja modeli

### Routing modeli z uwzględnieniem pozostałego zapasu quota (quota runway)

- **Data:** `Thu Sep 17 07:28:21 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100487003431477661)
- **Rodzaj:** Komentarz w dyskusji (@taras_korn)
- **Powiązane pojęcia:** [[Jev|Model Routing]] [[Harness|Quota Management]] [[Harness]] [[Harness|Agentic Workflow]] [[Harness|Rate Limiting]]

**Kontekst / Problem:**
Kun Chen odpowiada @taras_korn, który najprawdopodobniej zapytał, czy mechanizm automatycznego wyboru modelu w jego harnessie/agenci bierze pod uwagę limity quota (np. zużycie API, rate limity subskrypcji). Odpowiedź precyzuje, że selekcja modelu już uwzględnia ten czynnik — algorytm wybiera model z największym dostępnym zapasem limitu, a nie wyłącznie według jakości lub kosztu.

**Rada inżynierska:**
Przy automatycznym wyborze modelu w harnessie nie kieruj się tylko zdolnościami lub ceną — dodaj 'quota runway' jako wymiar decyzyjny: wybieraj model, który ma największy pozostały zapas limitu, tak aby długie zadanie agentowe nie zostało przerwane w połowie przez wyczerpanie quota. Zapobiega to blokadzie całego runu i wymusza płynne przełączanie między modelami o różnych limitach.

**Uwaga / Anty-wzorzec:**
Routing modelu wyłącznie po jakości (np. zawsze najsilniejszy model) lub po koszcie, bez śledzenia pozostałego zapasu limitu — prowadzi do wyczerpania quota w trakcie wieloetapowego zadania, przerwania pracy agenta i konieczności restartu lub fallbacku w najgorszym momencie.

> **Cytat:** *"@taras_korn it already takes quota into consideration. it will pick the model with the most quota runway available"*

---

## Architektura systemów agentowych / Optymalizacja kosztów

### Zastępowanie wywołań LLM logiką deterministyczną + lekkim decydentem (Jev) — architektura hybrydowa zamiast pętli agentowych

- **Data:** `Thu Sep 17 06:45:30 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100476218512748616)
- **Rodzaj:** Komentarz w dyskusji (@v10se)
- **Powiązane pojęcia:** [[Harness|Pętla agentowa]] [[Harness|Architektura hybrydowa]] [[Harness|Logika deterministyczna]] [[TypeSafe — przewodnik praktyczny|Redukcja kosztów LLM]] [[Jev]] [[Harness|Decydent lekki vs LLM]] [[Harness|Generacja treści a rozumowanie]]

**Kontekst / Problem:**
Kun Chen odpowiada @v10se w wątku o implikacjach nowego podejścia (najpewniej lekkiego modelu/komponentu decyzyjnego 'Jev', który przejmuje część zadań dotąd realizowanych przez duże LLM-y). Kontekst: dyskusja o tym, co realnie zmienia możliwość obsłużenia części zadań bez wywołania dużego modelu. Kun wskazuje, że większość osób widzi tylko oczywistą korzyść kosztową, a pomija istotniejszą konsekwencję architektoniczną — przymus przemyślenia projektu oprogramowania. Standardem stały się pętle agentowe budowane wokół LLM; nowy komponent pozwala wrócić do rozdzielenia odpowiedzialności: logika deterministyczna (kod), podejmowanie decyzji (Jev), sporadyczna generacja treści (LLM).

**Rada inżynierska:**
Rozdzielaj trzy warstwy zamiast wrzucać wszystko do pętli agentowej: (1) logika deterministyczna = zwykły kod (tanio, przewidywalnie, testowalnie), (2) inteligentne podejmowanie decyzji = lekki, wyspecjalizowany komponent decyzyjny (Jev) zamiast pełnego LLM-a, (3) generacja treści = LLM wywoływany okazjonalnie, tylko tam, gdzie naprawdę potrzebna jest swoboda językowa. Traktuj redukcję kosztów jako efekt uboczny — główną wartością jest wymuszenie lepszej architektury. Każde wywołanie LLM, które da się zastąpić deterministycznym kodem lub tanim decydentem, jest kandydatem do usunięcia z pętli.

**Uwaga / Anty-wzorzec:**
Domyślne budowanie pętli agentowej wokół LLM-a dla każdego zadania — to prowadzi do nadmiarowych kosztów i niepotrzebnej niedeterministyczności. Pomijanie warstwy deterministycznej i zlecanie LLM-owi zadań, które są w istocie regułami lub klasyfikacją, to anty-wzorzec. Drugą pułapką jest widzenie wyłącznie oszczędności kosztowej i przegapienie, że nowy komponent zmienia sposób projektowania całego systemu.

> **Cytat:** *"right now i'm seeing two - the most obvious implication is cost reduction. it's a massive saving whenever we can replace LLM calls with this the non-obvious one is that it forces us to think about our software differently. LLMs make us all build agent loops. this enables us to explore a different architecture - a combination of deterministic logic (code), intelligent decision making (Jev), and occasional generation of content (LLM)"*

---

## Paradygmaty budowania oprogramowania z AI

### Jev nie zastępuje LLM-ów — wymaga nowego paradygmatu budowania oprogramowania

- **Data:** `Thu Sep 17 06:26:13 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100471365912707312)
- **Rodzaj:** Komentarz w dyskusji (@janpfranke)
- **Powiązane pojęcia:** [[Jev]] [[Harness|LLM]] [[Harness|Paradygmat budowania oprogramowania]] [[Harness|Drop-in replacement]]

**Kontekst / Problem:**
Kun Chen odpowiada @janpfranke w wątku o narzędziu 'Jev'. Kontekst: dyskusja o tym, czy Jev jest kolejnym zamiennikiem/alternatywą dla LLM-ów w procesie tworzenia oprogramowania. Kun prostuje to założenie — Jev nie jest substytutem LLM-ów, lecz innym podejściem do budowania softu, którego implikacje inżynierskie nie są jeszcze w pełni przemyślane.

**Rada inżynierska:**
Nie traktuj nowych narzędzi AI (np. Jev) jako drop-in replacement dla LLM-ów ani jako 'lepszego promptu'. To osobny paradygmat budowania oprogramowania — jego adopcja wymaga przeprojektowania sposobu myślenia o architekturze, przepływie pracy i roli modelu, a nie tylko podmiany komponentu. Kun otwarcie przyznaje, że sam nie przepracował jeszcze wszystkich implikacji, co sugeruje: wdrażaj eksperymentalnie i mierz, zamiast zakładać z góry równoważność funkcjonalną.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: kategoryzowanie nowego narzędzia AI jako 'zamiennika LLM' i próba wpięcia go w istniejący stack bez zmiany mentalnego modelu budowania oprogramowania. Prowadzi to do błędnych oczekiwań co do zachowania narzędzia i rozczarowania w produkcji.

> **Cytat:** *"@janpfranke right - Jev is not a replacement for LLMs. it requires a new way of thinking about building software - tbh i'm still yet to think through the implications.."*

---

## Architektura agentów / Orkiestracja i optymalizacja kosztów

### Zastąpienie LLM-owego dispatchu deterministycznym API Jev w orkiestratorze Firstmate

- **Data:** `Thu Sep 17 06:16:35 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100468943853085061)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Firstmate Agent|Orkiestracja agentów]] [[Jev]] [[Firstmate Agent|Firstmate]] [[Harness|Deterministyczny dispatch]] [[TypeSafe — przewodnik praktyczny|Redukcja kosztów LLM]] [[Harness|Tool calls]] [[Harness|Ewaluacja równoważności]] [[Jev|Routing modeli i harnessów]]

**Kontekst / Problem:**
Firstmate jako orkiestrator inteligentnie kieruje każde zadanie do odpowiedniego agenta (permutacja: harness, model, reasoning effort) na podstawie preferencji użytkownika. Domyślnie robił to agent LLM: musiał 'pomyśleć', wykonać tool calls po reguły dispatchu i dane o kwotach (quota), a potem podjąć decyzję — co jest wolne i kosztuje tokeny. Kun zastąpił ten proces wywołaniem Jev (deterministyczne API), które podejmuje identyczną decyzję bez rozumowania i bez tool calli, w ~200 ms.

**Rada inżynierska:**
Reguła inżynierska: jeśli decyzja agenta jest deterministyczna i regułowa (routing zadań wg reguł dispatchu i danych o quota), NIE zostawiaj jej LLM-owi z rozumowaniem i tool callami — skompiluj ją do deterministycznego API (Jev) i zostaw LLM tylko samo wywołanie narzędzia. Przed podmianą zrób ewaluację równoważności na zbiorze zadań (tu: 25 zadań dało dokładnie tę samą odpowiedź, którą dałby LLM). Zmierz oszczędność osobno dla zastąpionego fragmentu i dla całego procesu: sam Jev to ~100x taniej, a end-to-end (z wliczonym tool callem LLM) -71% kosztu i -90% czasu ściennego dispatchu. Wniosek architektoniczny: LLM to tylko mały element architektury agentowej — kluczowe decyzje warto wynosić do deterministycznych, tanich komponentów. Konfiguracja: ustaw TYPESAFE_API_KEY w .env w repo firstmate, aby aktywować.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: używanie LLM-a z rozumowaniem i tool callami do podejmowania powtarzalnych, regułowych decyzji orkiestracyjnych — generuje opóźnienie, koszt tokenów i niepotrzebną zmienność tam, gdzie potrzebna jest deterministyczna, szybka decyzja. Drugą pułapką jest podmiana bez walidacji równoważności na zbiorze ewaluacyjnym — bez tego nie wiadomo, czy deterministyczny odpowiednik nie zmienia zachowania systemu.

> **Cytat:** *"i just replaced this dispatch process with Jev. it makes the same decision with no thinking or tool calls, done in ~200ms, and for the 25 tasks i evaluated this with, it gives the exact same answer fable would have given... but even with that counted, the saving from Jev still resulted in a -71% reduction in cost and -90% reduction in wall time of completing the whole dispatching process... i think this is starting to enable a whole new architectural paradigm for software. LLMs are just a small part of it."*

---

## Architektura narzędzi agenta (tool design / harness)

### Nie sprowadzaj narzędzi agenta do surowego bash-a — tracisz tool search

- **Data:** `Thu Sep 17 06:01:23 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100465119897809142)
- **Rodzaj:** Komentarz w dyskusji (@tanishqk)
- **Powiązane pojęcia:** [[Harness|Tool Search]] [[Harness|Agent Harness]] [[Harness|Projektowanie narzędzi agenta]] [[Harness|Function Calling]] [[Harness|MCP]] [[Harness|Bash Tool]]

**Kontekst / Problem:**
Wymiana zdań z @tanishqk i @trq212 wokół upraszczania harnessu agentowego: czy da się zastąpić zestaw strukturalnych narzędzi jednym uniwersalnym narzędziem shellowym (bash). Kun Chen prostuje ten pomysł: owszem, wtedy wszystko staje się znowu bashem, ale przestaje działać cała warstwa tool search i pokrewnych mechanizmów, przez co takie rozwiązanie jest 'strictly worse version of a cli' — czyli gorszą kopią zwykłego terminala, pozbawioną przewag agentowego toolingu.

**Rada inżynierska:**
Zachowuj strukturalne definicje narzędzi (nazwa, schemat parametrów, opis) zamiast sprowadzać cały interfejs agenta do jednego bash-a. To właśnie te metadane napędzają tool search, routing i walidację wywołań — bez nich harness degeneruje się do 'strictly worse version of a cli': ma ograniczenia shella, a nie ma korzyści zorganizowanego zestawu narzędzi. Jeśli rozważasz uproszczenie toolingu, pytaj nie 'czy bash to załatwi', ale 'co stracę z warstwy discovery i struktury'.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: redukcja wszystkich możliwości agenta do jednego generycznego narzędzia typu 'run bash', w przekonaniu że to uproszczenie harnessu. Efekt: tool search i strukturalne wywołania przestają działać, a agent dostaje najgorsze z obu światów — ograniczony shell bez agentowej warstwy abstrakcji.

> **Cytat:** *"@tanishqk @trq212 yes but that becomes bash again and none of the tool search etc would work, right? that becomes a strictly worse version of a cli"*

---

## Harness / Ekosystem narzędzi i strategia vendorowa

### Nie wiąż dostępu do modelu z harnessem dostawcy — wybieraj harness niezależny od modelu

- **Data:** `Sat Sep 12 19:22:48 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2098854862788440308)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness]] [[Harness|Model-Agnostic Harness]] [[Harness|Vendor Lock-in]] [[Harness|Transparentność zbierania danych treningowych]] [[Harness|Tech Debt narzędziowy]] [[Harness|Telemetria i prywatność kodu]]

**Kontekst / Problem:**
Kun komentuje praktykę dostawców modeli (porównując do modelu cenowego Meta dla 'muse spark'), którzy tańszy dostęp do modelu uzależniają od używania własnego harnessa — często potajemnie zbierającego dane lub wysyłającego kod użytkownika. Problem inżynierski: taki układ fragmentuje setup użytkownika, wprowadza ukrytą telemetrię/dane treningowe i zmusza do porzucenia własnego, dojrzałego stacku narzędziowego. Kun argumentuje, że zbieranie danych treningowych da się robić bez wymuszania harnessa — wystarczy przejrzystość i realny wybór.

**Rada inżynierska:**
Utrzymuj harness niezależny od dostawcy modelu: pi, opencode, hermes, openclaw, a nawet claude code i codex da się skonfigurować pod dowolny model — więc nie ma powodu przyjmować harnessa dostawcy. Jeśli dostawca wiąże dobrą cenę z użyciem swojego harnessa, traktuj to jako sygnał ostrzegawczy: żądaj jawnego oznaczenia, kiedy dane są zbierane, a kiedy nie, ile są warte i daj sobie wybór. Brak transparentności w zakresie zbierania danych = odrzuć ofertę, nie narzędzie.

**Uwaga / Anty-wzorzec:**
Przyjmowanie harnessa dostawcy w zamian za tańszy dostęp do modelu: (1) fragmentuje spójny, model-agnostyczny setup, (2) wprowadza ukryte zbieranie danych i/lub wysyłanie kodu na serwery dostawcy, (3) tworzy tech debt zależny od jednego vendora, który nie wnosi realnej wartości inżynierskiej. Anty-wzorzec po stronie dostawcy: 'chcesz dobrą cenę? użyj naszego harnessa' zamiast jawnego, wycenionego i opcjonalnego programu wymiany danych.

> **Cytat:** *""every model provider should learn from meta's pricing model for muse spark, with fully transparent subsidization labeled for the contributor tier

stop doing "in order to use our model at a good price, you must use our harness which secretly collects your data and/or upload your codebase"

meta clearly proved there's a way to collect training data without relying on a harness. just be transparent about when you collect data vs not, clearly communicate how much the data is worth, and give the choice to the user

and i really don't need your harness. i already have SO MANY state of the art harnesses to pick from. pi, opencode, hermes, openclaw, and even claude code and codex can be configured to use any model. your own harness is a tech debt that fragments my setup and doesn't add much value""*

---

## Ewaluacja i wybór modeli

### Empiryczna ocena wersji modelu: 4.5 vs 4.6 — nowsze nie znaczy lepsze

- **Data:** `Sat Sep 12 17:23:03 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2098824725866938875)
- **Rodzaj:** Komentarz w dyskusji (@tejasa97)
- **Powiązane pojęcia:** [[Harness|Ewaluacja modeli]] [[Harness|A/B testing modeli]] [[Harness|Upgrade bias]] [[TypeSafe — przewodnik praktyczny|Koszt i latencja w produkcji]] [[Harness|Wybór wersji modelu]]

**Kontekst / Problem:**
Kun Chen odpowiada @tejasa97 w wątku o porównaniu wersji modelu (4.5 vs 4.6). W kontekście ogólnej presji na aktualizację do najnowszej wersji modelu, Kun świadomie wykonuje regresję (revert) do starszej wersji 4.5, aby zweryfikować hipotezę, że nowszy model faktycznie jest lepszy w jego realnym zastosowaniu. To praktyka kontrolowanego testu A/B zamiast ślepego podążania za wydaniami.

**Rada inżynierska:**
Nie zakładaj, że nowsza wersja modelu jest automatycznie lepsza. Zrób świadomy revert do starszej wersji i przetestuj ją w swoim realnym workflow, mierząc nie tylko 'inteligencję', ale też szybkość i efektywność (koszt/latencję/tokeny). W obserwacji Kuna 4.5 okazał się szybszy i bardziej efektywny przy braku widocznej różnicy w jakości rozumowania — czyli w praktyce produkcyjnej wygrywa starszy model. Wybór modelu to decyzja inżynierska oparta na pomiarach, nie na numerze wersji.

**Uwaga / Anty-wzorzec:**
Upgrade bias — domyślne przechodzenie na najnowszą wersję modelu 'bo nowsza', bez pomiaru kosztu i latencji. Prowadzi to do wolniejszych, droższych pipeline'ów bez realnego zysku na jakości. Drugi anty-wzorzec: ocenianie modeli wyłącznie po benchmarkach 'inteligencji' z pominięciem szybkości i efektywności, które w produkcji często decydują.

> **Cytat:** *"i deliberately reverted to 4.5 to test whether it’s actually better than 4.6 — so far i think i like 4.5 better. it’s faster and more efficient with no visible difference on intelligence"*

---

## Wybór modelu / debugowanie agentowe

### Opus 4.8 vs Grok 4.5 w debugowaniu CI: hipoteza zamiast diagnozy, $10 vs $1.2

- **Data:** `Sat Sep 12 16:44:00 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2098814897354137710)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Model selection]] [[Harness|Agentic debugging]] [[Harness|Cost per resolution]] [[Harness|GitHub Actions]] [[Harness|CI runner limits]] [[Harness|Reasoning loops]] [[Harness]]

**Kontekst / Problem:**
GitHub Actions w repo OSS Kuna Chena nagle przestały się uruchamiać. Kun zlecił diagnozę Opusowi 4.8 — model spalił ~$10 tokenów i upierał się, że przyczyną jest nieopłacony rachunek albo awaria GitHuba. Po przełączeniu na Grok 4.5 (3 minuty, $1.2 tokenów) agent ustalił realną przyczynę: nagły wysyp runów CI w repo 'firstmate' wysycił limit współdzielonych runnerów na całym koncie, po czym anulował nadmiarowe runy i wszystko wróciło do normy. Wpis dokumentuje aktualny stan preferencji Kuna (domyślnie Grok) i jest argumentem za doborem modelu pod zadanie infrastrukturalne, a nie pod markę.

**Rada inżynierska:**
Dobieraj model do typu zadania, nie do domyślnego nawyku: przy debugowaniu infrastruktury licz nie koszt tokenów, a koszt do rozwiązania (cost-per-resolution). Model, który formułuje wiarygodne hipotezy zewnętrzne (nieopłacony bill, awaria dostawcy) zamiast zbadać stan własnego konta, potrafi spalić 8x więcej budżetu i nie dowieźć fixa. Preferuj agenta, który wykonuje akcje diagnostyczne i naprawcze (odpytanie API, lista runów, anulowanie nadmiarowych), a nie tylko rozumuje. Wniosek Kuna jest wprost ewolucyjny: 'people ask me why i default to grok and this is why' — po serii podobnych doświadczeń domyślnym modelem do pracy agentowej stał się Grok 4.5, a nie Opus 4.8.

**Uwaga / Anty-wzorzec:**
Anchoring na najbardziej prawdopodobnej hipotezie i brnięcie w nią mimo braku dowodów — agent uznaje, że problem jest po stronie zewnętrznej (billing/outage), bo to najłatwiejsze wyjaśnienie, i nie sprawdza własnego konta ani limitów. Drugi anty-wzorzec: traktowanie wysokiego kosztu tokenów jako sygnału głębszego rozumowania — $10 wydane na błędny wniosek to gorszy wynik niż $1.2 na trafny.

> **Cytat:** *"github actions in my oss repos suddenly stopped running today

i had opus 4.8 look into it, it spent ~$10 worth of tokens and insisted that either i haven't paid my bills or there's a github outage

switched to grok 4.5 and just 3 minutes in with $1.2 worth of tokens, it found there's a surge of CI runs in my firstmate repos starving all the allowed runners across my account, cancelled a bunch of them, and everything's back on track

this is just an anecdotal example but i've had many positive experiences like this. people ask me why i default to grok and this is why"*

---

## Architektura agentów / Orkiestracja

### Routing zadań do subagentów poza LLM-em — dedykowany router (Jev) zamiast autoregresji orkiestratora

- **Data:** `Mon Sep 21 04:57:11 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101898514523730033)
- **Rodzaj:** Komentarz w dyskusji (@CompleteSkeptic)
- **Powiązane pojęcia:** [[Harness|Subagenty]] [[Harness|Orkiestrator chief-of-staff]] [[Jev|Routing zadań]] [[Harness|LLM router]] [[Harness|Multi-agent orchestration]] [[Harness|Delegacja zadań w agentach]]

**Kontekst / Problem:**
Kun Chen odpowiada w wątku pod wpisem @CompleteSkeptic dotyczącym problemów z subagentami. Rozwiązuje jeden z wymienionych problemów: w orkiestratorze w stylu 'chief-of-staff', gdzie zakłada się, że każde istotne zadanie musi wykonać subagent, decyzja o tym, do którego subagenta przekazać zadanie, staje się wąskim gardłem, jeśli podejmuje ją sam LLM orkiestratora.

**Rada inżynierska:**
Decyzję routingową (wybór subagenta) warto wynieść z LLM-a orkiestratora do dedykowanego, lekkiego routera (tu: Jev), który działa jak drop-in zamiennik. Router podejmuje decyzję szybciej i taniej niż orkiestrator czytający dużą ilość danych i podejmujący decyzję autoregresyjnie token po tokenie. Wzorzec: orkiestrator planuje, ale klasyfikacja/rozgałęzienie ruchu to zadanie dla wyspecjalizowanego komponentu, nie dla generatywnego rozumowania.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: pozwalanie LLM-owi orkiestratora na podejmowanie decyzji routingowych poprzez wczytywanie obszernego kontekstu i 'autoregresywne' dochodzenie do wyboru — jest to nieefektywne, wolne i niepotrzebnie obciąża główny model tam, gdzie wystarczy prostszy router.

> **Cytat:** *"i used Jev to solve one of the listed problems around subagents and it works really well

in a chief-of-staff style orchestrator, it’s assumed that any substantial task has to be done by a subagent - in this scenario, Jev becomes a perfect drop-in router that can make the routing decision in a much more efficient way than letting the orchestrator LLM do it by reading a bunch of data and autoregressive its decision"*

---

## Harness i zarządzanie kontekstem / koszty

### Nie wznawiaj długiej sesji po wygaśnięciu cache — użyj transkryptu w nowej sesji

- **Data:** `Mon Sep 21 03:46:52 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101880818142515556)
- **Rodzaj:** Komentarz w dyskusji (@Paiky16)
- **Powiązane pojęcia:** [[Prompt Architecture|Cache wygasły w długiej sesji]] [[Harness|Transkrypty sesji]] [[TypeSafe — przewodnik praktyczny|Koszt kontekstu]] [[Harness|Nowa sesja zamiast wznawiania]]

**Kontekst / Problem:**
Kun Chen odpowiada na wpis @Paiky16, prawdopodobnie dotyczący kontynuowania pracy agenta po przerwie lub między sesjami. Wyjaśnia, że nie trzeba budować własnego mechanizmu przenoszenia stanu: większość harnessów domyślnie zapisuje transkrypty i potrafi je odczytać, więc wystarczy w nowej sesji poinformować agenta, że w poprzednim transkrypcie zostały niedokończone zadania. Ostrzega przy tym, że wznawianie długiej sesji, której cache wygasł, jest bardzo kosztowne.

**Rada inżynierska:**
Nie implementuj własnego mechanizmu przenoszenia kontekstu między sesjami — większość harnessów domyślnie zapisuje transkrypty i umie je odczytać. Zamiast tego w nowej sesji po prostu poinformuj agenta, że w transkrypcie poprzedniej sesji znajduje się niedokończona praca. Unikaj wznawiania długiej sesji po wygaśnięciu cache — brak trafień w cache przy dużym kontekście potrafi kosztować nawet ~5 USD za jedno żądanie.

**Uwaga / Anty-wzorzec:**
Wznawianie długiej sesji, której cache już wygasł — każdy request przelicza cały kontekst od zera, co drastycznie podnosi koszt (rzędu 5 USD za pojedyncze żądanie) i opóźnia odpowiedź. Zamiast tego startuj nową sesję i wskaż transkrypt poprzedniej.

> **Cytat:** *"most agent harnesses save transcripts by default and know how to look them up, so you don’t need to do anything special other than letting the new session know you have some unfinished work in the last session’s transcript

definitely DO NOT resume a long session whose cache expired. that’s what going to cost you $5 for one request"*

---

## Zarządzanie kontekstem / Harness

### Delegowanie decyzji o kompakcji kontekstu do agenta/harnessu

- **Data:** `Mon Sep 21 03:34:19 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101877657927655730)
- **Rodzaj:** Komentarz w dyskusji (@kunchenguid)
- **Powiązane pojęcia:** [[Context Compaction]] [[Harness]] [[Context Compaction|Zarządzanie kontekstem]] [[Harness|Nasycenie kontekstu]] [[Harness|Agentic Coding]]

**Kontekst / Problem:**
Kun Chen odpowiada na wpis dotyczący strategii kompakcji kontekstu (prawdopodobnie ręcznej vs automatycznej). Wskazuje alternatywne podejście: zamiast samodzielnie decydować, kiedy kompaktować, pozwala Jevowi (agentowi/harnessowi) sygnalizować moment kompakcji. Brak treści posta nadrzędnego, więc kontekst odtworzony na podstawie samej odpowiedzi.

**Rada inżynierska:**
Nie wymuszaj ręcznej kompakcji kontekstu według sztywnego progu; rozważ delegowanie tej decyzji do harnessu/agenta, który wykryje nasycenie kontekstu i sam wskaże, kiedy należy go skompaktować. Dzięki temu kompakcja następuje na podstawie rzeczywistego zużycia i zachowania modelu, a nie z góry założonego limitu.

**Uwaga / Anty-wzorzec:**
Ręczna, przedwczesna kompakcja może usuwać istotny kontekst i prowadzić do utraty informacji potrzebnych do dalszego rozumowania. Z kolei brak mechanizmu sygnalizacji ze strony harnessu może skutkować przepełnieniem okna kontekstowego i degradacją jakości odpowiedzi.

> **Cytat:** *"oh alternatively, which is what i do right now - let Jev tell you when to compact"*

---

## Zarządzanie kontekstem i kosztami

### Zarządzanie kosztami cache w długich sesjach: /compact przed odejściem, nie po powrocie

- **Data:** `Mon Sep 21 03:14:19 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101872626968969713)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Prompt Architecture|Prompt Caching]] [[Context Compaction|Zarządzanie kontekstem]] [[TypeSafe — przewodnik praktyczny|Koszty tokenów]] [[Context Compaction|/compact]] [[Prompt Architecture|TTL cache]] [[Harness|Długie sesje agentowe]] [[Harness|Transkrypt sesji]]

**Kontekst / Problem:**
Kun Chen wyjaśnia pułapkę kosztową związaną z wygaśnięciem cache promptu w długich sesjach agentowych. Problem: gdy użytkownik odchodzi od sesji i wraca po czasie dłuższym niż TTL cache (Claude: 1h, Codex: 30min domyślnie), cały kontekst jest przetwarzany ponownie jako niecache'owany prompt. Przy oknie 500k tokenów pojedyncze żądanie kosztuje ponad $5 — niezależnie od tego, czy to zwykła tura, czy komendanie /compact. Rozwiązanie: kompaktować PRZED odejściem od sesji, nie po powrocie.

**Rada inżynierska:**
Reguła inżynierska: uruchamiaj /compact ZANIM odejdziesz od długiej sesji, a nie po powrocie. Kompakcja sama w sobie jest pełnym żądaniem — jeśli cache wygasł, zapłacisz pełną cenę (~$5 przy 500k kontekstu) tylko za próbę zmniejszenia kontekstu. Jeśli wracasz do dużej, bezczynnej sesji, najlepiej: (1) uruchom /compact natychmiast przed przerwaniem pracy, lub (2) rozpocznij nową sesję i poproś agenta o odczytanie transkryptu poprzedniej sesji, jeśli potrzebuje kontekstu. Świadomość TTL cache (Claude 1h, Codex 30min) powinna być częścią planowania pracy z agentem — długie przerwy w sesji kosztują.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: powrót do długiej bezczynnej sesji i uruchomienie /compact z myślą, że obniży to koszty. Jest odwrotnie — gdy cache wygasł, kompakcja sama kosztuje pełną cenę niecache'owanego żądania (ponad $5 przy 500k okna). Drugi anty-wzorzec: ignorowanie TTL cache i pozostawianie długich sesji otwartych przez przerwy dłuższe niż czas życia cache.

> **Cytat:** *"a quick tip that may surprise some folks — an uncached prompt to fable at 500k context window will directly cost you over $5 for A SINGLE REQUEST... the most common way to fall into that case is when you walk away from a long session and come back after a while when cache expired (claude is 1 hr, codex is 30 mins by default)... don't run "/compact" there thinking it'll reduce your cost, because the compaction request is still a real request and it will cost $5 by itself right there. the best thing to do is to /compact BEFORE you walk away. the next best thing is when you come back and see a large context window, just start a new session, and ask your agent to look for the last session's transcript if it needs context."*

---

## Zarządzanie kontekstem / ewolucja praktyk inżynierskich

### Ewolucja podejścia do kompresji kontekstu: od „just auto compact” do taniego, szybkiego osądu modelu (Jev)

- **Data:** `Fri Sep 18 22:27:31 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101075672747970901)
- **Rodzaj:** Komentarz w dyskusji (@seflless)
- **Powiązane pojęcia:** [[Harness|Auto-compact]] [[Context Compaction|Zarządzanie kontekstem]] [[Harness|Kompresja kontekstu]] [[Harness|Ewolucja modeli]] [[TypeSafe — przewodnik praktyczny|Koszt osądu modelu]] [[Harness|Aktualizacja wiedzy inżynierskiej]]

**Kontekst / Problem:**
Kun Chen odpowiada @seflless w wątku o strategiach zarządzania kontekstem (auto-compact vs. ręczna, granularna optymalizacja). Wyjaśnia, że przez długi czas jego stałą rekomendacją było „just auto compact” — czyli oddanie kompresji kontekstu automatyce, ponieważ czas człowieka powinien być przeznaczony na decyzję „co dalej”, a nie na mikro-optymalizacje. Ta rekomendacja uległa jednak zmianie wraz z pojawieniem się „Jev”: gdy osąd modelu staje się wystarczająco szybki i tani, selektywna, świadoma ocena kontekstu przestaje być kosztowna — nie ma więc powodu z niej rezygnować. To jawna aktualizacja wcześniejszego stanowiska: starsza rada (auto-compact, nie mikro-optymalizuj) obowiązywała przy wolniejszym/droższym rozumowaniu modelu; nowszy wpis odzwierciedla zaktualizowany stan wiedzy.

**Rada inżynierska:**
Domyślną praktyką pozostaje „just auto compact” — nie marnuj czasu człowieka na mikro-optymalizację kontekstu, skup się na decyzji „what to do next”. ZASADA AKTUALIZACJI: wraz z modelami, których osąd (judgment) jest szybki i tani (przypadek „Jev”), kalkulacja się odwraca — granularna, świadoma selekcja/kompresja kontekstu staje się opłacalna i nie ma powodu z niej rezygnować. Zanim utrwalą się stare heurystyki kontekstowe, sprawdź koszt i szybkość osądu aktualnie używanego modelu — ta sama rada może być już nieaktualna.

**Uwaga / Anty-wzorzec:**
Traktowanie rekomendacji kontekstowych jako wiecznych dogmatów: rada „auto compact, nie optymalizuj” była poprawna przy starym reżimie kosztowym, ale przy szybkim i tanim osądzie modelu staje się anty-wzorcem — prowadzi do oddania kontroli nad kontekstem, gdy selektywna ocena jest już praktycznie darmowa. Drugi anty-wzorzec: ręczna mikro-optymalizacja kontekstu, która zjada czas człowieka przeznaczony na decyzje „co dalej”.

> **Cytat:** *""just auto compact" has actually been my recommendation all along, because i think our human time should be spent on "what to do next", not these micro optimizations

that changed with Jev. the judgment becomes so fast and cheap that there's no reason not to get it"*

---

## Zarządzanie kontekstem / Harness agentowy

### Ręczne etykietowanie checkpointów i kryterium „safe” w kompakcji kontekstu agenta

- **Data:** `Fri Sep 18 20:25:20 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101044924301156365)
- **Rodzaj:** Komentarz w dyskusji (@mktpavlenko)
- **Powiązane pojęcia:** [[Context Compaction]] [[Bezpieczny punkt kompaktowania|Checkpointing w harnessie agenta]] [[Harness|Persystencja stanu vs historia czatu]] [[Eval Set z realnych sesji|Ręczne etykietowanie ground truth]] [[Harness|Harness agentowy]]

**Kontekst / Problem:**
Kun Chen odpowiada @mktpavlenko w dyskusji o checkpointach sesji agenta (punktach kompakcji / porzucania wcześniejszego kontekstu). Wyjaśnia metodykę budowy zbioru referencyjnego: sam ręcznie etykietował wszystkie checkpointy, a status „safe” (bezpieczny do odcięcia wcześniejszej historii) wyznaczał nie po tym, co już się wydarzyło, lecz po tym, czy RESZTA sesji potrzebuje czegokolwiek z wcześniejszej części, co nie zostało utrwalone w stanie trwałym.

**Rada inżynierska:**
Bezpieczeństwo checkpointu definiuj przez zależność W PRZÓD, nie w tył: checkpoint jest 'safe' tylko wtedy, gdy żadna późniejsza część sesji nie odwołuje się do informacji z odcinanego segmentu, której nie ma w stanie persystowanym. Praktycznie: (1) najpierw utrwal wszystko, co może być potrzebne dalej (pliki, notatki, stan zadania), (2) dopiero potem odcinaj historię, (3) buduj ground truth ręcznym etykietowaniem — automatyczne metryki typu 'rozmiar kontekstu' nie mówią nic o bezpieczeństwie kompakcji.

**Uwaga / Anty-wzorzec:**
Ocenianie jakości kompakcji po tym, czy agent 'pamięta' przeszłość, zamiast po tym, czy przyszłe kroki mają wszystkie potrzebne dane. Odcinanie kontekstu bez zapisania wniosków do stanu trwałego prowadzi do cichej utraty informacji, którą agent 'odkrywa' dopiero wiele kroków później — wtedy debugowanie jest bardzo kosztowne.

> **Cytat:** *"@mktpavlenko all the checkpoints were manually labeled by myself and "safe" checkpoints were determined by looking at whether the rest of the session indeed needs anything in the prior session that's not persisted"*

---

## Inne obserwacje

### Nie rób „instant compaction

- **Data:** `Fri Sep 18 19:53:16 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101036854925779291)
- **Rodzaj:** Komentarz w dyskusji (@gehariharan)
---

## Zarządzanie kontekstem / Harnessy agentowe / Ewaluacja promptów

### compact-adviser: dynamiczny próg precision/recall przy decyzji o kompakcji sesji

- **Data:** `Fri Sep 18 19:36:40 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101032677940117875)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Context Compaction|Compaction kontekstu]] [[Harness|Zarządzanie oknem kontekstowym]] [[Harness|Precision vs Recall]] [[Eval Set z realnych sesji|Eval set z sesji]] [[Harness|Prompt hillclimbing]] [[Harness|Task boundary]] [[Harness|Agent plugin]] [[Jev|Jev klasyfikator]]

**Kontekst / Problem:**
Kun odpowiada na powracające pytanie społeczności: "kiedy powinienem zrobić /compact sesji?". Problem: nie ma uniwersalnej odpowiedzi, bo zależy to od tego, czy przyszłe akcje agenta będą potrzebować szczegółowego kontekstu z bieżącego okna. Rozwiązanie: plugin agentowy compact-adviser zbudowany na klasyfikatorze Jev, dostępny w Claude i pi, który ocenia, czy jesteśmy na bezpiecznej granicy zadania (task boundary) do kompakcji. Klasyfikator został wykalibrowany na prywatnym zbiorze ewaluacyjnym z 40 prawdziwych sesji z ręcznie oznaczonymi bezpiecznymi i niebezpiecznymi punktami kontrolnymi; prompt Jev był hillclimbowany do dobrej skuteczności.

**Rada inżynierska:**
Nie traktuj decyzji o kompakcji jako statycznej reguły – steruj nią dynamicznie względem zapełnienia okna kontekstowego. Gdy okno jest małe, optymalizuj pod PRECISION (nie kompaktuj przedwcześnie, bo stracisz szczegóły potrzebne w kolejnych krokach). W miarę zapełniania się okna stopniowo przesuwaj się w stronę RECALL (nie przegap okazji do kompakcji), ponieważ koszt braku kompakcji rośnie, a na końcu agent i tak zostanie zmuszony do kompakcji. Zbuduj prywatny eval set z rzeczywistych sesji z ręcznie oznaczonymi bezpiecznymi/niebezpiecznymi checkpointami i hillclimbuj prompt klasyfikatora – to jedyny sposób, by ocenić, czy próg jest sensowny. Rozdziel tryb 'hint' (sugestia, użytkownik sam uruchamia /compact) od 'auto' (kompakcja automatyczna, gdy klasyfikator uzna to za bezpieczne).

**Uwaga / Anty-wzorzec:**
Brak refleksji nad granicą zadania (task boundary) – kompaktowanie w środku zadania wymagającego detalu z bieżącego okna powoduje utratę kontekstu i błędy w kolejnych krokach. Odwrotna pułapka: zwlekanie z kompakcją przy zapełnionym oknie, co kończy się wymuszoną, niekontrolowaną kompakcją w najgorszym możliwym momencie.

> **Cytat:** *"there's no easy answer because it depends on how likely your future action will need detailed context in the existing window ... i built a private eval set from 40 real sessions and manually labeled all the safe vs unsafe checkpoints to evaluate this, and hillclimbed the Jev prompt till it performed quite well ... optimize for precision (not triggering a compaction prematurely) when context window is small - and gradually shift to optimize for recall (not missing an opportunity to compact) when context window fills up, because the cost of not compacting becomes higher, and at the end the agent will be forced to compact anyway"*

---

## Prompt Caching / Zarządzanie kontekstem

### Kompaktowanie kontekstu: pełna sesja w cache vs. wycinanie historii (cache miss 10x-40x)

- **Data:** `Fri Sep 18 05:15:45 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100816020932096060)
- **Rodzaj:** Komentarz w dyskusji (@DeccansoftAI)
- **Powiązane pojęcia:** [[Prompt Architecture|Prompt Caching]] [[Context Compaction]] [[Prompt Architecture|Cache Miss]] [[Context Compaction|Zarządzanie kontekstem]] [[Harness|Ekonomia tokenów]] [[Prompt Architecture|Anthropic Prompt Caching]]

**Kontekst / Problem:**
Kun Chen odpowiada w wątku (@DeccansoftAI, @tamarajtran, @typesafeai) na pytanie o to, czy przy kompaktowaniu sesji LLM warto najpierw usuwać część wiadomości z historii. Wyjaśnia ekonomię prompt cache: pełna, niezmodyfikowana sesja przy kompaktowaniu trafia w cache i kosztuje bardzo mało, natomiast jakakolwiek modyfikacja historii (usunięcie wiadomości) przed żądaniem kompaktowania powoduje cache miss i naliczenie pełnej ceny.

**Rada inżynierska:**
Kompaktuj CAŁĄ sesję bez modyfikacji historii — wtedy prompt w całości trafia w cache (cached prompt) i koszt jest bardzo niski. Każde usunięcie/przycięcie wiadomości z historii przed kompaktowaniem unieważnia cache (cache miss) i jest rozliczane po PEŁNEJ cenie, czyli 10x-40x drożej. Reguła: jeśli chcesz zaoszczędzić, nie 'sprzątaj' historii przed kompaktowaniem — pozwól, by prefiks promptu pozostał identyczny i w pełni cache'owalny.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: ręczne wycinanie/prune wiadomości z historii przed uruchomieniem compaction request. Intuicyjnie wydaje się, że 'mniejszy kontekst = taniej', ale w rzeczywistości psuje to cache (cache miss) i podnosi koszt 10x-40x względem kompaktowania całej, niezmienionej sesji.

> **Cytat:** *"no, because when the LLM compacts the whole session, it's a fully cached prompt whose price is very low

but if you remove some of the messages from the history and then run a compaction request, it's a cache miss and will be charged at FULL price 10x-40x more expensive"*

---

## Zarządzanie kontekstem / Compaction w harnessie agenta

### Krytyka selektywnej kompakcji usuwającej tylko wywołania narzędzi

- **Data:** `Fri Sep 18 04:15:10 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100800776620900454)
- **Rodzaj:** Komentarz w dyskusji (@tamarajtran)
- **Powiązane pojęcia:** [[Context Compaction]] [[Context Compaction|Context Window Management]] [[Prompt Architecture|Prompt Caching]] [[Harness|Agent Harness]] [[Harness|Ewaluacje agentów (DeepSWE, ProgramBench)]] [[Harness|Self-recovery agenta]]

**Kontekst / Problem:**
Kun Chen reaguje na szeroko rozprzestrzeniającą się technikę kompakcji kontekstu, która polega na selektywnym usuwaniu wyłącznie części wywołań narzędzi (tool calls), pozostawiając wszystkie wiadomości użytkownika i asystenta na stałe. Ostrzega, że mimo popularności tego podejścia jest ono fundamentalnie wadliwe i proponuje weryfikację empiryczną zamiast wiary w anegdotyczne sukcesy.

**Rada inżynierska:**
Prawdziwa kompakcja musi redukować CAŁY kontekst — w tym wiadomości user/assistant — a nie tylko wycinać wywołania narzędzi. Jeśli podsumowanie zamiast się kurczyć, rośnie monotonicznie, to przy długotrwałych zadaniach kontekst i tak się wyczerpie i agent nie będzie mógł się samodzielnie podnieść (self-recover) — co znosi główny cel kompakcji, czyli uwolnienie okna kontekstowego. Dodatkowo trzeba uwzględnić ekonomię cache'u: pozostawienie zbyt wielu elementów w kontekście sprawia, że kolejne zapytanie staje się ogromnym, niecache'owanym promptem, który bywa droższy niż kontynuacja długiej, zacache'owanej sesji — co znosi drugi cel kompakcji, czyli oszczędność kosztów. Zanim uznasz technikę za praktyczną, zmierz kompromis koszt/jakość na ewaluacjach (np. DeepSWE, ProgramBench) i podziel się wynikami.

**Uwaga / Anty-wzorzec:**
Selektywne usuwanie tylko tool calls przy trwałym zachowaniu wiadomości user/assistant: (1) podsumowanie kompakcji rośnie w nieskończoność zamiast maleć, co prowadzi do wyczerpania okna kontekstowego i braku możliwości samodzielnego odzyskania przez agenta; (2) pozostawia zbyt dużo treści w kontekście, zamieniając kolejny request w masywny uncached prompt — potencjalnie droższy niż dalsze korzystanie z długiej, zacache'owanej sesji. Anty-wzorzec: przyjmowanie popularnej techniki bez pomiaru tradeoffu koszt/wydajność.

> **Cytat:** *"umm.. since this is somehow spreading so widely, i feel obligated to point out that this is unfortunately a bad idea

the fundamental flaws -

1. it only selectively remove some tool calls. user and assistant messages are kept FOREVER, which means the compaction summary will only keep growing and never shrink. so long running tasks will eventually completely run out of context window and cannot self recover, defeating the primary purpose of compaction which is to free up the context window so the agent can keep going

2. this operation leaves a lot more stuff in the context window than a real compaction, which means the next request after doing this becomes a massive uncached prompt which in some cases even more expensive than letting the long cached session continue, which defeats the other purpose of compaction which is cost saving

i suggest running some evals such as deepswe, programbench etc to actually measure the cost and performance tradeoff and share it if you are truly convinced this is practical"*

---
