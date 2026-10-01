---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Sat Sep 12 16:44:00 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2098814897354137710"
kategoria: "Dobór modeli i koszt/efektywność w zadaniach agentowych"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Dobór modelu do debugowania: Grok 4.5 vs Opus 4.8 w diagnozie awarii GitHub Actions

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Sat Sep 12 16:44:00 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2098814897354137710)
- **Kluczowe pojęcia:** [[Harness|Dobór modelu]] [[Harness|Debugowanie agentowe]] [[Harness|GitHub Actions]] [[Harness|Analiza przyczyny źródłowej]] [[Harness|Koszt tokenów]] [[Harness|Współdzielone runnery CI]] [[Firstmate i Agenci Wykonawczy]]

---

## Kontekst i problem
Autor doświadczył nagłego zatrzymania workflow GitHub Actions w swoich repozytoriach OSS. Powierzył diagnozę dwóm różnym modelom, aby porównać skuteczność rozwiązywania problemów infrastrukturalnych, koszt tokenów i czas do znalezienia przyczyny źródłowej.

## Rada inżynierska
W zadaniach diagnostycznych wymagających inspekcji stanu infrastruktury (np. obciążenie runnerów, limity konta, kolejki CI) preferuj modele, które aktywnie eksplorują rzeczywisty stan systemu zamiast generować hipotezy na podstawie powierzchownych przesłanek. Porównuj nie tylko jakość odpowiedzi, ale metrykę kosztu tokenów i czasu do trafnej diagnozy: w tym przypadku Grok 4.5 znalazł przyczynę źródłową (zalew runów CI w repo firstmate wysycający współdzieloną pulę dozwolonych runnerów na koncie) w ~3 min za ~$1.2, podczas gdy Opus 4.8 po ~$10 tokenów utknął na błędnych hipotezach. Nie przywiązuj się do jednego domyślnego modelu — dobieraj go do klasy zadania i weryfikuj empirycznie na własnym workloadzie.

## Uwaga / Anty-wzorzec
Anty-wzorzec: model zamiast zbadać stan systemu formułuje fałszywe, pewne siebie hipotezy („nie zapłaciłeś rachunku” albo „awaria GitHuba”) i forsuje je mimo braku dowodów — marnuje budżet tokenowy i czas, nie rozwiązując problemu. Pułapka inżynierska: bezkrytyczne zaufanie do domyślnego, „najlepszego” modelu bez walidacji jego skuteczności w konkretnej klasie zadań diagnostycznych.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Teza stoi w sprzeczności z powszechnym konsensusem branżowym, w którym modele Claude (Opus) uchodzą za domyślny wybór do zadań koderskich i agentowych. Autor twierdzi na podstawie własnych doświadczeń, że Grok 4.5 jest skuteczniejszy i tańszy w diagnostyce infrastruktury, i domyślnie go wybiera. Jest to jednak dowód anegdotyczny (N=1) — do rozstrzygnięcia pozostaje, czy przewaga wynika z rzeczywistej różnicy w strategii eksploracji narzędzi (tool-use / inspekcja stanu systemu) między modelami, czy z wariancji pojedynczego uruchomienia. Warto zweryfikować na większej próbie zadań diagnostycznych.

## Oryginalny cytat
> *"github actions in my oss repos suddenly stopped running today

i had opus 4.8 look into it, it spent ~$10 worth of tokens and insisted that either i haven't paid my bills or there's a github outage

switched to grok 4.5 and just 3 minutes in with $1.2 worth of tokens, it found there's a surge of CI runs in my firstmate repos starving all the allowed runners across my account, cancelled a bunch of them, and everything's back on track

this is just an anecdotal example but i've had many positive experiences like this. people ask me why i default to grok and this is why"*
