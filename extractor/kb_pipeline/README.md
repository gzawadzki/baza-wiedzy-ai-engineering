# Pipeline wiedzy — stan wdrożenia

Faza 0: audyt read-only i snapshot wiedzy z manifestem SHA-256. Faza 1: kontrakty Pydantic, offline import cache z rewizjami SQLite, filtrowanie Jev pojedynczych źródeł (`jev-evaluate`) oraz ograniczona deterministyczna ekstrakcja claimów (`claim-extract`). Pionowy przebieg offline end-to-end jest dostępny przez `run --offline`. Retrieval CLI udostępnia komendy `reindex` i `search`. Biblioteka ma `apply_publication`, `rollback_publication` i `recover_publication`, ale publikacja do vaulta pozostaje zablokowana (`run --publish` jest zablokowane); brak komendy `rollback` (wznowienie przerwanego przebiegu offline obsługuje komenda `resume`). Stary `extract_kunchen_tips.py` pozostaje osobny i może pisać do vaulta; poniższe komendy tego nie robią.

Uruchamiaj z katalogu `extractor/` po instalacji `pip install -r requirements.txt` (do uruchomienia testów dodatkowo `pip install pytest`). Ścieżki raportu, snapshotu i workspace muszą wskazywać poza vault:

```bash
python -m kb_pipeline audit --vault .. --report ../../kb-audit.json
python -m kb_pipeline snapshot --vault .. --destination ../../kb-snapshot
python -m kb_pipeline verify-snapshot --destination ../../kb-snapshot
python -m kb_pipeline import-cache --input . --vault .. --workspace ../../kb-workspace
python -m kb_pipeline jev-evaluate --vault .. --workspace ../../kb-workspace --source-id x:123
python -m kb_pipeline claim-extract --vault .. --workspace ../../kb-workspace --source-id x:123 --content-hash <sha256>
python -m pytest -q tests
```

Import akceptuje plik `*_raw_tweets.json` lub katalog takich plików. Nie pobiera wpisów ani brakujących parentów; relacje parent/quote i braki są jawne. Brak ID lub treści jest błędem rekordu, nie negatywną oceną treści. `fetched_at` z mtime cache to przybliżenie chwili utrwalenia kopii, a nie data rzeczywistego pobrania z X. Ponowny import zachowuje istniejące rewizje, nie tworzy duplikatów. Snapshot nie zawiera `.env`, kodu ani konfiguracji Obsidiana; przed jakąkolwiek migracją sprawdź manifest i osobno zabezpiecz pozostałą pracę użytkownika.

## Offline pilot dry-run

Z katalogu `extractor/` uruchom dokładnie:

```bash
python -m kb_pipeline pilot-dry-run --vault .. --workspace ../../kb-pilot-workspace --fixture tests/fixtures/pilot_context.json
```

`--vault` wskazuje istniejący katalog wiedzy, a `--workspace` — katalog poza nim. Ścieżka workspace nie może znajdować się w vaultcie (także przez alias lub dowiązanie symboliczne). Polecenie wypisuje na stdout jeden obiekt JSON z podsumowaniem przebiegu i kończy się kodem różnym od zera, jeśli wynik ma `status: error` albo dane wejściowe są nieprawidłowe.

### Fixture semantics

`tests/fixtures/pilot_context.json` jest małym, syntetycznym wejściem offline. Zawiera jeden `SourceRecord` z kontekstem kompaktowania, jedno `Claim` z cytatem pasującym do tekstu źródła, relację `supports` w `mock_semantic_relations` oraz zapytanie `compaction`. Autor, `raw_ref` i treść claimu są oznaczone jako fixture/synthetic; nie są wypowiedzią ani oceną prawdziwości prawdziwego eksperta. Relacja jest danym testowym, a nie wynikiem niezależnej oceny.

Fixture jest walidowany przez ścisłe kontrakty Pydantic. Identyfikator źródła ma postać stabilnego `x:<liczbowy_id>`, hash treści jest wymagany, a cytat dowodu musi występować w rekordzie źródła. Zapytanie służy wyłącznie do lokalnego, tylko do odczytu wyszukiwania sekcji istniejącego vaultu. Ścieżki zwrócone jako kandydaci nie są automatycznie uznawane za poparcie ani za miejsce publikacji.

