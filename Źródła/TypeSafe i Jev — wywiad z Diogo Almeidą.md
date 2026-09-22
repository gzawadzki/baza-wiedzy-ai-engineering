---
typ: źródło
aliases: [Jev — wywiad Latent Space, Diogo Almeida o System One]
tagi: [TypeSafe, Jev, system-one, kalibracja, agenci, routing, kv-cache]
źródła:
  - "[Latent Space — Jev: System One models for Prod, not God](https://www.latent.space/p/jev)"
  - "[TypeSafe — Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)"
  - "[TypeSafe — The Bitterest Lesson](https://typesafe.ai/blog/bitterest-lesson)"
  - "[TypeSafe Docs — System One](https://docs.typesafe.ai/concepts/system-one)"
  - "[TypeSafe Docs — How to build with System One](https://docs.typesafe.ai/concepts/how-to-build-with-system-one)"
  - "[TypeSafe Docs — Confidence](https://docs.typesafe.ai/confidence)"
  - "[TypeSafe Docs — Models](https://docs.typesafe.ai/models)"
  - "[TypeSafe Docs — Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13)"
  - "[Diogo Almeida — (KV) Cache Rules Everything Around Me](https://www.completeskeptic.com/p/kv-cache-rules-everything-around)"
sprawdzono: 2026-09-22
---

# TypeSafe i Jev — wywiad z Diogo Almeidą

## Status źródła

Wywiad Swyxa z Diogo Almeidą, CEO TypeSafe, opublikowany 21 września 2026 r. w Latent Space. To wartościowe **źródło pierwotne dla intencji projektowych, hipotez i zapowiedzi firmy**, ale nie niezależna ocena produktu. Poniżej rozdzielono:

- **fakt produktu** — potwierdzony w aktualnej dokumentacji lub publicznym interfejsie TypeSafe,
- **teza Diogo** — interpretacja, priorytet badawczy albo przewidywanie przedstawione w wywiadzie,
- **wniosek praktyczny** — synteza dla projektowania systemu, nie obietnica producenta.

Szczegółowy kontrakt API, prymitywy i ograniczenia wersji opisują [[Jev]] oraz [[TypeSafe — przewodnik praktyczny]]. Ta notatka zachowuje głównie tezy, które wywiad dodaje do dokumentacji.

## Synteza

Najważniejsza myśl brzmi: model dla oprogramowania nie powinien udawać kompletnego programu ani współpracownika. Ma dostarczać mały, probabilistyczny osąd w miejscu, w którym zwykły kod nie radzi sobie z semantyką. Kod nadal posiada stan, politykę, progi i skutki uboczne.

Z tego wynikają cztery konsekwencje:

1. **Interfejs ważniejszy od swobodnej generacji.** Program definiuje dopuszczalne odpowiedzi, a model zwraca typowaną decyzję i rozkład prawdopodobieństwa.
2. **Niezawodność powstaje przez dekompozycję.** Duże polecenie zastępuje się zestawem małych, mierzalnych pytań; ich wyniki łączy kod.
3. **Kalibracja jest sterowaniem ryzykiem, nie certyfikatem prawdy.** Pozwala dobrać próg automatyzacji lub eskalacji, lecz nadal wymaga ewaluacji domenowej.
4. **Koszt agenta zależy od przepływu kontekstu.** Routing i subagenci nie są automatycznie tańsi: przekazanie długiego kontekstu do innego modelu niszczy korzyść z istniejącego KV-cache.

## Programowalna AI i System One

