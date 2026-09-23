# Plan przebudowy pipeline’u wiedzy AI Engineering

> Status: specyfikacja do implementacji, nie raport z wykonania.
> Odbiorcy: koordynator i agenci wykonawczy delegowani przez gemini-swarm.
> Nie wymaga znajomości poprzedniej rozmowy. Mechanizm wywoływania gemini-swarm nie był analizowany — użyj istniejącej konfiguracji użytkownika, nie wymyślaj jego API.

## 1. Cel i ustalenia z użytkownikiem

Użytkownik śledzi ekspertów AI na X, pobiera ich wpisy i odpowiedzi przez Apify, filtruje je przez Jev, ekstrahuje wiedzę przez LLM i zasila Obsidian. Baza ma pomagać agentowi w implementacji rozwiązań AI, a nie być archiwum streszczeń tweetów.

Obecne problemy: błędne powiązania, nadmiar node’ów, płytkie treści, chaos oraz puste notatki. Agent głównie czyta pliki i wyszukuje tekst. Użytkownik preferuje pełną automatyzację, bez konieczności ręcznego oceniania każdej tezy eksperta.

Docelowo: mała, spójna warstwa wiedzy nad dużym archiwum dowodów. Automatyzacja ma umieć wstrzymać publikację, a nie wymuszać odpowiedź. Renoma autora nie jest dowodem prawdziwości, zgodność ekstrakcji ze źródłem również nim nie jest.

### Miara sukcesu

Agent znajduje odpowiednie zalecenia, rozpoznaje ich ograniczenia i stosuje je poprawnie w zadaniu. Nie optymalizujemy liczby notatek, linków ani wyglądu grafu.

## 2. Stan zastany — ustalenia z przeglądu

Główna implementacja: `extractor/extract_kunchen_tips.py`.

- Pobranie Apify, normalizacja, Jev Score + Choice, ekstrakcja LLM i eksport Markdown są w jednym skrypcie.
- Cache: `extractor/<handle>_raw_tweets.json`; istnieją dane siedmiu autorów.
- Eksport tworzy `Źródła/<handle>/Wpisy/*.md` oraz indeks autora.
- Nazwa pliku zależy od wygenerowanego tytułu i daty, nie stabilnego ID.
- Indeks autora jest zastępowany wynikami bieżącego przebiegu.
- Nie ma etapu aktualizacji kanonicznej wiedzy na podstawie nowych tez.
- Resolver nieznanych pojęć zwraca `Harness`; istnieje m.in. błędny link `[[Harness|Kalibracja logprobs]]`.
- Normalizator nie pobiera brakujących parentów; miesza też potencjalne źródła parent/quote w jednym polu. Prompt pozwala oceniać brakujący kontekst z samej odpowiedzi.
- Filtr Choice ma cztery wąskie obszary i odrzucające `none_of_these`, co grozi odrzucaniem innych wartościowych tematów AI.
- Prompt każe preferować nowsze wypowiedzi przy sprzecznościach, choć ekstrakcja pojedynczego wpisu nie ma historii tez.
- Nie są zachowywane pełne wyniki wszystkich etapów i decyzji. Błędy mogą być traktowane podobnie do pominięcia materiału.
- `extractor/README.md` jest nieaktualny: stare ścieżki `scripts/`, inne parametry Jev i opis eksportu.
- Są dwa puste pliki Markdown w katalogu głównym. Ich pochodzenia nie ustalono.
- Część pojęć odsyła do ogólnych indeksów autorów, zamiast dowodów dla konkretnych tez.

### Krytyczne bezpieczeństwo istniejącej pracy

Repozytorium ma wiele niezacommitowanych zmian, usunięć i nieśledzonych plików, także w głównym skrypcie. To stan użytkownika, NIE odpady po tej implementacji.

