---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Tue Sep 22 03:30:29 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2102239083678650816"
kategoria: "Architektura harnessów i narzędzi agentowych"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Rozdzielenie harnessu agentowego według dostawcy modelu (pi dla modeli nie-Anthropic)

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Tue Sep 22 03:30:29 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102239083678650816)
- **Konwersacja:** Odpowiedź w dyskusji (@tanishqk)
- **Kluczowe pojęcia:** [[Harness|Harness agentowy]] [[Harness|Model-agnostic harness]] [[Harness|Tool calling]] [[Prompt Architecture|Prompt cache]] [[Kaskady Modeli i Routing Pewności|Routing modeli]] [[Harness|Benchmarking modeli]]

---

## Kontekst i problem
Odpowiedź w wątku o wyborze narzędzia/harnessu do pracy z modelami LLM. Autor deklaruje praktykę rozdzielenia środowiska uruchomieniowego agenta zależnie od dostawcy modelu: dla modeli Anthropic (np. Claude) używa natywnego narzędzia, a dla wszystkich pozostałych modeli — alternatywnego, model-agnostycznego harnessu („pi”). Problem, który to rozwiązuje: natywne harnessy są zwykle optymalizowane pod format tool-calling, tokenizer i zachowania jednego dostawcy, więc uruchamianie w nich modeli trzecich (OpenAI, Google, modele open-weight) prowadzi do degradacji jakości wywołań narzędzi i nieefektywnego zużycia kontekstu.

## Rada inżynierska
Traktuj harness agentowy jako warstwę zależną od dostawcy modelu, nie jako uniwersalny interfejs. Utrzymuj co najmniej dwie ścieżki uruchomieniowe: (1) natywny harness dostawcy dla modeli, pod które jest strojony (najlepsza zgodność formatu tool-call, prompt-cache i obsługi błędów), (2) lekki, model-agnostyczny harness dla pozostałych modeli — ułatwia to podmianę modelu bez przepisywania logiki agenta i pozwala porównywać modele w identycznych warunkach (A/B benchmarku). Utrzymuj abstrakcję narzędzi (definicje funkcji, schematy JSON) poza harnessem, aby przełączanie dostawcy było zmianą konfiguracji, a nie refaktorem.

## Uwaga / Anty-wzorzec
Wymuszanie jednego harnessu dla wszystkich modeli: natywne narzędzie dostawcy uruchamiane z modelami trzecimi często generuje błędne lub niepełne wywołania narzędzi, gubi konwencje formatu i marnuje tokeny na warstwę adaptacyjną. Odwrotnie — używanie generycznego harnessu dla modelu natywnie wspieranego odcina dostęp do optymalizacji prompt-cache i specyficznych mechanizmów dostawcy.

## Oryginalny cytat
> *"@tanishqk i use pi for any model that's not anthropic"*