### Evidence and artifacts

Weryfikacja cytatu jest deterministycznym sprawdzeniem lokalnego tekstu. Wynik semantyczny pochodzi wyłącznie z mocka w fixture (`independently_validated` pozostaje fałszywe), więc propozycja nie dowodzi poprawności claimu ani nie zastępuje weryfikacji źródłowej. Kontekst może być oznaczony jako niepełny lub niedostępny; brakujący kontekst należy zachować jako ograniczenie.

Dla identycznego fixture hash tworzony jest katalog `offline-<fixture_hash>` w workspace. Zawiera on bazę indeksu i cache, `proposal.md` (gdy claim przejdzie bramkę), oraz artefakty JSON: `validated_input_summary.json`, `context_bundles.json`, `verification_results.json`, `search_candidates.json` i `proposal_decisions.json`. Manifest przebiegu jest zapisywany w lokalnym cache. Ponowne uruchomienie z tym samym fixture korzysta z tego samego katalogu i nie zmienia vaultu.

Pilot nie uruchamia Jev, modelu językowego, ekstrakcji, migracji ani starego `extract_kunchen_tips.py`. Etapy semantyki i publikacji pozostają odroczone. `proposal.md` jest wyłącznie propozycją do ręcznego przeglądu: nie ma automatycznej publikacji ani zapisu do notatek vaultu.

## Publisher (biblioteka, bez komendy CLI)

`apply_publication` zapisuje tylko ścieżki z allowlisty, po ponownym sprawdzeniu hashy bazowych. Każdy plik jest podmieniany osobnym `os.replace` w jego katalogu; kilka takich podmian nie jest transakcją całego vaulta. Journal, lock i backup leżą w workspace poza vaultem. `rollback_publication` przywraca poprzednie bajty zarządzanych plików. Ręczna zmiana po zapisie zatrzymuje rollback konfliktem i niczego nie nadpisuje. Przerwany zapis zostawia journal `applying`; `recover_publication` cofa już zapisane pliki i nie dokańcza pozostałych. Ponowne wywołanie z tą samą treścią i zgodnymi hashami nie zapisuje plików drugi raz.

### Tests

Uruchom test CLI z katalogu `extractor/`:

```bash
python -m pytest -q tests/test_cli_pilot.py
python -m pytest -q tests
```

Pełny zestaw obejmuje 60+ istniejących testów (w tym test subprocess dla tego pilot dry-run).

## Filtrowanie Jev (`jev-evaluate`)

Polecenie `jev-evaluate` uruchamia bramkę filtrowania jakościowego i tematycznego dla pojedynczego zaimportowanego źródła X:

```bash
python -m kb_pipeline jev-evaluate --vault .. --workspace ../../kb-workspace --source-id x:123
```

Opcjonalnie przy wieloznacznych rewizjach:
```bash
python -m kb_pipeline jev-evaluate --vault .. --workspace ../../kb-workspace --source-id x:123 --content-hash <sha256>
```

Wymuszenie ponownego zapytania do API (zamiast odczytu z lokalnego cache):
```bash
python -m kb_pipeline jev-evaluate --vault .. --workspace ../../kb-workspace --source-id x:123 --refresh
```

### Zasada działania i rozróżnienie etapów

