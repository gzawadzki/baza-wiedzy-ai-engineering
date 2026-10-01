---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Fri Sep 18 05:15:45 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100816020932096060"
kategoria: "Inżynieria kontekstu / Prompt Caching / Ekonomia tokenów"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Kompakcja kontekstu a cache promptu: nie modyfikuj historii przed kompakcją

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Fri Sep 18 05:15:45 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100816020932096060)
- **Konwersacja:** Odpowiedź w dyskusji (@DeccansoftAI)
- **Kluczowe pojęcia:** [[Prompt Architecture|Prompt Caching]] [[Context Compaction|Kompakcja kontekstu]] [[Context Compaction|Inżynieria kontekstu]] [[Prompt Architecture|Cache Miss]] [[Harness|Ekonomia tokenów]] [[Harness|Zarządzanie historią sesji]]

---

## Kontekst i problem
Dyskusja dotyczy strategii kompakcji długich sesji agentowych (compaction) w celu redukcji rozmiaru kontekstu. Pytanie sprowadza się do tego, czy opłaca się najpierw usunąć część wiadomości z historii, a dopiero potem zlecić modelowi kompakcję. Autor wyjaśnia, że kolejność operacji ma kluczowy wpływ na trafienia w cache promptu i tym samym na realny koszt wywołania.

## Rada inżynierska
Kompakcję należy uruchamiać na pełnej, niezmodyfikowanej sesji, ponieważ wtedy cały prompt trafia w cache i jest rozliczany po bardzo niskiej cenie. Prefiks kontekstu, który nie został zmieniony, pozostaje cacheowalny — kluczowe jest, aby żadna operacja nie unieważniła prefiksu przed wysłaniem żądania kompakcji. Każda zmiana historii (usunięcie wiadomości) przed kompakcją powoduje cache miss i naliczenie pełnej stawki, która jest 10x–40x droższa.

## Uwaga / Anty-wzorzec
Anty-wzorzec: ręczne przycinanie/usuwanie wiadomości z historii przed wywołaniem kompakcji w przekonaniu, że zmniejszy to koszt. Efekt jest odwrotny — unieważnienie cache powoduje rozliczenie całego promptu po pełnej cenie (10x–40x drożej), co niweczy oszczędności z redukcji rozmiaru kontekstu.

## Oryginalny cytat
> *"no, because when the LLM compacts the whole session, it's a fully cached prompt whose price is very low

but if you remove some of the messages from the history and then run a compaction request, it's a cache miss and will be charged at FULL price 10x-40x more expensive"*
