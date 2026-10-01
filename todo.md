# Pozostała praca — pipeline wiedzy

> Stan na `20fcb56`. To lista tego, czego jeszcze nie ma. Nie jest raportem z wykonania.
> Vault nie był publikowany. Nie zaczynać migracji przed działającym rollbackiem.

## Zrobione

- Audyt read-only, snapshot z hashami SHA-256, import cache, kontrakty Pydantic, SQLite.
- Offline pilot na fixture, filtr Jev (`jev-evaluate`), heurystyczna ekstrakcja claimów (`claim-extract`).
- Sprawdzenie cytatu, wrapper weryfikacji semantycznej, wyszukiwanie sekcji FTS5 jako biblioteka.
- Decyzje integracji zapisywane poza vaultem. Planner publikacji jest tylko do odczytu.
- Publisher: `apply_publication`, journal, lock, backup, `rollback_publication` i `recover_publication`. Podmiana jest atomowa per plik, nie dla całego vaulta. Późniejsza ręczna zmiana zatrzymuje rollback konfliktem. CLI nadal nie publikuje.

## Do zrobienia

- [ ] **Podłączyć etapy do CLI.** Brakuje `run`, `resume`, `reindex`, `search` i `rollback`. Istniejące komendy to `audit`, `snapshot`, `verify-snapshot`, `import-cache`, `pilot-dry-run`, `jev-evaluate`, `claim-extract`.
- [ ] **Pobieranie brakującego kontekstu.** Brak parenta ma zostać jawnym brakiem. Nie zgadywać treści z URL-a ani z samej odpowiedzi. Adapter ma pokazać, co faktycznie zwraca actor Apify.
- [ ] **Weryfikacja semantyczna na żywym modelu.** Jest wrapper i fake checker. Brakuje wywołania modelu z limitem prób, zapisem błędu i bez ustawiania `independently_validated`.
- [ ] **Ekstrakcja claimów przez model.** Obecna ekstrakcja jest heurystyką offline. Model ma zwracać listę tez tylko z dostarczonych dowodów, z dokładnym cytatem i jawnymi brakami.
- [ ] **Przewodnik dla agenta.** Krótka mapa: tematy, aliasy, statusy, droga do dowodów. Najpierw w stagingu, bez ładowania całego vaulta do promptu.
- [ ] **Ewaluacja holdout.** Osobny zbiór od dostrajania, dzielony po rozmowach. Mierzyć selekcję, utratę warunków, integrację i retrieval. Brak pomiaru nie jest sukcesem.
- [ ] **Kontrolowana migracja.** Dopiero po pilocie publikacji i rollbacku. Propozycje merge/archive/repair, mapa starych i nowych ID, kopia i aktualizacja odsyłaczy. Pustych plików nie usuwać tylko dlatego, że mają 0 bajtów.
- [ ] **README i kontrakt CLI.** Opisać nowe moduły i brakujące komendy zgodnie z faktycznym kodem. Nie deklarować publikacji, której nie ma.

## Poza tą listą

Grafowa baza, vector DB, MCP, panel WWW, harmonogram produkcyjny i automatyczne usuwanie starych notatek pozostają poza pierwszym wdrożeniem.
