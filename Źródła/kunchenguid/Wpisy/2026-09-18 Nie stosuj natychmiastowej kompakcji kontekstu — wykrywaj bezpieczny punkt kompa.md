---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Fri Sep 18 19:53:16 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2101036854925779291"
kategoria: "Inżynieria kontekstu / zarządzanie pamięcią agenta"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Nie stosuj natychmiastowej kompakcji kontekstu — wykrywaj bezpieczny punkt kompakcji

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Fri Sep 18 19:53:16 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101036854925779291)
- **Konwersacja:** Odpowiedź w dyskusji (@gehariharan)
- **Kluczowe pojęcia:** [[Context Compaction|Kompakcja kontekstu]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Zarządzanie pamięcią agenta]] [[Context Compaction|Okno kontekstowe]] [[Harness|Harness agentowy]] [[Harness|Klasyfikacja stanu agenta]] [[Bezpieczny punkt kompaktowania]]

---

## Kontekst i problem
Dyskusja dotyczy strategii kompakcji (compaction) kontekstu w systemach agentowych LLM — czyli momentu, w którym historia rozmowy/stan agenta jest streszczana lub redukowana, aby zwolnić okno kontekstowe. Popularne podejście „instant compaction” zakłada kompakcję natychmiast po przekroczeniu progu zajętości kontekstu. Autor krytykuje to jako błędne, wskazując, że kompakcja wykonana w złym momencie (np. w połowie łańcucha narzędzi, niedomkniętej operacji, przedwczesnym stanie pośrednim) niszczy spójność stanu agenta.

## Rada inżynierska
Traktuj decyzję o kompakcji jako zadanie KLASYFIKACJI, a nie prosty trigger progowy. Agent powinien najpierw ocenić, czy znajduje się w stanie, w którym kompakcja jest bezpieczna (np. zamknięty krok zadania, brak oczekujących wywołań narzędzi, spójny stan logiczny). Dopiero po potwierdzeniu bezpieczeństwa wykonuj kompakcję. Odraczaj kompakcję, jeśli jesteś w środku sekwencji zależnych operacji.

## Uwaga / Anty-wzorzec
„Instant compaction” — automatyczna, natychmiastowa kompakcja wyzwalana wyłącznie progiem rozmiaru kontekstu, bez sprawdzenia semantycznego stanu agenta. Prowadzi do utraty krytycznego kontekstu pośredniego i przerywania niedokończonych łańcuchów rozumowania/narzędzi.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Sprzeczność z powszechnym w branży wzorcem automatycznej kompakcji opartej na progu zajętości kontekstu (np. „compact gdy >80% okna”). Autor twierdzi, że trigger progowy jest anty-wzorcem, a kompakcja powinna być warunkowana klasyfikacją bezpieczeństwa stanu — do rozstrzygnięcia, czy podejście klasyfikacyjne nie wprowadza zbyt dużego opóźnienia i kosztu dodatkowego wywołania modelu przy każdym kroku.

## Oryginalny cytat
> *"@gehariharan don't do the "instant compaction" thing. i commented on the post - it's a bad idea

this is just plain and simple classifying whether you are sitting at a place where it's safe to compact"*
