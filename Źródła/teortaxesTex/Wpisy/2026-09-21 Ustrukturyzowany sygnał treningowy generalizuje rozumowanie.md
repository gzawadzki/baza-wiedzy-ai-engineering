---
typ: wpis-źródłowy
autor: "@teortaxesTex"
data: "Mon Sep 21 23:13:59 +0000 2026"
źródło: "https://x.com/teortaxesTex/status/2102174532547080559"
kategoria: "Trening modeli / Generalizacja umiejętności"
tagi:
  - teortaxestex
  - ai-engineering
  - wpis-atomowy
---

# Ustrukturyzowany sygnał treningowy generalizuje rozumowanie

- **Autor:** [[teortaxesTex — Indeks|@teortaxesTex]] | **Data:** `Mon Sep 21 23:13:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102174532547080559)
- **Konwersacja:** Odpowiedź w dyskusji (@phl43)
- **Kluczowe pojęcia:** [[Harness|Generalizacja rozumowania]] [[Harness|Trening na kodzie]] [[Harness|RL z weryfikowalnym sygnałem]] [[Harness|Transfer umiejętności]] [[Harness|Czynnik g modelu]]

---

## Kontekst i problem
Dyskusja o transferze umiejętności w modelach językowych: logicznie ustrukturyzowane sygnały treningowe w pretreningu i RL mają poprawiać ogólne rozumowanie. Autor podaje przykłady modeli pretrenowanych na kodzie, które poprawiły się w niemal wszystkich zadaniach, oraz R1 trenowanego RL na matematyce i kodzie, który stał się znacznie lepszym pisarzem niż V3. Jednocześnie twierdzi, że styl nie jest silnie skorelowany z czynnikiem g.

## Rada inżynierska
Inwestuj w trening na zadaniach o ścisłej strukturze logicznej — kod, matematyka, dowody, RL z weryfikowalnym sygnałem — ponieważ takie sygnały transferują się na inne domeny i podnoszą ogólne zdolności rozumowania modelu. Nie zakładaj, że optymalizacja stylu lub formatu da podobny wzrost ogólnej inteligencji modelu.

## Uwaga / Anty-wzorzec
Traktowanie poprawy stylu, tonu lub formatowania odpowiedzi jako miary ogólnych zdolności rozumowania. Strojenie pod styl bez logicznego sygnału treningowego może nie przełożyć się na transfer do innych zadań.

## Oryginalny cytat
> *"@phl43 We see that logically structured training signal (both in pretraining and in RL) generalizes reasoning. First models pretrained on coding got better at ≈all tasks, R1 was RL'd for mafs&amp;coding and became a vastly better writer than V3.
but style, it seems, is not very g-loaded"*
