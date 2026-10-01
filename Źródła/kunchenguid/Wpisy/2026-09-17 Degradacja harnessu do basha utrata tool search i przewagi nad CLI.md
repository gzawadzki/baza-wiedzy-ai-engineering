---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Thu Sep 17 06:01:23 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100465119897809142"
kategoria: "Architektura harnessu / systemy agentowe"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Degradacja harnessu do basha: utrata tool search i przewagi nad CLI

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Thu Sep 17 06:01:23 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100465119897809142)
- **Konwersacja:** Odpowiedź w dyskusji (@tanishqk)
- **Kluczowe pojęcia:** [[Harness|Tool search]] [[Harness|Architektura harnessu]] [[Harness|Narzędzia agentowe]] [[Harness|Discoverability narzędzi]] [[Harness|Bash vs ustrukturyzowane narzędzia]] [[Context Compaction|Inżynieria kontekstu]]

---

## Kontekst i problem
Wątek dotyczy wyboru między ustrukturyzowaną warstwą narzędzi (tool calling z rejestrem i wyszukiwaniem narzędzi) a bezpośrednim wykonywaniem komend przez bash. Autor odpowiada, że zejście na poziom basha sprawia, iż cały mechanizm tool search przestaje działać, a system staje się jedynie gorszą wersją CLI — czyli traci dokładnie tę wartość dodaną, po którą zbudowano harness.

## Rada inżynierska
Warstwa narzędzi w harnessie musi być jedyną realną ścieżką wykonania — jeśli agent może obejść ją przez bash, to nią pójdzie. Utrzymuj ustrukturyzowane narzędzia + tool search jako kanał domyślny: dają one wykrywalność możliwości (discoverability), walidację argumentów, spójne kontrakty błędów, uprawnienia i telemetrię, których goły shell nie zapewnia. Projektuj narzędzia tak, by były nadzbiorem możliwości basha, nie jego konkurencją.

## Uwaga / Anty-wzorzec
Anty-wzorzec: 'wystarczy dać modelowi bash i niech sobie radzi'. Efekt to strictly worse version of a CLI — brak tool search, brak odkrywania nowych narzędzi przez agenta, brak kontroli uprawnień i jednolitych błędów, trudna telemetria i nieprzewidywalność wykonania. Osobno: dopuszczanie równoległych ścieżek (bash obok narzędzi) bez jasnej polityki, co powoduje dryf agenta w stronę najprostszego, najmniej kontrolowanego kanału.

## Oryginalny cytat
> *"@tanishqk @trq212 yes but that becomes bash again and none of the tool search etc would work, right? that becomes a strictly worse version of a cli"*
