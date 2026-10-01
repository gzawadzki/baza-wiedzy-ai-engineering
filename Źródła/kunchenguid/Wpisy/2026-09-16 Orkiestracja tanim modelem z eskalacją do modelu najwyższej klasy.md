---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Wed Sep 16 05:09:51 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100089760475930830"
kategoria: "Architektura systemów agentowych / Optymalizacja kosztów"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Orkiestracja tanim modelem z eskalacją do modelu najwyższej klasy

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Wed Sep 16 05:09:51 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100089760475930830)
- **Konwersacja:** Odpowiedź w dyskusji (@Steve_Yegge)
- **Kluczowe pojęcia:** [[Harness|Orkiestracja agentów]] [[Harness|Model tiering]] [[Harness|Eskalacja decyzji]] [[Harness|Optymalizacja kosztów LLM]] [[Kaskady Modeli i Routing Pewności|Routing modeli]] [[Harness|Multi-agent systemy]] [[Firstmate i Agenci Wykonawczy]]

---

## Kontekst i problem
Autor opisuje doświadczenie z wielomiesięcznym prowadzeniem agenta orkiestrującego ('firstmate'). Problem: powszechna praktyka przypisywania modeli najwyższej klasy (fable tier) do rutynowych zadań orkiestracyjnych — np. prostego przełączania między zadaniami ('zadanie 1 skończone, uruchamiam zadanie 2') — drastycznie zawyża koszty bez zysku jakościowego, ponieważ tego typu decyzje nie wymagają zaawansowanego rozumowania.

## Rada inżynierska
Rozdziel warstwy modeli według złożoności decyzji: użyj taniego modelu jako orkiestratora (routing, sekwencjonowanie zadań, proste przejścia stanów) i zaprojektuj w nim wyraźne reguły eskalacji — wszystkie decyzje niejednoznaczne, wymagające osądu lub kontekstu przekazuj do modelu klasy najwyższej (fable tier). Taki podział znacząco obniża koszt operacyjny przy zachowaniu jakości całego systemu.

## Uwaga / Anty-wzorzec
Anty-wzorzec: przypisywanie modeli najwyższej klasy do zadań czysto orkiestracyjnych i mechanicznych (np. 'task 1 finished, kick off task 2'). To prowadzi do nieakceptowalnych kosztów bez poprawy jakości — marnuje 'wisdom' drogiego modelu na zadania, które jej nie wymagają.

## Oryginalny cytat
> *"having been working with my firstmate for months, i learned one of the biggest traps is that we may put fable tier models on many mundane orchestration-ish tasks (like “oh task 1 finished let me kick off task 2”) that really don’t need fable level wisdom. that’s what makes the cost untenable

i’m having great success with using a cheap model for orchestration and heavily steer it to escalate ambiguous decisions to fable, which makes a surprisingly big difference without compromising the overall quality of the system"*
