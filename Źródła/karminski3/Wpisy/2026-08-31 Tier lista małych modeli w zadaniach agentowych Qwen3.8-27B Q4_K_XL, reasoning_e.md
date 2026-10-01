---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Aug 31 08:26:49 +0000 2026"
źródło: "https://x.com/karminski3/status/2094341123124985991"
kategoria: "Benchmarking i ewaluacja modeli / Agenci lokalni"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Tier lista małych modeli w zadaniach agentowych: Qwen3.8-27B Q4_K_XL, reasoning_effort a wybór runtime (llama.cpp vs MLX)

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Aug 31 08:26:49 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2094341123124985991)
- **Kluczowe pojęcia:** [[Test-Time Compute i Reasoning Tokens|reasoning_effort]] [[Harness|Qwen3]] [[Harness|llama.cpp]] [[Harness|MLX]] [[Architektura KV Cache i Rozumowanie Latentne|MTP (multi-token prediction)]] [[Harness|Kwantyzacja Q4_K_XL]] [[Harness|Tier lista modeli agentowych]] [[Harness|Single-GPU benchmarking]] [[Harness|H100 NVL]] [[Harness|Harness agentowy]] [[Firstmate i Agenci Wykonawczy]]

---

## Kontekst i problem
Autor publikuje ranking („drabinkę/tier listę”) małych modeli LLM testowanych pod kątem zdolności agentowych. Celem jest odpowiedź na pytanie, który mały model lokalny realnie nadaje się do pracy w harnessie agentowym, oraz jak dobrać runtime i poziom reasoning effort zależnie od zadania (agent vs generowanie kodu). Testy prowadzone były jednolicie na pojedynczej karcie H100 NVL z najnowszą wersją llama.cpp, co czyni wyniki porównywalnymi między modelami.

## Rada inżynierska
1) Z perspektywy testów autora najbardziej opłacalnym modelem do zastosowań agentowych jest Qwen3.8-27B w kwantyzacji UD-Q4_K_XL. 2) reasoning_effort należy dobierać zadaniowo: dla pętli agentowej (tool-calling, planowanie, orkiestracja) ustawiaj LOW — wysoki budżet rozumowania zwiększa latencję i zużycie tokenów bez proporcjonalnego zysku; dla generowania kodu ustawiaj MEDIUM/HIGH, bo tam dodatkowe rozumowanie przekłada się na jakość artefaktu. 3) Utrzymuj jednorodny stack pomiarowy (ta sama karta, ten sam runtime i jego wersja, ta sama kwantyzacja) — inaczej porównanie modeli jest bezwartościowe. 4) Na macOS preferuj MLX zamiast llama.cpp: w testach autora MLX z włączonym MTP (multi-token prediction) wypada szybciej niż llama.cpp z MTP na tym samym sprzęcie. 5) Uwaga na nazewnictwo/rewizje modeli — wersja kwantyzacji (UD-Q4_K_XL) jest częścią konfiguracji wynikowej i musi być raportowana razem z wynikiem.

## Uwaga / Anty-wzorzec
Anty-wzorzec: stosowanie jednego, globalnego ustawienia reasoning_effort do wszystkich zadań — wysoki effort w pętli agentowej marnuje budżet tokenów i podnosi latencję, a niski effort przy generowaniu kodu obniża jakość. Druga pułapka: przenoszenie wniosków wydajnościowych między runtime'ami i platformami — wyniki z H100 NVL + llama.cpp nie są transferowalne wprost na Apple Silicon; na Macu domyślny wybór llama.cpp może być wolniejszy niż MLX z MTP. Trzecia pułapka: porównywanie modeli w różnych kwantyzacjach lub różnych wersjach runtime'u i wyciąganie wniosków o samym modelu.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Sporne wobec typowego konsensusu branżowego: (a) autor zaleca MLX (z MTP) zamiast llama.cpp na macOS, podczas gdy domyślną rekomendacją w społeczności lokalnych LLM jest llama.cpp jako uniwersalny runtime — wymaga weryfikacji na konkretnym sprzęcie Apple Silicon; (b) autor twierdzi, że w zadaniach agentowych najlepszy jest NISKI reasoning_effort, co stoi w sprzeczności z popularną praktyką maksymalizowania rozumowania w agentach („thinking longer = lepsze planowanie”) — do rozstrzygnięcia empirycznie na własnym harnessie, z pomiarem sukcesu zadania, latencji i zużycia tokenów; (c) rekomendacja konkretnej kwantyzacji UD-Q4_K_XL jako „najbardziej opłacalnej” jest wynikiem pojedynczego setupu (1× H100 NVL + llama.cpp) i nie musi się przenosić na inne backendy.

## Oryginalny cytat
> *"小模型 Agent 能力测试的天梯在这里~ (希望图不要被压得太狠....)

目前来看最值得使用是我测试的 Qwen3.8-27B-UD-Q4_K_XL 版本,  Agent 用使用 reasoning_effort = low, 然后写代码开到 medium / high.

另外文中是统一使用单卡 H100 NVL+llama.cpp 最新版本测试的. 如果是Mac用户还是建议优先使用MLX, 实测 MLX 开 MTP 会比 llama.cpp 放在 Mac 上开MTP要快一些.

最后老铁们还想看什么模型的评测欢迎留言~ 我赶紧肝哈哈"*
