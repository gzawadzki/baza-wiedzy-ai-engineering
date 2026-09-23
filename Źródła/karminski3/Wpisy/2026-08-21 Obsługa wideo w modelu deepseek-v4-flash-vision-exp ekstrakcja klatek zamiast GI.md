---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Fri Aug 21 17:49:34 +0000 2026"
źródło: "https://x.com/karminski3/status/2090858863679750280"
kategoria: "Multimodalność / Obserwacje zachowania modeli"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Obsługa wideo w modelu deepseek-v4-flash-vision-exp: ekstrakcja klatek zamiast GIF-a

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Fri Aug 21 17:49:34 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2090858863679750280)
- **Kluczowe pojęcia:** [[Harness|DeepSeek V4]] [[Harness|Multimodalność]] [[Harness|Ekstrakcja klatek wideo]] [[Harness|GIF jako wejście modelu]] [[Harness|Ograniczenia modeli wizyjnych]] [[Harness|Harness multimodalny]]

---

## Kontekst i problem
DeepSeek wypuścił deepseek-v4-flash-vision-exp — pierwszy multimodalny (duży) model tej rodziny, o poziomie zdolności odpowiadającym v4-flash. Model przyjmuje obrazy, ale nie ma wejścia audio, a oficjalna strona i API DeepSeek nie udostępniają natywnego wejścia wideo. Autor opisuje obejście pozwalające przetwarzać wideo tym modelem: ręczną ekstrakcję klatek (frame extraction) po stronie klienta i podawanie ich jako sekwencji obrazów.

## Rada inżynierska
Aby przetwarzać wideo modelem bez natywnego wejścia wideo, wykonuj ekstrakcję klatek po stronie aplikacji i wysyłaj je jako osobne obrazy — to jedyna niezawodna ścieżka. Nie używaj konwersji wideo do GIF-a jako skrótu: mimo że model formalnie akceptuje wejście GIF, faktycznie odczytuje wyłącznie pierwszą klatkę (autor potwierdził to eksperymentalnie w kodzie), więc cała dynamika czasowa materiału zostaje bezpowrotnie utracona. Przy projektowaniu harnessu multimodalnego zakładaj rozdzielenie kanałów: obraz/wideo obsługiwane, audio nieobsługiwane — nie planuj pipeline'ów zakładających rozumienie ścieżki dźwiękowej.

## Uwaga / Anty-wzorzec
Anty-wzorzec: traktowanie obsługi formatu pliku jako równoznacznej z obsługą jego zawartości czasowej. Deklarowana obsługa GIF-a nie oznacza przetwarzania animacji — model bierze tylko pierwszą klatkę, co daje ciche, trudne do wykrycia błędy (model "widzi" statyczny obraz i halucynuje opis zdarzeń). Drugi anty-wzorzec: zakładanie, że nowy model multimodalny automatycznie obsługuje wideo i audio tylko dlatego, że obsługuje obrazy — zawsze weryfikuj realne wejścia na poziomie API i eksperymentem, zanim zbudujesz na tym architekturę.

## Oryginalny cytat
> *"给大家写了个 deepseek-v4-flash-vision-exp 输入视频教程 — deepseek 最近真的是高产, 刚刚又发了 deepseek-v4-flash-vision-exp, 首个多模态【大】模型. 而且是 v4-flash 能力级别的. 但是! 虽然不是瞎子了, 但是还是听力有问题, 不支持音频输入. 所以默认 deepseek 官网和API都不支持视频输入, 于是给大家写了个小教程, 如何使用这个模型处理视频. 简单来讲, 方法就是直接把视频抽帧. 而且需要注意, 虽然模型支持gif输入, 但是它只识别 gif 的第一帧(我写代码验证了). 所以把视频转换为gif是行不通的."*
