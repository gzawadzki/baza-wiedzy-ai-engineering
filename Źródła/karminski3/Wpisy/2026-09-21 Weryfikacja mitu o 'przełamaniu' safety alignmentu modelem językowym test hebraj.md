---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 21 00:09:21 +0000 2026"
źródło: "https://x.com/karminski3/status/2101826076762857867"
kategoria: "Bezpieczeństwo modeli / Red Teaming / Alignment"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Weryfikacja mitu o 'przełamaniu' safety alignmentu modelem językowym: test hebrajskiego na Fable-5.1 i DeepSeek-V4.1-Flash

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 21 00:09:21 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2101826076762857867)
- **Kluczowe pojęcia:** [[Harness|Jailbreak]] [[Harness|Safety Alignment]] [[Harness|Red Teaming]] [[Harness|Low-Resource Languages]] [[Harness|Gateway Guardrails]] [[Harness|Refusal Rate]] [[Harness|Control Variables in LLM Testing]] [[Eval Set z realnych sesji|Multi-language Evaluation]] [[CI Check Bypass Confirmation]]

---

## Kontekst i problem
Na X rozprzestrzenił się viralowy mit, że podania (appeals) w języku hebrajskim do platformy X skutkują natychmiastowym odblokowaniem konta, a następnie rozszerzono go na tezę, że hebrajski może bypassować warstwę bezpieczeństwa/cenzury modeli Anthropic. Autor postanowił zweryfikować empirycznie hipotezę 'przełamania pancerza' (破甲 = jailbreak / obejście safety layer) przy użyciu języka hebrajskiego. Zbudował framework testowy oparty na publicznych korpusach z HuggingFace, przygotował równoległe wersje treści w EN/ZH/HE i porównał modele: Fable-5.1 (testowany) oraz DeepSeek-V4.1-Flash (grupa kontrolna).

## Rada inżynierska
Metodologia testu: (1) Ten sam zestaw promptów w trzech językach (EN/ZH/HE) = kontrola zmiennej niezależnej; (2) Podział treści na 'wartości prawdziwe' (should-refuse: prośby o instrukcje do szkodliwych działań) oraz 'wartości fałszywe' (should-answer: neutralne pytania o absurdalnych założeniach) jako kontrola fałszywie dodatnich; (3) Pomiar dwóch niezależnych warstw obrony: gateway interception (blokada przed dojściem do LLM) oraz model-level refusal. Wyniki: brak istotnej różnicy w refusal rate między językami — Fable-5.1: EN 95,0%, ZH 94,4%, HE 95,1%; DeepSeek-V4.1-Flash: EN 100%, ZH 100%, HE 99,3%. Rozkład: ~32–36% blokad na gateway, ~54–60% odmów w treści modelu. Wniosek: współczesny safety alignment jest odporny na różnicę języka, a hebrajski nie jest już językiem 'niskim zasobem' w kontekście ataków.

## Uwaga / Anty-wzorzec
Anty-wzorce: (1) Wiara w viralowe mity o 'magicznych' językach/promptach bez własnych pomiarów — rozprzestrzenianie się niezweryfikowanych tez o jailbreakach; (2) Mylenie wniosków z 2023 (paper 'Low-Resource Languages Jailbreak GPT-4': zulu, szkocki gaelicki, hmong omijały safety) ze stanem obecnym — te luki zostały w większości załatane; (3) Zakładanie, że test języka == test prompt jailbreak — autor explicite zaznacza, że NIE testował promptów jailbreakowych, więc odporność na język ≠ odporność na zaawansowane techniki promptowe; (4) Pominięcie warstwy gateway w analizie — najgroźniejsze treści są blokowane zanim dotrą do modelu, co zafałszowałoby statystyki, gdyby mierzyć tylko refusal modelu.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor podważa viralowy konsensus na X, jakoby język hebrajski umożliwiał bypass safety alignmentu modeli (m.in. Anthropic) oraz obala (jako nieaktualne) ustalenia paperu 'Low-Resource Languages Jailbreak GPT-4' (2023) dotyczące obejść przez języki niskiego zasobu (zulu, gaelicki szkocki, hmong). Teza do rozstrzygnięcia: czy luka językowa jailbreak rzeczywiście została domknięta, czy wyniki są specyficzne dla testowanej klasy treści (autor nie testował promptów jailbreakowych ani zaawansowanych technik promptowych, co pozostawia otwarte pytanie o odporność na ataki hybrydowe: język + prompt).

## Oryginalny cytat
> *"对于有害内容, Fable-5.1的拒绝率是英语 95.0%, 中文 94.4%, 希伯来语 95.1%. 其中被网关拦截大约 32–36%，然后模型正文拒绝回答大约 54–60%. 尤其是极其危险的题目, 基本都没到大模型, 直接网关就拦掉了. 而 DeepSeek-V4.1-Flash 甚至表现更好一些, 英语 100%, 中文 100%, 希伯来语 99.3%. 从测试结论来看, 目前大模型的安全对齐已经做得很好了... 另外需要注意, 为了测试控制变量, 我只测试了语言对模型安全机制的影响, 并没有使用提示词进行越狱, 至于模型对各种破甲提示词的识别能力则又是另一个有趣的研究课题了."*
