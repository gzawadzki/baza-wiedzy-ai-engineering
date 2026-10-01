---
typ: wpis-źródłowy
autor: "@HamelHusain"
data: "Fri Sep 11 23:48:53 +0000 2026"
źródło: "https://x.com/HamelHusain/status/2098559434138206421"
kategoria: "Ewaluacja / Narzędzia eval dla agentów"
tagi:
  - hamelhusain
  - ai-engineering
  - wpis-atomowy
---

# Projektowanie narzędzi eval dla agentów: in-situ feedback i error discovery zamiast ankiet wstępnych

- **Autor:** [[HamelHusain — Indeks|@HamelHusain]] | **Data:** `Fri Sep 11 23:48:53 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2098559434138206421)
- **Kluczowe pojęcia:** [[Harness|Ewaluacja agentów]] [[Harness|Error discovery]] [[Harness|Trace annotation]] [[Harness|In-situ feedback]] [[Harness|LLM-as-a-judge]] [[Context Compaction|Inżynieria kontekstu]] [[Dynamiczne Skille i Metaprogramowanie Agenta|Plugin / Skill w agentach]]

---

## Kontekst i problem
Autor komentuje nowe narzędzia do ewaluacji pluginów/skillów w agentach (np. wbudowane affordances eval w Claude). Narzędzie działa, ale jego workflow jest niedopasowany do rzeczywistego procesu inżynierskiego: odpytuje użytkownika z pamięci z góry, automatycznie buduje datasety i judge'y, jest trudne w użyciu dla nie-pluginowych skillów i brakuje mu onboardingu do wyników.

## Rada inżynierska
Narzędzia eval powinny być projektowane wokół rzeczywistego procesu inżyniera, a nie wokół abstrakcyjnego formularza: (1) feedback in-situ — pozwól oznaczać plugin/skill w trakcie jego używania, a nie z pamięci z góry; (2) error discovery first — najpierw wspólne odkrywanie błędów na prawdziwych trace'ach/session history, dopiero potem budowa datasetu i judge'ów; (3) wsparcie dla dowolnych skillów, nie tylko pluginów; (4) onboardingu do wygenerowanego HTML/raportu, bo surowe wyniki są nieczytelne bez kontekstu.

## Uwaga / Anty-wzorzec
Anty-wzorzec: automatyczne generowanie datasetów i sędziów (judge) na podstawie deklaracji użytkownika z góry oraz dokumentacji pluginu — zamiast najpierw zakotwiczyć eval w rzeczywistych, oznaczonych trace'ach z sesji. Prowadzi to do evalów mierzących wyobrażenie o błędach, a nie realne awarie. Drugi anty-wzorzec: generowanie raportu HTML bez warstwy onboardingu — użytkownik musi 'gapić się' na wynik, by zrozumieć jego znaczenie.

## Oryginalny cytat
> *"It's cool that there is more interest in eval tools!   Some opportunities for improvement: 

1. Right now, this workflow tries to quiz you up front about your recollection of your experience with a plugin.    It would be better if it was more "in-situ", meaning you could give feedback on the plugins as you are using them.

2. It goes off and builds datasets and judges automatically based on what you tell it in up front as well as what's documented in the plugin.  I would like to see it try to do error discovery with you first to allow you to annotate real traces / session history etc so you can figure out what's not working better.  

3. It was clunky to do this against a skill that wasn't a plugin.  I had to ask claude to set it up for me and it took 10 minutes to figure that out.  

4. I had to stare at the generated HTML for a while before I could understand what everything meant.  There is some onboarding experience that is missing but I'm not sure what that is yet.  

I'm sure this will get better over time and the things above seem doable.  It's also positive to see affordances for evals directly in our agents!"*
