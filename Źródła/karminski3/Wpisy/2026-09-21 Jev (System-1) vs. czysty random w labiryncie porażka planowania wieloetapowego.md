---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 21 07:49:04 +0000 2026"
źródło: "https://x.com/karminski3/status/2101941770003361893"
kategoria: "Architektura systemów agentowych i planowanie"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Jev (System-1) vs. czysty random w labiryncie: porażka planowania wieloetapowego

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 21 07:49:04 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2101941770003361893)
- **Kluczowe pojęcia:** [[Harness|System-1]] [[Harness|System-2]] [[Harness|Lokalne optimum]] [[Harness|Random walk]] [[Harness|Twierdzenie Pólyi o powracaniu]] [[Harness|Planowanie wieloetapowe]] [[Jev]] [[Harness|xoshiro256++]] [[Harness|Heurystyka]] [[Harness|Agent AI]]

---

## Kontekst i problem
Autor przeprowadził eksperyment porównujący model Jev (szybki, jednokrokowy, System-1) z czystym generatorem liczb losowych w zadaniu znajdowania ścieżki w labiryncie. Jev otrzymał heurystykę (odległość Manhattan) i dodatkowe reguły (last_move, visited_count), ale mimo to utknął w lokalnym optimum, podczas gdy random walk, dzięki twierdzeniu Pólyi o powracaniu, rozwiązał labirynt szybciej. Wniosek: Jev nie jest plannerem, lecz jedynie szybkim klasyfikatorem pojedynczego kroku.

## Rada inżynierska
Do zadań wymagających planowania wieloetapowego, backtrackingu, unikania lokalnych optimów lub podejmowania nieodwracalnych decyzji nie używaj modeli System-1 (szybkich, jednokrokowych). Zamiast tego stosuj model System-2 lub architekturę hybrydową z dedykowanym plannerem. Nawet jeśli dasz modelowi System-1 heurystyki i pamięć, może je zignorować na rzecz natychmiastowej oceny kroku.

## Uwaga / Anty-wzorzec
Pułapka: zakładanie, że model System-1 z odpowiednimi cechami (np. odległość Manhattan) i dodatkowymi regułami (visited_count) będzie w stanie wyjść z lokalnego optimum. W praktyce model może trwale ignorować reguły drugorzędne, jeśli główna heurystyka wskazuje kierunek prowadzący do ślepego zaułka. To prowadzi do zapętlenia i przekroczenia limitu czasu.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Wyniki podważają powszechne przekonanie, że modele AI (nawet szybkie System-1) są lepsze od prostych algorytmów losowych w zadaniach planowania. Pokazują, że w niektórych przypadkach czysty random walk może być skuteczniejszy niż model oparty na heurystykach, co stoi w sprzeczności z optymizmem wobec agentów AI. Autor argumentuje, że Jev jest jedynie single-step structured judge, a nie plannerem, co może być kontrowersyjne dla zwolenników podejść end-to-end.
