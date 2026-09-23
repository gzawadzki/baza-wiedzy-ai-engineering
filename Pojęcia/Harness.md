---
typ: pojęcie
aliases: [Agent Harness, Środowisko wykonawcze agenta, Rusztowanie agentowe]
tagi:
  - agenci
  - harness
  - architektura
  - wykonanie
źródła:
  - "[[kunchenguid — Indeks]]"
  - "[[simonw — Indeks]]"
  - "[[karminski3 — Indeks]]"
  - "[[DrJimFan — Indeks]]"
---

# Harness

**Harness** (rusztowanie / środowisko uruchomieniowe agenta) to warstwa oprogramowania otaczająca model fundamentowy (LLM / System One), która kontroluje cykl życia agenta, dostarcza narzędzia, wstrzykuje wybiórczy kontekst, egzekwuje uprawnienia i weryfikuje wyniki.

Podczas gdy model dostarcza zdolności wnioskowania, to **harness decyduje o możliwości wykonania realnej pracy inżynierskiej** (*„Model daje inteligencję, harness daje pracę”* — Karminski).

## Kluczowe odpowiedzialności harnessu

1. **Izolacja wykonania ([[Sandbox i Granice Bezpieczeństwa Agenta]]):**
   - Zabezpieczenie systemu operacyjnego przed niekontrolowanymi akcjami agenta (konteneryzacja, brak dostępu do sieci produkcyjnej, ochrona przed [[Prompt Architecture|Prompt Injection]]).
2. **Zarządzanie oknem i pamięcią ([[Context Compaction]]):**
   - Monitorowanie zapełnienia bufora tokenów, wyznaczanie [[Bezpieczny punkt kompaktowania|bezpiecznych punktów kompaktowania]] i wymuszanie [[Persistencja stanu agenta|persistencji stanu na dysku]].
3. **Pętla decyzyjna i routing narzędzi ([[Kaskady Modeli i Routing Pewności]]):**
   - Przekazywanie wywołań narzędzi, obsługa błędów wykonania linterów i kompilatorów oraz sterowanie kaskadą modeli (np. lekki decydent [[Jev]] do dispatchu zamiast drogiego orkiestratora LLM).
4. **Weryfikacja i bramki jakościowe ([[Weryfikator]]):**
   - Wymuszanie procedur [[Selektywna weryfikacja kodu|selektywnej weryfikacji]] oraz blokowanie nieautoryzowanych pominięć testów ([[CI Check Bypass Confirmation]]).

## Architektura i skalowanie (Harness Scaling)

Według ustaleń inżynierskich Kuna Chena i Karminskiego, dalszy wzrost skuteczności agentów kodujących wynika dziś w większym stopniu z **Harness Scaling** (lepsze narzędzia, asynchroniczna współpraca wielu agentów [[Firstmate i Agenci Wykonawczy]], dynamiczne generowanie Micro-Skilli [[Dynamiczne Skille i Metaprogramowanie Agenta]]) niż z samego zwiększania liczby parametrów pojedynczego modelu.

## Powiązane

- [[Sandbox i Granice Bezpieczeństwa Agenta]]
- [[Context Compaction]]
- [[Weryfikator]]
- [[Firstmate i Agenci Wykonawczy]]
- [[Kaskady Modeli i Routing Pewności]]
- [[Dynamiczne Skille i Metaprogramowanie Agenta]]
- [[Interpretable Context Methodology]]
- [[Jev]]