- **Filtrowanie, a nie weryfikacja czy publikacja**: `jev-evaluate` odpowiada wyłącznie na pytania o wartość inżynierską (`engineering_value`), wystarczalność kontekstu (`context_sufficient`) oraz routing tematyczny (`topic`, w tym prawidłowa kategoria `other`). Nie ekstrahuje twierdzeń, nie weryfikuje cytatów w notatkach ani nie modyfikuje vaulta. Vault pozostaje ściśle tylko do odczytu.
- **Deterministyczna rezolucja rewizji**: Rekord źródłowy oraz powiązany kontekst (parent / quote) pobierane są z bazy `sources.sqlite3` w workspace. Jeśli dane źródło lub powiązany kontekst zawiera wiele rewizji, a nie wskazano jednoznacznego `--content-hash`, komenda kończy się błędem (`fail closed`).
- **Idempotentne odtwarzanie i oszczędzanie zapytań**: Wyniki filtrowania są indeksowane w `StageCache` (`stage_cache.sqlite3`) według dokładnego identyfikatora i hasha źródła, hasha zmontowanego kontekstu, modelu oraz wersji polityki i pytań wraz z progami. Ponowne uruchomienie dla tych samych danych korzysta z lokalnego cache i nie wysyła zapytania do API, chyba że podano flagę `--refresh`.
- **Wymagany klucz API dla wywołań na żywo**: Dla wywołań niebędących odczytem z cache (oraz przy użyciu flagi `--refresh`) wymagana jest zmienna środowiskowa `TYPESAFE_API_KEY`. W przypadku jej braku lub pustej wartości pipeline zatrzymuje się w bezpiecznym stanie (`fail closed`) bez wysyłania zapytania do API i bez utrwalania częściowego stanu. Odczyty z cache (idempotent replay) działają offline i nie wymagają `TYPESAFE_API_KEY`.
- **Bezpieczeństwo workspace i brak sekretów w artefaktach**: Workspace oraz katalog artefaktów muszą leżeć poza vaultem (walidowane również dla dowiązań symbolicznych). Artefakty JSON w `workspace/artifacts` oraz wpisy w cache nie zawierają nagłówków, tokenów ani poświadczeń. Przy błędach sieciowych lub niepoprawnej odpowiedzi API pipeline zatrzymuje się w bezpiecznym stanie z błędem JSON.

## Ekstrakcja claimów (`claim-extract`)

Polecenie `claim-extract` uruchamia deterministyczny, offline etap ekstrakcji konkretnych twierdzeń inżynierskich z pojedynczej, wskazanej rewizji źródła, która przeszła pomyślnie ocenę filtrowania Jev:

```bash
python -m kb_pipeline claim-extract --vault .. --workspace ../../kb-workspace --source-id x:123 --content-hash <sha256>
```

Opcjonalnie ze wskazaniem modelu (domyślnie spójnie z filtrem `jev-latest`):
```bash
python -m kb_pipeline claim-extract --vault .. --workspace ../../kb-workspace --source-id x:123 --content-hash <sha256> --model jev-latest
```

### Zasady działania, ograniczenia i granice etapu

- **Wymóg istniejącej pozytywnej oceny Jev w cache**: Ekstrakcja wymaga obecności wpisu w `StageCache` z oceną `decision: extract`, `bypass: false` oraz zgodnymi hashami źródła i kontekstu powiązanego. W przypadku braku oceny, niejednoznacznych lub przeterminowanych rewizji, innego modelu/polityki lub decyzji `reject`/`defer` pipeline zatrzymuje się w bezpiecznym stanie (`fail closed`) bez wywoływania API i bez kosztów. Jev nigdy nie jest wywoływany automatycznie podczas ekstrakcji.
- **Konserwatywna ekstrakcja bez fabrykowania treści**: Twierdzenia są wyodrębniane offline z tekstu focus source przy użyciu udokumentowanych heurystyk inżynierskich (rekomendacje, obserwacje empiryczne, ograniczenia, eksperymenty). Każde twierdzenie opiera się na dokładnym wycinku tekstu źródłowego (`exact quote`), a jego poprawność jest weryfikowana deterministycznym sprawdzeniem podciągu i offsetów `[start:end]` względem przypiętej rewizji. Jeśli źródło nie zawiera jednoznacznych twierdzeń technicznych, generowana jest pusta propozycja (`claims: []`), a nie wymyślone twierdzenia.
- **Stabilne identyfikatory i metadane dowodowe**: Każde twierdzenie otrzymuje stabilny identyfikator powiązany z rewizją źródła oraz slotem pozycji. W dowodach (`evidence`) zapisywany jest dokładny `content_hash` źródła. Status kontekstu (`context_status`) oraz brakujące identyfikatory (`missing_ids`) są jawnie odnotowane w propozycji i ograniczeniach twierdzenia.
- **Artefakty stagingowe wyłącznie poza vaultem**: Propozycja maszynowa (`workspace/proposals/claim_proposals_*.json`) oraz czytelna wersja Markdown (`workspace/proposals/claim_proposals_*.md`) zapisywane są wyłącznie w workspace poza vaultem. Zostają wyraźnie oznaczone jako niezweryfikowane i nieopublikowane (`UNVERIFIED / UNPUBLISHED — STAGING ONLY`).
- **Niezmienność vaulta (vault immutability)**: Polecenie nie tworzy ani nie modyfikuje żadnych notatek Obsidiana w vaultcie. Niezależna weryfikacja semantyczna oraz integracja/publikacja pozostają odroczone do kolejnych etapów.
- **Idempotentne odtwarzanie (replay)**: Ponowne wywołanie z identycznymi parametrami korzysta z zapisanego stanu w `StageCache` (`cached: true`) i nie modyfikuje plików.


