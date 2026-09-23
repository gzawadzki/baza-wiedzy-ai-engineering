---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 21 00:09:21 +0000 2026"
źródło: "https://x.com/karminski3/status/2101826076762857867"
kategoria: "Bezpieczeństwo modeli / Ewaluacja / Benchmarking"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Test empiryczny: hipoteza 'jailbreak przez język hebrajski' obalona — spójność refusal rate między językami

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 21 00:09:21 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2101826076762857867)
- **Kluczowe pojęcia:** [[Harness|Refusal rate]] [[Harness|Safety alignment]] [[Harness|Jailbreak]] [[Harness|Low-resource languages jailbreak]] [[Harness|Gateway-level filtering]] [[Harness|Ewaluacja modeli LLM]] [[Sandbox i Granice Bezpieczeństwa Agenta|Benchmarking bezpieczeństwa]] [[Harness|Kontrola zmiennych w testach]]

---

## Kontekst i problem
Wokół X krążyła wiralowa teza, że język hebrajski pozwala obejść warstwy bezpieczeństwa (tzw. '破甲' — jailbreak) modeli LLM oraz odblokować konta na platformach. Autor zbudował framework ewaluacyjny oparty na publicznych korpusach z HuggingFace, przygotował równoległe zestawy promptów w języku angielskim, chińskim i hebrajskim (z zachowaniem zmiennej kontrolnej: wyłącznie zmiana języka, bez promptów jailbreakujących) i przetestował modele Fable-5.1 oraz DeepSeek-V4.1-Flash na parach pytań 'toksyczne' (powinny zostać odrzucone) i 'benign' (powinny zostać obsłużone). Celem było zweryfikowanie mitu o niskoresursowych językach jako wektorze obejścia alignmentu.

## Rada inżynierska
Traktuj język promptu jako zmienną wymagającą walidacji empirycznej, a nie założenia. Wyniki testu: refusal rate dla treści szkodliwych jest praktycznie niezależny od języka — Fable-5.1: EN 95.0%, ZH 94.4%, HE 95.1%; DeepSeek-V4.1-Flash: EN 100%, ZH 100%, HE 99.3%. Krytyczna obserwacja architektoniczna: 32–36% blokad pochodzi z warstwy gateway (przed modelem), a 54–60% to odmowa w ciele modelu — najgroźniejsze zapytania są zatrzymywane na gateway i nigdy nie docierają do modelu. Przy projektowaniu harnessów ewaluacyjnych rozdzielaj metryki 'blokada na gateway' od 'odmowa modelu', bo inaczej mierzysz mieszankę dwóch różnych warstw bezpieczeństwa. Mit z pracy z 2023 'Low-Resource Languages Jailbreak GPT-4' (Zulu, Scottish Gaelic, Hmong) jest w 2026 już nieaktualny dla dojrzałych modeli.

## Uwaga / Anty-wzorzec
Anty-wzorzec: przyjmowanie wiralowych twierdzeń o 'magicznych' wektorach jailbreaku (rzadki język, kodowanie, cudzysłowy) jako faktu bez kontrolowanej ewaluacji. Drugi anty-wzorzec: brak rozróżnienia warstwy gateway i warstwy modelu w pomiarach refusal rate — zawyża to lub zaniża skuteczność alignmentu i prowadzi do błędnych wniosków o 'działającym jailbreaku'. Trzeci: testowanie jailbreaku promptowego i jailbreaku językowego łącznie, bez izolacji zmiennej — uniemożliwia przypisanie efektu do konkretnego wektora.

## Oryginalny cytat
> *"刷X看到了个热帖... 然后我突发奇想, 该不会由于训练语料少或者神奇的原因, 这玩意也会某种程度上实现 Anthroipc 模型的破甲(审查/模型安全层绕过)? ... 测了一波后直接说结论, 没有这回事. 中文, 英文, 希伯来语的拒绝率没太大区别. 对于有害内容, Fable-5.1的拒绝率是英语 95.0%, 中文 94.4%, 希伯来语 95.1%. 其中被网关拦截大约 32–36%，然后模型正文拒绝回答大约 54–60%. 尤其是极其危险的题目, 基本都没到大模型, 直接网关就拦掉了. 而 DeepSeek-V4.1-Flash 甚至表现更好一些, 英语 100%, 中文 100%, 希伯来语 99.3%... 另外需要注意, 为了测试控制变量, 我只测试了语言对模型安全机制的影响, 并没有使用提示词进行越狱, 至于模型对各种破甲提示词的识别能力则又是另一个有趣的研究课题了."*
