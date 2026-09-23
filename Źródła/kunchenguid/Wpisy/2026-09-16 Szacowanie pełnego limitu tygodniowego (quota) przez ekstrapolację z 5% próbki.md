---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Wed Sep 16 20:38:57 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100323574791962644"
kategoria: "Benchmarking i zarządzanie limitami API"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Szacowanie pełnego limitu tygodniowego (quota) przez ekstrapolację z 5% próbki

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Wed Sep 16 20:38:57 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100323574791962644)
- **Konwersacja:** Odpowiedź w dyskusji (@EthanClinick)
- **Kluczowe pojęcia:** [[Harness|Benchmarking]] [[Harness|Limity API (quota)]] [[Harness|Ekstrapolacja z próbki]] [[Test-Time Compute i Reasoning Tokens|Token Throughput]] [[Harness|Harness ewaluacyjny]] [[Harness|Inżynieria kosztów LLM]]

---

## Kontekst i problem
Dyskusja dotyczy pomiaru rzeczywistego zużycia tygodniowego limitu API (quota) przez harness/agent. Problem: jak oszacować, ile wyniósłby pełny przebieg ewaluacji, nie paląc całego limitu i nie wydłużając cyklu testowego.

## Rada inżynierska
Aby oszacować pełne zużycie limitu tygodniowego, uruchom eval na reprezentatywnej próbce ok. 5% i ekstrapoluj wartości tokenów z tej próbki liniowo na 100%. Próbkowanie daje wystarczającą dokładność oszacowania przy minimalnym koszcie — pełny przebieg nie jest potrzebny.

## Uwaga / Anty-wzorzec
Marnotrawstwo limitu i czasu przez wykonywanie pełnego przebiegu (100% obciążenia) tylko po to, by poznać jego koszt; dodatkowo pełny przebieg może zostać zniekształcony przez caching, rate limiting lub dryf modelu w trakcie długiego testu.

## Oryginalny cytat
> *"the eval runs through 5 whole % of my weekly quota and count the token value from those runs to calculate what 100% would be. it doesn't need to actually run through 100% of it :)"*