## Retrieval w CLI (`reindex`, `search`)

Existing retrieval (SQLite FTS5 over note sections) is now reachable from the CLI and is
independent of the rest of the run. The vault is only ever read; the index always lives in the
workspace, outside the vault. No models, no embeddings, no vector database: the tokenizer is the
deterministic `unicode61` FTS5 tokenizer, so a Polish query with diacritics matches the same word
typed without them, and English aliases match Polish content.

```bash
python -m kb_pipeline reindex --vault .. --workspace ../../kb-workspace
python -m kb_pipeline search "kompaktowanie" --workspace ../../kb-workspace --format json
python -m kb_pipeline search "\"bezpieczny punkt\"" --workspace ../../kb-workspace
python -m kb_pipeline search "safe checkpoint" --workspace ../../kb-workspace --limit 5 --include-sources
python -m kb_pipeline search "harness" --workspace ../../kb-workspace --vault ..
```

- `--workspace` is explicit and required for both commands; there is no hidden index in the current
  directory. It points at the workspace directory, and the index is `<workspace>/retrieval/index.sqlite3`
  with the metadata `<workspace>/retrieval/index-info.json`.
- `reindex` writes only the workspace (`vault_writes: 0`). It never writes, moves, or deletes a
  note, and it does not require `--apply`: indexing is not publication into the vault.
- `search` is read-only. It opens the index read-only, touches neither the vault nor the workspace,
  and its optional `--vault` selector is resolved and validated read-only and echoed in the output,
  so a caller can label the index they searched.
- `reindex` is idempotent: rebuilding from an unchanged vault yields the same `sections` count, the
  same content `fingerprint` (SHA-256 over the indexed rows) and byte-identical JSON output. Note
  ids fall back to a deterministic hash of the relative path, so a note without `note_id` keeps its
  identity across rebuilds. A manual edit or a deleted note disappears from the index on the next
  `reindex`.
- JSON output is deterministic and structured. `search` prints `{"status", "command", "query",
  "workspace", "index", "include_sources", "limit", "count", "results"}`; every result has exactly
  `path`, `note_id`, `heading`, `anchor`, `snippet`, `score`, `status`. `reindex` prints `{"status",
  "command", "vault", "workspace", "index", "sections", "fingerprint", "vault_writes"}`.
- Errors are structured, with a stable `code` and a `hint` where a next step helps, and exit code 1:
  `missing_workspace`, `missing_vault`, `invalid_workspace`, `invalid_vault`, `missing_index`
  (hint: run `reindex`), `empty_query`, `invalid_limit` (1–100), `index_inside_vault`,
  `index_write_failed`, `search_failed`. Nothing is written on an error path.
- `--format` accepts `json` and defaults to `json`, so an agent always parses the same structure.
- Query syntax stays the existing deterministic FTS5 one: separate words are combined with AND, a
  double-quoted span is a phrase, and a trailing `*` is a prefix. Diacritics are folded, so
  `"pojęcie"` and `"pojecie"` return the same hits; word forms are not stemmed, so
  `"weryfikacja"` does not match `"weryfikacje"`.

Tests: `python -m pytest -q tests/test_search_cli.py` (synthetic vault in `tmp_path`, offline).


## Przebieg pionowy offline (`run --offline`)

