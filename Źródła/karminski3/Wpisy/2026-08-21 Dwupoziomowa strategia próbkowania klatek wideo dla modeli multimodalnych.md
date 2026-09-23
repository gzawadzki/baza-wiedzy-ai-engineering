---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Fri Aug 21 17:49:35 +0000 2026"
źródło: "https://x.com/karminski3/status/2090858868989706352"
kategoria: "Inżynieria kontekstu / analiza wideo multimodalna"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Dwupoziomowa strategia próbkowania klatek wideo dla modeli multimodalnych

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Fri Aug 21 17:49:35 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2090858868989706352)
- **Konwersacja:** Odpowiedź w dyskusji (@karminski3)
- **Kluczowe pojęcia:** [[Harness|Analiza wideo przez VLM]] [[Prompt Architecture|Multimodalny prompt]] [[Harness|image_url w kontekście multimodalnym]] [[Harness|Dwupoziomowe próbkowanie klatek]] [[Context Compaction|Inżynieria kontekstu wizualnego]] [[Harness|Center crop przy analizie akcji]]

---

## Kontekst i problem
Problem: analiza wideo przez modele multimodalne (VLM) — jak podawać materiał wizualny, żeby model poprawnie rozpoznawał zarówno makro-kontekst sceny, jak i szybkie, drobne akcje (np. ruchy w CS2). Autor testował dwa przypadki: fragment 'Tom i Jerry' (rozpoznawanie obiektów/scen) oraz nagranie CS2 (szybka dynamika).

## Rada inżynierska
Konwersję wideo na analizę multimodalną realizuj przez wyekstrahowanie klatek jako JPEG/PNG i podanie ich jako wielu wpisów `image_url` w kolejności chronologicznej. W prompcie ZAWSZE jawnie deklaruj sampling rate oraz osi czasu (timeline), dzięki czemu model poprawnie mapuje klatki na zdarzenia. Dla materiałów z dynamiczną akcją nie stosuj jednorodnego (uniform) próbkowania całego wideo. Zamiast tego użyj dwupoziomowego schematu: (1) faza makro — 1 fps na pełnej rozdzielczości/pełnym kadrze dla globalnego kontekstu sceny, (2) faza zdarzeniowa — okna wokół interesujących zdarzeń próbkowane z wysokim fps i z przycięciem/zoomem na centrum kadru (center crop). Takie połączenie daje lepszą rozpoznawalność szybkich akcji niż równomierny pełny przebieg.

## Uwaga / Anty-wzorzec
Anty-wzorzec: jednorodne (uniform) próbkowanie całego wideo ze stałą, niską częstotliwością przy analizie szybkich akcji — gubi kluczowe klatki w oknach zdarzeń i prowadzi do błędnej interpretacji dynamiki. Dodatkowo: pomijanie w prompcie informacji o sampling rate i osi czasu zmusza model do zgadywania tempa zdarzeń, co psuje spójność wnioskowania.

## Oryginalny cytat
> *"把视频抽成 JPEG/PNG, 按时间顺序作为多个 `image_url` 传入, 并在 prompt 里写明采样率和时间轴. 这样分析会更准确. 我使用了一个猫和老鼠的片段进行分析, 这样做模型识别很准确. 另外, 我还用了一段 CS2 录像来验证分析快速动作时的最佳方案, 结论是不要匀速抽全片, 用「宏观 1fps 全图 + 事件窗口高帧率中心放大」两级采样。效果会更好. 详细教程和POV开源在这里: https://t.co/DaeLlbTySr"*
