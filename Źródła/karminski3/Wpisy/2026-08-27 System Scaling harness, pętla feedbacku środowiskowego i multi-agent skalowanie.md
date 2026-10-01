---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Thu Aug 27 08:39:50 +0000 2026"
źródło: "https://x.com/karminski3/status/2092894849619874210"
kategoria: "Architektura systemów agentowych / Harness i pętle weryfikacji"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# System Scaling: harness, pętla feedbacku środowiskowego i multi-agent > skalowanie parametrów

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Thu Aug 27 08:39:50 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2092894849619874210)
- **Konwersacja:** Odpowiedź w dyskusji (@karminski3)
- **Kluczowe pojęcia:** [[Harness|System Scaling]] [[Harness|Agentic System]] [[Harness|Multi-Agent Collaboration]] [[Harness|Environment Feedback Loop]] [[Harness|Harness Engineering]] [[Harness|DeepResearch]] [[Harness|Model Specialization]] [[Harness|External Verifier]] [[Firstmate i Agenci Wykonawczy]]

---

## Kontekst i problem
Autor komentuje rezultat działania własnego/udostępnianego frameworku agentowego: w ciągu ~10 minut system dostarczył gotową konfigurację firewalla dopasowaną do konkretnego wektora ataku. Kontekstem jest teza, że o realnej użyteczności AI w inżynierii nie decyduje rozmiar modelu, lecz architektura harnessu, która spina pętlę prób i błędów w środowisku oraz koordynację wielu agentów w jeden spójny system. Autor wskazuje też na otwarte źródła: framework oraz model DeepResearch dostrojony specjalnie pod zadania deep-research.

## Rada inżynierska
Traktuj 'System Scaling' jako główną dźwignię wdrożeń: (1) domknij pętlę sprzężenia zwrotnego — agent musi wykonywać realne akcje w środowisku i odbierać ich wynik (test, deploy, walidacja konfiguracji), a nie tylko generować tekst; (2) rozbij zadanie na role i pozwól wielu agentom na wymianę wyników oraz wzajemną weryfikację; (3) budżetuj czas pętli — dobrze zaprojektowany harness daje mierzalny artefakt (np. config firewalla) w kilku–kilkunastu minutach; (4) gdy istnieje gotowy, dostrojony model domenowy (np. DeepResearch) — używaj go zamiast promptować model ogólny, bo specjalizacja bije skalę parametrów.

## Uwaga / Anty-wzorzec
Skalowanie wyłącznie liczby parametrów i 'inteligencji' modelu bez zaprojektowania środowiska, w którym agent może testować i zbierać feedback — model nie może się sam skorygować, jeśli nie ma sprzężenia z rzeczywistością ani zewnętrznego weryfikatora. Drugi anty-wzorzec: pojedynczy monoliczny agent zamiast orkiestracji wielu ról, co powoduje kumulację błędu i brak niezależnej walidacji wyniku.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Teza kontrowersyjna względem dominującego konsensusu 'scale is all you need' / 'bigger models win': autor twierdzi, że przewaga konkurencyjna przesuwa się z liczby parametrów na skalowanie systemu (ujednolicenie pętli prób i błędów w środowisku oraz współpracy wielu agentów). Do rozstrzygnięcia: czy przyrost możliwości modeli bazowych nie zredukuje z czasem znaczenia ręcznie projektowanego harnessu, oraz jak mierzyć 'System Scaling' obiektywnymi metrykami (czas do artefaktu, koszt tokenów, odsetek poprawnych konfiguracji) zamiast pojedynczych anegdotycznych sukcesów.

## Oryginalny cytat
> *"最后, 在这个架构加持下, 它仅用了10分钟左右就给我交付了针对攻击的防火墙配置. 这真的是 Agentic 系统工程的胜利了. 

未来的 AI 竞争, 不仅是卷模型参数量, 能把环境试错反馈和多 Agent 协同做成统一的系统 (System Scaling), 才是真正让AI在各种工程中落地的关键.

另外, 这个框架还开源了! 这里: https://t.co/n4F2ulrtEc
配套的 DeepResearch 模型也在这里: https://t.co/f8BzbXFh1n (模型之前也给大家测过, 是针对 DeepResearch 特调的, 性能相当不错)"*
