---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Thu Aug 27 08:39:49 +0000 2026"
źródło: "https://x.com/karminski3/status/2092894843429363871"
kategoria: "Architektura systemów agentowych / Inżynieria kontekstu"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Harness Scaling: skalowanie orkiestracji agentów i środowiska zamiast samych parametrów modelu

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Thu Aug 27 08:39:49 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2092894843429363871)
- **Konwersacja:** Odpowiedź w dyskusji (@karminski3)
- **Kluczowe pojęcia:** [[Harness|Harness Scaling]] [[Harness|Agentic Coordination Scaling]] [[Harness|Environment Scaling]] [[Harness|Agent Swarm]] [[Harness|Agent Team]] [[Harness|AgentOS]] [[Harness|Utrata uwagi w długim kontekście]] [[Harness|Halucynacje w dużym kontekście]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Asynchroniczne agenty]] [[Harness|SOC Automation]] [[Harness|ModSecurity]] [[Sandbox i Granice Bezpieczeństwa Agenta|Sandbox / izolacja kodu]] [[Firstmate i Agenci Wykonawczy]]

---

## Kontekst i problem
Zadanie analizy ~1,2 mln linii logów (ok. 260 MB) w celu wyłapania ataków i wygenerowania reguł blokujących (ModSecurity). Klasyczny, jednowątkowy system agentowy nie jest w stanie tego udźwignąć — pojedynczy wątek rozumowania prowadzi do utraty uwagi (attention loss) i halucynacji, a w konsekwencji do twardego błędu całego zadania. Apodex 1.1 rozwiązuje problem przez tzw. Harness Scaling, czyli skalowanie samego 'rusztowania' (frameworku, narzędzi, zespołu agentów), a nie tylko liczby parametrów modelu.

## Rada inżynierska
Rozdziel dwie osie skalowania: (1) 'inteligencję' modelu zwiększa się przez parametry, (2) 'zdolność do wykonania pracy' zwiększa się przez Harness Scaling — skalowanie frameworku, zestawu narzędzi (Agent Tools) oraz zespołu agentów (Agent Team / Swarm). W praktyce: (a) Agentic Coordination Scaling — rozbij zadanie na role jak w realnym zespole SOC (agent wywiadowczy czyści dziesiątki tysięcy logów i wyciąga złośliwe IP oraz cechy, agent reguł pisze na tej podstawie reguły ModSecurity), uruchamiaj je asynchronicznie i równolegle, tak aby agent reguł zaczynał pracę, gdy tylko wywiadowczy wypuści pierwszą partię wykrytych ataków; projektuj pipeline tak, aby nowe wymagania można było dodawać w locie bez przerywania trwających zadań. (b) Environment Scaling — nie wrzucaj surowych danych do kontekstu; pisz dedykowane skrypty, które ekstrahują tylko istotne zdarzenia (np. logi ataków), a wykonuj je w izolowanym runtime (AgentOS), dzięki czemu model może uruchamiać ryzykowny kod bez zagrożenia dla systemu hosta.

## Uwaga / Anty-wzorzec
Anty-wzorzec: wrzucenie całego wolumenu (~1,2 mln linii / 260 MB) bezpośrednio do kontekstu pojedynczego, jednowątkowego agenta. Skutki: eksplozja liczby tokenów, rozproszenie uwagi (attention dilution), halucynacje i błąd końcowy całego zadania. Drugi anty-wzorzec: poleganie wyłącznie na skalowaniu parametrów modelu ('więcej mózgu') bez skalowania harnessu — sam model nie przełoży się na przepustowość pracy.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor kontruje dominujący w branży nacisk na skalowanie liczby parametrów modelu ('scale is all you need' / bigger model = better agent). Twierdzi, że parametry podnoszą wyłącznie 'inteligencję', natomiast realną zdolność wykonawczą (throughput, niezawodność na dużych zadaniach) daje dopiero skalowanie harnessu — frameworku, narzędzi i zespołu agentów. Do rozstrzygnięcia: czy dla zadań analitycznych na dużych wolumenach danych inwestycja w architekturę agentową (orkiestracja + izolowane środowisko + ekstrakcja skryptowa) jest istotniejsza niż dobór mocniejszego modelu bazowego. Teza jest spójna z nurtem 'context engineering > raw model size', ale podważa intuicję, że wystarczy poczekać na kolejny, większy model.

## Oryginalny cytat
> *"这个任务最难的点就是, 如果是最传统的Agent系统, 就只能单线思考, 120万条日志(约260MB), 绝对会导致各种注意力丢失或者产生幻觉, 最后整个任务就直接报错.

这次 Apodex 1.1 版本就针对这个场景做了升级. 这里必须要给大家介绍一个概念: Harness Scaling

简单来讲, 光堆模型参数量只能提升模型的"智力", 而堆模型的脚手架(framework), 工具箱(Agent Tools)和团队(Agent Team/Swarm), 就能提升模型干活的能力.

Apodex 1.1 在两个地方发力了:

首先是 Agentic Coordination Scaling（智能体协同扩展）：
它的 Agent Team 像一个真正的 SOC 安全团队一样把任务拆了, 情报 Agent 去清洗几十万条日志提取恶意 IP 和特征, 规则 Agent 根据特征去写 ModSecurity 拦截规则. 注意这些是异步并行的, 速度非常快, 甚至情报 Agent 刚吐出第一批探测到的攻击日志, 规则 Agent 就已经开始写防火墙规则了. 而且如果要改需求, 可以随时在这个过程中添加, 不用担心影响正在跑的任务.

紧接着是 Environment Scaling（环境扩展）：
如果这120万条日志全都让AI去读取, token量肯定直接炸了, 所以有针对性的编写脚本去抽取攻击日志就是工作的主要内容了, 而这些日志全都是运行在 AgentOS 上的, 它是整个 Apodex 系统的运行时承载, 在这个上面模型可以运行各种风险代码而不用担心影响宿主系统."*