`run --offline` to jedna komenda end-to-end: cache -> `SourceStore` -> kontekst -> bramka
lokalna -> CLM -> Jev -> kategoria -> ekstrakcja tez -> weryfikacja -> integracja ->
`NotePatch` -> plan publikacji **read-only**. Vault jest w tym trybie tylko czytany.

```bash
# jawne wejscie cache: pojedynczy plik <handle>_raw_tweets.json
python -m kb_pipeline run --offline \
  --offline-input ../../DrJimFan_raw_tweets.json \
  --vault .. --workspace ../../kb-workspace

# katalog z plikami *_raw_tweets.json (jak dotad --cache-dir)
python -m kb_pipeline run --offline --cache-dir ../.. \
  --vault .. --workspace ../../kb-workspace

# pojedynczy wpis (identyfikatory x:<id> sa powtarzalne)
python -m kb_pipeline run --offline --offline-input ../.. \
  --source-id x:123 --source-id x:456 \
  --vault .. --workspace ../../kb-workspace
```

### Zasady, ograniczenia i granice trybu offline

- **Dostawcy sa jawnie wstrzykiwani i zawsze oznaczeni**: `--offline` wybiera jawnie
  `fake-offline` (`kb_pipeline.offline_flow.fake_providers`). Kazdy artefakt zawiera
  `"provider": {"mode": ..., "fake": ...}`, a `summary.json` zapisuje `provider_mode`.
  Podmiana dostawcy na zywy nie moze wystapicc niepostrzezenie: `FlowProviders.mode` jest
  polem obowiazkowym, a wartosc inna niz `"fake-offline"`/`"live"` jest bledem. **Fake'i
  opisuja zachowanie na fixture'ach, nie jakosc semantyczna i nie poprawnosc modeli.**
- **Brak sieci i brak kluczy**: tryb offline nie pobiera z aktora i nie wywoluje zadnego
  dostawcy HTTP. Cache jest jedynym zrodlem wpisow.
- **`--vault` jest wymagane i uzywane read-only**: zapisuje sie wylacznie w workspace.
  Plan publikacji powstaje przez `publication.plan_publication` i ma `mode: plan_only`,
  `applied: false`; zawiera diff, ktorego **nie** wykonuje. `run --publish` nadal jest
  odrzucane, takze w trybie offline, przed jakimkolwiek wywolaniem dostawcy.
- **Rozdzielone liczniki `reject` / `defer` / `error`**: `reject` to ocena tresci (pusty
  focus, sam link, sama reakcja, reklama, cytat spoza tekstu autora), `defer` to
  niepewnosc (za malo kontekstu, kategoria ponizej pewnosci, `unsupported`), `error` to awaria
  etapu lub dostawcy. Awaria dostawcy nigdy nie jest zapisywana jako `defer`.
- **Progi w jednym miejscu, wartosci bez zmian**: `kb_pipeline/thresholds.py` (`DEFAULT_THRESHOLDS`)
  przepisuje istniejace stale (`CLAIM_REJECT` 0.30, `PROMO_REJECT` 0.75,
  `CATEGORY_CONFIDENCE` 0.50, Jev 0.70/0.60/0.20) i zapisuje je w `summary.json`
  (z odciskiem i pochodzeniem kazdej wartosci). Progi **nie wchodza** do klucza cache:
  zmiana progu przelicza decyzje z surowej odpowiedzi, bez ponownego wywolania dostawcy.
  Progi sa progami operacyjnymi, nie gwarancja jakosci.
- **Cytat musi pochodzic z tekstu autora**: tesa wskazujaca cytat rodzica lub cytowanego wpisu
  jest odrzucana jako cudza (`quote_not_in_author_text`). Rodzic, cytat i watk zyjaja w
  `ContextBundle.related[]` z `role` i `provenance`, a `focus.text` to wylacznie tekst autora.
- **Trwale artefakty i replay**: `workspace/runs/<run_id>/artifacts/*.json`, `proposed_section.md`,
  `manifest.json`, `summary.json` oraz `RunManifest` w `StageCache`. Dla każdego źródła
  powstaje niezależny `run_id` wyliczany z jego identyfikatora i haszy, co izoluje artefakty
  w przebiegach wsadowych. Identyczny powtórzony przebieg daje `provider_calls: 0` i te same
  `NotePatch`. Filtr `--handles` wymaga dopasowania do plików cache (brak dopasowania kończy
  się jawnym błędem).