**Fakt produktu.** TypeSafe określa System One jako modele przeznaczone do szybkich, ustrukturyzowanych decyzji konsumowanych bezpośrednio przez kod. Jev przyjmuje stan i pytania, a zwraca typowane odpowiedzi z prawdopodobieństwami; nie jest generatorem tekstu. Oficjalny opis ujmuje ten kontrakt jako „nieustrukturyzowany stan → typowane decyzje probabilistyczne”. [Źródła: [System One](https://docs.typesafe.ai/concepts/system-one), [launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev)]

**Teza Diogo.** Dzisiejsze LLM-y są bardzo zdolne, ale ich interfejs — generowany ciąg tekstu — źle pasuje do automatyzacji głęboko wewnątrz programu. System One ma być „kognitywnym rdzeniem” lub prymitywem podobnym do zależności programistycznej: wąskim, obserwowalnym i możliwym do wielokrotnego złożenia. Nazwa opisuje kształt zadań, przy których obecne modele działają dobrze; nie stanowi formalnej granicy zdolności.

**Wniosek praktyczny.** Jev nie zastępuje [[Harnessy|harnessu]] ani LLM-u wykonującego otwartą pracę. Jest kandydatem na komponent wewnątrz procesu: rozpoznaje intencję, wybiera handler lub skill, ocenia ryzyko, filtruje kontekst albo sprawdza wynik. Generowanie, narzędzia i zapis plików pozostają po stronie agenta i kodu.

## Kalibracja, RLHF i RLCD

**Fakt produktu.** `Noul` zwraca prawdopodobieństwo odpowiedzi „tak”; `Choice` i `Score` zwracają rozkład oraz `confidence`, które streszcza jego koncentrację. Dokumentacja ostrzega, że `confidence` nie mierzy poprawności całego workflow i nie jest zgodą na wykonanie ryzykownej akcji. Progi należy stroić na własnych danych i konsekwencjach błędu. [Źródła: [Confidence](https://docs.typesafe.ai/confidence), [How to build](https://docs.typesafe.ai/concepts/how-to-build-with-system-one)]

**Teza TypeSafe.** Firma przeciwstawia cele treningowe w następujący sposób:

| Kierunek | Cel w ujęciu TypeSafe | Ograniczenie istotne dla automatyzacji |
| --- | --- | --- |
| RLHF | odpowiedź preferowana przez człowieka | preferencja może nagradzać pewny i przekonujący tekst zamiast uczciwej niepewności |
| RLVR | wynik z nagrodą możliwą do programowego sprawdzenia | najlepiej pasuje do problemów z tanim weryfikatorem, np. matematyki lub kodu |
| RLCD | skalibrowana decyzja dla programu | wymaga sprawdzenia kalibracji i jakości w konkretnej domenie |

Diogo wiąże RLHF z mode droppingiem, nadmierną pewnością i optymalizacją odpowiedzi „dobrze wyglądającej” dla człowieka. Jest to **argument badawczy TypeSafe**, nie bezsporny fakt o każdym systemie RLHF. TypeSafe nazywa własny kierunek *Reinforcement Learning for Calibrated Decisions*, lecz w chwili wywiadu nie opublikował pracy opisującej algorytm i dane treningowe. Nie da się więc niezależnie ocenić RLCD na podstawie samego wywiadu; publicznie weryfikowalne są kontrakt API, zachowanie modeli i wyniki testów użytkownika. [Źródła: [wywiad](https://www.latent.space/p/jev), [launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev)]

Powiązanie z [[Weryfikator]] jest operacyjne: osąd modelu może wskazać, **czy** uruchomić regułę, dodatkowy test, człowieka albo droższy model, ale sam rozkład prawdopodobieństwa nie zastępuje weryfikacji wyniku.

## „Zadanie > dane > compute > algorytmy”

**Teza Diogo.** Rozszerzenie „gorzkiej lekcji” Suttona brzmi: najpierw trzeba wybrać właściwe zadanie optymalizacyjne, potem zbudować właściwe dane, następnie skalować compute, a dopiero potem przeceniać szczegóły algorytmu. Zły cel może mieć piękne krzywe uczenia i nadal tworzyć bezużyteczny produkt.

TypeSafe ilustruje to historią InstructGPT: zmiana zadania z przewidywania kolejnego tokenu na podążanie za instrukcją dała większą wartość użytkową niż samo skalowanie bazowego modelu. Dla Jev nowym „north star” ma być decyzja konsumowana przez program, a nie odpowiedź preferowana w rozmowie. To opublikowana filozofia projektowa firmy, nie uniwersalne prawo ML. [Źródło: [The Bitterest Lesson](https://typesafe.ai/blog/bitterest-lesson)]

**Wniosek praktyczny.** Przed wyborem modelu należy zdefiniować akcję programu, koszt błędu i obserwowalny wynik. Dopiero wtedy projektuje się pytania, dane i ewaluację. Benchmark oderwany od docelowego grafu obliczeń może premiować inny problem niż ten, który ma rozwiązać produkt.

## API jako narzędzie dekompozycji

**Fakt produktu.** `state`, `instructions` i `criteria` mogą zachować strukturę JSON. Niezależne pytania nad wspólnym stanem można wysłać razem i ocenić równolegle. `Choice`, `Noul` i `Score` są odpowiednio zbliżone do programistycznych operacji: wyboru gałęzi, bramki warunkowej oraz sortowania lub progowania. Szczegóły są w [[TypeSafe — przewodnik praktyczny]]. [Źródła: [State](https://docs.typesafe.ai/concepts/state), [Primitives](https://docs.typesafe.ai/primitives), [Parallel questions](https://docs.typesafe.ai/cookbooks/parallel_questions)]

**Teza Diogo.** Dobrym poziomem podziału jest „najmniejsza samodzielnie użyteczna jednostka semantyczna”. Zamiast pytać „czy odrzucić?”, lepiej osobno zmierzyć konkretne powody odrzucenia, a politykę połączyć w kodzie. Wtedy błąd naprawia się przez dodanie brakującego warunku, testu i progu, zamiast rozbudowywania globalnego promptu.

**Wniosek praktyczny.** Taki układ daje lepszą lokalizację awarii:

1. brak dowodu w `state`,
2. źle zdefiniowane pytanie lub kryteria,
3. błąd osądu modelu,
4. błędny próg lub kompozycja w kodzie,
5. awaria wykonania akcji.

Typowany wynik usuwa klasę błędów parsowania, ale nie gwarantuje prawdziwości. Dekompozycja ma sens wtedy, gdy każdy wynik można osobno ocenić i wykorzystać; sztuczne rozbijanie zależnego rozumowania może pogorszyć jakość.

## Niezawodność, odporność i wersjonowanie

**Teza Diogo.** Ważniejszym celem niż ścisły determinizm jest **odporność semantyczna**: podobne wejścia powinny prowadzić do podobnych wyników. Stały seed ułatwia test jednostkowy, lecz nie wykrywa kruchości na nieistotne zmiany, np. losowy identyfikator w stanie. Dlatego testy powinny obejmować parafrazy i perturbacje, a nie tylko powtórzenie identycznego requestu.

**Fakt produktu.** API zwraca identyfikator użytego modelu. Aliasy, takie jak `jev-latest`, mogą zostać skierowane na nową wersję, a lista znanych ograniczeń jest wersjonowana. Workflow z dostrojonymi progami powinien przypiąć konkretny model, logować wersję i przeprowadzać ponowną ewaluację przy migracji. Aktualne identyfikatory i limity należy sprawdzać w [Models](https://docs.typesafe.ai/models) oraz [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13).

**Zapowiedź z wywiadu.** Diogo deklaruje, że wdrożona wersja modelu nie będzie po cichu zmieniana, lecz jednocześnie nie obiecuje długiego wsparcia każdej wersji. Rozważa LTS, różne rozmiary modeli i kaskady, ale nie przedstawia ich jako dostępnych funkcji. Architektura produkcyjna nie powinna zależeć od tych zapowiedzi.

## Trwałe rodziny zastosowań

Wywiad grupuje zastosowania w cztery rodziny, zgodne z oficjalnym opisem produktu:

1. **„Dark data”** — masowa ocena istniejących tekstów i rekordów, których nie opłacało się dotąd analizować LLM-em.
2. **Pętla czasu rzeczywistego** — decyzje w interfejsie, grze, asystencie lub sterowaniu, gdy opóźnienie ma znaczenie.
3. **„Verify everything”** — ocena cytowań, pól ekstrakcji, ryzyka, promptów i wyników generatywnego LLM-u; naturalne miejsce dla [[Weryfikator]].
4. **Inteligentne oprogramowanie** — semantyczne `if`, routing, ranking i dobór funkcji w zwykłym grafie programu.

Są to kategorie projektowe, nie dowód jakości w dowolnej domenie. Przykłady producenta obejmują także demonstracje Doom i wikiracing, lecz sam Diogo zaznacza w wywiadzie, że efektowny demo nie zastępuje testu niezawodności. [Źródło: [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)]

## KV-cache: routing i subagenci

**Teza techniczna Diogo.** W długiej sesji agenta duża część rachunku może pochodzić z wielokrotnego odczytu rosnącego kontekstu. Agent wykonuje pętlę model → narzędzie → model, a każdy kolejny krok korzysta z historii. Cache ogranicza ponowne obliczenia prefilla, ale jego ekonomia i rozliczenie nadal wpływają na koszt sesji. Dokładne udziały procentowe w artykule zależą od cennika, cache hit rate i badanego śladu, więc nie są stałą architektoniczną. [Źródło: [KV Cache Rules Everything Around Me](https://www.completeskeptic.com/p/kv-cache-rules-everything-around)]

Najważniejsze implikacje:

- **Routing między modelami traci istniejący cache.** KV-cache jest zależny od konkretnego modelu; drugi model musi ponownie przetworzyć przekazany kontekst. Oszczędność na tańszym kroku może być mniejsza niż koszt przekazania historii.
- **Subagent pomaga, gdy dostaje mały brief.** Delegacja typu „znajdź X i zwróć 200 tokenów” izoluje dużą eksplorację od kontekstu rodzica. Subagent, który musi dostać całą historię rodzica, może jedynie powielić koszt stanu.
- **Dobra granica agenta jest granicą stanu.** Do podzadania przekazuje się minimalny kontrakt, potrzebne pliki i oczekiwany wynik, a nie pełny transcript sesji. To uzupełnia zasady z [[Harnessy]].
- **Koszt trzeba mierzyć per trajektoria.** Ważne są liczba wywołań narzędzi, długość narastającego kontekstu, hit rate cache, rozmiar briefu subagenta i długość wyniku — nie tylko cena tokenu wyjściowego.

**Hipoteza, nie funkcja produktu.** W wywiadzie Diogo proponuje użycie tanich osądów do wyszukiwania właściwego fragmentu historii, wyboru podzadania, koordynacji zapisów lub nawigacji po drzewie zadań. To kierunek badawczy „agentów uwolnionych od tyranii KV-cache”, a nie obecna gwarancja Jev.

## Co zachować, a czego nie przenosić bez testu

**Zachować:** kod jako właściciel polityki; małe mierzalne osądy; jawna niepewność; osobna walidacja domenowa; przypięta wersja modelu; testy perturbacyjne; routing oparty na koszcie całej trajektorii; subagenci z wąskim kontraktem.

**Nie przenosić bez testu:** deklarowane przewagi szybkości i kosztu, tezę o pełnej przewadze RLCD nad RLHF, ogólne stwierdzenie „subagenci nie działają”, zapewnienia o przyszłym LTS, automatycznym fine-tuningu lub nowych klasach modeli oraz prognozy ekonomiczne. Są to wyniki producenta, uproszczenia zależne od obciążenia albo zapowiedzi.

## Powiązania

- [[Jev]] — bieżący kontrakt modelu, prymitywy, limity i sprostowania.
- [[TypeSafe — przewodnik praktyczny]] — wzorce API, cookbooki i checklista wdrożenia.
- [[Harnessy]] — miejsce Jev wewnątrz agenta oraz granice kontekstu subagentów.
- [[Weryfikator]] — bramki jakości, eskalacja i rozdzielenie osądu od sprawdzenia wyniku.