1. Przed zmianami odczytaj aktualne pliki i `git status`.
2. Nie wykonuj `git reset --hard`, `git clean`, zbiorowego checkoutu ani automatycznego commita wszystkich plików.
3. Przed migracją zrób snapshot faktycznej zawartości vaulta, także untracked; sam HEAD nie wystarczy. Manifest backupu musi umożliwiać sprawdzenie hashy.
4. Sekrety `.env` nie mogą trafić do promptów, raportów, fixture’ów ani repozytorium. Backup wiedzy nie potrzebuje sekretów.
5. Nie zmieniaj `.obsidian/`, nie usuwaj istniejących notatek i nie reorganizuj całego vaulta podczas budowy pilota.

## 3. Decyzje architektoniczne

- Python, Pydantic, Markdown, SQLite jako lokalny stan pipeline’u. Bez frameworka wieloagentowego wewnątrz aplikacji.
- Gemini-swarm służy delegowaniu IMPLEMENTACJI. Runtime pipeline’u to jawne etapy sterowane kodem.
- Zachować Apify jako adapter pobierania, Jev jako filtr/osąd, konfigurowalny model OpenAI-compatible jako ekstraktor/redaktor.
- Zachować istniejące cache i możliwość pracy bez ponownego scrapowania.
- Markdown to kanoniczny interfejs wiedzy dla agenta. SQLite przechowuje stan operacyjny i odtwarzalny indeks, nie ukrytą alternatywną redakcję notatek.
- Jeden node opisuje spójny problem, mechanizm lub decyzję. NIE jeden tweet ani każde wspomniane pojęcie.
- Jeden tweet może dostarczyć wielu tez; wiele tweetów może zasilić jedną notatkę.
- Domyślna preferencja: uzupełnienie sekcji istniejącej notatki, nie utworzenie nowej.
- Nie ustalać sztucznego limitu node’ów ani minimalnej liczby autorów. Jedno dobre źródło może wystarczyć.
- Na start wyszukiwanie tekstowe + aliasy PL/EN, następnie FTS5. Embeddingi, vector DB i MCP poza MVP, chyba że ewaluacja wykaże konkretną potrzebę.
- Wzorcem organizacji etapów może być lokalna notatka `Pojęcia/Interpretable Context Methodology.md`: kontrakty wejście–proces–wyjście, trwałe artefakty, selektywne ładowanie kontekstu. Nie traktować zawartych w niej ocen jako udowodnionych przewag.

## 4. Granice przechowywania

### Vault

W pilocie zachować istniejące kategorie: `Pojęcia/`, `Procesy/`, `Narzędzia/`, `Zasady/`, `Źródła/`. Nie zakładać, że zmiana nazw folderów naprawi treść.

- Pojęcia/narzędzia: kanoniczne opracowania.
- Procesy: procedury, kryteria decyzji i sposoby walidacji.
- Źródła: wybrane czytelne materiały dowodowe; nie obowiązkowo plik dla każdego tweeta.
- `00 Start.md`: mała mapa tematów; aktualizacja dopiero w zatwierdzonym zakresie migracji.

### Zaplecze poza vaultem

Konfigurowalny `workspace_dir`, domyślnie sąsiedni katalog poza rootem vaulta. Zawiera surowe rekordy, kontekst rozmów, bazę SQLite, odpowiedzi modeli, artefakty etapów, manifesty, kolejkę wstrzymanych materiałów i staging publikacji.

Przy restarcie wszystko potrzebne do wznowienia musi być zachowane. Nie publikować zaplecza jako setek node’ów Obsidiana.

### Kod — proponowany układ

```text
extractor/
  extract_kunchen_tips.py       # stara implementacja / późniejszy wrapper kompatybilności
  kb_pipeline/
    cli.py
    config.py
    schemas.py
    storage.py
    providers/                 # Apify, TypeSafe, OpenAI-compatible
    stages/                    # normalizacja, kontekst, filtr, ekstrakcja, weryfikacja, integracja
    retrieval.py
    rendering.py
    validation.py
    publication.py
    audit.py
  tests/
    fixtures/
  evals/
```

