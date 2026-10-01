---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Fri Aug 21 17:49:35 +0000 2026"
źródło: "https://x.com/karminski3/status/2090858868989706352"
kategoria: "Inżynieria kontekstu multimodalnego / Analiza wideo"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Dwupoziomowa strategia próbkowania klatek w analizie wideo przez modele multimodalne

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Fri Aug 21 17:49:35 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2090858868989706352)
- **Konwersacja:** Odpowiedź w dyskusji (@karminski3)
- **Kluczowe pojęcia:** [[Harness|Multimodal VLM]] [[Harness|image_url]] [[Prompt Architecture]] [[Harness|Adaptacyjne próbkowanie klatek]] [[Harness|Dwupoziomowa analiza wideo]] [[Context Compaction|Inżynieria kontekstu]] [[Harness|Analiza wideo]]

---

## Kontekst i problem
Problem: modele wizyjno-językowe (VLM) są niedokładne przy analizie wideo, gdy klatki są podawane bez struktury czasowej lub próbkowane w sposób jednorodny. Autor odpowiada na pytanie, jak przekazywać materiał wideo do modelu, aby uzyskać wiarygodną analizę scen i szybkich akcji.

## Rada inżynierska
Wideo należy dekomponować do sekwencji klatek JPEG/PNG i przekazywać je jako wiele pól `image_url` w kolejności chronologicznej — w promptcie trzeba jawnie zadeklarować współczynnik próbkowania (sampling rate) oraz oś czasu (time axis), aby model poprawnie mapował klatki na zdarzenia. Przy materiałach o dużej dynamice (np. nagrania z gier FPS) nie stosować jednorodnego próbkowania całego materiału — właściwym wzorcem jest dwupoziomowa strategia: (1) makro-przegląd całego wideo w ~1 fps dla zrozumienia kontekstu globalnego, oraz (2) okno zdarzeniowe o wysokiej częstotliwości klatek z przycięciem i powiększeniem centrum kadru (center crop/zoom) wokół wykrytych momentów kluczowych. Takie podejście znacząco poprawia precyzję rozpoznawania szybkich akcji.

## Uwaga / Anty-wzorzec
Powszechny błąd: jednorodne (liniowe) próbkowanie całego wideo ze stałym interwałem. Skutkuje to albo utratą krytycznych klatek w momentach szybkich zdarzeń, albo eksplozją liczby tokenów wizyjnych w obszarach bez informacji — obniżając trafność i podnosząc koszt.

## Oryginalny cytat
> *"把视频抽成 JPEG/PNG, 按时间顺序作为多个 `image_url` 传入, 并在 prompt 里写明采样率和时间轴. 这样分析会更准确. 我使用了一个猫和老鼠的片段进行分析, 这样做模型识别很准确. 另外, 我还用了一段 CS2 录像来验证分析快速动作时的最佳方案, 结论是不要匀速抽全片, 用「宏观 1fps 全图 + 事件窗口高帧率中心放大」两级采样。效果会更好. 详细教程和POV开源在这里: https://t.co/DaeLlbTySr"*
