---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Mon Sep 21 04:57:11 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2101898514523730033"
kategoria: "Architektura systemów agentowych / Routing zadań"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Jev jako dedykowany router w orkiestratorze typu chief-of-staff

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Mon Sep 21 04:57:11 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101898514523730033)
- **Konwersacja:** Odpowiedź w dyskusji (@CompleteSkeptic)
- **Kluczowe pojęcia:** [[Kaskady Modeli i Routing Pewności|Routing zadań do subagentów]] [[Harness|Orkiestrator chief-of-staff]] [[Harness|Dedykowany router zamiast decyzji LLM]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Koszt tokenów i latencja]] [[Firstmate i Agenci Wykonawczy]]

---

## Kontekst i problem
W architekturze orkiestratora w stylu 'chief-of-staff' zakłada się, że każde istotne zadanie musi zostać wykonane przez subagenta. Pojawia się więc problem decyzyjny: który subagent ma obsłużyć dane zadanie? Domyślne rozwiązanie — powierzenie routingu orkiestrującemu LLM-owi, który musi przeczytać dużo danych kontekstowych i autoregresyjnie wygenerować decyzję — jest kosztowne pod względem tokenów i latencji. Autor wskazuje, że użył narzędzia 'Jev' jako wyspecjalizowanego routera i sprawdziło się ono w tej roli znacznie lepiej.

## Rada inżynierska
Wydziel routing zadań z orkiestratora LLM do dedykowanego, lekkiego komponentu-routera (np. Jev). Zamiast pozwalać orkiestrującemu LLM-owi czytać duży kontekst i autoregresyjnie 'rozpisywać' decyzję o wyborze subagenta, deleguj tę decyzję do wyspecjalizowanego mechanizmu, który podejmuje ją szybciej i taniej. Orkiestrator zachowuje rolę koordynatora, a routing staje się wymiennym, wyspecjalizowanym modułem (drop-in router).

## Uwaga / Anty-wzorzec
Anty-wzorzec: powierzanie orkiestrującemu LLM-owi routingu przez wczytywanie obszernego kontekstu i autoregresyjne generowanie decyzji — marnuje tokeny, zwiększa latencję i wprowadza wariancję, podczas gdy routing to często prostszy problem klasyfikacyjny, który lepiej rozwiązać dedykowanym, tańszym komponentem.

## Oryginalny cytat
> *"i used Jev to solve one of the listed problems around subagents and it works really well

in a chief-of-staff style orchestrator, it’s assumed that any substantial task has to be done by a subagent - in this scenario, Jev becomes a perfect drop-in router that can make the routing decision in a much more efficient way than letting the orchestrator LLM do it by reading a bunch of data and autoregressive its decision"*
