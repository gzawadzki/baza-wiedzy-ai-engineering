---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Thu Sep 17 07:59:19 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100494796687340001"
kategoria: "Architektura systemów agentowych / Inżynieria kontekstu"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Brief zadania jako obowiązkowy element kontekstu wejściowego przy delegacji do agenta

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Thu Sep 17 07:59:19 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100494796687340001)
- **Konwersacja:** Odpowiedź w dyskusji (@ArtifexPraxis)
- **Kluczowe pojęcia:** [[Context Compaction|Inżynieria kontekstu]] [[Harness|Systemy multi-agentowe]] [[Harness|Task Brief]] [[Harness|Orkiestracja agentów]] [[Kaskady Modeli i Routing Pewności|Routing modeli]] [[Harness|Zarządzanie budżetem tokenowym]] [[Harness|Audytowalność decyzji agenta]] [[Firstmate i Agenci Wykonawczy]]

---

## Kontekst i problem
Autor odpowiada na pytanie o sposób działania orkiestratora agentów („firstmate”). Wyjaśnia, że zanim firstmate wyśle wykonawcę („crewmate”) do realizacji zadania, musi najpierw sporządzić brief zadania. Ten brief, w połączeniu z regułami dyspozycji (dispatch rules) zdefiniowanymi przez użytkownika oraz danymi o limitach/kwotach (quota data), tworzy kontekst wejściowy dla komponentu decyzyjnego („Jev”). Jest to opis konkretnej, trzyskładnikowej kompozycji kontekstu sterującego delegacją i wyborem modelu/ścieżki wykonania.

## Rada inżynierska
W systemie wieloagentowym traktuj brief zadania jako artefakt obowiązkowy i tworzony PRZED delegacją, a nie po niej. Kontekst wejściowy dla routera/decydenta buduj jawnie z trzech źródeł: (1) brief zadania — cel, zakres, kryteria akceptacji; (2) reguły dyspozycji użytkownika — polityki wyboru wykonawcy/modelu; (3) dane o limitach i zużyciu kwot — budżet tokenowy, koszt, dostępność. Taka separacja czyni decyzję o routingu audytowalną, reprodukowalną i podatną na testy regresyjne (podmiana jednego z trzech wejść bez zmiany pozostałych).

## Uwaga / Anty-wzorzec
Delegowanie zadania bez uprzedniego spisania briefu — decyzje o wyborze wykonawcy/modelu podejmowane na podstawie niejawnego, ulotnego kontekstu rozmowy. Skutki: brak reprodukowalności routingu, niekontrolowany wzrost kosztów (brak sprzężenia z danymi o kwotach), oraz brak możliwości ustalenia, czy błąd wynikał z briefu, reguł, czy limitów.

## Oryginalny cytat
> *"@ArtifexPraxis when firstmate is about to dispatch a crewmate to do a task, it first has to write a task brief anyway

that task brief + the user's dispatch rules + the user's quota data = input context to Jev here"*
