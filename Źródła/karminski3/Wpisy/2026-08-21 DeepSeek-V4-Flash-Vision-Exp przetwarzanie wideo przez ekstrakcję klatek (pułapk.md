---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Fri Aug 21 17:49:34 +0000 2026"
źródło: "https://x.com/karminski3/status/2090858863679750280"
kategoria: "Modele multimodalne / inżynieria danych wejściowych (wideo)"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# DeepSeek-V4-Flash-Vision-Exp: przetwarzanie wideo przez ekstrakcję klatek (pułapka GIF = tylko pierwsza klatka)

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Fri Aug 21 17:49:34 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2090858863679750280)
- **Kluczowe pojęcia:** [[Harness|Modele multimodalne]] [[Harness|Ekstrakcja klatek (frame sampling)]] [[Harness|GIF first-frame limitation]] [[Harness|DeepSeek-V4-Flash-Vision-Exp]] [[Harness|Wideo jako wejście modelu]] [[Harness|ASR jako uzupełnienie modalności]] [[Harness|Budżet tokenów wizyjnych]]

---

## Kontekst i problem
Autor opisuje świeżo wydany model deepseek-v4-flash-vision-exp — pierwszy multimodalny („duży”) model DeepSeeka na poziomie możliwości v4-flash. Mimo że model „już nie jest ślepy”, nadal nie przyjmuje audio, a oficjalna strona i API nie wspierają wejścia wideo. Problem inżynierski: jak w praktyce podać materiał wideo do modelu, który obsługuje wyłącznie obrazy. Autor podaje obejście i ostrzega przed naiwnym podejściem (konwersja do GIF). Wpis zapowiada też best practices dla ekstrakcji klatek, ale w zacytowanej treści nie podaje ich jeszcze w rozwiniętej formie.

## Rada inżynierska
Gdy model multimodalny nie ma natywnego wejścia wideo, nie próbuj oszukiwać go formatem animowanym — zamiast tego wykonaj deterministyczną ekstrakcję klatek (frame sampling) i podaj klatki jako sekwencję niezależnych obrazów, kontrolując gęstość próbkowania, rozdzielczość i budżet tokenów wizyjnych. Dla modelu obsługującego tylko pojedyncze obrazy traktuj wideo jako batch obrazów + osobny etap ASR dla ścieżki dźwiękowej (model jest „głuchy”, więc audio trzeba transkrybować zewnętrznie i doklejać jako kontekst tekstowy).

## Uwaga / Anty-wzorzec
Konwersja wideo → GIF w celu „przemycenia” wideo do modelu nie działa: mimo że model formalnie akceptuje GIF, rozpoznaje wyłącznie jego pierwszą klatkę (autor zweryfikował to eksperymentalnie kodem). Efekt to cicha utrata całego materiału poza pierwszym kadrem — model odpowiada pewnie, ale na podstawie szczątkowej informacji. Drugi anty-wzorzec: zakładanie, że multimodalność oznacza pełną percepcję — brak wejścia audio powoduje, że treść mówiona jest niewidoczna bez dodatkowego pipeline'u ASR.

## Oryginalny cytat
> *""给大家写了个 deepseek-v4-flash-vision-exp 输入视频教程

deepseek 最近真的是高产, 刚刚又发了 deepseek-v4-flash-vision-exp, 首个多模态【大】模型. 而且是 v4-flash 能力级别的. 但是! 虽然不是瞎子了, 但是还是听力有问题, 不支持音频输入. 所以默认 deepseek 官网和API都不支持视频输入, 于是给大家写了个小教程, 如何使用这个模型处理视频.

简单来讲, 方法就是直接把视频抽帧. 而且需要注意, 虽然模型支持gif输入, 但是它只识别 gif 的第一帧(我写代码验证了). 所以把视频转换为gif是行不通的.

抽帧的最佳实践也给大家:

#deepseekv4flashvisionexp #deepseek多模态 #deepseek多模态模型""*
