---
typ: wpis-źródłowy
autor: "@HamelHusain"
data: "Fri Sep 18 17:11:20 +0000 2026"
źródło: "https://x.com/HamelHusain/status/2100996105127534723"
kategoria: "Architektura systemów agentowych / Ewaluacja"
tagi:
  - hamelhusain
  - ai-engineering
  - wpis-atomowy
---

# Agentów używaj, ale weryfikuj na danych

- **Autor:** [[HamelHusain — Indeks|@HamelHusain]] | **Data:** `Fri Sep 18 17:11:20 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2100996105127534723)
- **Konwersacja:** Odpowiedź w dyskusji (@skull8888888888)
- **Kluczowe pojęcia:** [[Harness|Systemy agentowe]] [[Harness|Ewaluacja agentów]] [[Harness|Data-driven development]] [[Harness|Observability LLM]]

---

## Kontekst i problem
Krótka odpowiedź pod wpisem innego użytkownika (@skull8888888888) w dyskusji o systemach agentowych. Autor zgadza się z kierunkiem 'używaj agentów', ale dokłada warunek: równolegle trzeba patrzeć na dane. Kontekst sugeruje spór między entuzjazmem dla agentów a potrzebą mierzalnej, danych opartej weryfikacji ich działania.

## Rada inżynierska
Wdrażając agentów, nie poprzestawaj na obserwacji ich zachowania 'na oko' — równolegle analizuj dane (logi, trajektorie, metryki sukcesu/porażki, rozkłady błędów). Decyzje o architekturze harnessu i promptów powinny być podejmowane na podstawie danych z realnych przebiegów, a nie wyłącznie na podstawie wrażeń z demo.

## Uwaga / Anty-wzorzec
Pułapka: budowanie systemów agentowych w oparciu o anegdotyczne sukcesy pojedynczych przebiegów, bez systematycznego zbierania i analizy danych o rozkładzie zachowań modelu (drift, saturation, typowe tryby awarii).

## Oryginalny cytat
> *"Yes, use agents but also we need to look at the data"*