- **Poza zakresem tego trybu**: zapis do vaulta, cokolwiek w `Zrodla/`, migracja, embeddingi,
  harmonogram. `independently_validated` pozostaje `false`; wynik weryfikacji oznacza
  wylacznie "tekst zrodla wspiera teze w zakresie podanym przez zrodlo", nie prawdziwosc.

Testy: `python -m pytest -q tests/test_offline_flow.py` (syntetyczny vault w `tmp_path`,
offline, bez kluczy i bez sieci).
## Stan, cache i budzet (PKG-2B)

Cztery rzeczy, ktore przebieg offline wczesniej udawal, a teraz ma: trwala
tozsamosc tezy niezalezna od rewizji zrodla, punkty kontrolne z realnym
wznowieniem, klucz surowej oceny bez progow, oraz usage i limity prob/tokenow
w manifescie.

### Klucz zaleznosci, nie nazwa katalogu

`manifest.input_hashes` zawiera `vault_fingerprint` (SHA-256 z sciezek i bajtow
notatek, ktore czyta indekser i publisher) oraz `index_fingerprint` i
`notes_fingerprint`. Nazwa katalogu vaultu jest sciezka, nie zaleznoscia.
Klucz etapu to wciaz `StageCache.key(stage, input, context, model, prompt,
schema)`; **progi, decyzja, wersja polityki, budzet i run_id sa poza kluczem**.
`live_jev.evaluate_live_source` takze tego wymaga: zmiana progu albo polityki
przelicza decyzje z cache i **nie wywoluje modelu ponownie**
(`decision_fingerprint` opisuje decyzje, nie surowa odpowiedz).

Zmiana zawartosci notatki uniewaznia tylko to, co ja czytalo: etap integracji
przelicza sie od nowa, a CLM, Jev, kategoria i ekstrakcja odtwarzaja sie z cache
bez nowego wywolania. Zmiana modelu, promptu, kontekstu albo rewizji zrodla
uniewaznia etap, ktory te rzeczy widzial.

### Trwala tozsamosc tezy i notatki

`kb_pipeline/identity.py` prowadzi rejestr w workspace
(`identity/registry.json`, zapisywany atomowo):

- identyfikator jest nadawany **raz**, przy pierwszym zapisie, i nie zalezy od
  tytulu notatki ani od pojedynczego tweeta (`kb-clm-...` dla nowej notatki);
- dopasowanie idzie po **id zrodla + znormalizowanym cytacie**, nigdy po
  offsetach: przesuniecie fragmentu w tekscie nie tworzy nowej tozsamosci;
- zmiana warunkow, ograniczen, zakresu, rodzaju lub wersji technologii to
  **nowa rewizja tej samej tezy** (`revision: 2`), a rewizja zrodla jest
  zapisywana obok, nie wewnatrz tozsamosci;
- ten sam cytat dajacy inna teze (parafraza) albo kilka rekordow dla tego samego
  dowodu to **jednoznaczny brak dopasowania**: oba rekordy zostaja jako kandydaci
  do uzgodnienia (`status: "ambiguous"`, `unresolved_candidates`). Nic nie jest
  scalane automatycznie, a kazdy raport ma `semantic_dedup: "not guaranteed"`;
- ten sam cytat z **innego** zrodla to kandydat do scalenia, nie scalenie.

Artefakty: `artifacts/claim_identity.json` (wynik tozsamosci, bajtowo stabilny
miedzy powtorzeniami), `artifacts/note_identity.json`, `identity/registry.json`.
Przejscie (`new` / `unchanged` / `revision` / `ambiguous`) jest w `summary.json`
i w checkpointach, bo rozni sie miedzy pierwszym zapisem a odtwarzaniem.

### Wznowienie: `resume --run-id ... --workspace ...`

Kazdy etap zapisuje po sobie `checkpoints.json` (status, klucz cache, SHA-256
kazdego artefaktu) i `artifacts/raw/<etap>.json` z surowa odpowiedzia dostawcy.

