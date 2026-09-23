---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Tue Sep 22 03:32:12 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2102239513980608520"
kategoria: "Architektura harnessów / systemy agentowe"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Konfiguracja polityki rygoru per repozytorium w harnessie agentowym (firstmate)

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Tue Sep 22 03:32:12 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102239513980608520)
- **Konwersacja:** Odpowiedź w dyskusji (@kunchenguid)
- **Kluczowe pojęcia:** [[Harness|Harness agentowy]] [[Harness|Polityka rygoru per repozytorium]] [[Weryfikator|Zewnętrzny weryfikator]] [[Harness|Bramki jakości w CI agenta]] [[Prompt Architecture|Konfiguracja a prompt]] [[Firstmate i Agenci Wykonawczy]] [[Selektywna weryfikacja kodu]]

---

## Kontekst i problem
Odpowiedź w wątku o narzędziu agentowym 'firstmate'. Autor wskazuje, że harness pozwala zadeklarować, które repozytoria wymagają trybu 'no-mistakes' (rygor, brak tolerancji błędów), a które nie — i że narzędzie samo wyprowadza z tego reguły operacyjne dla agenta.

## Rada inżynierska
Traktuj politykę rygoru jako konfigurację per repozytorium, a nie globalną. Repozytoria krytyczne (produkcja, kod finansowy, infrastruktura) ustaw w trybie 'no-mistakes' — wymuszającym dodatkową weryfikację, wolniejsze i ostrożniejsze kroki oraz twardsze bramki jakości. Repozytoria eksperymentalne/prototypowe zostaw w trybie swobodnym, by nie płacić narzutem weryfikacji za każdą zmianę. Docelowo pozwól harnessowi wygenerować reguły automatycznie na podstawie tej deklaracji, zamiast ręcznie pisać polityki w promptach — deklaracja intencji powinna być oddzielona od jej mechanicznej egzekucji.

## Uwaga / Anty-wzorzec
Anty-wzorzec: jedna globalna polityka rygoru dla wszystkich repozytoriów — albo paraliżuje pracę w repo prototypowych (nadmiar weryfikacji, wysoka latencja, koszt tokenów), albo przepuszcza błędy w repo krytycznych. Drugi anty-wzorzec: ręczne wklejanie reguł rygoru do promptu systemowego zamiast zadeklarowania ich w konfiguracji harnessu — reguły rozjeżdżają się między sesjami i są niespójne.

## Oryginalny cytat
> *"@EthanClinick in firstmate, you can also tell firstmate which repos need no-mistakes vs not. it can setup the rules for you"*
