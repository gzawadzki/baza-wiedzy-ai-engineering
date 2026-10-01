---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Thu Sep 17 06:01:23 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100465119897809142"
kategoria: "Architektura harnessów i systemów agentowych"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Tool calling przez bash degraduje harness do gorszej wersji CLI

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Thu Sep 17 06:01:23 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100465119897809142)
- **Konwersacja:** Odpowiedź w dyskusji (@tanishqk)
- **Kluczowe pojęcia:** [[Harness|Tool calling]] [[Harness|Tool search]] [[Harness|Harness agentowy]] [[Harness|Bash]] [[Harness|CLI]] [[Context Compaction|Inżynieria kontekstu]]

---

## Kontekst i problem
Wątek dotyczy sposobu, w jaki agent powinien wywoływać narzędzia: przez natywną warstwę tool-calling z mechanizmem wyszukiwania narzędzi (tool search) czy przez generowanie surowych komend bash. Autor odpowiada, że sprowadzenie wywołań narzędzi do bash usuwa warstwę wyszukiwania/dopasowywania narzędzi i innych funkcji harnessu, przez co całość staje się wyłącznie gorszą wersją CLI — bez korzyści, jakie daje dedykowany protokół narzędziowy.

## Rada inżynierska
Nie implementuj interfejsu narzędzi agenta jako surowych komend bash. Jeśli zejdziesz do powłoki, tracisz mechanizmy tool search, indeksowania i dynamicznego doboru narzędzi, a otrzymany system będzie funkcjonalnie podzbiorem zwykłego CLI. Utrzymuj natywną warstwę tool-calling (schematy, opisy, wyszukiwanie) i traktuj bash jako jedno z narzędzi, nie jako warstwę transportową dla wszystkich pozostałych.

## Uwaga / Anty-wzorzec
Anty-wzorzec „wszystko przez bash”: pozorna prostota i uniwersalność, ale w praktyce utrata walidacji schematów, opisów narzędzi, wyszukiwania oraz możliwości selektywnego ładowania kontekstu narzędzi — czyli degradacja harnessu do „strictly worse version of a cli”.

## Oryginalny cytat
> *"yes but that becomes bash again and none of the tool search etc would work, right? that becomes a strictly worse version of a cli"*
