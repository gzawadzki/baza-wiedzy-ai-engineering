---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Wed Sep 16 02:41:33 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100052440343294172"
kategoria: "Architektura systemów agentowych / Inżynieria kosztów i opóźnień"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Selektywne stosowanie LLM: routing modeli, eskalacja i triage zamiast LLM-do-wszystkiego

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Wed Sep 16 02:41:33 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100052440343294172)
- **Konwersacja:** Odpowiedź w dyskusji (@EthanSDE)
- **Kluczowe pojęcia:** [[Kaskady Modeli i Routing Pewności|Model routing]] [[Harness|Eskalacja modeli]] [[Code Review|Triage code review]] [[Harness|LLM-do-wszystkiego (anty-wzorzec)]] [[Harness|Zużycie tokenów]] [[Harness|Latencja]] [[Harness|Harness agentowy]]

---

## Kontekst i problem
Autor odpowiada na pytanie, czy istnieją przypadki, w których użycie deterministycznych lub klasycznych mechanizmów (heurystyk, klasyfikatorów, reguł) jest lepsze niż wywołanie LLM. Wskazuje konkretne obszary systemów agentowych — routing modeli, decyzja o eskalacji do mocniejszego modelu oraz triage wyników code review — gdzie naiwne 'LLM do wszystkiego' prowadzi do przepalania tokenów i wysokich opóźnień.

## Rada inżynierska
Traktuj LLM jako jeden z wielu komponentów, a nie domyślny mechanizm dla każdej decyzji. Wzorce wymagające taniej, szybkiej i deterministycznej klasyfikacji — routing żądań do odpowiedniego modelu (np. tani vs. mocny), ocena czy sprawa wymaga eskalacji, wstępny triage/priorytetyzacja znalezisk z code review — implementuj za pomocą reguł, heurystyk, klasyfikatorów ML lub mniejszych, wyspecjalizowanych modeli. Rezerwuj drogie wywołania LLM dla przypadków rzeczywiście wymagających rozumowania. To redukuje zużycie tokenów, koszt i latency całego harnessu.

## Uwaga / Anty-wzorzec
Anty-wzorzec: 'LLM for everything' — wstawianie wywołania dużego modelu w każdy punkt decyzyjny pipeline'u (routing, eskalacja, triage). Skutki: przepalanie tokenów, wysoka latencja, nieprzewidywalność i niepotrzebne koszty, mimo że decyzja jest często prosta i deterministyczna.

## Oryginalny cytat
> *"@EthanSDE yes! many many examples - model routing, escalation judgment, triaging code review findings etc etc

right now it’s LLM for everything which burns tokens and is super slow"*
