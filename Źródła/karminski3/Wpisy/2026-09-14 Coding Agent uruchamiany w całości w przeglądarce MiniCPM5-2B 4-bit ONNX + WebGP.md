---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 14 22:55:34 +0000 2026"
źródło: "https://x.com/karminski3/status/2099633181934907654"
kategoria: "Architektura agentów / Edge AI (WebGPU, modele端侧)"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Coding Agent uruchamiany w całości w przeglądarce: MiniCPM5-2B 4-bit ONNX + WebGPU bez Dockera i Node

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 14 22:55:34 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099633181934907654)
- **Kluczowe pojęcia:** [[Harness|WebGPU]] [[Harness|ONNX Runtime]] [[Harness|Kwantyzacja 4-bit]] [[Harness|Coding Agent]] [[Harness|Tool Calling]] [[Harness|MiniCPM]] [[Harness|Edge AI]] [[Harness|Self-healing UI]] [[Harness|Wirtualny terminal w agencie]]

---

## Kontekst i problem
Klasyczny deployment agenta kodującego wymaga Dockera/Node, kluczy API i dostępu do sieci — co jest problemem dla projektów wewnętrznych (intranet) i SaaS-ów odciętych od publicznego internetu. Projekt HuggingFace Space 'MiniCPM5-2B-WebGPU-Pi' pokazuje alternatywę: cały stack (framework agenta opakowany przez Pi + model MiniCPM5-2B w wersji 4-bit ONNX, <2 GB) działa w przeglądarce, udostępniając wirtualny terminal, edycję plików i tool_call bez żadnej infrastruktury serwerowej.

## Rada inżynierska
Uruchamiaj agenta i model w całości po stronie klienta (przeglądarka + WebGPU + skwantyzowany ONNX), gdy potrzebujesz: (1) dziedziczenia istniejącej sesji użytkownika (cookies, login) bez konfiguracji kluczy API, (2) pracy w sieciach zamkniętych / na wewnętrznych SaaS bez dostępu do internetu, (3) automatyzacji 'na żywo' w kontekście uwierzytelnionej aplikacji. Drugi wzorzec: plugin samo-naprawiający strony — nasłuchuj błędów w konsoli przeglądarki i generuj hot-patch w miejscu awarii bez przeładowania strony. Wydajność referencyjna: 25 tps na 3080 Ti dla MiniCPM5-2B 4-bit, przy zaskakująco stabilnym tool_callu jak na model 2B.

## Uwaga / Anty-wzorzec
Wydajność 25 tps pochodzi z desktopowego GPU (3080 Ti) — na słabszych klientach (laptopy bez dedykowanego GPU, urządzenia mobilne) throughput i latencja tool_callu będą znacznie gorsze, co może zniweczyć sens agenta interaktywnego. Dodatkowo podejście '白嫖登录态' (wykorzystanie cudzej/zalogowanej sesji i cookies do automatyzacji) jest ryzykowne prawnie i bezpieczeństwowo — może naruszać ToS platformy oraz otwierać wektor na wyciek poświadczeń; traktuj to wyłącznie jako technikę dla własnych, autoryzowanych środowisk. Nie zakładaj też, że stabilność tool_callu małego modelu utrzyma się przy dłuższych łańcuchach narzędzi i złożonych zadaniach.

## Oryginalny cytat
> *"看到个神奇的 huggingface Space项目, 思路很值得借鉴跟大家说下. Space 叫 MiniCPM5-2B-WebGPU-Pi, 不用起 Docker, 也不用装 Node 啥的, 打开网页就是一个带虚拟终端, 能进行文件编辑和 tool_call 的完整Coding Agent. 这玩意用 Pi 包了个 Coding Agent, 然后使用 MiniCPM5-2B 模型驱动. 神奇的地方就是, 这里用的是 MiniCPM5-2B 4bit ONNX 封装版本 (不到2G), 所以从框架到推理模型全都运行在了浏览器上. ... 我实测这玩意在我的3080Ti上能跑到25tps, 框架内部模拟了shell环境和提供了最基础的文件编辑tool_call. ... 另外 MiniCPM5-2B 的 tool_call 稳定性意外的不错, 大家对 2B 这种迷你模型跑 Agent 感兴趣吗?"*
