---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Tue Sep 22 03:31:40 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2102239379536433551"
kategoria: "Proces weryfikacji / Code Review AI"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Selektywne code review: kiedy NIE uruchamiać automatycznej weryfikacji zmian

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Tue Sep 22 03:31:40 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102239379536433551)
- **Konwersacja:** Odpowiedź w dyskusji (@EthanClinick)
- **Kluczowe pojęcia:** [[Code Review]] [[Weryfikacja krokowa|Automatyczna weryfikacja zmian]] [[Weryfikator|Zewnętrzny weryfikator]] [[Harness|Pętla feedbacku agenta]] [[Harness|Koszt tokenów]] [[Harness|Anty-wzorce w systemach agentowych]] [[Selektywna weryfikacja kodu]]

---

## Kontekst i problem
Odpowiedź w dyskusji pod wpisem @EthanClinick dotyczącej stosowania automatycznej weryfikacji kodu (tzw. "no-mistakes") do zmian w repozytorium. Autor odpiera założenie, że każda zmiana powinna przechodzić przez review, i proponuje prostą heurystykę decyzyjną opartą na tym, czy zmiana w ogóle zasługiwałaby na uwagę drugiego człowieka.

## Rada inżynierska
Nie każda zmiana wymaga automatycznego review ani zewnętrznego weryfikatora. Stosuj heurystykę: zadaj sobie pytanie "czy poprosiłbym innego człowieka o code review tej zmiany?". Jeśli odpowiedź brzmi "nie" (zmiana trywialna, oczywisty refaktor, drobna korekta), to prawdopodobnie nie potrzebujesz też automatycznej weryfikacji. Selektywne uruchamianie review oszczędza tokeny, budżet i latencję oraz utrzymuje krótką pętlę feedbacku w pracy z agentem.

## Uwaga / Anty-wzorzec
Traktowanie automatycznej weryfikacji jako obowiązkowego kroku dla absolutnie każdej zmiany ("review everything") — prowadzi to do przepalania budżetu tokenowego, wydłużenia czasu odpowiedzi, szumu w wynikach i spowolnienia iteracji bez realnego zysku jakościowego.

## Oryginalny cytat
> *"@EthanClinick no - not every change! i talked about this in more depth in my latest video but tl;dr is you can ask yourself "would i ask another human to do code review for this change" and if the answer is no, then you probably don't need no-mistakes"*
