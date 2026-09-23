---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Mon Sep 21 03:14:19 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2101872626968969713"
kategoria: "Inżynieria kontekstu / Zarządzanie kosztami i cache"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Koszt niezacache'owanego promptu przy 500k kontekstu — kiedy uruchamiać /compact

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Mon Sep 21 03:14:19 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101872626968969713)
- **Kluczowe pojęcia:** [[Prompt Architecture|Prompt Caching]] [[Prompt Architecture|TTL cache promptu]] [[Context Compaction|Kompresja kontekstu /compact]] [[Context Compaction|Zarządzanie oknem kontekstu]] [[Harness|Koszty tokenów]] [[Harness|Długotrwałe sesje agentowe]] [[Harness|Transkrypt sesji jako pamięć zewnętrzna]] [[Persistencja stanu agenta]]

---

## Kontekst i problem
Długie sesje agentowe (Claude, Codex) utrzymują ogromny kontekst, który normalnie jest pokryty przez cache promptu. Cache ma jednak ograniczony czas życia (domyślnie 1 h dla Claude, 30 min dla Codex). Po powrocie do sesji, która przez dłuższy czas była bezczynna, cache wygasa i każdy kolejny request wysyła cały kontekst jako niezacache'owany — przy oknie 500k tokenów to koszt rzędu kilku dolarów za pojedyncze wywołanie, niezależnie od tego, czy mamy subskrypcję z limitem, czy płacimy per token.

## Rada inżynierska
Kompresję kontekstu (/compact) wykonuj ZAWSZE przed odejściem od sesji, a nie po powrocie do niej. Jeśli wracasz do długiej, bezczynnej sesji i widzisz duże okno kontekstu — załóż nową sesję i poproś agenta o sięgnięcie do transkryptu poprzedniej sesji tylko wtedy, gdy faktycznie potrzebuje kontekstu. Traktuj cache jako zasób z TTL, a nie jako trwały stan sesji.

## Uwaga / Anty-wzorzec
Uruchomienie /compact po powrocie do wygasłej sesji w przekonaniu, że obniży to koszt — samo wywołanie kompakcji jest pełnym, niezacache'owanym requestem i kosztuje tyle samo (ok. 5 USD przy 500k kontekstu). Antywzorzec: zostawianie długiej sesji otwartej na dłużej niż TTL cache i liczenie na to, że „subskrypcja to pokryje”.

## Oryginalny cytat
> *"a quick tip that may surprise some folks

an uncached prompt to fable at 500k context window will directly cost you over $5 for A SINGLE REQUEST. that's a cup of coffee or a cheese burger gone. even with subscription quota, this hits like a truck

the most common way to fall into that case is when you walk away from a long session and come back after a while when cache expired (claude is 1 hr, codex is 30 mins by default)

in particular, when you come back to a long idle session, don't run "/compact" there thinking it'll reduce your cost, because the compaction request is still a real request and it will cost $5 by itself right there

the best thing to do is to /compact BEFORE you walk away

the next best thing is when you come back and see a large context window, just start a new session, and ask your agent to look for the last session's transcript if it needs context"*