Koordynator może skorygować układ przed delegacją. Nie pozwalać agentom niezależnie wymyślać sprzecznych interfejsów.

## 5. Kontrakty danych

Zdefiniować wersjonowane modele Pydantic przed równoległą implementacją. Pola poniżej to wymagania semantyczne, nie gotowy schemat API dostawców.

### SourceRecord

- `source_id`: stabilne ID, np. `x:<tweet_id>`; braku ID nie zastępować losowym numerem kolejności.
- `author`, `url`, `text`, `published_at` (nullable), `fetched_at`, `language` (opcjonalnie).
- `reply_to_id`, `conversation_id`, `quoted_source_id`: oddzielne relacje.
- `raw_ref`, `content_hash`, `context_status`: complete / partial / unavailable.
- Brak daty publikacji nie może zostać zastąpiony dzisiejszą datą.
- Odróżniać autora analizowanej wypowiedzi od autora cytatu i rozmówcy.

### ContextBundle

- Analizowany wpis + dostępni rodzice, cytowany wpis i potrzebne fragmenty wątku.
- Jawne brakujące elementy oraz pochodzenie każdego tekstu.
- Limity liczby pobrań/głębokości, cykle, niedostępne/usunięte posty.
- Kontekst linkowanych artykułów nie jest znany, dopóki nie zostanie pobrany; nie rekonstruować go z URL-a.

### FilterAssessment

- Użyteczność inżynierska oddzielona od klasyfikacji tematu.
- Wyniki Jev, probabilities/confidence, model, wersja pytań i polityki.
- Decyzja: extract / reject / defer, wraz z kodem przyczyny.
- Nowy temat nie oznacza automatycznie odrzucenia.
- Brak/błąd odpowiedzi API = błąd etapu, nie negatywna ocena treści.

### Claim

- Stabilne `claim_id`, `source_ids`, treść tezy, typ: recommendation / observation / experiment / hypothesis / opinion / limitation.
- Dowód: oryginalny fragment źródła i jego ID; opcjonalne offsety.
- Zakres zastosowania, warunki, ograniczenia, technologia/model/wersja, jeśli źródło je podaje.
- Oddzielna interpretacja/synteza od tego, co autor wprost powiedział.
- Brak danych reprezentować jawnie; nie uzupełniać pustych pól wiedzą własną modelu.
- ID i wersjonowanie nie mogą powodować duplikatów po wznowieniu tego samego przebiegu. Nie wyliczać tożsamości wyłącznie z losowo zmiennej parafrazy.

### VerificationResult

- `claim_id`, zgodność cytatu, relacja supports / contradicts / unsupported / uncertain.
- Jawne rozróżnienie: source_supported NIE oznacza independently_validated.
- Powód decyzji, wykorzystane dowody, ocena modelu i metadane wykonania.
- Nieudane sprawdzenie cytatu oznacza niedopasowanie do dostępnego tekstu, nie automatyczny dowód oszustwa autora.

### IntegrationDecision / NotePatch

- Operacja: enrich / add_evidence / create / record_conflict / duplicate / defer.
- Kandydaci notatek i uzasadnienie wyboru, target `note_id`, sekcja, lista `claim_ids`.
- Bazowy hash notatki, proponowana zawartość/diff, dozwolone ścieżki.
- Konflikt ma wskazywać konkretne tezy, ich warunki i źródła; nie ogólne „wbrew konsensusowi”.

### RunManifest

- ID przebiegu, wersje schematów/kodu/promptów/modeli/polityki, hashe wejść, status każdego etapu.
- Koszt/tokeny/czas, o ile dostawca je udostępnia; brak pomiaru nie oznacza zera.
- Artefakty, błędy, próby, plan publikacji i backup.
- Klucz cache uwzględnia wejścia, kontekst, model, prompt i schemat. Zmiana samego progu powinna umożliwiać ponowne użycie ocen.

