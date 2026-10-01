---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Thu Sep 17 06:45:30 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100476218512748616"
kategoria: "Architektura systemów agentowych / Inżynieria kosztów wnioskowania"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Architektura hybrydowa zamiast pętli agentowej: kod deterministyczny + lekki model decyzyjny + okazjonalny LLM

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Thu Sep 17 06:45:30 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100476218512748616)
- **Konwersacja:** Odpowiedź w dyskusji (@v10se)
- **Kluczowe pojęcia:** [[Harness|Architektura hybrydowa]] [[Harness|Pętla agentowa]] [[Harness|Agent-first by default (anty-wzorzec)]] [[Kaskady Modeli i Routing Pewności|Routing modeli]] [[Harness|Redukcja kosztów inferencji]] [[Harness|Logika deterministyczna]] [[Harness|Małe modele decyzyjne]] [[Kaskady Modeli i Routing Pewności|Kaskadowanie modeli]] [[Harness|Testowalność systemów LLM]]

---

## Kontekst i problem
Autor odpowiada pod wpisem @v10se, komentując konsekwencje zastępowania wywołań LLM lżejszym komponentem (w cytacie: „Jev” – prawdopodobnie lekki model/silnik decyzyjny). Wskazuje dwa skutki: oczywisty – drastyczna redukcja kosztów inferencji; nieoczywisty – wymuszenie zmiany paradygmatu projektowania oprogramowania. Zamiast domyślnie budować pętle agentowe oparte na LLM (bo tak podpowiada obecna moda i wygoda frameworków), można zaprojektować architekturę rozdzielającą trzy warstwy odpowiedzialności: logikę deterministyczną (kod), podejmowanie decyzji przez lekki model oraz generowanie treści przez LLM tylko wtedy, gdy jest niezbędne.

## Rada inżynierska
Rozdzielaj odpowiedzialności w systemie według kosztu i determinizmu: (1) przepływ sterowania, reguły biznesowe i walidacja → kod deterministyczny; (2) klasyfikacja, routing, wybór akcji, scoring → lekki model decyzyjny (tani, szybki, testowalny); (3) generowanie tekstu/treści → LLM wywoływany punktowo, nie w każdym kroku pętli. Traktuj wywołanie LLM jako drogi, rzadki zasób o niedeterministycznym zachowaniu, a nie jako domyślny element sterujący. Taka separacja obniża koszty, latency i wariancję odpowiedzi oraz czyni system w większości testowalnym jednostkowo.

## Uwaga / Anty-wzorzec
Anty-wzorzec: „agent-first by default” – budowanie całego produktu jako pętli agentowej, w której każdy krok (routing, decyzja, formatowanie, walidacja) to kolejne wywołanie LLM. Skutki: wielokrotnie wyższe koszty i opóźnienia, niedeterministyczne zachowanie, trudność w testowaniu i debugowaniu, a także niepotrzebne narażenie na dryf modelu oraz zmiany zachowania przy każdej migracji wersji modelu. Drugi anty-wzorzec: utożsamianie „inteligentnego podejmowania decyzji” wyłącznie z LLM – pomijanie lżejszych modeli klasyfikacyjnych/routingowych, które w wąskich zadaniach decyzyjnych wypadają porównywalnie, a kosztują ułamek ceny.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Teza stoi w opozycji do dominującego konsensusu branżowego („agent-first”), w którym zakłada się, że rdzeniem nowych aplikacji powinny być autonomiczne pętle agentowe z LLM podejmującym decyzje na każdym kroku. Autor twierdzi, że dla wielu zastosowań LLM jest nadmiarowym i kosztownym rdzeniem decyzyjnym, a wystarczająca jest kombinacja kodu deterministycznego i lekkiego modelu decyzyjnego, z LLM używanym jedynie do generowania treści. Do rozstrzygnięcia pozostaje granica: w jakich klasach zadań lekki model decyzyjny dorównuje LLM pod względem jakości decyzji i generalizacji na przypadki brzegowe, a w jakich przewaga LLM (rozumienie kontekstu, rozumowanie wieloetapowe, obsługa nieznanych przypadków) jest niezbędna i uzasadnia koszt.

## Oryginalny cytat
> *"right now i'm seeing two -

the most obvious implication is cost reduction. it's a massive saving whenever we can replace LLM calls with this

the non-obvious one is that it forces us to think about our software differently. LLMs make us all build agent loops. this enables us to explore a different architecture - a combination of deterministic logic (code), intelligent decision making (Jev), and occasional generation of content (LLM)"*
