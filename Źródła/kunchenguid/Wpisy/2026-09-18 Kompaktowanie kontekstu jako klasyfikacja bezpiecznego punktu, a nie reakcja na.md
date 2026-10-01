---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Fri Sep 18 19:53:16 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2101036854925779291"
kategoria: "Inżynieria kontekstu / zarządzanie pamięcią agenta"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Kompaktowanie kontekstu jako klasyfikacja bezpiecznego punktu, a nie reakcja na próg

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Fri Sep 18 19:53:16 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101036854925779291)
- **Konwersacja:** Odpowiedź w dyskusji (@gehariharan)
- **Kluczowe pojęcia:** [[Context Compaction|Compaction kontekstu]] [[Context Compaction|Zarządzanie oknem kontekstowym]] [[Harness|Harness agentowy]] [[Harness|Safe point / punkty bezpiecznego kompaktowania]] [[Harness|Antywzorce agentowe]] [[Context Compaction|Inżynieria kontekstu]] [[Bezpieczny punkt kompaktowania]]

---

## Kontekst i problem
Dyskusja dotyczy strategii compactingu (kompresji) okna kontekstowego w harnessach agentowych. Domyślny, powszechnie stosowany mechanizm wyzwala kompaktowanie natychmiast po przekroczeniu progu tokenów (np. 80% okna). Autor odpowiada na wątek @gehariharan, ostrzegając, że takie 'instant compaction' jest błędem projektowym. Problem: kompaktowanie w losowym momencie przerywa niedokończone łańcuchy rozumowania i operacje (tool calls), gubi stan i degraduje jakość dalszego działania agenta.

## Rada inżynierska
Nie kompaktuj kontekstu natychmiast po przekroczeniu progu. Potraktuj kompaktowanie jako zadanie KLASYFIKACYJNE: wykryj, czy agent znajduje się w bezpiecznym punkcie (ukończony tool call, domknięty podcel, brak otwartej transakcji/edycji), i dopiero wtedy wykonaj kompresję. Wyzwalaczem powinien być stan semantyczny (safe point), a nie sam licznik tokenów.

## Uwaga / Anty-wzorzec
Antywzorzec 'instant compaction' — reaktywne, natychmiastowe kompaktowanie w momencie przekroczenia limitu tokenów. Przerywa ciągłość rozumowania, rozcina niedokończone wywołania narzędzi i prowadzi do utraty spójności kontekstu oraz halucynacji przy wznowieniu.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Teza stoi w sprzeczności z powszechnym konsensusem branżowym, w którym auto-compaction jest wyzwalane progowo (np. procent zajętości okna kontekstowego) i traktowane jako mechanizm deterministyczny. Autor twierdzi, że jest to zły pomysł i że kompaktowanie wymaga decyzji klasyfikacyjnej o bezpieczeństwie punktu — co do rozstrzygnięcia: czy prosty próg tokenów wystarcza, czy konieczny jest detektor stanu agenta.

## Oryginalny cytat
> *"@gehariharan don't do the "instant compaction" thing. i commented on the post - it's a bad idea

this is just plain and simple classifying whether you are sitting at a place where it's safe to compact"*