**Kazde zrodlo ma wlasny przebieg:**
`offline_cli` wylicza osobny `run_id` na zrodlo, wiec kazde ma wlasny
`runs/<run_id>/` z wlasnymi `artifacts/`, `artifacts/raw/`, `summary.json`,
`manifest.json`, `usage.json`, `checkpoints.json` i `run_descriptor.json`.
Dzielenie jednego `artifacts/` miedzy zrodlami boku oznaczalo, ze drugie
zrodlo nadpisywalo dowody pierwszego, a wznowiony przebieg znajdowal digest
nalezacy do innego zrodla. Katalog partii (`batch_run_dir`) trzyma tylko
`run_descriptor.json`, `summary.json`, `usage_manifest.json` i
`usage_log.jsonl`; `result["runs"][i]["run_dir"]` wskazuje przebieg zrodla.
`resume` czyta `run_descriptor.json` i:

- etap dostawcy, ktory sie ukonczyl, ma ten sam klucz i niezmieniony artefakt,
  jest **podawany z tego artefaktu** - bez ponownego wywolania, nawet gdy
  `stage_cache.sqlite3` zniknie;
- brak albo zmieniony artefakt jest **zgloszony** (`artifact_problems`) i etap jest
  przeliczany; jesli zniknela tez baza cache, dostawca jest wolany jeszcze raz,
  ale tylko dla tego etapu;
- brak `run_descriptor.json` to **odmowa**, nie zgadywanie: resume nie wie, czym
  byl przebieg. Podobnie resume odmawia podmiany `fake-offline` na przebieg
  `live` - zywe dostawcy trzeba wstrzyknac jawnie.

```bash
python -m kb_pipeline run --offline --offline-input ../../cache.json \
  --vault .. --workspace ../../kb-workspace
python -m kb_pipeline resume --run-id offline-flow-<hash> --workspace ../../kb-workspace
```

### Usage i budzet

`usage.json` (na przebieg zrodla), `usage_manifest.json` i `usage_log.jsonl`
(partia) plus `summary.usage` i `summary.budget`.
Brak usage od dostawcy to **`not_measured`**, nigdy `0`; `RunManifest.token_count`
i `.cost` pozostaja `null`, a `.duration_seconds` jest zmierzony.

`--max-attempts` i `--max-tokens` to twarde limity sprawdzane **przed** wywolaniem,
ktore by je przekroczono. Przekroczenie zatrzymuje przebieg ze statusem
`budget_exhausted` i `budget_stopped: true` w raporcie - nie `defer` i nie
`error`, a liczniki `extract`/`reject`/`defer`/`error` zachowuja swoje
znaczenie. Rezerwacja
tokenow to najwieksze zmierzone wywolanie; wywolanie, ktore nic nie zglosilo,
jest obciazane ta rezerwacja. Gdy z `--max-tokens`
zaden dostawca nie raportuje tokenow, przebieg zatrzymuje sie po pierwszej
probie pomiaru: limit, ktorego nie da sie zmierzyc, nie jest limitem, a ta jedna
proba jest jawnie raportowana - nigdy cicha, bez limitu.
**Budzet nie jest gwarancja kosztu ani udowodniona granica tokenow.**
Tylko limit prob liczy kazde wywolanie; tokeny sa ograniczone wylacznie tym, co
dostawcy zglosily, a koszt pozostaje niezmierzony tam, gdzie nikt go nie zwraca.
Rezerwacja oparta na poprzednich, zmierzonych wywolaniach **nie jest gorna granica**
`budzet.not_guaranteed`.

### Poza zakresem tego pakietu

`independently_validated` nadal `false`, deduplikacja semantyczna nie jest
gwarantowana, publisher pozostaje plan-only (`run --publish` odrzucone), a
zapis do vaultu i wszystko w `Zrodla/` pozostaja poza zakresem. Synchronizacja
progow jest jednym miejscem (`thresholds.DEFAULT_THRESHOLDS`); `local_gate` i
`filtering` maja te same wartosci jako wiazane nazwy, nie drugie kopie.

Testy: `python -m pytest -q tests/test_state_cache.py` (offline, wstrzyknieci
dostawcy, syntetyczny vault w `tmp_path`, bez kluczy i bez sieci).
