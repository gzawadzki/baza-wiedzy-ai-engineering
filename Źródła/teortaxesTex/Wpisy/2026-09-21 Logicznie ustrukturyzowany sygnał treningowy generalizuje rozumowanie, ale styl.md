---
typ: wpis-źródłowy
autor: "@teortaxesTex"
data: "Mon Sep 21 23:13:59 +0000 2026"
źródło: "https://x.com/teortaxesTex/status/2102174532547080559"
kategoria: "Trening modeli / Transfer wiedzy / Architektura sygnału treningowego"
tagi:
  - teortaxestex
  - ai-engineering
  - wpis-atomowy
---

# Logicznie ustrukturyzowany sygnał treningowy generalizuje rozumowanie, ale styl nie jest g-loaded

- **Autor:** [[teortaxesTex — Indeks|@teortaxesTex]] | **Data:** `Mon Sep 21 23:13:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102174532547080559)
- **Konwersacja:** Odpowiedź w dyskusji (@phl43)
- **Kluczowe pojęcia:** [[Harness|Transfer wiedzy]] [[Harness|Generalizacja rozumowania]] [[Harness|RL dla matematyki i kodu]] [[Harness|Pretrening na kodzie]] [[Harness|g-loaded]] [[Harness|R1 vs V3]]

---

## Kontekst i problem
Dyskusja o tym, które rodzaje sygnału treningowego przekładają się na ogólną zdolność rozumowania. Autor argumentuje, że trening na danych o logicznej strukturze (kod, matematyka) — zarówno w pretreningu, jak i w RL — prowadzi do transferu umiejętności rozumowania na praktycznie wszystkie zadania. Kontrastuje to ze stylem pisania, który według niego nie koreluje silnie z ogólną inteligencją (g-loaded) i nie generalizuje w ten sam sposób.

## Rada inżynierska
Traktuj logicznie ustrukturyzowany sygnał (kod, matematyka) jako uniwersalny nośnik zdolności rozumowania: pretrening na kodowaniu poprawia wyniki na ≈wszystkich zadaniach, a RL na matematyce i kodzie (przypadek R1 vs V3) daje efekt uboczny w postaci znacznie lepszego pisania. Wniosek inżynierski: jeśli chcesz podnieść ogólne zdolności rozumowania modelu, inwestuj w trening na danych o twardej strukturze logicznej, a nie w optymalizację samego stylu.

## Uwaga / Anty-wzorzec
Optymalizacja pod styl/powierzchniową formę wypowiedzi nie przekłada się na wzrost ogólnej zdolności rozumowania — styl nie jest silnie g-loaded, więc nie generalizuje na zadania wymagające logiki. Zakładanie, że poprawa stylu pociągnie za sobą poprawę rozumienia, jest błędne.

## Oryginalny cytat
> *"@phl43 We see that logically structured training signal (both in pretraining and in RL) generalizes reasoning. First models pretrained on coding got better at ≈all tasks, R1 was RL'd for mafs&coding and became a vastly better writer than V3.
but style, it seems, is not very g-loaded"*
