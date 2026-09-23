# Pipeline wiedzy — stan wdrożenia

Faza 0: audyt read-only i snapshot wiedzy z manifestem SHA-256. Faza 1: kontrakty Pydantic, offline import cache z rewizjami SQLite oraz filtrowanie Jev pojedynczych źródeł (`jev-evaluate`). **Nie ma jeszcze** pełnej ekstrakcji claimów, automatycznej publikacji notatek ani komend `run` i `resume`; pilot ma wyłącznie lokalne wyszukiwanie read-only. Stary `extract_kunchen_tips.py` pozostaje osobny i może pisać do vaulta; poniższe komendy tego nie robią.

Uruchamiaj z katalogu `extractor/` po instalacji `pip install -r requirements.txt` (do uruchomienia testów dodatkowo `pip install pytest`). Ścieżki raportu, snapshotu i workspace muszą wskazywać poza vault:

```bash
python -m kb_pipeline audit --vault .. --report ../../kb-audit.json
python -m kb_pipeline snapshot --vault .. --destination ../../kb-snapshot
python -m kb_pipeline verify-snapshot --destination ../../kb-snapshot
python -m kb_pipeline import-cache --input . --vault .. --workspace ../../kb-workspace
python -m kb_pipeline jev-evaluate --vault .. --workspace ../../kb-workspace --source-id x:123
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
