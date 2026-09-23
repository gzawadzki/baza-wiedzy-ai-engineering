---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 14 22:55:34 +0000 2026"
źródło: "https://x.com/karminski3/status/2099633181934907654"
kategoria: "Architektura agentów / Edge AI / WebGPU"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Agent kodujący uruchamiany w całości w przeglądarce: MiniCPM5-2B 4-bit ONNX + WebGPU (framework Pi)

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 14 22:55:34 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099633181934907654)
- **Kluczowe pojęcia:** [[Harness|WebGPU]] [[Harness|ONNX Runtime]] [[Harness|Kwantyzacja 4-bit]] [[Harness|Coding Agent]] [[Harness|Tool Call]] [[Harness|MiniCPM5-2B]] [[Harness|Edge AI]] [[Harness|Inferencja w przeglądarce]] [[Harness|Framework Pi]] [[Harness|End-side Agent Benchmark]]

---

## Kontekst i problem
Problem: uruchomienie pełnego Coding Agenta (wirtualny terminal, edycja plików, tool_call) zwykle wymaga infrastruktury — Dockera, Node.js, backendu i kluczy API. Projekt MiniCPM5-2B-WebGPU-Pi na HuggingFace Space pokazuje alternatywę: cały stack — od frameworku agentowego (Pi) po model inferencyjny (MiniCPM5-2B w wersji 4-bit ONNX, poniżej 2 GB) — działa wyłącznie w przeglądarce, bez instalacji czegokolwiek poza otwarciem strony.

## Rada inżynierska
Reguła inżynierska: kwantyzacja modelu do 4-bit ONNX (<2 GB) pozwala zmieścić inferencję całkowicie w środowisku przeglądarki (WebGPU), co eliminuje potrzebę Dockera, Node.js, backendu i kluczy API. Dzięki temu agent dziedziczy naturalnie kontekst przeglądarki — stan zalogowania, Cookie i sesję użytkownika — co otwiera dwa praktyczne scenariusze: (1) automatyzacja wewnętrznych/niepublicznych projektów oraz SaaS-ów bez dostępu do sieci publicznej, bez konfiguracji API KEY i bez połączenia sieciowego; (2) wtyczka „self-healing

## Uwaga / Anty-wzorzec
Pułapka bezpieczeństwa: agent uruchamiany w kontekście przeglądarki dziedziczy Twoje Cookie i stan zalogowania — automatyczna manipulacja wewnętrznym SaaS-em czy panelem firmowym bez świadomej kontroli uprawnień to ryzyko wycieku danych i nieautoryzowanych operacji. Dodatkowo stabilność tool_call małych modeli (2B) jest „zaskakująco dobra

## Oryginalny cytat
> *"看到个神奇的 huggingface Space项目, 思路很值得借鉴跟大家说下. Space 叫 MiniCPM5-2B-WebGPU-Pi, 不用起 Docker, 也不用装 Node 啥的, 打开网页就是一个带虚拟终端, 能进行文件编辑和 tool_call 的完整Coding Agent. 这玩意用 Pi 包了个 Coding Agent, 然后使用 MiniCPM5-2B 模型驱动.

神奇的地方就是, 这里用的是 MiniCPM5-2B 4bit ONNX 封装版本 (不到2G), 所以从框架到推理模型全都运行在了浏览器上.

我玩了一会想出来的两个奇葩玩法脑洞:

可以白嫖登录态, 框架+模型直接运行在你的浏览器里, 天然带你的登录信息和 Cookie, 可能你会想, 现在是个网站都有 MCP / API KEY 了要这玩意干嘛. 如果你有内网私有项目呢? 甚至你打工用的SAAS不能访问公网呢? 想不想来个全自动操作? 甚至由于模型都是运行在浏览器上的, 所以不用配 API KEY 也不用联网就能让它接管.

另一个脑洞大开的是可以做一个网站自愈插件, 框架监听浏览器console报错, 网页哪儿炸了就可以现场打热补丁, 不用刷新页面网页就直接修好了.

我实测这玩意在我的3080Ti上能跑到25tps, 框架内部模拟了shell环境和提供了最基础的文件编辑tool_call. 感兴趣的同学可以顺着这个思路深挖一下, 另外 MiniCPM5-2B 的 tool_call 稳定性意外的不错, 大家对 2B 这种迷你模型跑 Agent 感兴趣吗? 可以留言跟我说, 人多我攒一局端侧小模型 Agent 横评."*
