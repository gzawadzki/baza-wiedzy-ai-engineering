---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Thu Sep 17 06:26:13 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100471365912707312"
kategoria: "Architektura systemów agentowych"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Jev nie zastępuje LLM-ów — wymaga nowego paradygmatu budowy oprogramowania

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Thu Sep 17 06:26:13 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100471365912707312)
- **Konwersacja:** Odpowiedź w dyskusji (@janpfranke)
- **Kluczowe pojęcia:** [[Harness|Systemy agentowe]] [[Harness|LLM jako komponent systemu]] [[Harness]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Paradygmat wytwarzania oprogramowania z LLM]]

---

## Kontekst i problem
Wymiana zdań w wątku @janpfranke na temat narzędzia/ram frameworkowego „Jev”. Autor potwierdza tezę rozmówcy i doprecyzowuje pozycjonowanie: nie jest to zamiennik modeli językowych, lecz odmienna warstwa, która wymusza przemyślenie na nowo procesu wytwarzania oprogramowania. Autor przyznaje zarazem, że sam nie przepracował jeszcze wszystkich implikacji tej zmiany — co sugeruje, że jest to teza robocza, a nie ustalony konsensus.

## Rada inżynierska
Nie pozycjonuj frameworków agentowych (typu harness, orkiestrator, warstwa narzędziowa) jako „lepszego LLM-a”. Traktuj model językowy jako jeden z komponentów, a właściwą wartość nowego podejścia ulokuj w przeprojektowaniu procesu budowy oprogramowania: podziale ról, kontraktach między komponentami, weryfikacji i przepływie kontekstu. Wdrożenie takiej warstwy bez równoległej zmiany sposobu myślenia o architekturze aplikacji nie da oczekiwanego efektu.

## Uwaga / Anty-wzorzec
Anty-wzorzec: wstawienie nowego harnessu/frameworku agentowego do istniejącego pipeline'u „jeden do jednego” w miejsce wywołania LLM, przy zachowaniu dotychczasowego sposobu projektowania systemu. Prowadzi to do oceny narzędzia przez pryzmat jakości pojedynczego completionu, a nie przez pryzmat architektury — i do wniosku, że „nie działa lepiej niż model”.

## Oryginalny cytat
> *"@janpfranke right - Jev is not a replacement for LLMs. it requires a new way of thinking about building software - tbh i'm still yet to think through the implications.."*
