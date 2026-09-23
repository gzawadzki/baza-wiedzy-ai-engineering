---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 14 07:14:23 +0000 2026"
źródło: "https://x.com/karminski3/status/2099396323942547519"
kategoria: "Parametry inferencji / inżynieria rozumowania (reasoning effort, thinking budget)"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Reasoning effort (thinking budget) realnie wpływa na wyniki modelu — dowody z DeepSeek-R1-Zero

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 14 07:14:23 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099396323942547519)
- **Kluczowe pojęcia:** [[Test-Time Compute i Reasoning Tokens|Reasoning Effort]] [[Harness|Thinking Budget]] [[Harness|Chain-of-Thought]] [[Harness|DeepSeek-R1-Zero]] [[Harness|Zero-SFT RL]] [[Test-Time Compute i Reasoning Tokens|Test-time Compute]] [[Harness|AIME24 Benchmark]] [[Harness|Parametry Inferencji]] [[Harness|Benchmarking Modeli]]

---

## Kontekst i problem
Spór wokół testowania modelu deepseek-v4.1-flash: autor uruchomił go z ustawieniem 'max' (maksymalna intensywność rozumowania), a komentujący twierdzili, że powinien użyć 'high' oraz że przełącznik intensywności myślenia nie ma związku z wydajnością. Autor odpiera te zarzuty, powołując się na ubiegłoroczną pracę DeepSeek-R1-Zero, która empirycznie wykazała zależność między długością rozumowania a jakością wyników.

## Rada inżynierska
Traktuj parametr reasoning effort / thinking budget jako realny czynnik wydajności, a nie kosmetyczny przełącznik. Praca DeepSeek-R1-Zero pokazała, że przy RL bez SFT (Zero-SFT RL) i bez dodawania jakiejkolwiek nowej wiedzy sama rosnąca długość rozumowania (chain-of-thought) podniosła wynik AIME24 z ~15% do ~71%. Zasada inżynierska: przed porównywaniem modeli lub wyciąganiem wniosków o ich możliwościach zawsze raportuj i normalizuj poziom reasoning effort — różne ustawienia (high vs max) dają nieporównywalne wyniki, a niedoszacowanie budżetu rozumowania prowadzi do fałszywie niskich ocen modelu.

## Uwaga / Anty-wzorzec
Anty-wzorzec: bagatelizowanie przełącznika intensywności rozumowania jako 'tylko kosmetyki bez wpływu na wydajność' oraz krytykowanie cudzych testów bez znajomości literatury. Prowadzi to do błędnych benchmarków, zaniżonych ocen modeli i sporów opartych na opiniach zamiast na danych. Autor porównuje to do kupienia Ferrari i radzenia jeździć na pierwszym biegu zamiast drugiego.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor wchodzi w spór z powszechną (jego zdaniem błędną) opinią części społeczności DeepSeek, że przełącznik思考强度 (thinking strength) jest niezależny od wydajności i że 'high' jest lepsze niż 'max'. Teza autora: wyższa intensywność rozumowania = wyższa zdolność modelu, co potwierdza praca DeepSeek-R1-Zero. Do rozstrzygnięcia: czy na poziomie 'max' występuje nasycenie (saturation) lub degradacja jakości przy zbyt długim CoT, oraz czy zalecenie 'high' wynika z realnych ograniczeń (latency, koszt, ryzyko over-thinkingu) czy z nieporozumienia — brak tu twardych danych, jedynie argumentacja przez odwołanie do paperu.

## Oryginalny cytat
> *""DS民科怎么这么多, 我测完了 deepseek-v4.1-flash, 开 max, 然后评论跟我说应该开high, 不应该开max. 〇的我买法拉利然后你跟我说挂一档比挂二挡快是吧? 然后跟我说这只是思考强度开关, 跟性能没关系. 干你〇怎么就没关系..... 去年 deepseek 自家发的 DeepSeek-R1-Zero 论文怎么都忘了: https://t.co/FICrqgGzb0 就这个论文证明了思考强度越强模型能力越强的. 论文里Zero-SFT RL了一波, 没有增加任何新知识, 随着思考长度增加, AIME24 跑分就从 15% 魔法般的飙到了 71%. 然后震撼业界的雷霆大思考就如同雨后春笋般普及了..... 劝D小鬼对线前看看论文, 大水冲了自家龙王庙了.""*
