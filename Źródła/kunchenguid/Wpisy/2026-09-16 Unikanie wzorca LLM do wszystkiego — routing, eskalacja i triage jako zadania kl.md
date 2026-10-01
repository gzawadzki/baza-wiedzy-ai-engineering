---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Wed Sep 16 02:41:33 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100052440343294172"
kategoria: "Architektura systemów agentowych / Optymalizacja kosztów i latencji"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Unikanie wzorca "LLM do wszystkiego" — routing, eskalacja i triage jako zadania klasyfikacyjne

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Wed Sep 16 02:41:33 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100052440343294172)
- **Konwersacja:** Odpowiedź w dyskusji (@EthanSDE)

---

## Kontekst i problem
Dyskusja pod wpisem @EthanSDE o miejscach, w których w systemach agentowych można zastąpić pełny wywołanie LLM tańszymi mechanizmami decyzyjnymi. Autor wskazuje konkretne przypadki: routing między modelami, ocena czy eskalują do mocniejszego modelu, oraz wstępna klasyfikacja/priorytetyzacja wyników code review. Problem: domyślne podejście 'LLM do wszystkiego' drastycznie zużywa tokeny i zwiększa opóźnienia.
