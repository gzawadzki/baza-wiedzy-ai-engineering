---
typ: pojęcie
aliases: [Firstmate, Agent Orkiestrujący, Executive Agent]
tagi: [orkiestracja, agenci, firstmate, architektura]
źródła:
  - "[[Kun Chen — Baza Wskazówek i Komentarzy]]"
---

# Firstmate Agent

**Firstmate Agent** to wyspecjalizowany agent pełniący rolę głównego oficera wykonawczego / orkiestratora pomiędzy ludzkim inżynierem a agentami wykonawczymi (tzw. [[Firstmate i Agenci Wykonawczy|agentami-liśćmi]]).

Szczegółowy opis architektury, ról i kompromisów znajduje się w:
[[Firstmate i Agenci Wykonawczy]]

## Główne cechy Firstmate'a:
- Wymaga modelu o bardzo wysokiej zgodności z system promptem ([[Stabilność modeli i przestrzeganie promptu]]).
- Pilnuje procedur bezpieczeństwa (np. [[CI Check Bypass Confirmation|wymóg potwierdzenia pominięcia CI]]).
- Odpowiada za skalowanie pracy inżyniera kosztem akceptowalnego wskaźnika poprawek ([[Rework Rate]]).
