---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Thu Sep 17 07:28:21 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100487003431477661"
kategoria: "Architektura harnessów i routing modeli"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Routing modeli z uwzględnieniem pozostałego limitu kwot (quota runway)

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Thu Sep 17 07:28:21 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100487003431477661)
- **Konwersacja:** Odpowiedź w dyskusji (@taras_korn)
- **Kluczowe pojęcia:** [[Kaskady Modeli i Routing Pewności|Model Routing]] [[Harness|Quota Management]] [[Harness|Rate Limiting]] [[Harness|Agent Harness]] [[Harness|Load Balancing Modeli]] [[Harness|429 Too Many Requests]]

---

## Kontekst i problem
Dyskusja pod wpisem @taras_korn dotyczy mechanizmu wyboru modelu w harnessie/agentowym systemie wielomodelowym. Pytanie nadrzędne dotyczyło prawdopodobnie tego, czy router bierze pod uwagę limity użycia (rate limits / quota) przy wyborze dostawcy lub modelu. Autor odpowiada, że selektor modeli jest już świadomy kwot i wybiera model, który ma największy zapas limitu.

## Rada inżynierska
W warstwie routingu modeli nie wystarczy kierować się jakością, kosztem czy latency — trzeba uwzględnić 'quota runway', czyli oszacowany zapas pozostałego limitu (RPM/TPM/kredyty/dobowe okno) dla każdego kandydata. Reguła: wybierz model z największym dostępnym zapasem kwoty, aby uniknąć przerwania długich sesji agentowych przez 429 / wyczerpanie kredytów w trakcie wykonywania zadania. Utrzymuj licznik zużycia per klucz/model i prognozę wyczerpania okna (burn rate) jako wejście do decyzji routera.

## Uwaga / Anty-wzorzec
Optymalizacja routera wyłącznie po jakości lub koszcie bez stanu kwot — prowadzi do twardych błędów rate-limit w środku łańcucha narzędziowego, nieodwracalnych przerwań i konieczności restartu zadania. Pomijanie prognozy burn rate sprawia, że model 'z największą kwotą nominalnie' może wyczerpać się szybciej niż model z mniejszym, ale stabilniejszym zapasem.

## Oryginalny cytat
> *"it already takes quota into consideration. it will pick the model with the most quota runway available"*