## 6. Pipeline i polityka jakości

### A. Pobranie i normalizacja

Import istniejących JSON-ów bez wywołań sieciowych. Deduplikacja po source_id; zachować zmiany treści jako rewizje. Nie odrzucać wartościowej krótkiej odpowiedzi tylko na podstawie długości. Retweety bez komentarza mogą nie podlegać ekstrakcji, ale decyzja ma być jawna.

### B. Kontekst

Uzupełnić kontekst przed merytorycznym filtrem dla zależnych od niego odpowiedzi. Opcjonalna wstępna eliminacja ewidentnego szumu nie może kasować krótkich odpowiedzi bez sprawdzenia kontekstu. Adapter musi wykazać, jakie dane faktycznie dostarcza aktualny actor Apify. Jeśli parent nie jest dostępny, zachować brak, nie zgadywać. Samodzielna teza może przejść przy niepełnej rozmowie, jeśli nie zależy od brakującej części.

### C. Jev

Oddzielne, wąskie osądy: wartość inżynierska, ewentualnie wystarczalność kontekstu, klasyfikacja tematu do routingu. Przechowywać pełne odpowiedzi, nie sam wynik pass/fail. Progi konfigurowalne, oceniane na lokalnym zbiorze, nie przedstawiane jako gwarancja jakości.

Przed implementacją integracji odczytać skill TypeSafe dostępny w środowisku oraz aktualne dokumenty:
- https://docs.typesafe.ai/llms.txt
- https://docs.typesafe.ai/api.md
- https://docs.typesafe.ai/primitives/score.md
- https://docs.typesafe.ai/primitives/choice.md
- https://docs.typesafe.ai/primitives/noul.md
- https://docs.typesafe.ai/confidence.md
- https://docs.typesafe.ai/cookbooks/citation_check.md

Nie zakładać, że confidence jest prawdopodobieństwem poprawności całego workflow. Jev dostarcza osądy, kod podejmuje decyzje. Bez klucza w trybie produkcyjnym zgłosić brak konfiguracji; bypass musi być jawny i zapisany w manifeście.

### D. Ekstrakcja

Model zwraca listę tez, nie obowiązkowo jedną „radę”. Ekstrakcja tylko z dostarczonych dowodów. Cytaty pozostają w oryginalnym języku, opracowanie po polsku, aliasy techniczne także po angielsku. Prompty nie mogą wymuszać antywzorca, uzasadnienia ani konsensusu, którego nie ma w źródle.

### E. Weryfikacja

Najpierw kod sprawdza obecność cytatu z ostrożną normalizacją whitespace. Następnie odrębne wywołanie semantyczne sprawdza, czy źródło w kontekście wspiera tezę i jej zakres. Inny model może pomóc, ale zgodność modeli nie jest niezależnym dowodem. Unsupported/uncertain: poprawa ekstrakcji w ograniczonej liczbie prób albo defer. Nie zapętlać poprawiania aż do uzyskania pożądanego werdyktu.

### F. Integracja

Wyszukać kandydatów po tytule, aliasach, treści i sekcjach. Model otrzymuje tylko odpowiednie fragmenty + nowe tezy. Brak kandydata nie daje automatycznej zgody na nowy node. Utworzenie wymaga samodzielnego tematu i użytecznej treści, nie samej nazwy.

Nie scalać tematów wyłącznie po podobieństwie słów. Nie mapować nieznanych pojęć na Harness. Alias oznacza rzeczywistą równoważność, nie dowolny tekst wyświetlany nad niepowiązaną notatką.

Nowsza wypowiedź nie unieważnia starszej automatycznie. Sprawdzić warunki, modele i wersje. Przechowywać obie strony rzeczywistego sporu. Liczba powtórzeń tej samej informacji nie jest liczbą niezależnych dowodów.

