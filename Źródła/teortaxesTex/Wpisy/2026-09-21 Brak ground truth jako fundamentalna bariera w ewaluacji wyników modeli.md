---
typ: wpis-źródłowy
autor: "@teortaxesTex"
data: "Mon Sep 21 23:05:13 +0000 2026"
źródło: "https://x.com/teortaxesTex/status/2102172327232385279"
kategoria: "Ewaluacja i weryfikacja modeli (Benchmarking)"
tagi:
  - teortaxestex
  - ai-engineering
  - wpis-atomowy
---

# Brak ground truth jako fundamentalna bariera w ewaluacji wyników modeli

- **Autor:** [[teortaxesTex — Indeks|@teortaxesTex]] | **Data:** `Mon Sep 21 23:05:13 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102172327232385279)
- **Konwersacja:** Odpowiedź w dyskusji (@phl43)
- **Kluczowe pojęcia:** [[Eval Set z realnych sesji|Ground truth]] [[Harness|LLM-as-a-judge]] [[Weryfikacja krokowa|Weryfikacja formalna]] [[Harness|Lean]] [[Harness|Ewaluacja modeli]] [[Harness|Testy jednostkowe jako reward signal]] [[Harness|Pętla sprzężenia zwrotnego w treningu]]

---

## Kontekst i problem
Autor odpowiada na zarzut, że problem weryfikacji wyników modeli nie został rozwiązany. Wskazuje, że podejmowano punktowe próby naprawy tego stanu, ale nie jest to priorytet, ponieważ brak jest obiektywnego sygnału prawdy (ground truth). Porównuje domeny, w których weryfikacja jest tania i deterministyczna (kod — testy, obliczenia — natychmiastowe sprawdzenie wyniku, matematyka — asystent dowodowy Lean) z domenami otwartymi, gdzie takiego sygnału nie ma, przez co scoring opiera się na innych modelach, co samo w sobie jest problematyczne.

## Rada inżynierska
Zdolność do automatycznej weryfikacji wyniku zależy wyłącznie od istnienia deterministycznego, niezależnego od modelu sygnału zwrotnego. Reguła inżynierska: projektuj harness tak, aby każdy krok agenta kończył się weryfikowalnym artefaktem — testem jednostkowym/integracyjnym dla kodu, dokładnym porównaniem liczbowym dla obliczeń, dowodem w systemie formalnym (np. Lean) dla matematyki. Im silniejszy i tańszy sygnał weryfikacyjny, tym większa szansa na realną poprawę jakości przez trening i pętlę sprzężenia zwrotnego. Dla domen bez ground truth nie da się zbudować wiarygodnego scorera bez zewnętrznego, niezależnego źródła prawdy.

## Uwaga / Anty-wzorzec
Ocena wyników w domenach otwartych przy użyciu innych modeli jako sędziów (LLM-as-a-judge) bez zakotwiczenia w ground truth — jest to rozumowanie cyrkularne: sędzia dziedziczy te same słabości i halucynacje co oceniany model, co prowadzi do zawyżania metryk, dryfu benchmarków i optymalizacji pod artefakty sędziego zamiast pod rzeczywistą jakość. Antywzorzec: traktowanie wyników takiej ewaluacji jako twardego sygnału do treningu lub do decyzji produktowych.

## Oryginalny cytat
> *"There have been attempts to fix this in a targeted fashion, but yes, not a priority, and it's genuinely hard because you don't have ground truth. Literally how do you score online? With clankers? Coding has tests, calculation has instant checking, Lean makes math verifiable."*
