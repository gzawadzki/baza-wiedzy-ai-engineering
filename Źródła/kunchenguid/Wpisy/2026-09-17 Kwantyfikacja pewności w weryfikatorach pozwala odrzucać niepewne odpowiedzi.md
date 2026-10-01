---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Thu Sep 17 15:29:09 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100608000042127434"
kategoria: "Weryfikacja agentów i inżynieria wymagań"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Kwantyfikacja pewności w weryfikatorach pozwala odrzucać niepewne odpowiedzi

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Thu Sep 17 15:29:09 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100608000042127434)
- **Konwersacja:** Odpowiedź w dyskusji (@PremiumGoblin)
- **Kluczowe pojęcia:** [[Harness|LLM-as-a-judge]] [[Weryfikator|Zewnętrzny weryfikator]] [[Harness|Kalibracja pewności modelu]] [[Harness|Próg pewności]] [[Harness|Inżynieria wymagań]] [[Harness|Systemy agentowe]]

---

## Kontekst i problem
Autor komentuje problem oceny, czy wymagania są wystarczająco dobrze zdefiniowane oraz ile niejednoznaczności pozostaje w fazie implementacji. Wskazuje, że nie zawsze da się to rozstrzygnąć jednoznacznie, ale narzędzie jev dostarcza skwantyfikowaną pewność, co pozwala odrzucać odpowiedzi o niskiej pewności.

## Rada inżynierska
W harnessach i systemach weryfikacji opartych na modelach nie traktuj oceny wymagań jako binarnej. Wymagaj od weryfikatora (np. LLM-as-a-judge) zwracania poziomu pewności i ustaw próg odrzucenia: gdy pewność jest niska, odrzuć odpowiedź zamiast podejmować decyzję na jej podstawie.

## Uwaga / Anty-wzorzec
Przyjmowanie odpowiedzi weryfikatora bez miary pewności, szczególnie przy niejednoznacznych wymaganiach, prowadzi do błędnych decyzji i propagacji niepewności w systemie agentowym.

## Oryginalny cytat
> *"not always - but for some cases yes, the judgment on whether requirements are “well defined” enough and how much ambiguity still exists during the implementation phase is not easy to answer

the extra nice thing about jev is that it quantifies the confidence, so i can say “if it’s not confident the i discard its answer”"*