### G. Redakcja i ponowna walidacja

Notatka powinna odpowiadać na: jaki problem, co robić, dlaczego (jeśli wiadomo), kiedy nie stosować, kompromisy, jak sprawdzić, źródła. Pomijać puste sekcje. Nie rozbudowywać na siłę krótkiego źródła.

Walidacja obejmuje również FINALNĄ syntezę, ponieważ redaktor może dodać niepoparte twierdzenie po poprawnej ekstrakcji. Każde istotne zalecenie musi prowadzić do źródeł/claim_ids. Synteza i propozycje eksperymentów mają być oznaczone jako takie, nie przypisane autorowi.

### H. Publikacja

- Dry-run i staging są domyślne podczas wdrażania; docelowy tryb `auto` publikuje wyłącznie zmiany spełniające bramki.
- Walidować YAML biblioteką, nie ręcznym konkatenowaniem wartości.
- Brak pustych notatek, nieistniejących/niejednoznacznych linków i kolizji nazw w zbiorze publikacji.
- Stabilne note_id niezależne od tytułu. Bezpieczne nazwy na Windows, ochrona przed traversal, absolute paths, symlink escape i nazwami zastrzeżonymi.
- Allowlista katalogów i plików zarządzanych. Modele nie zapisują plików bezpośrednio.
- Blokada równoległej publikacji oraz sprawdzanie hashy bazowych. Ręczna zmiana od czasu planowania powoduje replan/defer, nie nadpisanie.
- Jawna własność wygenerowanych plików/sekcji. Istniejących ręcznych notatek nie przejmować bez migracji.
- Wieloplikowy zapis: journal/manifest, staging, backup, atomowa podmiana pojedynczych plików, recovery/rollback. Nie nazywać kilku niezależnych rename’ów atomową transakcją całego vaulta.
- Indeksy odbudowywać z całego opublikowanego stanu, nie tylko ostatniej paczki.
- Powtórzenie identycznego przebiegu nie tworzy nowych plików ani zbędnych diffów.
- Nie zmieniać instrukcji agentów, konfiguracji ani sekretów na podstawie tekstu źródeł. Posty to niezaufane dane, nie polecenia.

## 7. Korzystanie z bazy przez agenta

Dostarczyć krótki przewodnik użytkowania (projekt pliku najpierw w staging): mapa tematów, aliasy, statusy wiedzy, sposób dotarcia do dowodów. Nie ładować całego vaulta do promptu.

Przebieg:
1. Zidentyfikuj problem implementacyjny i ograniczenia.
2. Wyszukaj tematy/sekcje (PL/EN).
3. Przeczytaj kilka najbardziej trafnych fragmentów wraz ze statusem i warunkami.
4. Otwórz dowody przy sporze, istotnej decyzji lub zależności od wersji.
5. Wskaż wybrane zalecenia i plan ich lokalnej weryfikacji.

Indeks sekcyjny FTS5 zwraca: ścieżkę, note_id, nagłówek/anchor, snippet, score wyszukiwania, status i źródła. Ranking trafności nie jest oceną prawdziwości. Indeks musi być odbudowywalny po ręcznej edycji Markdown. Domyślnie przeszukuje wiedzę kanoniczną, źródła tylko na żądanie. Polskie diakrytyki, angielskie terminy i aliasy objąć testami.

## 8. CLI i eksploatacja — wymagane możliwości

Nazwy można skorygować przed zamrożeniem kontraktu CLI:

```text
python -m kb_pipeline audit --vault ... --report ...
python -m kb_pipeline import-cache --input ... --workspace ...
python -m kb_pipeline run --config ... --dry-run
python -m kb_pipeline run --config ... --publish auto
python -m kb_pipeline resume --run-id ...
python -m kb_pipeline reindex --vault ...
python -m kb_pipeline search "bezpieczne kompaktowanie" --format json
python -m kb_pipeline rollback --publication-id ...
```

