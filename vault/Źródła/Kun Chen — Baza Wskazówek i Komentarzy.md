---
autor: Kun Chen (@kunchenguid)
źródło: https://x.com/kunchenguid
wygenerowano: 2026-09-23 01:14
typ: synteza-wiedzy
tagi: [kun-chen, ai-engineering, prompt-engineering, twitter-extract]
---

# Kun Chen (@kunchenguid) — Baza Wskazówek i Komentarzy

> Destylacja praktycznych porad, heurystyk inżynierskich i komentarzy technicznych Kuna Chena z Twittera/X. Wyciągnięto 7 wartościowych wpisów.

## Spis kategorii

- [Prompt Architecture / Ewaluacja systemów agentowych](#prompt-architecture--ewaluacja-systemów-agentowych) (1)
- [Weryfikacja i code review w procesie z AI](#weryfikacja-i-code-review-w-procesie-z-ai) (1)
- [Obserwacje zachowania modeli / Prompt Architecture](#obserwacje-zachowania-modeli--prompt-architecture) (1)
- [Harness / zarządzanie kontekstem agenta (compaction)](#harness--zarządzanie-kontekstem-agenta-(compaction)) (1)
- [Zarządzanie kontekstem / kompakcja sesji agenta](#zarządzanie-kontekstem--kompakcja-sesji-agenta) (1)
- [Zarządzanie kontekstem / Harness agentowy](#zarządzanie-kontekstem--harness-agentowy) (1)
- [Zarządzanie kontekstem / Harness i agenci](#zarządzanie-kontekstem--harness-i-agenci) (1)

---

## Prompt Architecture / Ewaluacja systemów agentowych

### Ewaluacja agentów: mierz rework i rezultat, nie jakość pojedynczego promptu

- **Data:** `Tue Sep 22 07:10:43 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102294506062385364)
- **Rodzaj:** Komentarz w dyskusji (@kryptm4n)
- **Powiązane pojęcia:** [[Prompt Architecture]] [[Harness|Agent Harness]] [[Firstmate i Agenci Wykonawczy|Leaf Node Agent]] [[Firstmate i Agenci Wykonawczy|Firstmate / Orkiestracja Agentów]] [[Rework Rate|Ewaluacja Agentów]] [[Rework Rate]] [[Interpretable Context Methodology|Human-in-the-loop]] [[Firstmate i Agenci Wykonawczy|Skalowanie systemów agentowych]]

**Kontekst / Problem:**
Kun odpowiada na pytanie @kryptm4n o porównanie jakości promptów między ręcznym pisaniem promptów do agenta-liścia a promptami generowanymi przez 'firstmate' (warstwa orkiestracji/nadzoru). Problem: jak sensownie porównać skuteczność obu podejść, skoro w jednym z nich prompt nigdy nie istnieje w izolowanej, finalnej formie.

**Rada inżynierska:**
Nie da się uczciwie porównywać jakości promptów, jeśli jedno z podejść jest z natury iteracyjne — przy bezpośredniej pracy z agentem-liściem inżynier nie pisze pełnego wymagania z góry i nie oczekuje autonomicznego wykonania, tylko steruje iteracyjnie, więc często nie powstaje żaden pojedynczy 'prompt' porównywalny z tym, co wygeneruje warstwa orkiestracji. Praktyczniejsza metryka to rezultat końcowy oraz częstość reworku (ile poprawek trzeba wprowadzić później). Jakościowo: bezpośrednie sterowanie agentem daje lepsze wyniki szybciej, ale nie skaluje się (pochłania czas); warstwa orkiestracji skaluje, ale generuje okazjonalne misalignmenty wymagające korekty. To ten sam tradeoff co między zarządzaniem dużą organizacją ludzką a robieniem wszystkiego samemu.

**⚠️ Pułapka / Anty-wzorzec:**
Oczekiwanie, że prompt do agenta-liścia da się porównać 1:1 z promptem generowanym przez warstwę orkiestracji — to błąd metodologiczny, bo tryb pracy iteracyjnej nie produkuje porównywalnego artefaktu. Drugi anty-wzorzec: ewaluowanie promptu w izolacji zamiast mierzenia outcome'u i kosztu poprawek.

> **Cytat:** *"this is a very good question and i have not done a dedicated evaluation on just the quality of the prompts — it’s tricky because when i talk directly to a leaf node agent i don’t attempt to write a full requirement upfront and expect autonomous execution. i typically end up doing it a lot more iteratively, so often times i don’t have a single “prompt” that’s comparable to what firstmate would write — i think what’s more practical is to evaluate the outcome, and how often rework happens. i haven’t quantified this but it’s a good thing to look into. qualitatively i definitely think whenever i directly talk to a leaf node agent i can steer it more closely and get better results faster - but i end up spending a lot of time and it doesn’t scale. firstmate helps me scale but occasionally there will be misalignment and needs correction later on. much like the tradeoff between managing a large human organization vs doing everything myself"*

---

## Weryfikacja i code review w procesie z AI

### Kiedy stosować no-mistakes: test „czy zleciłbym to człowiekowi do code review?”

- **Data:** `Tue Sep 22 03:31:40 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102239379536433551)
- **Rodzaj:** Komentarz w dyskusji (@EthanClinick)
- **Powiązane pojęcia:** [[Code Review]] [[Weryfikacja krokowa]] [[Code Review|AI Code Review]] [[Selektywna weryfikacja kodu|No-mistakes]] [[Harness]]

**Kontekst / Problem:**
Kun Chen odpowiada @EthanClinick, prostując założenie, że każda zmiana wymaga dodatkowej weryfikacji typu no-mistakes. Wskazuje prostą heurystykę decyzyjną: jeśli nie poprosiłbyś człowieka o code review danej zmiany, prawdopodobnie nie potrzebujesz też no-mistakes.

**Rada inżynierska:**
Nie każdą zmianę należy przepuszczać przez dodatkowy, zewnętrzny proces weryfikacji AI. Stosuj go selektywnie: tylko do zmian, które normalnie skierowałbyś do code review przez człowieka. To pozwala uniknąć niepotrzebnego narzutu i szumu weryfikacyjnego.

**⚠️ Pułapka / Anty-wzorzec:**
Anty-wzorzec: automatyczne uruchamianie no-mistakes / zewnętrznego weryfikatora dla każdej, nawet trywialnej zmiany. Prowadzi to do marnowania czasu, fałszywych alarmów i rozmycia odpowiedzialności za code review.

> **Cytat:** *"no - not every change! i talked about this in more depth in my latest video but tl;dr is you can ask yourself "would i ask another human to do code review for this change" and if the answer is no, then you probably don't need no-mistakes"*

---

## Obserwacje zachowania modeli / Prompt Architecture

### Grok 4.7 jako firstmate: ścisłe trzymanie się system promptu, stabilność vs 'spiky' modele i konserwatyzm działania

- **Data:** `Tue Sep 22 03:11:03 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102234191639257399)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|System Prompt Adherence]] [[Stabilność modeli i przestrzeganie promptu|Model Stability vs Spikiness]] [[Stabilność modeli i przestrzeganie promptu|Conservative Agent Behavior]] [[Stabilność modeli i przestrzeganie promptu|Benchmark Skepticism]] [[Rework Rate|Harness Evaluation]] [[Firstmate Agent]] [[CI Check Bypass Confirmation]] [[Stabilność modeli i przestrzeganie promptu|Model Cost Latency Tradeoff]]

**Kontekst / Problem:**
Kun Chen opisuje jednodniowe obserwacje z używania Grok 4.7 jako swojego agenta 'firstmate' (głównego asystenta wykonawczego). Odnosi się do dwóch typów doniesień, które odrzuca: (1) raportów opartych wyłącznie o publiczne benchmarki (te same benchmarki miały wskazywać Opus 5 > Fable, co okazało się bezużyteczne), oraz (2) porównań modeli przez pryzmat gier 3D, które nie są prawdziwą pracą, a jedynie materiałem na social media. W zamian podaje jakościowe różnice zaobserwowane w realnym użyciu produkcyjnym.

**Rada inżynierska:**
Oceniaj modele na podstawie realnego użycia w swoim harnessie, nie benchmarków ani demówek. Kluczowa różnica Grok 4.7: wyjątkowo wiernie wykonuje system prompt — dopiero ten model ujawnił zachowania zapisane w prompcie firstmate, których żaden inny model nie egzekwował wystarczająco ściśle (np. żądanie wskazania konkretnych czerwonych checków CI, które użytkownik zgadza się pominąć, oraz odmowa wykonania prostego 'yolo'). To pokazuje, że instrukcje warunkowe i wymagania weryfikacyjne w system promptcie mogą pozostawać uśpione na słabszych modelach i aktywować się dopiero na modelu o wysokiej zgodności z promptem. Drugi wniosek: preferuj modele 'stabilne' (przewidywalne, bez dużych wahań jakości) nad 'spiky' (genialne momenty przeplatane głupimi wpadkami) — przewidywalność buduje zaufanie szybciej niż okazjonalny błysk. Trzeci: model konserwatywny (pytający przed działaniem) jest bezpieczniejszy w produkcji, bo wiele przypadków 'oczywistych' w rzeczywistości jest niejednoznacznych.

**⚠️ Pułapka / Anty-wzorzec:**
Dwa anty-wzorce: (1) wyrabianie opinii o modelu na podstawie publicznych benchmarków lub porównań przez gry 3D — to nie odzwierciedla prawdziwej pracy i prowadzi do błędnych decyzji (przykład: benchmarki wskazały Opus 5 > Fable, co Kun uznaje za bezwartościowe); (2) zakładanie, że model wykonuje wszystkie instrukcje z system promptu — słabsze modele mogą je ignorować, przez co zapisane reguły weryfikacji/bezpieczeństwa pozostają nieaktywne. Dodatkowo pułapka kosztowa: Grok 4.7 jest zauważalnie wolniejszy i droższy niż 4.5 (szybsze drenowanie quota), co trzeba uwzględnić przy wyborze modelu domyślnego.

> **Cytat:** *"ignore the reports that say "it's terrible" and the only thing they reference is a public benchmark. the same benchmarks told us opus 5 was better that fable - they are useless ... also ignore the reports that compare models with 3d games - that's not real work ... 1. it follows system prompt very, very closely ... i traced it and it's indeed how i instructed it in firstmate's system prompt, but none of the other models followed it closely enough to make this behavior visible - grok 4.7 is the first to pick that up ... 2. it's very "stable" ... if you've used astra then you know what a "spiky" model is. it can have some genius moments but you occasionally also wonder "how could it be so dumb and doesn't get me". grok 4.7 is the opposite of that ... 3. it's a conservative model. it doesn't like to take actions without asking, and would explicitly say so ... 4. it's a bit slower and costs more than 4.5, visibly"*

---

## Harness / zarządzanie kontekstem agenta (compaction)

### Delegowanie momentu kompakcji kontekstu do harnessu/agenta (Jev)

- **Data:** `Mon Sep 21 03:34:19 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101877657927655730)
- **Rodzaj:** Komentarz w dyskusji (@kunchenguid)
- **Powiązane pojęcia:** [[Context Compaction|Context compaction]] [[Harness]] [[Context Compaction|Zarządzanie kontekstem agenta]] [[Bezpieczny punkt kompaktowania|Automatyczne triggery w agentach]]

**Kontekst / Problem:**
Odpowiedź Kuna w wątku o kompakcji kontekstu w workflow agentowym (m.in. Claude Code). Rozmówca prawdopodobnie proponował ręczne strategie decydowania o tym, kiedy kompaktować kontekst. Kun wskazuje alternatywę, którą sam stosuje: zamiast samemu ustalać moment kompakcji, pozwala, by zrobił to 'Jev' — czyli warstwa harnessu/agenta sygnalizuje, kiedy kontekst wymaga kompakcji.

**Rada inżynierska:**
Nie decyduj ręcznie o momencie kompakcji kontekstu — pozwól, aby harness/agent sam zgłosił, kiedy kontekst wymaga kompaktowania (w praktyce: trigger automatyczny na podstawie zapełnienia/zużycia kontekstu). Zdjęcie tej decyzji z człowieka eliminuje błędne osądy 'teraz czy później' i przenosi ją do warstwy, która ma realny podgląd na stan kontekstu.

**⚠️ Pułapka / Anty-wzorzec:**
Ręczne wywoływanie kompakcji w złym momencie: zbyt wcześnie ucina kontekst jeszcze potrzebny do rozumowania, zbyt późno prowadzi do degradacji/utraty spójności przez przepełniony kontekst. Poleganie na subiektywnym osądzie zamiast na sygnale z harnessu.

> **Cytat:** *"oh alternatively, which is what i do right now - let Jev tell you when to compact"*

---

## Zarządzanie kontekstem / kompakcja sesji agenta

### Ręczne etykietowanie checkpointów sesji i kryterium "safe checkpoint"

- **Data:** `Fri Sep 18 20:25:20 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101044924301156365)
- **Rodzaj:** Komentarz w dyskusji (@mktpavlenko)
- **Powiązane pojęcia:** [[Context Compaction]] [[Bezpieczny punkt kompaktowania|Checkpointing sesji agenta]] [[Persistencja stanu agenta]] [[Eval Set z realnych sesji|Ground truth w ewaluacji agentów]] [[Eval Set z realnych sesji|Manual labeling]]

**Kontekst / Problem:**
Kun Chen odpowiada na wpis @mktpavlenko, wyjaśniając metodologię budowy zbioru checkpointów do kompakcji kontekstu sesji agenta. Problem: jak automatycznie lub półautomatycznie decydować, w którym momencie sesji można bezpiecznie uciąć/kompaktować kontekst, nie tracąc informacji potrzebnych do dalszego działania.

**Rada inżynierska:**
Nie ufaj heurystykom 'rozmiar kontekstu > próg' jako sygnałowi do kompakcji. Definicja bezpiecznego checkpointu powinna być operacyjna: checkpoint jest 'safe' wtedy i tylko wtedy, gdy dalsza część sesji nie potrzebuje niczego z wcześniejszej części, co nie zostało zapisane (persisted). W praktyce buduj ground truth przez ręczne etykietowanie checkpointów — dopiero na takim zbiorze możesz walidować automatyczne detektory momentu kompakcji.

**⚠️ Pułapka / Anty-wzorzec:**
Automatyczne wyznaczanie punktów kompakcji na podstawie samych proxy (np. liczby tokenów, liczby tur) bez sprawdzenia, czy niezpersistowane informacje z wcześniejszej sesji są jeszcze potrzebne — prowadzi do cichej utraty kontekstu i halucynacji w dalszej części sesji.

> **Cytat:** *"@mktpavlenko all the checkpoints were manually labeled by myself and "safe" checkpoints were determined by looking at whether the rest of the session indeed needs anything in the prior session that's not persisted"*

---

## Zarządzanie kontekstem / Harness agentowy

### Nie stosuj „instant compaction” — kompaktowanie kontekstu to problem klasyfikacji bezpiecznego punktu

- **Data:** `Fri Sep 18 19:53:16 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101036854925779291)
- **Rodzaj:** Komentarz w dyskusji (@gehariharan)
- **Powiązane pojęcia:** [[Context Compaction]] [[Context Compaction|Zarządzanie kontekstem agenta]] [[Bezpieczny punkt kompaktowania]] [[Bezpieczny punkt kompaktowania|Klasyfikacja stanu agenta]] [[Harness|Anty-wzorce harnessu agentowego]]

**Kontekst / Problem:**
Kun Chen odpowiada @gehariharan w wątku o strategiach kompaktowania kontekstu (context compaction) w agentach LLM. Ktoś zaproponował lub rozważał podejście „instant compaction” — natychmiastowe, bezwarunkowe streszczanie/kompaktowanie kontekstu. Kun ostrzega, że to zły pomysł i wskazuje właściwy sposób myślenia o tym problemie.

**Rada inżynierska:**
Nie kompaktuj kontekstu natychmiast i bezwarunkowo. Kompaktowanie należy modelować jako zadanie klasyfikacji: czy agent znajduje się w punkcie, w którym kompaktowanie jest bezpieczne (np. na granicy zadania, po zakończeniu kroku, bez otwartych zależności)? Dopiero po spełnieniu warunku bezpieczeństwa wykonuj kompaktowanie. To decyzja warunkowa, nie mechaniczna akcja wyzwalana natychmiast.

**⚠️ Pułapka / Anty-wzorzec:**
„Instant compaction” — agresywne, natychmiastowe streszczanie kontekstu bez sprawdzenia, czy agent jest w bezpiecznym punkcie. Prowadzi do utraty istotnego stanu pośredniego i zerwania ciągłości rozumowania, bo kompaktowanie w złym momencie obcina kontekst potrzebny do dalszego kroku.

> **Cytat:** *"@gehariharan don't do the "instant compaction" thing. i commented on the post - it's a bad idea

this is just plain and simple classifying whether you are sitting at a place where it's safe to compact"*

---

## Zarządzanie kontekstem / Harness i agenci

### compact-adviser: klasyfikator momentu bezpiecznej kompakcji sesji (precision→recall w miarę zapełniania kontekstu)

- **Data:** `Fri Sep 18 19:36:40 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101032677940117875)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Context Compaction|Context Window Management]] [[Context Compaction|Kompakcja sesji (/compact)]] [[Bezpieczny punkt kompaktowania|Task Boundary Detection]] [[Bezpieczny punkt kompaktowania|Precision-Recall Tradeoff]] [[Harness|Agent Harness]] [[Prompt Architecture|Prompt Hillclimbing]] [[Eval Set z realnych sesji]] [[Harness|Agent Plugin]]

**Kontekst / Problem:**
Kun Chen odpowiada na powtarzające się pytanie „kiedy powinienem zrobić /compact w sesji agenta?”. Problem: nie istnieje prosta reguła, bo decyzja zależy od tego, czy przyszłe akcje agenta będą potrzebować szczegółowego kontekstu obecnego okna. Rozwiązanie: plugin agentowy 'compact-adviser' oparty na klasyfikatorze Jev, dostępny w Claude i pi, który wykrywa, czy jesteśmy na granicy zadania (task boundary) bezpiecznej do kompakcji.

**Rada inżynierska:**
Traktuj decyzję o kompakcji jako problem klasyfikacji z zadaniową granicą, a nie stały próg tokenów. Buduj prywatny eval set z realnych sesji i ręcznie etykietuj checkpointy jako safe/unsafe, potem hillclimbuj prompt klasyfikatora, aż wyniki będą dobre. Kluczowa reguła: dynamicznie przesuwaj cel optymalizacji — przy małym wypełnieniu okna optymalizuj PRECISION (nie kompaktuj przedwcześnie i nie trać potrzebnego kontekstu), a w miarę zapełniania okna stopniowo przechodź do RECALL (nie przegap okazji do kompakcji), bo koszt braku kompakcji rośnie, a na końcu agent i tak będzie zmuszony kompaktować. Udostępniaj dwa tryby: 'hint' (sygnał + decyzja użytkownika) oraz 'auto' (kompakcja natychmiast, gdy klasyfikator uzna to za bezpieczne).

**⚠️ Pułapka / Anty-wzorzec:**
Stosowanie jednej statycznej reguły / sztywnego progu kontekstu do decyzji o kompakcji — ignoruje to zależność od przyszłych potrzeb kontekstowych i prowadzi albo do przedwczesnej utraty szczegółów, albo do przepłynięcia okna. Drugi anty-wzorzec: optymalizacja wyłącznie pod precision albo wyłącznie pod recall, bez uwzględnienia fazy zapełnienia okna. Trzeci: brak własnego, ręcznie etykietowanego eval setu — ocena klasyfikatora „na wyczucie” zamiast na realnych sesjach.

> **Cytat:** *"there's no easy answer because it depends on how likely your future action will need detailed context in the existing window ... i built a private eval set from 40 real sessions and manually labeled all the safe vs unsafe checkpoints to evaluate this, and hillclimbed the Jev prompt till it performed quite well ... optimize for precision (not triggering a compaction prematurely) when context window is small - and gradually shift to optimize for recall (not missing an opportunity to compact) when context window fills up, because the cost of not compacting becomes higher, and at the end the agent will be forced to compact anyway"*

---
