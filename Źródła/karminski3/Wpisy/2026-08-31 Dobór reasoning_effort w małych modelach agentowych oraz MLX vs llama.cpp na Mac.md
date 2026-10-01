---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Aug 31 08:26:49 +0000 2026"
źródło: "https://x.com/karminski3/status/2094341123124985991"
kategoria: "Benchmarking modeli / Agenci / Inference runtime"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Dobór reasoning_effort w małych modelach agentowych oraz MLX vs llama.cpp na Macu

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Aug 31 08:26:49 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2094341123124985991)
- **Kluczowe pojęcia:** [[Test-Time Compute i Reasoning Tokens|reasoning_effort]] [[Harness|llama.cpp]] [[Harness|MLX]] [[Architektura KV Cache i Rozumowanie Latentne|MTP]] [[Harness|Kwantyzacja UD-Q4_K_XL]] [[Harness|Agent]] [[Harness|H100 NVL]] [[Harness|Benchmark modeli LLM]]

---

## Kontekst i problem
Autor publikuje drabinkę (ladder) wyników testów zdolności agentowych małych modeli LLM. Problem, który rozwiązuje: jak dobrać model, kwantyzację i runtime dla lokalnego agenta kodującego, oraz jak ustawić reasoning_effort zależnie od zadania, aby nie przepalać budżetu tokenów w pętli agentowej.

## Rada inżynierska
1) Rozdzielaj reasoning_effort od typu zadania: w pętli agentowej (tool-calling, planowanie, iteracyjne wywołania) ustawiaj reasoning_effort = low, a dopiero przy generowaniu kodu podnoś do medium/high. Wysoki effort w każdej iteracji agenta mnoży koszt i latencję bez proporcjonalnego zysku. 2) Testowany model Qwen3-27B w kwantyzacji UD-Q4_K_XL (Unsloth Dynamic) okazał się najlepszym kompromisem jakości do rozmiaru dla zadań agentowych. 3) Utrzymuj jednorodne środowisko benchmarku: pojedyncza karta H100 NVL + najnowsza wersja llama.cpp — zmiana runtime/GPU między modelami unieważnia porównanie. 4) Na macOS preferuj MLX zamiast llama.cpp: z włączonym MTP (Multi-Token Prediction) MLX jest zauważalnie szybszy niż llama.cpp z MTP na tym samym sprzęcie.

## Uwaga / Anty-wzorzec
Utrzymywanie stałego, wysokiego reasoning_effort dla wszystkich wywołań w agencie (typowy anty-wzorzec: 'skoro model ma reasoning, to niech myśli zawsze na maxa') — drastycznie zwiększa latencję i zużycie tokenów w pętlach tool-calling. Drugi anty-wzorzec: porównywanie modeli uruchamianych na różnych runtime'ach/backendach (llama.cpp vs MLX vs vLLM) i wyciąganie wniosków o jakości modelu zamiast o wydajności backendu.

## Oryginalny cytat
> *"小模型 Agent 能力测试的天梯在这里~ (希望图不要被压得太狠....)

目前来看最值得使用是我测试的 Qwen3.8-27B-UD-Q4_K_XL 版本,  Agent 用使用 reasoning_effort = low, 然后写代码开到 medium / high.

另外文中是统一使用单卡 H100 NVL+llama.cpp 最新版本测试的. 如果是Mac用户还是建议优先使用MLX, 实测 MLX 开 MTP 会比 llama.cpp 放在 Mac 上开MTP要快一些."*