README musi wskazać poprawny cwd/PYTHONPATH lub instalację pakietu — powyższe polecenia to interfejs docelowy, nie już działające komendy.

- Timeouty, retry z backoff dla przejściowych błędów, respektowanie rate limits.
- Limity workerów, tokenów/kosztu, liczby pobrań i prób naprawy. Awaria nie może uruchamiać nieograniczonego kosztowo fallbacku.
- Stany odróżniają reject, defer i error. Raport pokazuje osobno wszystkie trzy.
- Raport przebiegu: nowe/zmienione notatki, dołączone dowody, odrzucone i wstrzymane tezy, błędy, koszt, czas, wyniki bramek.
- Brak harmonogramu w MVP; poprawne ręczne uruchomienie i wznowienie przed automatyzacją cykliczną.

## 9. Fazy i bramki odbioru

### Faza 0 — audit i baseline

- [ ] Audyt read-only: liczby plików, puste pliki, duplikaty ID/URL, błędne YAML, broken/ambiguous links, aliasy, źródła tez.
- [ ] Rozróżniaj stare błędy od błędów wprowadzonych przez nowy pipeline.
- [ ] Manifest snapshotu i procedura odtworzenia.
- [ ] Baseline wyszukiwania i zestaw przykładowych zadań.

Odbiór: raport bez zmian vaulta, sekrety nie ujawnione, aktualny skrypt i cache zachowane.

### Faza 1 — kontrakty i deterministyczny fundament

- [ ] Schematy, konfiguracja, SQLite/migracje schematu, adaptery interfejsów, fixture’y.
- [ ] Import cache, normalizacja, ID, rewizje, cache etapów, manifesty.
- [ ] Mock/fake provider pozwalający przejść pipeline bez sieci.

Odbiór: powtórzony import nie duplikuje danych; restart działa; testy offline przechodzą.

### Faza 2 — kontekst, filtr, ekstrakcja, weryfikacja

- [ ] Zweryfikowany adapter pobierania kontekstu, jawne braki.
- [ ] Jev bez odrzucania tylko za nieznany temat.
- [ ] Strukturalna ekstrakcja wielu tez i walidacja dowodów.
- [ ] Ograniczone retries, zapisy błędów, limity kosztu.

Odbiór: fixtures obejmują reply bez parenta, chiński wpis, ironię, opinię, warunkowe zalecenie, nowy temat, konflikt i awarię API. Niepublikowalne przypadki są wstrzymywane, nie zmyślane.

### Faza 3 — integracja i pilot w staging

Pilot: zarządzanie kontekstem agenta. Kandydaci: `Context Compaction`, `Bezpieczny punkt kompaktowania`, `Checkpointing sesji agenta`, `Persistencja stanu agenta`. To zbiór do analizy, nie nakaz scalenia wszystkich w jedną notatkę.

- [ ] Retrieval kandydatów i decyzje integracji.
- [ ] Synteza sekcji, śledzenie tez i poprawne linkowanie.
- [ ] Przejrzysty diff/propozycja zmian w odrębnym staging.
- [ ] Finalna walidacja syntezy.

Odbiór: brak nowych pustych node’ów i fallbacku do Harness; każda nowa istotna teza ma dowód; porównanie z bazową wersją pilota.

### Faza 4 — bezpieczny publisher i dostęp agenta

- [ ] Dry-run, auto-publish, allowlista, conflict detection, journal, backup i rollback.
- [ ] Testy awarii w połowie publikacji i ręcznej edycji pomiędzy planem a zapisem.
- [ ] FTS5, wyszukiwanie sekcyjne, przewodnik dla agenta.

Odbiór: idempotentny drugi przebieg, indeks zawiera stare i nowe materiały, rollback odtwarza poprzednie hashe zarządzanych plików i nie niszczy późniejszych cudzych zmian (w takim przypadku zatrzymuje się z konfliktem).

