---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Tue Sep 22 03:31:40 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2102239379536433551"
kategoria: "Architektura harnessów / weryfikacja kodu"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Heurystyka selektywnego stosowania zewnętrznego recenzenta kodu (no-mistakes)

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Tue Sep 22 03:31:40 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102239379536433551)
- **Konwersacja:** Odpowiedź w dyskusji (@EthanClinick)
- **Kluczowe pojęcia:** [[Weryfikator|Zewnętrzny weryfikator]] [[Code Review|Agent code review]] [[Harness|Harness agentowy]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Selekcja zadań dla agenta]] [[Selektywna weryfikacja kodu]]

---

## Kontekst i problem
Autor odpowiada na pytanie @EthanClinick, czy każda zmiana w kodzie powinna przechodzić przez narzędzie/weryfikator typu „no-mistakes” (zewnętrzny recenzent kodu). Wyjaśnia, że nie jest to mechanizm do stosowania bezwarunkowo — potrzebne jest kryterium decyzyjne oparte na analogii do ludzkiego code review.

## Rada inżynierska
Stosuj zewnętrznego weryfikatora / agenta recenzującego selektywnie, a nie do każdej zmiany. Praktyczna reguła decyzyjna: zadaj sobie pytanie „czy poprosiłbym innego człowieka o code review tej konkretnej zmiany?”. Jeśli odpowiedź brzmi „nie” (zmiana trywialna, rutynowa, oczywista), to najprawdopodobniej nie potrzebujesz uruchamiać no-mistakes. Pełny pipeline weryfikacji rezerwuj dla zmian, które realnie wymagałyby uwagi drugiego inżyniera — pozwala to oszczędzić tokeny, latencję i ograniczyć szum w sygnale zwrotnym.

## Uwaga / Anty-wzorzec
Bezwarunkowe przepuszczanie każdej zmiany przez zewnętrzny review / weryfikator — marnotrawstwo budżetu tokenowego i czasu, a także ryzyko szumu i fałszywych alarmów przy trywialnych diffach, co osłabia zaufanie do narzędzia.

## Oryginalny cytat
> *"no - not every change! i talked about this in more depth in my latest video but tl;dr is you can ask yourself "would i ask another human to do code review for this change" and if the answer is no, then you probably don't need no-mistakes"*
