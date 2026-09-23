---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Wed Sep 16 05:09:51 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100089760475930830"
kategoria: "Architektura systemów agentowych / Routing modeli i koszty"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Tani model jako orkiestrator z eskalacją do modelu top-tier (fable tier)

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Wed Sep 16 05:09:51 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100089760475930830)
- **Konwersacja:** Odpowiedź w dyskusji (@Steve_Yegge)
- **Kluczowe pojęcia:** [[Kaskady Modeli i Routing Pewności|Tiered model routing]] [[Harness|Model escalation pattern]] [[Harness|Tan i model jako orkiestrator]] [[Harness|Koszty systemów agentowych]] [[Prompt Architecture|Prompt steering]] [[Harness|System agentowy]] [[Firstmate i Agenci Wykonawczy]]

---

## Kontekst i problem
Autor po miesiącach pracy z agentem orkiestrującym („firstmate”) zauważa, że kluczowym problemem kosztowym jest przypisywanie zadań czysto orkiestracyjnych — przejść między krokami, typu „zadanie 1 skończone, uruchom zadanie 2” — do najdroższych, frontierowych modeli. Takie zadania nie wymagają „mądrości” najwyższej klasy, a drastycznie podnoszą koszt całego systemu. Rozwiązaniem jest rozdzielenie ról: tani model wykonuje rutynę orkiestracyjną, a decyzje niejednoznaczne są eskalowane do modelu top-tier.

## Rada inżynierska
Stosuj hierarchiczny routing modeli (tiered routing): powierz orkiestrację i deterministyczne przejścia między zadaniami tanimu modelowi, a model frontierowy (fable tier) wywołuj wyłącznie punktowo — gdy pojawia się niejednoznaczność lub decyzja wymagająca głębokiego rozumowania. Kluczowe jest agresywne sterowanie (heavy steering) promptem/regułami taniego orkiestratora, aby sam rozpoznawał granice swojej kompetencji i jawnie eskalował wątpliwe przypadki w górę. Takie rozdzielenie ról znacząco obniża koszt przy zachowaniu jakości całego systemu.

## Uwaga / Anty-wzorzec
Anty-wzorzec: używanie modelu top-tier do zadań orkiestracyjnych typu „krok N zakończony → rozpocznij krok N+1”. To marnotrawstwo budżetu na zadania nie wymagające wysokiej klasy rozumowania i główna przyczyna nieakceptowalnie wysokich kosztów systemu agentowego.

## Oryginalny cytat
> *"having been working with my firstmate for months, i learned one of the biggest traps is that we may put fable tier models on many mundane orchestration-ish tasks (like “oh task 1 finished let me kick off task 2”) that really don’t need fable level wisdom. that’s what makes the cost untenable

i’m having great success with using a cheap model for orchestration and heavily steer it to escalate ambiguous decisions to fable, which makes a surprisingly big difference without compromising the overall quality of the system"*
