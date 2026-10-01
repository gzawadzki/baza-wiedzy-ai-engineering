---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Thu Sep 17 22:46:03 +0000 2026"
źródło: "https://x.com/karminski3/status/2100717948881326224"
kategoria: "Architektura modeli / Latencja i wnioskowanie / Systemy agentowe"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Jev (TypeSafe AI): model System One z równoległym samplingiem i latencją 70 ms do decyzji o niskim opóźnieniu

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Thu Sep 17 22:46:03 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2100717948881326224)
- **Konwersacja:** Odpowiedź w dyskusji (@karminski3)
- **Kluczowe pojęcia:** [[Harness|System One vs System Two]] [[Harness|Równoległy sampling (architektura predykcji)]] [[Harness|Memory bandwidth w LLM]] [[Harness|Forward pass a koszt inferencji]] [[Harness|Projektowanie budżetu latencji end-to-end]] [[Harness|Diogo Almeida]] [[Harness|InstructGPT]] [[Harness|RLHF]] [[Harness|Vercel AI Gateway]] [[Harness|Klasyfikacja ryzykownych poleceń shell]] [[Harness|Modele flash jako decision maker]]

---

## Kontekst i problem
Autor omawia nowy model Jev od TypeSafe AI (założonej przez Diogo Almeidę — współtwórcę InstructGPT i wczesnego RLHF w OpenAI). Model adresuje scenariusze wymagające ultraniskiej latencji w produkcji, np. real-time klasyfikację ryzykownych poleceń shell (detekcja `rm -rf /`) na bastionie. Omówiona jest architektura (równoległy sampling zamiast klasycznego forward-pass-per-token), cennik, ograniczenia sieciowe oraz relacja System One / System Two.

## Rada inżynierska
Przy budowie systemów decyzyjnych o wysokiej częstotliwości stosuj modele o architekturze równoległego samplingu, które w JEDNYM forward passie zwracają dyskretne predykcje wszystkich pól schematu wraz z prawdopodobieństwami gałęzi — to eliminuje wąskie gardło przepustowości pamięci (memory bandwidth) typowe dla klasycznych LLM-ów (jeden token = jeden przebieg aktywacji). Kluczowa reguła inżynierska: rozdziel role — model System One (szybki, reaktywny, np. Jev ~70 ms) do natychmiastowych klasyfikacji, oraz model System Two (wolniejszy, strategiczny) do generowania polityki/strategii, którą następnie wstrzykujesz jako prompt do System One, aby podnieść jakość odpowiedzi. Dodatkowo: projektuj budżet latencji end-to-end uwzględniając narzut sieciowy — przy braku węzłów lokalnych i łączu do US West dodaj ~120 ms opóźnienia światłowodowego, więc realne SLO to ≥200 ms, nie 70 ms. To model idealny dla decyzji typu whitelist/blacklist command check, gdzie PRZEPUSTOWOŚĆ i TANIOŚĆ ($0.042 / 1M tokenów wej., wyjście darmowe) przewyższają głębię rozumowania.

## Uwaga / Anty-wzorzec
Mylenie latencji lokalnej modelu (70 ms) z latencją end-to-end — bez lokalnych węzłów narzut transmisji morskiej (~120 ms) winduje realny czas do ≥200 ms. Drugi anty-wzorzec: próba użycia modelu czysto reaktywnego (System One) jako samodzielnego decydenta strategicznego — bez modelu System Two generującego politykę/strategię jako prompt, jakość decyzji spada; to modele komplementarne, nie zamienne. Trzeci: zakładanie, że brak bezpośredniego dostępu (waitlist) blokuje testy — Vercel AI Gateway już udostępnia model.

## Oryginalny cytat
> *"但天下武功唯快不破, 这玩意从输入到输出最快只需要70ms! 所以完全可以用在高频的生产级场景, 比如接到堡垒机里面实时判断用户输入的shell命令是否存在危险(rm -rf /). 再加上输入每百万token只需要$0.042, 输出不要钱. 妥妥的新一代flash模型斩杀线(有的flash模型会被企业用作决策器). 说完了用途再来看它的架构, 传统大模型有多少token就要把激活参数过多少遍(前向传播)所以特别吃显存带宽, 而这个模型设计了一个特殊的并行采样架构, 只需要一次前向传播, 就能输出所有预设schema字段的离散预测与分支概率. 达成了极低的延迟. 而推出Jev的 TypeSafe AI 这个公司也很有噱头, 它是 Diogo Almeida 一手创办的, 就是他曾经在 OpenAI 的 InstructGPT 和早期 RLHF（基于人类反馈的强化学习) 团队中的贡献才有了如今的ChatGPT. 最后说一下目前模型的限制, 首先由于没有本土节点, 所以虽然它只需要70ms, 但是到美西这海底光缆延迟120ms是躲不掉的, 所以至少还是200ms打底. 另外, 模型被官方称为 System One 模型, 所以理想搭配还需要一个 System Two 模型用来进行战略判断, 然后生成策略当作提示词输入进去, 这样才能提升模型的输出质量. 另外, 官网还在申请使用, 不过vercel的AI Gateway已经能直接用了, 所以想测试的同学直接去vercel用就行."*
