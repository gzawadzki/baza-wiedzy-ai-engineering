---
typ: pojęcie
aliases: [Wskaźnik przeróbek, Koszt poprawek, Outcome Evaluation]
tagi: [ewaluacja, agenci, jakosc, metryki]
źródła:
  - "[[Kun Chen — Baza Wskazówek i Komentarzy]]"
---

# Rework Rate

**Rework Rate** (wskaźnik poprawek/przeróbek) to praktyczna inżynierska metryka oceny skuteczności systemów agentowych i promptów, oparta na mierzalnym nakładzie pracy potrzebnym do skorygowania błędów modelu.

## Dlaczego ocena pojedynczego promptu zawodzi

W tradycyjnym podejściu inżynierowie próbują oceniać "jakość promptu" w izolacji. W systemach agentowych (zwłaszcza z pętlami iteracyjnymi i orkiestracją) prompt rzadko istnieje w finalnej, zamkniętej postaci.

Zamiast ewaluacji estetycznej lub syntaktycznej promptu, ewaluuje się:
1. **Końcowy rezultat (Outcome)** — czy kod przechodzi testy i spełnia wymagania biznesowe.
2. **Częstotliwość i koszt reworku (Rework Rate)** — jak często człowiek lub weryfikator musi ingerować, cofać zmiany lub ręcznie poprawiać wynik agenta.

System agentowy, który pozwala człowiekowi oszczędzić 80% czasu, ale wymaga 20% czasu na poprawki, ma wysoką wartość produkcyjną w porównaniu z systemem o pozornie "idealnych promptach", który generuje subtelne błędy architektoniczne.

## Powiązane

- [[Firstmate i Agenci Wykonawczy]]
- [[Weryfikator]]
- [[Harness]]
- [[Prompt Architecture]]