### Faza 5 — ewaluacja i kontrolowana migracja

- [ ] Porównanie starego i nowego podejścia na zestawie zadań.
- [ ] Import pozostałych źródeł i analiza istniejących notatek.
- [ ] Propozycje merge/archive/repair z mapą starych i nowych ID/ścieżek.
- [ ] Aktualizacja odsyłaczy przed wycofaniem starych plików, kopia i rollback.
- [ ] Puste pliki usuwać/archiwizować tylko jako jawny element planu migracji, nigdy automatycznie dlatego, że mają 0 bajtów.
- [ ] Aktualizacja README, parametrów konfiguracji i ewentualnego wrappera starego CLI.

Odbiór: brak utraty źródeł i ręcznej treści, brak regresji testów, pełny raport zmian. Nie uruchamiać masowej migracji bez ukończonego pilota i mechanizmu cofania.

## 10. Testy i ewaluacja

### Deterministyczne — obowiązkowe w CI/offline

- Normalizacja różnych formatów cache, brak daty/ID, rozróżnienie parent/quote.
- Deduplikacja, rewizje, cache hit/miss po zmianie promptu/modelu/kontekstu.
- Walidacja schematów i rozróżnienie błędu dostawcy od odrzucenia treści.
- Cytat obecny, nieobecny, wielojęzyczny, whitespace, negacja i warunek w otoczeniu.
- YAML z cudzysłowami i wieloliniowymi wartościami.
- Windows paths, kolizje po skróceniu tytułu, case-insensitivity, Unicode, traversal.
- Broken/ambiguous links, aliasy, zero pustych wygenerowanych notatek.
- Niepoparty nowy fragment dodany dopiero przez redaktora jest blokowany.
- Nieznany temat nie prowadzi do Harness ani automatycznego odrzucenia.
- Idempotencja, wznowienie, zachowanie wcześniejszych indeksów i ręcznych zmian.
- Lock, crash recovery i rollback, także konflikt z późniejszą zmianą.
- Wstrzyknięte instrukcje w tweetach nie mogą zmienić allowlisty ani wykonać poleceń.
- Logi i fixture’y bez sekretów.

### Jakość semantyczna

Przygotować 50–100 reprezentatywnych materiałów, w tym próbkę odrzuconych. Oddzielić zbiór do dostrajania od holdoutu, dzieląc po rozmowach, by fragmenty jednego wątku nie przeciekały między zbiorami.

Etykiety możliwe do sprawdzenia wprost w źródle: przydatność, kompletność kontekstu, zachowanie warunków, zgodność cytatu i atrybucji. Ground truth nie może być po prostu werdyktem tego samego modelu. Oceny eksperckiej prawdziwości nie udawać, jeśli jej nie mamy. Nie wymagać od użytkownika rutynowej akceptacji produkcyjnych notatek.

Mierzyć osobno:
- recall wartościowych materiałów i precision selekcji;
- odsetek niepopartych tez oraz utraty warunków;
- poprawność integracji: nowe / uzupełnienie / duplikat / spór;
- trafność retrieval na zadaniach i koszt kontekstu;
- skuteczność zadań implementacyjnych, gdy istnieje wykonywalny test;
- koszty, czas, liczbę wstrzymań i błędów.

Twarde bramki: zero nowych pustych plików, błędnych linków w publikowanym zakresie, utraty ręcznych zmian i nieprzypisanych istotnych tez. To nie gwarantuje prawdziwości treści. Progi jakości modelowej ustalić na baseline i zamrozić przed oceną holdoutu; brak pomiaru = brak podstaw do deklaracji sukcesu.

Przykładowe zadania retrieval: „agent traci stan po kompakcji”, „kiedy utrwalić checkpoint”, „czy każde przekroczenie progu tokenów wymaga natychmiastowego streszczenia”, „jak odróżnić zapis stanu od kompresji historii”. Odpowiedź musi zachowywać ograniczenia źródeł, nie wymuszać ustalonej z góry tezy.

