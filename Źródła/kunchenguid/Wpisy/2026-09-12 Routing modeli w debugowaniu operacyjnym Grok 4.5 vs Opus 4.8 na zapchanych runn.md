---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Sat Sep 12 16:44:00 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2098814897354137710"
kategoria: "Benchmarking modeli agentowych / Debugowanie incydentów CI-CD"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Routing modeli w debugowaniu operacyjnym: Grok 4.5 vs Opus 4.8 na zapchanych runnerach GitHub Actions

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Sat Sep 12 16:44:00 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2098814897354137710)
- **Kluczowe pojęcia:** [[Kaskady Modeli i Routing Pewności|Routing modeli]] [[Harness|Benchmarking modeli agentowych]] [[Harness|GitHub Actions]] [[Harness|Limity runnerów]] [[Harness|Debugowanie incydentów CI-CD]] [[Harness|Koszt tokenów a skuteczność]] [[Harness|Pułapka potwierdzenia w agentach]] [[Harness|Anegdotalna ocena modeli]] [[Firstmate i Agenci Wykonawczy]]

---

## Kontekst i problem
W repozytoriach OSS autora nagle przestały działać workflow GitHub Actions. Opus 4.8 po spaleniu ~10 USD tokenów nie znalazł przyczyny i upierał się, że to nieopłacone rachunki albo awaria GitHuba. Grok 4.5 w 3 minuty i za ~1.2 USD tokenów zdiagnozował realną przyczynę: lawina uruchomień CI w repozytoriach 'firstmate' wyczerpała limit dozwolonych runnerów na całym koncie, zagłodziła pozostałe pipeline'y; po anulowaniu części uruchomień wszystko wróciło do normy.

## Rada inżynierska
Przy incydentach infrastrukturalnych (CI/CD, limity konta, kolejkowanie, wyczerpanie zasobów) wybieraj model, który aktywnie eksploruje stan systemu przez narzędzia i wykonuje akcje naprawcze, zamiast wnioskować z wiedzy ogólnej. Optymalizuj metrykę 'koszt i czas do rezultatu', nie 'ogólną inteligencję' modelu — dobieraj model per typ zadania (routing) i domyślnie sięgaj po ten, który ma udokumentowane sukcesy w danej klasie problemów operacyjnych.

## Uwaga / Anty-wzorzec
Przypisywanie awarii do czynników zewnętrznych (brak płatności, outage dostawcy) bez sprawdzenia własnego konta, limitów i współdzielonych zasobów — klasyczna pułapka potwierdzenia po stronie agenta. Drugi anty-wzorzec: bezkrytyczne trzymanie się jednego 'domyślnego' modelu i płacenie ~8x więcej tokenów za gorszy wynik diagnostyczny. Trzeci: brak izolacji limitów między repozytoriami (współdzielona pula runnerów na koncie = jeden głośny projekt zagładza całą resztę).

## ⚡ Kwestia sporna / do rozstrzygnięcia
Teza sprzeczna z dominującym konsensusem, że Opus to najsilniejszy model do złożonych zadań agentowych. Autor twierdzi, że w debugowaniu operacyjnym Grok 4.5 jest ~8x tańszy i ~3x szybszy do rezultatu niż Opus 4.8. Zastrzeżenie: autor sam przyznaje, że to przykład anegdotyczny (n=1), bez powtarzalnego benchmarku — spór do rozstrzygnięcia wymaga systematycznych testów na zbiorze incydentów infrastrukturalnych.

## Oryginalny cytat
> *"github actions in my oss repos suddenly stopped running today

i had opus 4.8 look into it, it spent ~$10 worth of tokens and insisted that either i haven't paid my bills or there's a github outage

switched to grok 4.5 and just 3 minutes in with $1.2 worth of tokens, it found there's a surge of CI runs in my firstmate repos starving all the allowed runners across my account, cancelled a bunch of them, and everything's back on track

this is just an anecdotal example but i've had many positive experiences like this. people ask me why i default to grok and this is why"*
