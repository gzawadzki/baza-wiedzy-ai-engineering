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

# Harness Scaling: skalowanie rusztowania agentowego zamiast parametrów modelu (Apodex 1.1)

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Thu Aug 27 08:39:49 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2092894843429363871)
- **Konwersacja:** Odpowiedź w dyskusji (@karminski3)
- **Kluczowe pojęcia:** [[Harness|Harness Scaling]] [[Harness|Agentic Coordination Scaling]] [[Harness|Environment Scaling]] [[Harness|Agent Team]] [[Harness|Agent Swarm]] [[Harness|AgentOS]] [[Harness|Apodex]] [[Harness|Utrata uwagi / Attention Loss]] [[Harness|Halucynacje]] [[Context Compaction|Eksplozja tokenów kontekstu]] [[Harness|ModSecurity]] [[Harness|Zespół SOC]] [[Harness|Szkielet agentowy / Agent Framework]] [[Sandbox i Granice Bezpieczeństwa Agenta|Izolacja piaskownicy wykonawczej]]

---

## Kontekst i problem
Zadanie analizy 1,2 mln linii logów (~260 MB) w celu wykrycia ataków i wygenerowania reguł ModSecurity. Klasyczny, jednowątkowy system agentowy (single-chain) nie jest w stanie tego przetworzyć: przeciążenie kontekstu prowadzi do utraty uwagi (attention loss), halucynacji i finalnie do błędu całego zadania. Apodex 1.1 rozwiązuje to przez rozdzielenie skalowania 'inteligencji' (parametry modelu) od skalowania 'zdolności wykonawczej' (framework, narzędzia, zespół agentów).

## Rada inżynierska
Wprowadź pojęcie Harness Scaling: samo zwiększanie liczby parametrów modelu podnosi jedynie jego 'inteligencję', natomiast skalowanie rusztowania (framework), zestawu narzędzi (Agent Tools) oraz zespołu agentów (Agent Team / Swarm) podnosi rzeczywistą zdolność wykonawczą systemu. Realizuj to w dwóch wymiarach: (1) Agentic Coordination Scaling – dekompozycja zadania jak w realnym zespole SOC, gdzie agent analityczny (Intel) czyści setki tysięcy logów i ekstrahuje złośliwe IP oraz sygnatury, a agent regułowy (Rules) na podstawie tych sygnatur pisze reguły blokujące ModSecurity; agenci działają asynchronicznie i równolegle, więc agent regułowy zaczyna pisać reguły, gdy tylko pierwsza partia logów ataku zostanie wyemitowana. (2) Environment Scaling – nie wrzucaj surowych 260 MB logów do kontekstu modelu (eksplozja tokenów), lecz pisz dedykowane skrypty ekstrahujące wyłącznie istotne logi ataków; uruchamiaj je w izolowanym środowisku wykonawczym (AgentOS) jako runtime całego systemu, dzięki czemu model może wykonywać ryzykowny kod bez wpływu na system hosta. Projektuj pętlę agentową tak, aby wymagania można było dodawać w trakcie działania bez przerywania już uruchomionych zadań (hot-reload wymagań).

## Uwaga / Anty-wzorzec
Anty-wzorzec: próba wczytania całego, dużego zbioru danych (setki MB logów) bezpośrednio do kontekstu LLM – gwarantowana eksplozja zużycia tokenów, utrata uwagi, halucynacje i twardy błąd zadania. Drugi anty-wzorzec: monolit jednowątkowego łańcucha agentowego (single-line thinking) dla zadań wymagających równoległej specjalizacji; brak izolacji wykonawczej dla kodu generowanego przez model zagraża systemowi hosta.

## Oryginalny cytat
> *"这个任务最难的点就是, 如果是最传统的Agent系统, 就只能单线思考, 120万条日志(约260MB), 绝对会导致各种注意力丢失或者产生幻觉, 最后整个任务就直接报错.

这次  Apodex 1.1 版本就针对这个场景做了升级. 这里必须要给大家介绍一个概念: Harness Scaling

简单来讲, 光堆模型参数量只能提升模型的"智力", 而堆模型的脚手架(framework), 工具箱(Agent Tools)和团队(Agent Team/Swarm), 就能提升模型干活的能力.

Apodex 1.1 在两个地方发力了:

首先是 Agentic Coordination Scaling（智能体协同扩展）：
它的 Agent Team 像一个真正的 SOC 安全团队一样把任务拆了, 情报 Agent 去清洗几十万条日志提取恶意 IP 和特征, 规则 Agent 根据特征去写 ModSecurity 拦截规则. 注意这些是异步并行的, 速度非常快, 甚至情报 Agent 刚吐出第一批探测到的攻击日志, 规则 Agent 就已经开始写防火墙规则了. 而且如果要改需求, 可以随时在这个过程中添加, 不用担心影响正在跑的任务.

紧接着是 Environment Scaling（环境扩展）：
如果这120万条日志全都让AI去读取, token量肯定直接炸了, 所以有针对性的编写脚本去抽取攻击日志就是工作的主要内容了, 而这些日志全都是运行在 AgentOS 上的, 它是整个 Apodex 系统的运行时承载, 在这个上面模型可以运行各种风险代码而不用担心影响宿主系统."*