## 11. Delegacja do gemini-swarm

### Zasady koordynatora

1. Najpierw faza 0 i zamrożenie schematów/interfejsów z fazy 1.
2. Każdy agent otrzymuje: zakres plików, kontrakty, wejścia/wyjścia, testy i zakazy. Nie wysyłać sekretów.
3. Agenci nie edytują wspólnie tego samego pliku. `schemas.py`, główna konfiguracja, CLI i dokumentacja integracyjna mają jednego właściciela.
4. Osobne worktree/gałęzie mogą nie zawierać aktualnych untracked i dirty danych — koordynator musi jawnie dostarczyć potrzebny snapshot/fixtures bez nadpisywania pracy użytkownika.
5. Równoleglić niezależne moduły po uzgodnieniu kontraktów, nie uruchamiać pięciu niezależnych przebudów całego skryptu.
6. Agenci implementują i testują na fixture’ach/staging. Tylko koordynator może uruchomić publikację/migrację rzeczywistego vaulta po bramkach.
7. Raport agenta: zmienione pliki, uruchomione testy i wyniki, założenia, znane ograniczenia, nowe zależności. Nie uznawać zadania za ukończone przy failing tests.
8. Nie deklarować integracji live, jeżeli testowano wyłącznie mocki. Płatne wywołania ograniczyć jawnym budżetem konfiguracyjnym.

### Pakiety pracy

| Pakiet | Zakres | Zależności |
|---|---|---|
| P0: koordynator/fundament | audit, snapshot, schematy, konfiguracja, storage, interfejsy providerów | brak |
| P1: ingestion | import cache, normalizacja, adapter Apify, ContextBundle | P0 |
| P2: inteligencja | Jev, ekstrakcja, weryfikacja, prompty, fake providers | P0; fixture ContextBundle |
| P3: retrieval | parser Markdown, aliasy, indeks sekcyjny FTS5, wyszukiwanie | P0 |
| P4: integracja/redakcja | decyzje integracji, patche, rendering, finalny verifier | P2 + P3 |
| P5: publikacja | walidatory, allowlista, journal, locks, recovery, rollback | P0; kontrakt NotePatch |
| P6: integrator/ewaluacja | CLI, e2e, pilot, metryki, README, migracja | P1–P5 |

P1/P2/P3/P5 mogą pracować równolegle po P0, korzystając z uzgodnionych fixture’ów. P4 i P6 nie powinny obchodzić nieukończonych zależności przez własne alternatywne schematy.

## 12. Poza zakresem pierwszego wdrożenia

- Zmiana całego vaulta na nową taksonomię bez pilota.
- Grafowa baza danych, vector DB, własny serwer MCP, panel WWW.
- Automatyczne „udowadnianie prawdziwości” opinii ekspertów przez głosowanie modeli.
- Pełne pobieranie całego X i dowolnych linkowanych stron.
- Harmonogram produkcyjny przed obsługą restartu i limitów kosztu.
- Automatyczne usuwanie starych plików tylko dlatego, że nie pojawiły się w nowej paczce.

## 13. Pierwsze polecenie dla kolejnego koordynatora

> Przeczytaj cały `plan.md`, aktualny kod i git status. Nie implementuj wszystkiego naraz. Rozpocznij od audytu read-only i uzgodnienia kontraktów danych. Następnie deleguj niezależne pakiety zgodnie z sekcją 11. Pierwszym działającym rezultatem ma być offline dry-run pilota zarządzania kontekstem, z trwałymi artefaktami i testami, bez zmian w istniejącym vaulcie. Dopiero potem dołącz wywołania live, bezpieczną publikację i migrację. Zachowuj aktualny stan użytkownika i raportuj rzeczywiste wyniki testów.
