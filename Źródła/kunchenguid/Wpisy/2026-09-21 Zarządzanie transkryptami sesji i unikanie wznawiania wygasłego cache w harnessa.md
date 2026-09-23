---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Mon Sep 21 03:46:52 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2101880818142515556"
kategoria: "Architektura agentów / Zarządzanie kontekstem"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Zarządzanie transkryptami sesji i unikanie wznawiania wygasłego cache w harnessach agentowych

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Mon Sep 21 03:46:52 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101880818142515556)
- **Konwersacja:** Odpowiedź w dyskusji (@Paiky16)
- **Kluczowe pojęcia:** [[Harness|Agent Harness]] [[Harness|Transkrypt sesji]] [[Context Compaction|Cache kontekstu]] [[Harness|Zarządzanie sesjami agentowymi]] [[Harness|Koszt inferencji]]

---

## Kontekst i problem
Problem dotyczy kontynuacji pracy agenta między sesjami. Autor wyjaśnia, że nie trzeba podejmować specjalnych kroków, aby kontynuować niedokończoną pracę, ponieważ większość harnessów zapisuje transkrypty i potrafi je odszukać. Wystarczy poinformować nową sesję o niedokończonej pracy z poprzedniej sesji. Jednak ostrzega przed wznawianiem długiej sesji, której cache wygasł, ponieważ może to być bardzo kosztowne.

## Rada inżynierska
W harnessach agentowych domyślnie zapisywane są transkrypty sesji. Aby kontynuować pracę, nie trzeba robić nic specjalnego – wystarczy nowej sesji przekazać informację, że w poprzedniej sesji pozostały niedokończone zadania. Bezwzględnie nie należy wznawiać długiej sesji, której cache wygasł – koszt pojedynczego żądania może wynieść nawet 5 dolarów.

## Uwaga / Anty-wzorzec
Wznawianie długiej sesji po wygaśnięciu cache – prowadzi do ogromnych kosztów (np. 5 USD za jedno żądanie).

## Oryginalny cytat
> *"most agent harnesses save transcripts by default and know how to look them up, so you don’t need to do anything special other than letting the new session know you have some unfinished work in the last session’s transcript

definitely DO NOT resume a long session whose cache expired. that’s what going to cost you $5 for one request"*
