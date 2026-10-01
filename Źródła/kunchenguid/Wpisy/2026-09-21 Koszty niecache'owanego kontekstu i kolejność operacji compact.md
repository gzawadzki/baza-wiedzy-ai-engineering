---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Mon Sep 21 03:14:19 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2101872626968969713"
kategoria: "Inżynieria kontekstu / zarządzanie cache i kosztami"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Koszty niecache'owanego kontekstu i kolejność operacji /compact

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Mon Sep 21 03:14:19 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101872626968969713)
- **Kluczowe pojęcia:** [[Prompt Architecture|Prompt Cache]] [[Prompt Architecture|TTL cache'u promptu]] [[Context Compaction|Kompakcja kontekstu]] [[Context Compaction|Zarządzanie oknem kontekstu]] [[Harness|Koszty tokenów]] [[Harness|Sesje agentowe]] [[Harness|Transkrypt sesji]]

---

## Kontekst i problem
Długie sesje agentowe (np. 500k tokenów kontekstu) przy wygasłym cache'u promptu generują ekstremalnie wysokie koszty pojedynczego żądania. Problem pojawia się, gdy użytkownik odchodzi od sesji i wraca po czasie dłuższym niż TTL cache'u (domyślnie 1 godzina dla Claude, 30 minut dla Codex). Wtedy każda operacja — w tym samo /compact — jest pełnym, niecache'owanym żądaniem i kosztuje tyle, co cały kontekst.

## Rada inżynierska
Zawsze wykonuj /compact PRZED odejściem od długiej sesji — kompakcja z ciepłym cache'em jest tania, a wykonana po powrocie (z wygasłym cache'em) kosztuje pełny, niecache'owany prompt. Jeżeli wracasz do sesji z dużym oknem kontekstu i wygasłym cache'em, drugą najlepszą opcją jest rozpoczęcie nowej sesji i polecenie agentowi odczytania transkryptu poprzedniej sesji tylko w razie potrzeby kontekstu.

## Uwaga / Anty-wzorzec
Uruchamianie /compact po powrocie do bezczynnej, długiej sesji w przekonaniu, że obniży to koszty — w rzeczywistości sam request kompakcji jest pełnym, niecache'owanym żądaniem i kosztuje ok. $5 przy 500k kontekstu. Analogicznie: pozostawienie długiej sesji bez wcześniejszej kompakcji i powrót po upływie TTL cache'u.

## Oryginalny cytat
> *"a quick tip that may surprise some folks

an uncached prompt to fable at 500k context window will directly cost you over $5 for A SINGLE REQUEST. that's a cup of coffee or a cheese burger gone. even with subscription quota, this hits like a truck

the most common way to fall into that case is when you walk away from a long session and come back after a while when cache expired (claude is 1 hr, codex is 30 mins by default)

in particular, when you come back to a long idle session, don't run "/compact" there thinking it'll reduce your cost, because the compaction request is still a real request and it will cost $5 by itself right there

the best thing to do is to /compact BEFORE you walk away

the next best thing is when you come back and see a large context window, just start a new session, and ask your agent to look for the last session's transcript if it needs context"*
