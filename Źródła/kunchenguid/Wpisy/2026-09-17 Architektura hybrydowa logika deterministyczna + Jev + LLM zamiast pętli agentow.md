---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Thu Sep 17 06:45:30 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100476218512748616"
kategoria: "Architektura systemów agentowych / Inżynieria kosztów"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Architektura hybrydowa: logika deterministyczna + Jev + LLM zamiast pętli agentowych

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Thu Sep 17 06:45:30 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100476218512748616)
- **Konwersacja:** Odpowiedź w dyskusji (@v10se)
- **Kluczowe pojęcia:** [[Harness|Pętla agentowa]] [[Harness|Architektura hybrydowa]] [[Harness|Redukcja kosztów LLM]] [[Harness|Logika deterministyczna vs LLM]] [[Harness|Inżynieria systemów agentowych]]

---

## Kontekst i problem
Autor odpowiada pod wpisem @v10se, omawiając implikacje technologii (nazywanej 'Jev') zdolnej zastąpić część wywołań LLM. Wskazuje dwa skutki: oczywistą redukcję kosztów oraz mniej oczywistą zmianę paradygmatu projektowania oprogramowania. LLM-y skłaniają deweloperów do budowania pętli agentowych (agent loops), w których model sam decyduje i iteruje. Alternatywa polega na rozdzieleniu odpowiedzialności: logika deterministyczna w kodzie, inteligentne podejmowanie decyzji przez dedykowany komponent, a LLM używany tylko okazjonalnie do generowania treści.

## Rada inżynierska
Projektuj systemy jako hybrydę trzech warstw: (1) deterministyczna logika w kodzie, (2) wyspecjalizowany komponent decyzyjny (np. Jev) do inteligentnych wyborów, (3) LLM wyłącznie do okazjonalnego generowania treści. Tam, gdzie to możliwe, zastępuj wywołania LLM tańszymi mechanizmami — to nie tylko oszczędność kosztów, ale wymuszenie zdrowszej architektury niż bezrefleksyjne pętle agentowe. Traktuj redukcję kosztu jako sygnał do przeprojektowania, nie tylko do optymalizacji budżetu.

## Uwaga / Anty-wzorzec
Anty-wzorzec: domyślne budowanie wszystkiego wokół pętli agentowych z LLM w środku każdej decyzji. Prowadzi to do nadmiarowych kosztów, nieprzewidywalności i utraty kontroli nad przepływem sterowania, gdy prosta logika deterministyczna lub dedykowany komponent decyzyjny wystarczyłyby.

## Oryginalny cytat
> *"right now i'm seeing two - the most obvious implication is cost reduction. it's a massive saving whenever we can replace LLM calls with this; the non-obvious one is that it forces us to think about our software differently. LLMs make us all build agent loops. this enables us to explore a different architecture - a combination of deterministic logic (code), intelligent decision making (Jev), and occasional generation of content (LLM)"*
