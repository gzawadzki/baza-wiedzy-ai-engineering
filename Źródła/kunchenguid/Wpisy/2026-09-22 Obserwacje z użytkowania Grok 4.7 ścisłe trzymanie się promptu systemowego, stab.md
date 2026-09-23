---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Tue Sep 22 03:11:03 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2102234191639257399"
kategoria: "Zachowanie modeli i ocena"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Obserwacje z użytkowania Grok 4.7: ścisłe trzymanie się promptu systemowego, stabilność i konserwatyzm

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Tue Sep 22 03:11:03 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102234191639257399)
- **Kluczowe pojęcia:** [[Prompt Architecture|Prompt systemowy]] [[Harness|Zachowanie modelu]] [[Harness|Benchmarkowanie LLM]] [[Stabilność modeli i przestrzeganie promptu|Stabilność modelu]] [[Harness|Konserwatyzm modelu]] [[Harness|Koszt tokenów]] [[Harness|Opóźnienie modelu]] [[CI Check Bypass Confirmation]] [[Firstmate i Agenci Wykonawczy]]

---

## Kontekst i problem
Autor opisuje pierwsze wrażenia z używania Grok 4.7 jako asystenta (firstmate) przez cały dzień. Porównuje go do wcześniejszych wersji (4.5, 4.6) i innych modeli. Krytykuje publiczne benchmarki i testy z grami 3D jako niemiarodajne. Wskazuje na kluczowe różnice: ścisłe przestrzeganie promptu systemowego, stabilność, konserwatyzm oraz wyższe koszty i opóźnienia.

## Rada inżynierska
Podczas oceny modeli LLM skupiaj się na jakościowych obserwacjach z rzeczywistego użytkowania, a nie na publicznych benchmarkach czy testach w grach 3D. Modele takie jak Grok 4.7 mogą ściślej przestrzegać promptu systemowego, co ujawnia nowe zachowania. Stabilność i przewidywalność mogą być cenniejsze niż sporadyczne 'genialne' momenty. Konserwatyzm modelu (pytanie o zgodę) może być zaletą w niejednoznacznych sytuacjach.

## Uwaga / Anty-wzorzec
Poleganie na publicznych benchmarkach i porównaniach w grach 3D jako wskaźnikach rzeczywistej użyteczności modelu. Może to prowadzić do błędnych wniosków. Również ignorowanie kosztów i opóźnień: nowsze modele mogą być wolniejsze i droższe, co trzeba uwzględnić w budżecie i architekturze systemu.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor twierdzi, że publiczne benchmarki i porównania modeli w grach 3D są bezużyteczne i nie odzwierciedlają rzeczywistej pracy. To stoi w sprzeczności z powszechną praktyką oceny modeli LLM na podstawie tych metod. Wskazuje, że benchmarki mogą dawać mylące wyniki (np. Opus 5 vs Fable) i że prawdziwa ocena wymaga jakościowych obserwacji z rzeczywistego użytkowania.

## Oryginalny cytat
> *"day 1 observations for grok 4.7

ignore the reports that say “it’s terrible” and the only thing they reference is a public benchmark. the same benchmarks told us opus 5 was better that fable - they are useless

also ignore the reports that compare models with 3d games - that’s not real work. it's made for attention on social media

i used grok 4.7 for a whole day as my firstmate, and it has been a really solid model with visible improvements over 4.5 (i'm ignoring 4.6 because 4.5 has been working better in my experience)

key differences with 4.7 -

1. it follows system prompt very, very closely

i noticed firstmate showing many new behaviors that i've never seen before, such as asking me to name specific red CI checks that i'm ok with bypassing, and refuse a simple "yolo" instruction

i traced it and it's indeed how i instructed it in firstmate's system prompt, but none of the other models followed it closely enough to make this behavior visible - grok 4.7 is the first to pick that up

there were a few other similar examples as well. so to me this is a clear behavioral difference

2. it's very "stable"

if you've used astra then you know what a "spiky" model is. it can have some genius moments but you occasionally also wonder "how could it be so dumb and doesn't get me". grok 4.7 is the opposite of that

throughout the whole day so far, i'll be honest i haven't get a "wow this is absolutely genius" moment yet, but grok 4.7 has been very steady with no big surprises. its behavior feels predictable, which does help it gain trust from me quickly

3. it's a conservative model

it doesn't like to take actions without asking, and would explicitly say so

this is a bit of a double edged sword, because it means i sometimes have to state the obvious "yes i do want that", but in hindsight a lot of those cases are indeed a bit ambiguous and i may not have preferred the model to just move forward without my confirmation

4. it's a bit slower and costs more than 4.5, visibly

turns are taking a bit longer and my quota is draining at a visibly faster pace. i haven't quantified exactly where this is coming from yet

so overall, i think it's showing some clearly different traits, and i mostly like the changes. i'm going to keep it as my primary firstmate and observe more

if you've been using it, what qualitative insights have you gathered from real usage so far?"*
