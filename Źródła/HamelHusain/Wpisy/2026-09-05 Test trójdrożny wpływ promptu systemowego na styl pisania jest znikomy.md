---
typ: wpis-źródłowy
autor: "@HamelHusain"
data: "Sat Sep 05 00:58:16 +0000 2026"
źródło: "https://x.com/HamelHusain/status/2096040183502373248"
kategoria: "Inżynieria promptów / Ewaluacja"
tagi:
  - hamelhusain
  - ai-engineering
  - wpis-atomowy
---

# Test trójdrożny: wpływ promptu systemowego na styl pisania jest znikomy

- **Autor:** [[HamelHusain — Indeks|@HamelHusain]] | **Data:** `Sat Sep 05 00:58:16 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2096040183502373248)
- **Konwersacja:** Odpowiedź w dyskusji (@HamelHusain)
- **Kluczowe pojęcia:** [[Prompt Architecture|Prompt Engineering]] [[Stabilność modeli i przestrzeganie promptu|System Prompt]] [[Harness|Ewaluacja modeli]] [[Prompt Architecture|A/B Testing promptów]] [[Prompt Architecture|Writing Density Prompt]] [[Harness|Slop]]

---

## Kontekst i problem
Autor przeprowadził test trójdrożny na 5 przykładach, porównując trzy warianty sterowania stylem pisania: (1) 'unmannered slop prompt' — prompt gęstości pisania, (2) 'plain writing prompt' — uprzejmy, standardowy prompt pisarski, (3) brak promptu systemowego. Celem było sprawdzenie, jak silnie prompt systemowy steruje stylem generowanego tekstu.

## Rada inżynierska
Nie zakładaj z góry, że starannie zaprojektowany prompt systemowy znacząco zmieni styl pisania modelu. W małych, kontrolowanych testach A/B/C różnice między 'eleganckim' promptem, 'prostackim' promptem i brakiem promptu mogą być minimalne — a czasem wariant uznawany za gorszy (slop) wypada lepiej w subiektywnej ocenie. Zawsze weryfikuj wpływ promptu empirycznie na własnym zbiorze przykładów, zamiast opierać się na intuicji.

## Uwaga / Anty-wzorzec
Wiara w to, że 'dopracowany' prompt systemowy jest kluczowym dźwignią kontroli stylu — prowadzi to do przepalania czasu na iteracyjne szlifowanie promptu bez mierzalnego zysku. Drugi anty-wzorzec: ocenianie promptu na zbyt małej próbie (5 przykładów) i wyciąganie zbyt mocnych wniosków.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Wynik stoi w sprzeczności z powszechnym konsensusem branżowym, że prompt engineering (w tym prompt systemowy) ma duży wpływ na jakość i styl odpowiedzi. Autor zaobserwował, że prompt 'nie wydaje się mieć dużego znaczenia' w sterowaniu pisaniem, a wariant 'unmannered slop' bywał preferowany — co podważa założenie, że uprzejme, rozbudowane prompty są zawsze lepsze. Wymaga rozstrzygnięcia: czy to artefakt małej próby (5 przykładów), specyfiki zadania pisarskiego, czy realny sygnał o ograniczonej roli promptu systemowego w nowoczesnych modelach.

## Oryginalny cytat
> *"Here are the results, we felt that the prompt doesn't seem to matter much in steering writing on the 5 examples we looked at in the three way test. To our surprise, we sometimes preferred the unmannered slop prompt and we thought it would surely do poorly. The unmannered prompt is the writing density prompt from here: https://t.co/EOyNuJghvu The plain writing prompt is adapted from https://t.co/m1U35qV1fL And the no sys prompt is just no system prompt at all."*
