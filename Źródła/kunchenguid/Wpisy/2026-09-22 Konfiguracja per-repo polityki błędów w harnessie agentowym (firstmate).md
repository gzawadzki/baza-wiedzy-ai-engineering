---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Tue Sep 22 03:32:12 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2102239513980608520"
kategoria: "Architektura harnessów / Systemy agentowe"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Konfiguracja per-repo polityki błędów w harnessie agentowym (firstmate)

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Tue Sep 22 03:32:12 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102239513980608520)
- **Konwersacja:** Odpowiedź w dyskusji (@kunchenguid)
- **Kluczowe pojęcia:** [[Harness|Harness agentowy]] [[Harness|Polityka per-repo]] [[Weryfikacja krokowa|Zewnętrzna weryfikacja]] [[Harness|Tryb no-mistakes]] [[Harness|Konfiguracja agenta]] [[Firstmate i Agenci Wykonawczy]] [[Selektywna weryfikacja kodu]]

---

## Kontekst i problem
W odpowiedzi pod wpisem @EthanClinick autor opisuje mechanizm harnessu firstmate, który pozwala zdefiniować różne poziomy rygoru dla różnych repozytoriów: jedne wymagają trybu 'no-mistakes' (zero tolerancji błędów), inne mogą działać w trybie bardziej swobodnym. Harness potrafi sam wygenerować takie reguły.

## Rada inżynierska
Traktuj politykę jakości jako konfigurację per-repozytorium, a nie globalną stałą harnessu. Repozytoria krytyczne (produkcja, kod finansowy, infrastruktura) ustaw w trybie 'no-mistakes' z rygorystyczną weryfikacją zewnętrzną, a repozytoria eksperymentalne/prototypowe w trybie łagodniejszym, aby nie blokować iteracji. Pozwól agentowi wygenerować wstępne reguły na podstawie charakteru repo, a następnie zweryfikuj je ręcznie.

## Uwaga / Anty-wzorzec
Ustawienie jednego globalnego poziomu rygoru dla wszystkich repozytoriów — zbyt ostry zabija szybkość prototypowania, zbyt łagodny przepuszcza błędy do kodu produkcyjnego. Automatyczne generowanie reguł przez agenta bez późniejszego audytu może utrwalić błędne założenia o krytyczności danego repo.

## Oryginalny cytat
> *"@EthanClinick in firstmate, you can also tell firstmate which repos need no-mistakes vs not. it can setup the rules for you"*
