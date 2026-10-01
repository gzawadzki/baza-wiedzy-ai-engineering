---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Mon Sep 21 03:46:52 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2101880818142515556"
kategoria: "Inżynieria kontekstu / pamięć agentów / cache"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Nie wznawiaj długiej sesji po wygaśnięciu cache — użyj transkryptu w nowej sesji

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Mon Sep 21 03:46:52 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101880818142515556)
- **Konwersacja:** Odpowiedź w dyskusji (@Paiky16)
- **Kluczowe pojęcia:** [[Harness|Agent harness]] [[Harness|Transkrypt sesji]] [[Context Compaction|Cache kontekstu]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Zarządzanie pamięcią agenta]] [[Harness|Koszt tokenów]] [[Prompt Architecture|Cache miss]]

---

## Kontekst i problem
Wpis dotyczy zarządzania długimi sesjami agentowymi i kosztów wynikających z cache'owania kontekstu. Autor odpowiada na problem kontynuowania niedokończonej pracy bez ponoszenia wysokich kosztów tokenowych.

## Rada inżynierska
Większość harnessów agentowych domyślnie zapisuje transkrypty sesji i potrafi je odczytać. Zamiast wznawiać starą, długą sesję, rozpocznij nową sesję i poinformuj ją, że w transkrypcie poprzedniej sesji znajduje się niedokończona praca. Nie wznawiaj długiej sesji, której cache wygasł — spowoduje to pełne ponowne przetworzenie kontekstu i ogromny koszt pojedynczego żądania.

## Uwaga / Anty-wzorzec
Wznowienie długiej sesji po wygaśnięciu cache prowadzi do braku trafień w cache i kosztownego reprocessingu całego kontekstu — autor podaje przykład kosztu rzędu 5 USD za jedno żądanie.

## Oryginalny cytat
> *"most agent harnesses save transcripts by default and know how to look them up, so you don’t need to do anything special other than letting the new session know you have some unfinished work in the last session’s transcript

definitely DO NOT resume a long session whose cache expired. that’s what going to cost you $5 for one request"*
