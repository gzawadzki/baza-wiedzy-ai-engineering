---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Fri Sep 18 05:15:45 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100816020932096060"
kategoria: "Inżynieria kontekstu / Cache i koszty inferencji"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Kompakcja sesji a cache promptów: pełny prefiks vs cache miss

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Fri Sep 18 05:15:45 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100816020932096060)
- **Konwersacja:** Odpowiedź w dyskusji (@DeccansoftAI)
- **Kluczowe pojęcia:** [[Prompt Architecture|Prompt Caching]] [[Context Compaction|Kompakcja kontekstu]] [[Prompt Architecture|Cache Miss]] [[Harness|Zarządzanie historią sesji]] [[Harness|Koszty inferencji]] [[Context Compaction|Append-only kontekst]]

---

## Kontekst i problem
Dyskusja dotyczy tego, czy przed uruchomieniem kompakcji (podsumowania/streszczenia) długiej sesji LLM należy najpierw usunąć część wiadomości z historii. Autor wyjaśnia, że kolejność i sposób modyfikacji historii determinują, czy request trafi w cache promptu, czy zostanie rozliczony po pełnej cenie.

## Rada inżynierska
Kompakcję całej sesji uruchamiaj na pełnej, niezmodyfikowanej historii — taki prompt jest w całości pokryty cache'em, więc koszt inferencji pozostaje bardzo niski. Traktuj historię sesji jako append-only prefiks: każda zmiana (usunięcie/przycięcie wiadomości) przed requestem unieważnia prefiks cache i wymusza ponowne przetworzenie całego kontekstu po pełnej cenie.

## Uwaga / Anty-wzorzec
Anty-wzorzec: ręczne usuwanie części wiadomości z historii tuż przed wysłaniem requestu kompakcji. Powoduje to cache miss i rozliczenie po pełnej stawce — według autora od 10x do 40x drożej niż w przypadku w pełni zacache'owanego promptu. Modyfikacja historii 'w locie' niweczy korzyść ekonomiczną cache'owania.

## Oryginalny cytat
> *"no, because when the LLM compacts the whole session, it's a fully cached prompt whose price is very low

but if you remove some of the messages from the history and then run a compaction request, it's a cache miss and will be charged at FULL price 10x-40x more expensive"*
