---
typ: pojęcie
aliases: [Firstmate, Leaf Node Agent, Hierarchy of Agents]
tagi: [agenci, architektura, orkiestracja, skalowanie]
źródła:
  - "[[Kun Chen — Baza Wskazówek i Komentarzy]]"
---

# Firstmate i Agenci Wykonawczy (Leaf Nodes)

W architekturze agentowej dla złożonych systemów inżynierskich wprowadza się podział ról na warstwę orkiestracji (**Firstmate**) oraz agentów bezpośredniego wykonania (**Leaf Node Agents**).

## Role w architekturze

1. **Firstmate (Orkiestrator / Asystent główny)**:
   - Działa na poziomie strategicznym: dekomponuje cele inżyniera na zadania techniczne, monitoruje spójność architektury i nadzoruje pracę agentów-liści.
   - Posiada wysokie wymagania co do stabilności oraz ścisłego stosowania się do instrukcji systemowych (*system prompt adherence*).
2. **Leaf Node Agent (Agent wykonawczy / liść)**:
   - Skupiony na wąskim, konkretnym zadaniu (np. edycja jednego modułu, napisanie testu jednostkowego, inspekcja logu błędu).
   - Działa w małym, czystym oknie kontekstowym i szybko kończy pracę.

## Tradeoff inżynierski

- **Bezpośrednia praca z agentem-liściem**: Inżynier bezpośrednio steruje agentem krok po kroku. Daje to natychmiastową kontrolę i najszybsze rozwiązanie pojedynczego problemu, ale nie skaluje się (angażuje 100% uwagi człowieka).
- **Praca przez Firstmate**: Człowiek deleguje zadanie do firstmate'a, który kieruje agentami-liśćmi. Zapewnia to skalowalność, lecz wprowadza ryzyko drobnych niezgodności (*misalignment*), wymagających późniejszej korekty (rework).

## Powiązane

- [[Rework Rate]]
- [[Harness]]
- [[Prompt Architecture]]
