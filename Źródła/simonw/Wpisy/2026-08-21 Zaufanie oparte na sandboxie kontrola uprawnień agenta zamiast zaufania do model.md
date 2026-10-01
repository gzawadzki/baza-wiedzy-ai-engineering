---
typ: wpis-źródłowy
autor: "@simonw"
data: "Fri Aug 21 09:07:37 +0000 2026"
źródło: "https://x.com/simonw/status/2090727511751639185"
kategoria: "Architektura agentowa / Bezpieczeństwo i izolacja wykonania"
tagi:
  - simonw
  - ai-engineering
  - wpis-atomowy
---

# Zaufanie oparte na sandboxie: kontrola uprawnień agenta zamiast zaufania do modelu

- **Autor:** [[simonw — Indeks|@simonw]] | **Data:** `Fri Aug 21 09:07:37 +0000 2026` | **Źródło:** [Post na X](https://x.com/simonw/status/2090727511751639185)
- **Konwersacja:** Odpowiedź w dyskusji (@ksredelinghuys)
- **Kluczowe pojęcia:** [[Sandbox i Granice Bezpieczeństwa Agenta|Sandboxing agentów]] [[Harness|Claude Code]] [[Harness|Apple Containers]] [[Sandbox i Granice Bezpieczeństwa Agenta|Zasada najmniejszych uprawnień]] [[Prompt Architecture|Prompt injection]] [[Sandbox i Granice Bezpieczeństwa Agenta|Bezpieczeństwo agentów AI]] [[Harness|Harness agentowy]]

---

## Kontekst i problem
Wpis jest odpowiedzią w dyskusji o tym, jak można zaufać agentowi AI wykonującemu kod i operacje na systemie. Problem: agent (np. CLI z dostępem do shella, plików i sieci) może wykonać destrukcyjne lub niepożądane akcje, a mechanizmy oparte na instrukcjach w prompcie są zawodne. Autor wskazuje, że realną granicą zaufania nie jest model ani jego zachowanie, lecz warstwa izolacji środowiska wykonawczego, która fizycznie ogranicza zakres dozwolonych operacji.

## Rada inżynierska
Nie buduj bezpieczeństwa agenta na promptach ani na założeniu, że model 'będzie grzeczny'. Jedynym mechanizmem, któremu można zaufać, jest środowisko wykonawcze kontrolujące, co agent może zrobić: sandbox z ograniczonym systemem plików, siecią i uprawnieniami procesu. W praktyce autor używa do tego Claude Code for web (środowisko zdalne, w pełni kontrolowane) i eksperymentuje z Apple Containers jako lokalną alternatywą opartą na kontenerach. Reguła inżynierska: najpierw zaprojektuj granicę uprawnień (co agent może odczytać, zapisać, do kogo się połączyć), potem dopiero pisz prompt.

## Uwaga / Anty-wzorzec
Anty-wzorzec: uruchamianie agenta kodującego bezpośrednio na hoście z pełnym dostępem do systemu plików, poświadczeń i sieci, przy jednoczesnym 'zabezpieczaniu' go wyłącznie instrukcjami w prompcie lub mechanizmami potwierdzeń (human-in-the-loop). Instrukcje tekstowe nie są granicą bezpieczeństwa — model może je zignorować, zostać zmanipulowany przez wstrzykniętą treść (prompt injection) lub po prostu źle zinterpretować. Drugi anty-wzorzec: traktowanie sandboxa jako opcjonalnego dodatku zamiast jako podstawowej architektury harnessu.

## Oryginalny cytat
> *"@ksredelinghuys The only thing I trust is an environment that controls what they can do - that's why I use Claude Code for web so much, but I've been experimenting with Apple Containers too"*
