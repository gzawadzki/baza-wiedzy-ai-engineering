---
autor: Kun Chen (@kunchenguid)
źródło: https://x.com/kunchenguid
wygenerowano: 2026-09-23 01:39
typ: synteza-wiedzy
tagi: [kun-chen, ai-engineering, prompt-engineering, twitter-extract]
---

# Kun Chen (@kunchenguid) — Baza Wskazówek i Komentarzy

> Destylacja praktycznych porad, heurystyk inżynierskich i komentarzy technicznych Kuna Chena z Twittera/X. Wyciągnięto 18 wartościowych wpisów.

## Spis kategorii

- [Inżynieria promptów / Systemy agentowe](#inżynieria-promptów--systemy-agentowe) (1)
- [Praktyki weryfikacji / Code Review](#praktyki-weryfikacji--code-review) (1)
- [Obserwacje zachowania modeli / Prompt Architecture](#obserwacje-zachowania-modeli--prompt-architecture) (1)
- [Orkiestracja multi-agentowa / Routing](#orkiestracja-multi-agentowa--routing) (1)
- [Zachowanie modeli / Prompt architecture](#zachowanie-modeli--prompt-architecture) (1)
- [Zarządzanie kontekstem / Harness](#zarządzanie-kontekstem--harness) (1)
- [Zarządzanie kosztami / Prompt caching / Higiena sesji agenta](#zarządzanie-kosztami--prompt-caching--higiena-sesji-agenta) (1)
- [Inżynieria produktu AI / ocena modeli](#inżynieria-produktu-ai--ocena-modeli) (1)
- [Harness / Zarządzanie kontekstem i sesją agenta](#harness--zarządzanie-kontekstem-i-sesją-agenta) (1)
- [Zarządzanie kontekstem / Harness agenta](#zarządzanie-kontekstem--harness-agenta) (1)
- [Context Engineering / zarządzanie oknem kontekstowym agenta](#context-engineering--zarządzanie-oknem-kontekstowym-agenta) (1)
- [Zarządzanie kontekstem / Prompt Caching](#zarządzanie-kontekstem--prompt-caching) (1)
- [Zarządzanie kontekstem / Kompakcja i okno kontekstowe agenta](#zarządzanie-kontekstem--kompakcja-i-okno-kontekstowe-agenta) (1)
- [Architektura systemów LLM / Wybór podejścia](#architektura-systemów-llm--wybór-podejścia) (1)
- [Weryfikacja i harness](#weryfikacja-i-harness) (1)
- [Architektura systemów AI / Agent Design](#architektura-systemów-ai--agent-design) (1)
- [Architektura harnessów i routing zadań / optymalizacja kosztów i latencji](#architektura-harnessów-i-routing-zadań--optymalizacja-kosztów-i-latencji) (1)
- [Architektura systemów agentowych / Routing modeli i koszty](#architektura-systemów-agentowych--routing-modeli-i-koszty) (1)

---

## Inżynieria promptów / Systemy agentowe

### Ocena promptów przez wyniki i rework zamiast izolowanej jakości

- **Data:** `Tue Sep 22 07:10:43 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102294506062385364)
- **Rodzaj:** Komentarz w dyskusji (@kryptm4n)
- **Powiązane pojęcia:** [[Prompt Architecture]] [[Firstmate Agent|Agent Orchestration]] [[Firstmate i Agenci Wykonawczy|Leaf Node Agent]] [[Firstmate Agent|Firstmate]] [[Rework Rate]] [[Prompt Architecture|Iterative Prompting]] [[Firstmate i Agenci Wykonawczy|Tradeoff skalowania]]

**Kontekst / Problem:**
Kun Chen odpowiada na pytanie o ocenę jakości promptów w kontekście agentów. Wyjaśnia, że bezpośrednia rozmowa z agentem (leaf node) jest iteracyjna i nie da się jej porównać do pojedynczego promptu pisanego przez orkiestratora (firstmate). Zamiast tego proponuje oceniać wyniki i częstotliwość poprawek (rework). Dzieli się obserwacją o kompromisie: bezpośrednie sterowanie daje lepsze rezultaty szybciej, ale nie skaluje się; firstmate skaluje, lecz czasem wymaga korekt.

**Rada inżynierska:**
Nie oceniaj jakości promptów w izolacji, zwłaszcza gdy pracujesz iteracyjnie z agentem. Zamiast tego mierz wynik końcowy i częstotliwość reworku (poprawek). Pamiętaj o tradeoffie: bezpośrednia iteracja z leaf node agentem daje lepszą kontrolę i szybsze rezultaty, ale nie skaluje się; użycie orkiestratora (np. firstmate) skaluje, ale może powodować niedopasowanie wymagań i konieczność późniejszych korekt.

**Uwaga / Anty-wzorzec:**
Próba oceny pojedynczego promptu w podejściu iteracyjnym jest myląca, ponieważ nie masz jednego 'promptu' do porównania. Brak kwantyfikacji reworku utrudnia obiektywną ocenę. Zakładanie, że orkiestrator zawsze napisze idealny prompt, prowadzi do niedopasowań i kosztownych poprawek.

> **Cytat:** *"this is a very good question and i have not done a dedicated evaluation on just the quality of the prompts

it’s tricky because when i talk directly to a leaf node agent i don’t attempt to write a full requirement upfront and expect autonomous execution. i typically end up doing it a lot more iteratively, so often times i don’t have a single “prompt” that’s comparable to what firstmate would write

i think what’s more practical is to evaluate the outcome, and how often rework happens. i haven’t quantified this but it’s a good thing to look into. qualitatively i definitely think whenever i directly talk to a leaf node agent i can steer it more closely and get better results faster - but i end up spending a lot of time and it doesn’t scale. firstmate helps me scale but occasionally there will be misalignment and needs correction later on. much like  the tradeoff between managing a large human organization vs doing everything myself"*

---

## Praktyki weryfikacji / Code Review

### Heurystyka stosowania 'no-mistakes' – kiedy potrzebny przegląd kodu

- **Data:** `Tue Sep 22 03:31:40 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102239379536433551)
- **Rodzaj:** Komentarz w dyskusji (@EthanClinick)
- **Powiązane pojęcia:** [[Weryfikacja krokowa]] [[Code Review]] [[Harness|Heurystyki inżynierskie]] [[Code Review|AI Code Review]]

**Kontekst / Problem:**
Kun Chen odpowiada na pytanie @EthanClinick, prawdopodobnie czy każda zmiana w kodzie wymaga użycia 'no-mistakes' (narzędzia/procesu weryfikacji). Wyjaśnia, że nie każda – podaje prostą heurystykę decyzyjną.

**Rada inżynierska:**
Nie każda zmiana wymaga dodatkowej weryfikacji (np. AI code review / 'no-mistakes'). Zadaj sobie pytanie: 'Czy poprosiłbym innego człowieka o code review tej zmiany?' Jeśli odpowiedź brzmi 'nie', to prawdopodobnie nie potrzebujesz 'no-mistakes'. Stosuj weryfikację selektywnie, proporcjonalnie do ryzyka i złożoności zmiany.

**Uwaga / Anty-wzorzec:**
Automatyczne uruchamianie weryfikacji/AI code review dla każdej, nawet błahej zmiany – marnuje zasoby, spowalnia proces i może prowadzić do zmęczenia weryfikacją (alert fatigue). Brak selektywności w stosowaniu narzędzi weryfikacyjnych.

> **Cytat:** *"no - not every change! i talked about this in more depth in my latest video but tl;dr is you can ask yourself "would i ask another human to do code review for this change" and if the answer is no, then you probably don't need no-mistakes"*

---

## Obserwacje zachowania modeli / Prompt Architecture

### Grok 4.7: ścisłe trzymanie się system promptu, stabilność vs 'spiky' modele i konserwatyzm w działaniu

- **Data:** `Tue Sep 22 03:11:03 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102234191639257399)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|System Prompt Fidelity]] [[Stabilność modeli i przestrzeganie promptu|Model Stability vs Spikiness]] [[Stabilność modeli i przestrzeganie promptu|Benchmarki są bezużyteczne]] [[Stabilność modeli i przestrzeganie promptu|Konserwatywne zachowanie agenta]] [[Interpretable Context Methodology|Human-in-the-loop]] [[TypeSafe — przewodnik praktyczny|Koszt i latencja modelu]] [[Firstmate Agent|Firstmate]]

**Kontekst / Problem:**
Kun Chen opisuje jednodniowe obserwacje z Grok 4.7 używanym jako jego 'firstmate' (agent główny). Odnosi się do dwóch typów doniesień, które odrzuca: (1) raportów opartych wyłącznie na publicznych benchmarkach, (2) porównań modeli przez pryzmat gier 3D. Zamiast tego podaje jakościowe różnice behawioralne zaobserwowane w realnej pracy produkcyjnej.

**Rada inżynierska:**
Oceniaj modele wyłącznie na podstawie realnej pracy, nie benchmarków ani demówek (gry 3D). Kluczowa różnica Grok 4.7: bardzo wiernie wykonuje system prompt — ujawnia zachowania, które były w prompcie, ale inne modele nie egzekwowały ich na tyle konsekwentnie, by stały się widoczne (np. żądanie wskazania konkretnych czerwonych checków CI do pominięcia, odmowa prostego 'yolo'). To znaczy, że dobrze zaprojektowany system prompt zaczyna realnie działać dopiero na modelu o wysokiej wierności instrukcjom. Preferuj modele 'stabilne' (przewidywalne, bez dużych wahań) nad 'spiky' (genialne momenty przeplatane głupimi wpadkami) — przewidywalność buduje zaufanie szybciej niż okazjonalny błysk.

**Uwaga / Anty-wzorzec:**
Dwa anty-wzorce: (1) wyciąganie wniosków o modelu z publicznych benchmarków — te same benchmarki twierdziły, że Opus 5 jest lepszy od Fable, co Kun uznaje za bezwartościowe; (2) porównywanie modeli przez zabawkowe zadania (gry 3D) — to nie jest prawdziwa praca, a jedynie materiał pod uwagę na social media. Dodatkowo: model konserwatywny (pytający przed działaniem) bywa uciążliwy, ale w praktyce wiele z tych pytań dotyczy rzeczywiście niejednoznacznych przypadków — wymuszanie 'idź dalej bez pytania' może być błędem. Uwaga też na koszt: Grok 4.7 jest wolniejszy i wyraźnie szybciej zużywa limit niż 4.5.

> **Cytat:** *"ignore the reports that say "it's terrible" and the only thing they reference is a public benchmark. the same benchmarks told us opus 5 was better that fable - they are useless. also ignore the reports that compare models with 3d games - that's not real work. it's made for attention on social media ... 1. it follows system prompt very, very closely ... i traced it and it's indeed how i instructed it in firstmate's system prompt, but none of the other models followed it closely enough to make this behavior visible - grok 4.7 is the first to pick that up ... 2. it's very "stable" ... if you've used astra then you know what a "spiky" model is. it can have some genius moments but you occasionally also wonder "how could it be so dumb and doesn't get me". grok 4.7 is the opposite of that ... 3. it's a conservative model. it doesn't like to take actions without asking, and would explicitly say so ... 4. it's a bit slower and costs more than 4.5, visibly."*

---

## Orkiestracja multi-agentowa / Routing

### Dedykowany router (Jev) zamiast decyzji routingowej podejmowanej przez LLM orkiestratora

- **Data:** `Mon Sep 21 04:57:11 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101898514523730033)
- **Rodzaj:** Komentarz w dyskusji (@CompleteSkeptic)
- **Powiązane pojęcia:** [[Firstmate Agent|Orkiestrator chief-of-staff]] [[Firstmate i Agenci Wykonawczy|Subagenty]] [[Jev|Routing zadań w systemach multi-agentowych]] [[Jev|LLM jako router]] [[Harness|Autoregresyjne podejmowanie decyzji]] [[TypeSafe — przewodnik praktyczny|Koszt i latencja routingu]]

**Kontekst / Problem:**
Kun odpowiada pod wpisem @CompleteSkeptic, w którym wymieniono listę problemów związanych z subagentami. Kun wskazuje, że jedno z tych wyzwań rozwiązał przy pomocy narzędzia Jev. Kontekst: architektura 'chief-of-staff' — orkiestrator, w której zakłada się, że każde istotne zadanie musi zostać wykonane przez subagenta. W takim układzie kluczowa staje się decyzja, do którego subagenta skierować zadanie.

**Rada inżynierska:**
W architekturze typu chief-of-staff (gdzie każde istotne zadanie idzie do subagenta) użyj dedykowanego routera (np. Jev) jako drop-in komponentu podejmującego decyzję routingową. Jest to znacznie wydajniejsze niż powierzanie routingu LLM-owi orkiestratora, który musi wczytać dużo danych i autoregresyjnie wygenerować decyzję. Rozdzielenie roli routingu od roli orkiestracji redukuje koszt i latencję decyzji o wyborze subagenta.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: pozwolenie, by LLM orkiestratora samodzielnie podejmował decyzję routingową poprzez czytanie obszernego kontekstu i autoregresyjne 'przemyślenie' wyboru. To marnuje tokeny, zwiększa latencję i wprowadza niepotrzebną wariancję w decyzji, którą można rozwiązać lżejszym, dedykowanym routerem.

> **Cytat:** *"i used Jev to solve one of the listed problems around subagents and it works really well

in a chief-of-staff style orchestrator, it’s assumed that any substantial task has to be done by a subagent - in this scenario, Jev becomes a perfect drop-in router that can make the routing decision in a much more efficient way than letting the orchestrator LLM do it by reading a bunch of data and autoregressive its decision"*

---

## Zachowanie modeli / Prompt architecture

### Prompt caching jako ukryty czynnik kształtujący zachowanie modelu

- **Data:** `Mon Sep 21 03:57:28 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101883484696653984)
- **Rodzaj:** Komentarz w dyskusji (@elvissun)
- **Powiązane pojęcia:** [[Prompt Architecture|Prompt caching]] [[Prompt Architecture|Prompt architecture]] [[Prompt Architecture|Stabilny prefiks promptu]] [[TypeSafe — przewodnik praktyczny|Koszt i opóźnienie inferencji]] [[Prompt Architecture|Zachowanie modelu a struktura promptu]]

**Kontekst / Problem:**
Kun Chen odpowiada @elvissun, potwierdzając jego obserwację i wskazując przyczynę: model (lub agent/harness) zachowuje się w ten sposób, ponieważ próbuje wykorzystać prompt caching. Brak treści posta nadrzędnego, więc dokładny objaw nie jest znany — najprawdopodobniej chodzi o powtarzalność prefiksu, kolejność generowanych elementów lub stabilność struktury promptu między turami.

**Rada inżynierska:**
Traktuj prompt caching jako realną siłę projektową, a nie tylko optymalizację kosztów. Jeśli chcesz, aby cache trafiał, utrzymuj niezmienny, stabilny prefiks promptu (system prompt, instrukcje, definicje narzędzi, kontekst statyczny) i dokładaj zmienną treść (dane zadania, wyniki narzędzi, historię) na końcu. Gdy zmieniasz cokolwiek w prefiksie — choćby kolejność sekcji czy whitespace — cache przestaje działać i model zaczyna zachowywać się inaczej (np. generuje mniej spójne odpowiedzi, bo nie ma już 'zakotwiczonego' kontekstu).

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: wstawianie dynamicznych danych (timestamp, losowe ID, zmienna kolejność sekcji, przeformatowany system prompt) na początek promptu. To unieważnia cache przy każdym wywołaniu, drastycznie zwiększa koszt i opóźnienie, a dodatkowo powoduje, że model nie może polegać na stabilnym kontekście — co bywa mylone z 'niestabilnością modelu' lub 'driftem', gdy w rzeczywistości winna jest architektura promptu.

> **Cytat:** *"@elvissun yup.. and that’s because it’s trying to leverage prompt caching"*

---

## Zarządzanie kontekstem / Harness

### Zdalne zarządzanie kompaktowaniem kontekstu — oddaj decyzję harnessowi

- **Data:** `Mon Sep 21 03:34:19 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101877657927655730)
- **Rodzaj:** Komentarz w dyskusji (@kunchenguid)
- **Powiązane pojęcia:** [[Context Compaction]] [[Context Compaction|Context Window Management]] [[Harness|Agent Harness]] [[Context Compaction|Długie sesje agentowe]]

**Kontekst / Problem:**
Kun Chen odpowiada w wątku o strategiach kompaktowania kontekstu (context compaction) w długich sesjach agenta. Alternatywa dla ręcznego decydowania, kiedy streszczać/zrzucać historię rozmowy, to pozostawienie tego mechanizmowi narzędzia — w tym wypadku 'Jev' (prawdopodobnie agent/integracja w stylu Jevonsa Liu), który sam sygnalizuje moment kompaktowania.

**Rada inżynierska:**
Nie steruj kompaktowaniem kontekstu ręcznie — pozwól, by harness/agent wykrywał moment (np. zbliżanie się do limitu okna, spadek trafności) i sam sygnalizował oraz wykonywał kompaktowanie. To jest aktualna praktyka Kuna Chena: przenieś politykę kompaktowania z człowieka do warstwy wykonawczej.

**Uwaga / Anty-wzorzec:**
Automatyczne kompaktowanie jest nieprzejrzyste — jeśli harness streszcza bez audytu, możesz stracić krytyczne szczegóły zadania. Warto mieć punkt kontrolny/log, żeby móc zweryfikować, co zostało wypchnięte z kontekstu; ślepe poleganie na triggerach utrudnia debugowanie regresji.

> **Cytat:** *"oh alternatively, which is what i do right now - let Jev tell you when to compact"*

---

## Zarządzanie kosztami / Prompt caching / Higiena sesji agenta

### Zarządzanie kosztami cache'u: /compact PRZED odejściem od długiej sesji

- **Data:** `Mon Sep 21 03:14:19 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101872626968969713)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Prompt Architecture|Prompt Caching]] [[Context Compaction|Context Window]] [[Context Compaction|Compaction]] [[TypeSafe — przewodnik praktyczny|Koszt tokenów]] [[Context Compaction|Higiena sesji agenta]] [[Prompt Architecture|Cache Expiration]]

**Kontekst / Problem:**
Wskazówka o realnych kosztach niecache'owanego promptu przy dużym oknie kontekstu (500k → ponad $5 za pojedyncze żądanie). Problem pojawia się, gdy użytkownik odchodzi od długiej sesji i wraca po wygaśnięciu cache'u (Claude domyślnie 1 godzina, Codex 30 minut). Wtedy każde żądanie — w tym samo /compact — jest pełnym, drogim requestem.

**Rada inżynierska:**
Najlepsza praktyka: uruchom /compact ZANIM odejdziesz od długiej sesji, żeby cache był jeszcze aktywny i kompakcja była tania. Druga najlepsza opcja: gdy wracasz i widzisz duże okno kontekstu, po prostu zacznij nową sesję i poproś agenta, by sięgnął po transkrypt poprzedniej sesji, jeśli potrzebuje kontekstu. Świadomie planuj moment kompakcji względem czasu życia cache'u (Claude 1h, Codex 30 min).

**Uwaga / Anty-wzorzec:**
Uruchamianie /compact po powrocie do długiej, bezczynnej sesji z wygasłym cache'em — ludzie myślą, że kompakcja obniży koszt, ale sam request kompakcji jest pełnym, niecache'owanym żądaniem i kosztuje ~$5 w momencie wykonania. To najczęstsza droga do nieświadomego przepalenia budżetu (nawet przy kwocie subskrypcyjnej).

> **Cytat:** *"a quick tip that may surprise some folks

an uncached prompt to fable at 500k context window will directly cost you over $5 for A SINGLE REQUEST. that's a cup of coffee or a cheese burger gone. even with subscription quota, this hits like a truck

the most common way to fall into that case is when you walk away from a long session and come back after a while when cache expired (claude is 1 hr, codex is 30 mins by default)

in particular, when you come back to a long idle session, don't run "/compact" there thinking it'll reduce your cost, because the compaction request is still a real request and it will cost $5 by itself right there

the best thing to do is to /compact BEFORE you walk away

the next best thing is when you come back and see a large context window, just start a new session, and ask your agent to look for the last session's transcript if it needs context"*

---

## Inżynieria produktu AI / ocena modeli

### Luka między badaniami a użytecznym produktem: ocena modelu Laya (512–1k kontekstu, trafność jak rzut monetą)

- **Data:** `Sun Sep 20 04:51:10 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101534610710761923)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|Ocena modelu]] [[Context Compaction|Okno kontekstu]] [[TypeSafe i Jev — wywiad z Diogo Almeidą|Fine-tuning]] [[Stabilność modeli i przestrzeganie promptu|Luka research-produkt]] [[Stabilność modeli i przestrzeganie promptu|Adopcja modelu]] [[Interpretable Context Methodology|Pakowanie rozwiązania]]

**Kontekst / Problem:**
Kun reaguje na narrację, że autor modelu Laya 'zbudował to samo rok wcześniej', a Jev 'ukradł mu cały rozgłos' — i że wystarczyło 'opowiedzieć swoją historię' albo 'lepiej się promować'. Kun weryfikuje sam model Laya i pokazuje, że różnica nie leży w marketingu, lecz w gotowości produktu do adopcji.

**Rada inżynierska:**
Zanim uznasz model badawczy za gotowy do użycia, oceń go bezpośrednio pod kątem realnych ograniczeń produkcyjnych: sprawdź okno kontekstu (Laya obsługuje tylko 512–1k tokenów, więc wiele przypadków użycia się nie zmieści) oraz bazową trafność (bez fine-tuningu wynik jest jak rzut monetą). Wartość powstaje dopiero, gdy z interesującego researchu zrobisz zapakowane rozwiązanie, które da się wziąć i użyć — ten wysiłek integracyjny to nie 'marketing', to realna inżynieria i ona decyduje o adopcji.

**Uwaga / Anty-wzorzec:**
Zrzucanie braku adopcji na słabą promocję ('trzeba opowiedzieć swoją historię') przy jednoczesnym pominięciu, że model wymaga fine-tuningu i ma zbyt mały kontekst, by cokolwiek na nim zbudować. Zakładanie, że sam wynik badawczy jest produktem gotowym do wdrożenia — mylenie 'ciekawego researchu' z 'użytecznym produktem'.

> **Cytat:** *"i just looked into this laya model and: - it only supports 512-1k context… a lot of use cases won’t fit at all - evaluating the model directly shows its accuracy is as good as a coin flip. in order to get good results, you need to first fine tune it ... there’s a massive gap between an interesting research and a useful product ... Jev is not completely new from an academic sense, just like how ChatGPT was not the first LLM. don’t underestimate the effort and value in putting together something that’s actually good enough for adoption - it makes all the difference"*

---

## Harness / Zarządzanie kontekstem i sesją agenta

### Ręczne etykietowanie checkpointów sesji i kryterium "safe checkpoint"

- **Data:** `Fri Sep 18 20:25:20 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101044924301156365)
- **Rodzaj:** Komentarz w dyskusji (@mktpavlenko)
- **Powiązane pojęcia:** [[Context Compaction|Context compaction]] [[Bezpieczny punkt kompaktowania|Checkpointing sesji agenta]] [[Harness|Ewaluacja harnessu]] [[Eval Set z realnych sesji|Manualne etykietowanie danych]] [[Persistencja stanu agenta|Persistencja stanu sesji]]

**Kontekst / Problem:**
Kun Chen odpowiada na wpis @mktpavlenko, wyjaśniając metodologię budowy zbioru checkpointów do ewaluacji kompresji/ucięcia kontekstu sesji agenta. Problem: jak obiektywnie ustalić, w którym miejscu sesji można bezpiecznie uciąć kontekst (compaction/truncation), nie tracąc informacji krytycznej dla dalszego przebiegu zadania.

**Rada inżynierska:**
Nie ufaj automatycznemu wykrywaniu punktów cięcia kontekstu — etykietuj checkpointy ręcznie. Punkt uznawany za "safe" definiuj operacyjnie: sprawdź, czy pozostała część sesji faktycznie potrzebuje czegokolwiek z wcześniejszego kontekstu, co nie zostało utrwalone (persisted). Jeśli nic takiego nie potrzebuje — checkpoint jest bezpieczny do ucięcia.

**Uwaga / Anty-wzorzec:**
Traktowanie "safe checkpoint" jako pojęcia intuicyjnego lub zależnego wyłącznie od rozmiaru kontekstu, zamiast od realnej zależności kolejnych kroków od nieutrwalonej informacji z przeszłości. Grozi to utratą krytycznego stanu przy kompresji i cichym regresem jakości w produkcji.

> **Cytat:** *"@mktpavlenko all the checkpoints were manually labeled by myself and "safe" checkpoints were determined by looking at whether the rest of the session indeed needs anything in the prior session that's not persisted"*

---

## Zarządzanie kontekstem / Harness agenta

### Nie stosuj natychmiastowej kompakcji kontekstu — najpierw sprawdź, czy jesteś w bezpiecznym punkcie

- **Data:** `Fri Sep 18 19:53:16 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101036854925779291)
- **Rodzaj:** Komentarz w dyskusji (@gehariharan)
- **Powiązane pojęcia:** [[Context Compaction]] [[Context Compaction|Zarządzanie kontekstem agenta]] [[Harness|Harness agenta]] [[Bezpieczny punkt kompaktowania|Bezpieczne punkty kontrolne]] [[Bezpieczny punkt kompaktowania|Klasyfikacja stanu agenta]]

**Kontekst / Problem:**
Kun Chen odpowiada @gehariharan w wątku o strategiach kompakcji kontekstu (context compaction) w agentach LLM. Ktoś zaproponował podejście 'instant compaction' — natychmiastowe streszczanie/kompresowanie kontekstu, gdy tylko się zapełni. Kun ostrzega, że to zły pomysł i wskazuje właściwy sposób myślenia o tym problemie.

**Rada inżynierska:**
Nie kompaktuj kontekstu natychmiast po przekroczeniu progu zapełnienia. Kompakcja to w istocie zadanie klasyfikacyjne: musisz najpierw ustalić, czy agent znajduje się w punkcie, w którym kompakcja jest bezpieczna (np. na granicy logicznego kroku, po zakończeniu operacji, bez otwartego stanu pośredniego). Dopiero wtedy wykonuj kompakcję. Traktuj decyzję 'kompaktować teraz czy nie' jako osobny problem klasyfikacji stanu, a nie jako prosty trigger progowy.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec 'instant compaction': automatyczna kompakcja wyzwalana wyłącznie progiem rozmiaru kontekstu, bez oceny, czy agent jest w bezpiecznym punkcie. Prowadzi to do przerywania operacji w połowie, utraty spójności stanu i błędów w dalszym rozumowaniu.

> **Cytat:** *"@gehariharan don't do the "instant compaction" thing. i commented on the post - it's a bad idea

this is just plain and simple classifying whether you are sitting at a place where it's safe to compact"*

---

## Context Engineering / zarządzanie oknem kontekstowym agenta

### compact-adviser: klasyfikator momentu bezpiecznej kompakcji kontekstu z adaptacyjnym balansem precision/recall

- **Data:** `Fri Sep 18 19:36:40 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101032677940117875)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Context Compaction|Context Engineering]] [[Context Compaction|Kompakcja kontekstu]] [[Context Compaction|/compact]] [[Bezpieczny punkt kompaktowania|Task Boundary]] [[Bezpieczny punkt kompaktowania|Precision vs Recall]] [[Eval Set z realnych sesji|Eval Set]] [[Prompt Architecture|Prompt Hillclimbing]] [[Harness|Agent Harness]] [[Harness|Agent Plugin]] [[Jev]] [[Bezpieczny punkt kompaktowania|compact-adviser]]

**Kontekst / Problem:**
Kun Chen odpowiada na powtarzające się pytanie użytkowników Claude Code / pi: „kiedy powinienem zrobić /compact w sesji?”. Problem: nie ma prostej reguły, bo bezpieczeństwo kompakcji zależy od tego, jak prawdopodobne jest, że przyszłe akcje agenta będą potrzebować szczegółowego kontekstu obecnego okna. Rozwiązanie: plugin agentowy compact-adviser (oparty na prompcie „Jev”), który klasyfikuje, czy jesteśmy na granicy zadania (task boundary) bezpiecznej do kompakcji. Autor zbudował prywatny eval set z 40 prawdziwych sesji, ręcznie oznaczył checkpointy safe vs unsafe i hillclimbował prompt, aż osiągnął dobre wyniki. Wtyczka wspiera tryb „hint” (tylko podpowiedź, /compact uruchamiasz sam) oraz „auto” (kompakcja uruchamiana automatycznie, gdy Jev uzna to za bezpieczne).

**Rada inżynierska:**
Nie traktuj kompakcji kontekstu jako decyzji binarnej ani stałego progu — zrób z niej klasyfikator z polityką zależną od zapełnienia okna: (1) przy małym zużyciu okna optymalizuj PRECISION, żeby nie wyzwalać kompakcji przedwcześnie (unikając utraty szczegółów potrzebnych w przyszłych krokach), (2) w miarę zapełniania się okna stopniowo przesuwaj optymalizację w stronę RECALL, bo koszt niekompaktowania rośnie, a na końcu agent i tak zostanie zmuszony do kompakcji. Klasyfikator oprzyj na jawnym kryterium „czy jestem na granicy zadania”, a nie na liczbie tokenów. Zawsze waliduj taki prompt na własnym, ręcznie oznaczonym zbiorze realnych sesji (autor: 40 sesji, etykiety safe/unsafe checkpointów) i hillclimbuj prompt względem tej metryki — dopiero wtedy wtyczka nadaje się do trybu auto. Warto rozdzielić tryb „hint” (agent doradza, człowiek decyduje) od „auto” (agent wykonuje kompakcję sam) — hint jest bezpiecznym krokiem pośrednim przed automatyzacją.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: sztywne progi i rutynowe /compact oparte wyłącznie na zapełnieniu kontekstu. Kompakcja zbyt wczesna niszczy szczegółowy kontekst, którego potrzebują przyszłe akcje agenta; kompakcja zbyt późna kończy się wymuszoną, chaotyczną kompakcją w najgorszym możliwym momencie (w środku zadania). Drugi anty-wzorzec: wdrażanie takiego klasyfikatora w trybie „auto” bez własnego eval setu i ręcznie oznaczonych etykiet — bez pomiaru precision/recall nie wiesz, czy plugin nie kompaktuje w środku krytycznego kroku.

> **Cytat:** *"almost every day i hear people ask "when should i /compact my session" — there's no easy answer because it depends on how likely your future action will need detailed context in the existing window ... i built a private eval set from 40 real sessions and manually labeled all the safe vs unsafe checkpoints to evaluate this, and hillclimbed the Jev prompt till it performed quite well ... the classifier will - optimize for precision (not triggering a compaction prematurely) when context window is small - and gradually shift to optimize for recall (not missing an opportunity to compact) when context window fills up, because the cost of not compacting becomes higher, and at the end the agent will be forced to compact anyway"*

---

## Zarządzanie kontekstem / Prompt Caching

### Cache'owanie promptu: kompakcja całej sesji vs. selektywne usuwanie wiadomości

- **Data:** `Fri Sep 18 05:15:45 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100816020932096060)
- **Rodzaj:** Komentarz w dyskusji (@DeccansoftAI)
- **Powiązane pojęcia:** [[Prompt Architecture|Prompt Caching]] [[Context Compaction]] [[Prompt Architecture|Cache Miss]] [[Context Compaction|Zarządzanie kontekstem]] [[TypeSafe — przewodnik praktyczny|Ekonomia tokenów]]

**Kontekst / Problem:**
Odpowiedź Kun Chena w dyskusji (@DeccansoftAI, @tamarajtran, @typesafeai) dotyczącej strategii kompakcji długich sesji LLM. Ktoś zasugerował, że przed kompakcją warto usuwać część wiadomości z historii, by zaoszczędzić tokeny. Kun prostuje to błędne założenie, tłumacząc realny mechanizm rozliczania cache'u promptu.

**Rada inżynierska:**
Kompaktuj całą sesję naraz — pełny, niezmodyfikowany kontekst sesji jest w pełni trafieniem w cache (fully cached prompt) i kosztuje bardzo mało. Kompakcja to więc tania operacja, dopóki nie modyfikujesz historii wejściowej.

**Uwaga / Anty-wzorzec:**
Selektywne usuwanie wiadomości z historii przed uruchomieniem kompakcji powoduje cache miss — prefiks promptu się zmienia, więc cały request jest rozliczany po PEŁNEJ cenie, czyli 10x–40x drożej niż przy trafieniu w cache. Oszczędzanie na tokenach przez wycinanie historii paradoksalnie drastycznie zwiększa koszt.

> **Cytat:** *"no, because when the LLM compacts the whole session, it's a fully cached prompt whose price is very low

but if you remove some of the messages from the history and then run a compaction request, it's a cache miss and will be charged at FULL price 10x-40x more expensive"*

---

## Zarządzanie kontekstem / Kompakcja i okno kontekstowe agenta

### Selektywne usuwanie wywołań narzędzi to zła strategia kompakcji kontekstu

- **Data:** `Fri Sep 18 04:15:10 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100800776620900454)
- **Rodzaj:** Komentarz w dyskusji (@tamarajtran)
- **Powiązane pojęcia:** [[Context Compaction|Kompakcja kontekstu]] [[Context Compaction|Okno kontekstowe]] [[Context Compaction|Tool calls]] [[Prompt Architecture|Prompt caching]] [[Context Compaction|Długotrwałe zadania agenta]] [[Rework Rate|Ewaluacje agentów]] [[Stabilność modeli i przestrzeganie promptu|DeepSWE]] [[Stabilność modeli i przestrzeganie promptu|ProgramBench]] [[Context Compaction|Anty-wzorce zarządzania kontekstem]]

**Kontekst / Problem:**
Kun Chen odpowiada pod wpisem @tamarajtran, w którym promowana (i szeroko rozprzestrzeniająca się) technika kompakcji kontekstu polega na selektywnym usuwaniu z historii tylko wywołań narzędzi (tool calls), przy zachowaniu wszystkich wiadomości użytkownika i asystenta. Kun ostrzega, że to pozornie praktyczne podejście jest w rzeczywistości błędne i szkodliwe w produkcji.

**Rada inżynierska:**
Prawdziwa kompakcja musi realnie ZMNIEJSZAĆ okno kontekstowe — usuwanie jedynie części wywołań narzędzi, przy trwałym zachowaniu wiadomości user/assistant, prowadzi do tego, że podsumowanie kompakcji może tylko rosnąć. Zamiast wymyślać selektywne sztuczki, stosuj pełną kompakcję i ZAWSZE mierz kompromis koszt/wydajność za pomocą evalów (np. DeepSWE, ProgramBench), zanim uznasz rozwiązanie za praktyczne.

**Uwaga / Anty-wzorzec:**
Dwa fundamentalne błędy selektywnego usuwania tool calls: (1) kontekst nigdy się nie kurczy — wiadomości user/assistant zostają na zawsze, więc podsumowanie kompakcji rośnie bez ograniczeń i długotrwałe zadania w końcu wyczerpią okno kontekstowe bez możliwości samo-naprawy, co niweczy podstawowy cel kompakcji; (2) pozostawia się znacznie więcej treści niż przy prawdziwej kompakcji, przez co następne zapytanie staje się ogromnym, nie-zbuforowanym (uncached) promptem — w niektórych przypadkach droższym niż kontynuacja długiej, zbuforowanej sesji, co niweczy drugi cel kompakcji, czyli oszczędność kosztów.

> **Cytat:** *"umm.. since this is somehow spreading so widely, i feel obligated to point out that this is unfortunately a bad idea

the fundamental flaws -

1. it only selectively remove some tool calls. user and assistant messages are kept FOREVER, which means the compaction summary will only keep growing and never shrink. so long running tasks will eventually completely run out of context window and cannot self recover, defeating the primary purpose of compaction which is to free up the context window so the agent can keep going

2. this operation leaves a lot more stuff in the context window than a real compaction, which means the next request after doing this becomes a massive uncached prompt which in some cases even more expensive than letting the long cached session continue, which defeats the other purpose of compaction which is cost saving

i suggest running some evals such as deepswe, programbench etc to actually measure the cost and performance tradeoff and share it if you are truly convinced this is practical"*

---

## Architektura systemów LLM / Wybór podejścia

### Dlaczego klasyfikatory tradycyjne nie zastąpią LLM przy kategoriach definiowanych przez użytkownika

- **Data:** `Thu Sep 17 15:35:36 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100609623531421915)
- **Rodzaj:** Komentarz w dyskusji (@winterspeak)
- **Powiązane pojęcia:** [[Jev|LLM vs klasyczne klasyfikatory]] [[Jev|Zero-shot classification]] [[Jev|User-defined categories]] [[Jev|Freeform taxonomy]] [[Stabilność modeli i przestrzeganie promptu|Wybór modelu do zadania]]

**Kontekst / Problem:**
Kun Chen odpowiada @winterspeak, który prawdopodobnie sugerował użycie klasycznego klasyfikatora (np. ML/trenowanego modelu) zamiast LLM do kategoryzacji. Kun wyjaśnia, że w jego przypadku kategorie są definiowane przez użytkownika i całkowicie swobodne (freeform), co uniemożliwia zastosowanie klasycznego klasyfikatora.

**Rada inżynierska:**
Gdy kategorie/etykiety są definiowane dynamicznie przez użytkownika i mają charakter freeform, klasyczny klasyfikator ML jest bezużyteczny — nie da się wytrenować jednego modelu pokrywającego wszystkie możliwe schematy kategorii, a wymuszanie treningu per-użytkownik jest niepraktyczne. W takich przypadkach LLM (zero/few-shot) jest właściwym wyborem, bo działa na dowolnie zdefiniowanym schemacie bez treningu.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: sięganie po klasyczny klasyfikator (supervised ML) do zadań, w których przestrzeń etykiet jest otwarta, zależna od kontekstu użytkownika lub zmienna w czasie. Prowadzi to do niekończącego się re-treningu, sztywnego schematu i braku generalizacji na nowych użytkowników.

> **Cytat:** *"@winterspeak not exactly - if you think about the use case i have here, the categories are user-defined and completely freeform

there’s no way i can train a traditional classifier that will work for every user, and there’s no way every user will train their own classifier"*

---

## Weryfikacja i harness

### Kwantyfikacja pewności modelu jako warunek odrzucania odpowiedzi

- **Data:** `Thu Sep 17 15:29:09 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100608000042127434)
- **Rodzaj:** Komentarz w dyskusji (@PremiumGoblin)
- **Powiązane pojęcia:** [[Jev|Confidence scoring]] [[Weryfikator|External verifier]] [[Stabilność modeli i przestrzeganie promptu|Requirement ambiguity]] [[Weryfikator|Answer rejection threshold]] [[Jev]]

**Kontekst / Problem:**
Kun Chen odpowiada na wpis @PremiumGoblin, prawdopodobnie sugerujący, że wystarczy dobrze zdefiniować wymagania, by model radził sobie z implementacją. Kun prostuje: nie zawsze to działa, bo sama ocena, czy wymagania są 'wystarczająco dobrze zdefiniowane' i ile dwuznaczności pozostaje w fazie implementacji, jest trudnym, niejednoznacznym problemem — a nie binarnym warunkiem wstępnym.

**Rada inżynierska:**
Nie traktuj 'dobrego zdefiniowania wymagań' jako jedynego zabezpieczenia przed błędami modelu. Wprowadź mechanizm kwantyfikacji pewności (np. Jev), który zwraca confidence score dla odpowiedzi — wtedy możesz zbudować regułę odrzucania: 'jeśli model nie jest pewny, odrzucam jego odpowiedź' zamiast ślepo ją przyjmować. To przenosi ciężar decyzji z ludzkiej (niejednoznacznej) oceny klarowności wymagań na mierzalny sygnał z systemu.

**Uwaga / Anty-wzorzec:**
Założenie, że jeśli wymagania są 'well defined', to implementacja przez model pójdzie dobrze. Ocena stopnia zdefiniowania wymagań i resztkowej dwuznaczności w trakcie implementacji jest subiektywna i trudna — sam ten warunek nie jest weryfikowalny, więc nie chroni przed błędami. Bez kwantyfikacji pewności nie masz progu odcięcia dla niepewnych odpowiedzi.

> **Cytat:** *"not always - but for some cases yes, the judgment on whether requirements are “well defined” enough and how much ambiguity still exists during the implementation phase is not easy to answer

the extra nice thing about jev is that it quantifies the confidence, so i can say “if it’s not confident the i discard its answer”"*

---

## Architektura systemów AI / Agent Design

### Architektura hybrydowa: logika deterministyczna + model decyzyjny zamiast pętli agentowych LLM

- **Data:** `Thu Sep 17 06:45:30 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100476218512748616)
- **Rodzaj:** Komentarz w dyskusji (@v10se)
- **Powiązane pojęcia:** [[Harness|Agent Loops]] [[Harness|Deterministic Logic]] [[Harness|Hybrid Architecture]] [[TypeSafe — przewodnik praktyczny|LLM Cost Reduction]] [[Jev|Decision Model vs LLM]]

**Kontekst / Problem:**
Kun Chen odpowiada w komentarzu pod wpisem @v10se, odnosząc się do pojawienia się czegoś (prawdopodobnie modelu/mechanizmu o nazwie 'Jev') zdolnego zastępować wywołania LLM. Wskazuje dwie konsekwencje tego zjawiska: oczywistą (redukcja kosztów) oraz nieoczywistą (wymuszenie innego myślenia o architekturze oprogramowania). Problem, który rozwiązuje: domyślne budowanie wszystkiego jako pętli agentowych z LLM jest kosztowne i nadmiernie złożone.

**Rada inżynierska:**
Rozdzielaj odpowiedzialności w systemie na trzy warstwy: (1) logika deterministyczna w kodzie — sterowanie przepływem i reguły, (2) wyspecjalizowany model decyzyjny (np. 'Jev') — podejmowanie decyzji, (3) LLM — tylko okazjonalne generowanie treści. Zastępowanie wywołań LLM tańszymi komponentami to ogromna oszczędność, ale kluczowa wartość to wymuszenie architektury, w której LLM nie jest domyślnym centrum sterowania. Zamiast pętli agentowej buduj pipeline, gdzie decyzje podejmuje dedykowany, tańszy mechanizm, a generacja treści jest zdarzeniem wyjątkowym, nie regułą.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: traktowanie LLM jako domyślnego silnika decyzyjnego i budowanie wszystkiego wokół pętli agentowych ('LLMs make us all build agent loops'). Prowadzi to do wysokich kosztów, nieprzewidywalności i niepotrzebnej złożoności tam, gdzie wystarczyłaby deterministyczna logika lub prostszy model decyzyjny.

> **Cytat:** *"right now i'm seeing two - the most obvious implication is cost reduction. it's a massive saving whenever we can replace LLM calls with this. the non-obvious one is that it forces us to think about our software differently. LLMs make us all build agent loops. this enables us to explore a different architecture - a combination of deterministic logic (code), intelligent decision making (Jev), and occasional generation of content (LLM)"*

---

## Architektura harnessów i routing zadań / optymalizacja kosztów i latencji

### Zastąpienie dispatchu opartego na LLM szybkim dedykowanym modelem (Jev) w orkiestratorze Firstmate

- **Data:** `Thu Sep 17 06:16:35 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100468943853085061)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Prompt Architecture]] [[Jev|Task Routing]] [[Firstmate Agent|Orchestrator Agent]] [[Context Compaction|Tool Calls]] [[Stabilność modeli i przestrzeganie promptu|Reasoning Effort]] [[TypeSafe i Jev — wywiad z Diogo Almeidą|Model Distillation]] [[TypeSafe — przewodnik praktyczny|Latency Optimization]] [[TypeSafe — przewodnik praktyczny|Cost Optimization]] [[Eval Set z realnych sesji|Eval Set]] [[Firstmate Agent|Firstmate]] [[Harness]]

**Kontekst / Problem:**
Firstmate to orkiestrator, który przydziela każde zadanie do odpowiedniego agenta (permutacja: harness + model + reasoning effort) na podstawie preferencji użytkownika. Domyślnie decyzję routingu podejmował agent LLM: musiał 'pomyśleć', wykonać tool calls (odczyt reguł dispatchu, danych o kwotach itd.), a dopiero potem dispatchować. Było to wolne i kosztowało tokeny LLM. Kun zastąpił ten proces dedykowanym, wyspecjalizowanym modelem Jev.

**Rada inżynierska:**
Decyzje routingu/dyspatcherowania, które są deterministyczne i oparte na regułach + danych (reguły dispatchu, limity kwot), nie powinny być podejmowane przez ogólny LLM z reasoningiem i tool calls — można je skompilować do małego, dedykowanego modelu. Kun zmierzył: ten sam wynik co model 'fable level' na 25 ocenianych zadaniach, ~200 ms na decyzję, bez myślenia i bez tool calls. W całym procesie dispatchu (wliczając wciąż potrzebny tool call wywołujący Jev przez agenta LLM) dało to -71% kosztu i -90% wall time; jeśli patrzeć tylko na zastąpiony fragment, oszczędność jest rzędu ~100x. Koszt samych wywołań API Jev jest praktycznie zerowy (100+ wywołań, dashboard wciąż pokazuje $0.01). Wniosek architektoniczny: LLM to tylko mały element systemu — warto wydzielać z niego warstwy decyzyjne na rzecz taniej, szybkiej, wyspecjalizowanej komponenty.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: używanie ogólnego LLM z reasoningiem i tool calls do podejmowania decyzji, które są w istocie deterministyczne (routing wg reguł i danych) — to wolne, kosztowne i niepotrzebnie angażuje tokeny. Dodatkowa ostrożność: wynik oparto na ewaluacji tylko 25 zadań, więc zgodność z zachowaniem 'fable level' (25/25 identycznych odpowiedzi) ma ograniczony zakres — przed produkcyjnym wdrożeniem warto rozszerzyć zbiór ewaluacyjny i monitorować rozjazdy decyzji. Należy też pamiętać, że wywołanie Jev nadal wymaga tool call po stronie agenta LLM — całkowitej eliminacji LLM z pętli nie ma.

> **Cytat:** *"alright - just got Jev deployed for a real production use case, which now performs at fable level quality but 10x faster and saves a ton of money ... by default, that's done by the firstmate agent and the LLM would have to do some thinking, make tool calls to read dispatch rules, quota data etc and then do the dispatch. this is slow and does cost a bit of LLM tokens. i just replaced this dispatch process with Jev. it makes the same decision with no thinking or tool calls, done in ~200ms, and for the 25 tasks i evaluated this with, it gives the exact same answer fable would have given... ... even with that counted, the saving from Jev still resulted in a -71% reduction in cost and -90% reduction in wall time of completing the whole dispatching process ... if we just look at the part Jev replaced and not the whole system, then the saving is on the magnitude of ~100x ... if you also have Jev and you use firstmate, set TYPESAFE_API_KEY in your .env file in your firstmate repo to activate this"*

---

## Architektura systemów agentowych / Routing modeli i koszty

### Tania orkiestracja + eskalacja niejednoznaczności do modelu wysokiej klasy

- **Data:** `Wed Sep 16 05:09:51 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100089760475930830)
- **Rodzaj:** Komentarz w dyskusji (@Steve_Yegge)
- **Powiązane pojęcia:** [[Jev|Model Routing]] [[Firstmate Agent|Agent Orchestration]] [[Jev|Escalation Policy]] [[TypeSafe — przewodnik praktyczny|Cost-Aware Agent Design]] [[Firstmate Agent|LLM-as-Orchestrator]] [[Prompt Architecture]] [[Stabilność modeli i przestrzeganie promptu|Model Tiering]]

**Kontekst / Problem:**
Kun Chen odpowiada pod wpisem @Steve_Yegge, dzieląc się obserwacją z wielomiesięcznej pracy z własnym agentem-orchestratorem ('firstmate'). Problem: przypisywanie modeli najwyższej klasy (określanych jako 'fable tier') do rutynowych zadań orkiestracyjnych — typu sekwencyjne odpalanie kroków ('task 1 się skończył, odpal task 2') — drastycznie podnosi koszt bez zysku jakościowego. Rozwiązanie: tani model do orkiestracji, ale z twardym sterowaniem eskalacją.

**Rada inżynierska:**
Rozdziel role według poziomu poznawczej złożoności, nie według wygody. Orkiestrację, sekwencjonowanie kroków i rutynowy routing oddaj tanim modelom. Modelom wysokiej klasy ('fable tier') zostaw wyłącznie decyzje wymagające rozumowania: niejednoznaczne wybory, konflikty wymagań, planowanie. Kluczowy element to NIE sam podział, a wymuszenie eskalacji: zaprojektuj prompt taniego orkiestratora tak, by agresywnie kierował niejednoznaczne decyzje w górę hierarchii modeli. Kun raportuje, że ta eskalacja robi 'zaskakująco dużą różnicę' i nie pogarsza ogólnej jakości systemu.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: 'wisdom inflation' — używanie modelu najwyższej klasy do zadań orkiestracyjnych niskiej złożoności (np. 'task 1 finished, kick off task 2'). Prowadzi to do nieosiągalnego kosztu ('untenable cost') bez poprawy jakości. Drugi, ukryty anty-wzorzec: sam podział na taniego orkiestratora bez mechanizmu eskalacji — tani model zacznie samodzielnie rozstrzygać sprawy, których rozstrzygać nie powinien.

> **Cytat:** *"having been working with my firstmate for months, i learned one of the biggest traps is that we may put fable tier models on many mundane orchestration-ish tasks (like “oh task 1 finished let me kick off task 2”) that really don’t need fable level wisdom. that’s what makes the cost untenable

i’m having great success with using a cheap model for orchestration and heavily steer it to escalate ambiguous decisions to fable, which makes a surprisingly big difference without compromising the overall quality of the system"*

---
