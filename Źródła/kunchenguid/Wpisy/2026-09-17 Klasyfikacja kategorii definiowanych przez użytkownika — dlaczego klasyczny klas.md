---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Thu Sep 17 15:35:36 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100609623531421915"
kategoria: "Architektura systemów agentowych / Klasyfikacja z LLM"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Klasyfikacja kategorii definiowanych przez użytkownika — dlaczego klasyczny klasyfikator nie działa

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Thu Sep 17 15:35:36 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100609623531421915)
- **Konwersacja:** Odpowiedź w dyskusji (@winterspeak)
- **Kluczowe pojęcia:** [[Harness|In-context classification]] [[Harness|LLM jako klasyfikator]] [[Prompt Architecture|Few-shot prompting]] [[Harness|Dynamiczne przestrzenie etykiet]] [[Harness|User-defined taxonomy]] [[Kaskady Modeli i Routing Pewności|Embedding-based routing]] [[Prompt Architecture|Prompt engineering]]

---

## Kontekst i problem
Autor odpowiada na sugestię, że problem klasyfikacji można rozwiązać klasycznym klasyfikatorem (tradycyjnym modelem ML). Kontekst: system, w którym użytkownicy sami definiują kategorie (user-defined, freeform), a system musi przypisywać do nich treści. Problem dotyczy zastosowań takich jak tagowanie, etykietowanie, organizacja notatek, routing czy filtrowanie treści.

## Rada inżynierska
Gdy kategorie są definiowane przez użytkownika w sposób dowolny (freeform), klasyczne klasyfikatory ML są nieadekwatne z dwóch powodów: (1) nie da się wytrenować jednego modelu, który pokryje nieskończoną, zależną od użytkownika przestrzeń etykiet; (2) nie można wymagać, by każdy użytkownik trenował własny klasyfikator. W takich przypadkach właściwym podejściem jest użycie LLM z definicjami kategorii wstrzykiwanymi do kontekstu (prompt engineering / in-context classification), few-shot examples generowanymi per-user, lub embeddingów + semantycznego dopasowania do opisu kategorii. Dobór metody powinien zaczynać się od charakteru przestrzeni etykiet: zamknięta i stała → klasyczny klasyfikator; otwarta i per-user → LLM/in-context.

## Uwaga / Anty-wzorzec
Anty-wzorzec: próba rozwiązania problemu o dynamicznej, otwartej przestrzeni etykiet (user-defined) poprzez trenowanie klasycznego klasyfikatora. Prowadzi to do nieprzenośnych modeli per-użytkownik, ogromnego narzutu na trening/utrzymanie oraz braku generalizacji na nowe kategorie dodane po fakcie — model trzeba by retrenować przy każdym dodaniu kategorii.

## Oryginalny cytat
> *"@winterspeak not exactly - if you think about the use case i have here, the categories are user-defined and completely freeform

there’s no way i can train a traditional classifier that will work for every user, and there’s no way every user will train their own classifier"*
