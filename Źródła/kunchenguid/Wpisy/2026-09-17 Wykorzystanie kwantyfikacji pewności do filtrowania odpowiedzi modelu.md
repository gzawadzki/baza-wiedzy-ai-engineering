---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Thu Sep 17 15:29:09 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100608000042127434"
kategoria: "Inżynieria systemów agentowych / Zarządzanie niepewnością"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Wykorzystanie kwantyfikacji pewności do filtrowania odpowiedzi modelu

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Thu Sep 17 15:29:09 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100608000042127434)
- **Konwersacja:** Odpowiedź w dyskusji (@PremiumGoblin)
- **Kluczowe pojęcia:** [[Harness|Kwantyfikacja pewności]] [[Harness|Zarządzanie niepewnością w LLM]] [[Harness|Filtrowanie odpowiedzi modelu]] [[Harness|Inżynieria wymagań]]

---

## Kontekst i problem
Autor odpowiada na wpis dotyczący oceny, czy wymagania są dobrze zdefiniowane. Zauważa, że ocena poziomu niejednoznaczności wymagań w fazie implementacji jest trudna. Wskazuje, że narzędzie 'jev' kwantyfikuje pewność, co pozwala odrzucać odpowiedzi o niskiej pewności.

## Rada inżynierska
Stosuj kwantyfikację pewności (confidence) w odpowiedziach modeli, aby automatycznie odrzucać te o niskiej pewności. Dzięki temu możesz filtrować wyniki w warunkach niejednoznacznych wymagań, zamiast polegać wyłącznie na własnej ocenie.

## Uwaga / Anty-wzorzec
Nie zakładaj, że wymagania są zawsze dobrze zdefiniowane; niepewność jest nieunikniona. Poleganie wyłącznie na confidence bez dodatkowej weryfikacji może prowadzić do błędów, jeśli model jest nadmiernie pewny siebie.

## Oryginalny cytat
> *"not always - but for some cases yes, the judgment on whether requirements are “well defined” enough and how much ambiguity still exists during the implementation phase is not easy to answer

the extra nice thing about jev is that it quantifies the confidence, so i can say “if it’s not confident the i discard its answer”"*
