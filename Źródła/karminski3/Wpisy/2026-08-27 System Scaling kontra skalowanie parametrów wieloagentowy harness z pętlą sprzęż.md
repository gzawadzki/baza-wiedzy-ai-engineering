---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Thu Aug 27 08:39:50 +0000 2026"
źródło: "https://x.com/karminski3/status/2092894849619874210"
kategoria: "Architektura systemów agentowych (Agentic Engineering)"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# System Scaling kontra skalowanie parametrów: wieloagentowy harness z pętlą sprzężenia zwrotnego z środowiskiem

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Thu Aug 27 08:39:50 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2092894849619874210)
- **Konwersacja:** Odpowiedź w dyskusji (@karminski3)
- **Kluczowe pojęcia:** [[Harness|System Scaling]] [[Harness|Multi-Agent System]] [[Harness|Pętla sprzężenia zwrotnego ze środowiskiem]] [[Harness|Agentic Engineering]] [[Weryfikator|Zewnętrzny weryfikator]] [[Harness|Harness agentowy]] [[Harness|DeepResearch]]

---

## Kontekst i problem
Autor komentuje rezultat działania własnego/otwartoźródłowego harnessu agentowego: w architekturze wieloagentowej z zamkniętą pętlą testowania na środowisku system dostarczył gotową konfigurację firewalla dopasowaną do konkretnego wektora ataku w około 10 minut. Teza: przewaga w inżynierii AI nie wynika już z liczby parametrów modelu, lecz z umiejętności zbudowania spójnego systemu, który łączy środowiskowy feedback z prób i błędów oraz koordynację wielu agentów. Wpis zapowiada też udostępnienie frameworka i specjalizowanego modelu DeepResearch.

## Rada inżynierska
Traktuj model jako jeden komponent większego systemu, a nie jako całe rozwiązanie. Kluczowe elementy inżynierskie: (1) zamknięta pętla wykonanie → obserwacja → korekta na realnym środowisku (np. ruch sieciowy, logi, kod wyjściowy narzędzia), (2) podział pracy między agentów z jasnymi rolami i punktami synchronizacji, (3) weryfikacja wyniku zewnętrznym testem, a nie samooceną modelu. Dopiero takie 'System Scaling' — spójny harness + pętla feedbacku + multi-agent — pozwala domykać zadania inżynierskie end-to-end w minutach zamiast godzin.

## Uwaga / Anty-wzorzec
Wyścig wyłącznie o liczbę parametrów lub benchmarki modelu bez zbudowania otoczenia, które dostarcza modelowi sygnału zwrotnego z rzeczywistego środowiska — agent nie ma wtedy jak wykryć i naprawić własnego błędu, a wynik pozostaje niezweryfikowany. Drugą pułapką jest traktowanie wieloagentowości jako celu samego w sobie: bez wspólnego stanu, protokołu komunikacji i zewnętrznego weryfikatora koordynacja wielu agentów generuje koszt i szum zamiast jakości.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Teza 'przyszła konkurencja w AI to nie skalowanie liczby parametrów, lecz System Scaling' stoi w napięciu z dominującym w branży paradygmatem scaling laws / 'scale is all you need', w którym jakość wyniku jest przede wszystkim funkcją skali modelu i danych. Do rozstrzygnięcia: czy dla zadań inżynierskich (konfiguracja, security, kod) wartość dodana leży głównie w harnessie i pętli feedbacku, czy też przewaga systemowa jest tylko artefaktem obecnych ograniczeń modeli i zniknie wraz ze wzrostem ich możliwości. Dodatkowo wpis ma charakter częściowo promocyjny (linki do własnego frameworka i modelu), a dowód stanowi pojedynczy, anegdotyczny przypadek (10 minut na konfigurację firewalla) bez danych porównawczych ani baseline'u.

## Oryginalny cytat
> *"最后, 在这个架构加持下, 它仅用了10分钟左右就给我交付了针对攻击的防火墙配置. 这真的是 Agentic 系统工程的胜利了. 

未来的 AI 竞争, 不仅是卷模型参数量, 能把环境试错反馈和多 Agent 协同做成统一的系统 (System Scaling), 才是真正让AI在各种工程中落地的关键.

另外, 这个框架还开源了! 这里: https://t.co/n4F2ulrtEc
配套的 DeepResearch 模型也在这里: https://t.co/f8BzbXFh1n (模型之前也给大家测过, 是针对 DeepResearch 特调的, 性能相当不错)"*
