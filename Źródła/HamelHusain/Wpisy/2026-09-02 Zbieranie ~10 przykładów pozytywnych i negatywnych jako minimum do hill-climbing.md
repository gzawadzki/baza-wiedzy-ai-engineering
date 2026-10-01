---
typ: wpis-źródłowy
autor: "@HamelHusain"
data: "Wed Sep 02 04:18:52 +0000 2026"
źródło: "https://x.com/HamelHusain/status/2095003500992503835"
kategoria: "Ewaluacja agentów / Inżynieria promptów (few-shot)"
tagi:
  - hamelhusain
  - ai-engineering
  - wpis-atomowy
---

# Zbieranie ~10 przykładów pozytywnych i negatywnych jako minimum do hill-climbingu agenta

- **Autor:** [[HamelHusain — Indeks|@HamelHusain]] | **Data:** `Wed Sep 02 04:18:52 +0000 2026` | **Źródło:** [Post na X](https://x.com/HamelHusain/status/2095003500992503835)
- **Konwersacja:** Odpowiedź w dyskusji (@petergyang)
- **Kluczowe pojęcia:** [[Harness|Hill Climbing agenta]] [[Harness|Few-shot examples]] [[Harness|Ewaluacja agentów]] [[Harness|Kontrprzykłady negatywne]] [[Prompt Architecture|Iteracyjne doskonalenie promptów]] [[Harness|Zbiór ewaluacyjny]]

---

## Kontekst i problem
Hamel Husain odpowiada na wpis Petera Yanga, łagodząc krytykę i przechodząc do praktycznej rady: zamiast czekać na duży, 'produkcyjny' zbiór danych ewaluacyjnych, wystarczy szybko zebrać kilkanaście przykładów (pozytywnych i negatywnych) zachowań agenta, aby iteracyjnie go doskonalić metodą wspinaczki (hill climbing). Problem dotyczy typowego paraliżu zespołów, które odkładają poprawę agenta do momentu zebrania 'wystarczająco dużego' datasetu.

## Rada inżynierska
Rozpocznij iteracyjne doskonalenie agenta od małego, ręcznie zebranego zbioru ok. 10 przypadków pozytywnych i negatywnych — to wystarczy, by ruszyć z pętlą hill-climbingu (kolejne zmiany promptu/harnessu mierzone na tym samym zbiorze). Nie blokuj pracy na zebraniu 'pełnego' datasetu: mały, ale skonfrontowany z rzeczywistością zbiór kontrprzykładów daje natychmiastowy sygnał zwrotny. Liczebność zwiększaj proporcjonalnie do krytyczności zadania — im wyższa stawka (np. produkcja, compliance), tym więcej przykładów, ale próg startowy pozostaje niski.

## Uwaga / Anty-wzorzec
Anty-wzorzec: odkładanie poprawy agenta do momentu zebrania dużego, 'reprezentatywnego' zbioru ewaluacyjnego — prowadzi to do paraliżu decyzyjnego i braku jakiejkolwiek iteracji. Druga pułapka: zbieranie wyłącznie pozytywnych przykładów bez kontrprzykładów, co uniemożliwia wykrycie regresji i granic zachowania agenta.

## Oryginalny cytat
> *"@petergyang I’m just giving you a hard time.  If you can collect ~10 pos/neg examples quickly it will help your agent hill climb it 

The more the better but depends how critical it is"*
