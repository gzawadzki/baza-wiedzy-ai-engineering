---
typ: wpis-źródłowy
autor: "@simonw"
data: "Sat Aug 15 15:26:51 +0000 2026"
źródło: "https://x.com/simonw/status/2088648622942638557"
kategoria: "Inżynieria kontekstu / Parametry API modeli"
tagi:
  - simonw
  - ai-engineering
  - wpis-atomowy
---

# Domyślny limit kontekstu może odrzucić żądanie do modelu

- **Autor:** [[simonw — Indeks|@simonw]] | **Data:** `Sat Aug 15 15:26:51 +0000 2026` | **Źródło:** [Post na X](https://x.com/simonw/status/2088648622942638557)
- **Konwersacja:** Odpowiedź w dyskusji (@simonw)
- **Kluczowe pojęcia:** [[Context Compaction|Inżynieria kontekstu]] [[Harness|Context length]] [[Harness|Parametry API modeli]] [[Harness|Serwer inferencyjny]] [[Harness|Obsługa błędów API]]

---

## Kontekst i problem
Simon W. opisuje sytuację, w której zapomniał zwiększyć długość kontekstu z wartości domyślnej. Serwer odrzucił żądanie, zanim model zdążył wygenerować odpowiedź. To praktyczna lekcja o tym, że domyślne parametry API/modelu serwerowego bywają zbyt niskie i mogą blokować poprawne użycie modelu.

## Rada inżynierska
Zawsze jawnie ustawiaj wymaganą długość kontekstu przed wywołaniem modelu. Nie zakładaj, że domyślna wartość z API, serwera inferencyjnego lub frameworka odpowiada realnemu limitowi modelu albo potrzebom promptu. Parametr context length traktuj jako część konfiguracji żądania i waliduj go przed wysłaniem.

## Uwaga / Anty-wzorzec
Poleganie na domyślnym context length bez sprawdzenia jego wartości. Nawet jeśli model teoretycznie obsługuje większy kontekst, serwer może odrzucić żądanie, gdy klient nie podniósł jawnie limitu. Prowadzi to do błędów trudnych do zdiagnozowania, zwłaszcza gdy objawem jest odrzucenie przed rozpoczęciem generowania.

## Oryginalny cytat
> *"... disaster! I forgot to bump up the context length from the default and the server rejected it before it could draw its no-doubt beautiful circle https://t.co/CbFd2ZrutP"*
