---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Tue Sep 15 07:47:29 +0000 2026"
źródło: "https://x.com/karminski3/status/2099767043155218568"
kategoria: "Benchmarkowanie i ewaluacja modeli LLM"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# reasoning_effort jako marketing i problem porównywalności benchmarków

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Tue Sep 15 07:47:29 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2099767043155218568)
- **Kluczowe pojęcia:** [[Harness|Benchmarkowanie modeli LLM]] [[Test-Time Compute i Reasoning Tokens|reasoning_effort]] [[Harness|Koszt obliczeń vs jakość]] [[Harness|Post-training]] [[Test-Time Compute i Reasoning Tokens|Ewaluacja modeli reasoning]] [[Harness|DeepSeek]]

---

## Kontekst i problem
Autor odpiera zarzut, że powinien testować DeepSeek na poziomie reasoning_effort=high, skoro inne modele testuje na max. Twierdzi, że w benchmarkach trzeba zachować porównywalny budżet rozumowania, a reasoning_effort to mechanizm vendorów przenoszący wybór compute-vs-accuracy oraz ryzyko kosztów na użytkownika. Wskazuje, że producenci raportują benchmarki na max, a jednocześnie sugerują 'sweet spot' na high, co prowadzi do błędnego wniosku, że high jest najlepsze.

## Rada inżynierska
W benchmarkach porównawczych ustawiaj ten sam poziom reasoning_effort/thinking budget dla wszystkich modeli, zgodnie z deklaracją producenta (często max), i raportuj osobno wynik oraz koszt/czas. Nie testuj wyłącznie high tylko dlatego, że dla jednego modelu wygląda dobrze. reasoning_effort traktuj jako parametr kosztowy i operacyjny, nie jako gwarancję jakości; dla najtrudniejszych zadań używaj max, jeśli tech report tak zaleca. Dąż do tego, by wyższy effort nie pogarszał jakości — jeśli pogarsza, to raczej problem post-trainingu niż niezmienna własność modelu.

## Uwaga / Anty-wzorzec
Nieuczciwe porównanie benchmarkowe: inne modele na max, DeepSeek na high. Ślepe założenie 'high = najlepsze', bo vendor nazywa high sweet spotem. Przenoszenie na użytkownika decyzji compute-vs-accuracy i ryzyka kosztów bez jasnych danych o billingu. Utożsamianie higher thinking effort z lepszą jakością, gdy post-training powoduje, że effort nie jest monotoniczny względem performance.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor podważa powszechne traktowanie reasoning_effort jako użytecznego mechanizmu kontroli jakości. Twierdzi, że to głównie marketing i przenoszenie kosztów na użytkownika; sprzeczne z narracją vendorów, że 'high' jest optymalnym sweet spotem. Do rozstrzygnięcia: czy wyższy reasoning effort powinien być monotonicznie lepszy, czy trade-off compute-performance jest nieunikniony.

## Oryginalny cytat
> *"问题在于我做的是 benchmark, 不是日常使用. 不能因其他模型都用max然后deepseek high 好单独用high测.

然后评论说应该用high测.

以及, reasoning_effort 在我看来是大模型厂商的营销手段. 把算力与精度的权衡交给了用户, 顺便把算力计费的风险也转移给了用户. 而且巧妙地进行掩饰: 宣称benchmark全是max跑出来的. 最后又说甜区(注意论文里称作cost–performance balance) 在high.

造成的结果就是, 有人认为high就是最好的.

我当然同意 thinking effort 不等价于 performance. 而且我认为之所以不等价是因为后训练拉了. 理想上应该追求让它等价.

但请注意, deepseek-v4-1-flash技术报告里给max评价为: best reserved for the most challenging tasks."*
