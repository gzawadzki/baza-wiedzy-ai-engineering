---
typ: wpis-źródłowy
autor: "@teortaxesTex"
data: "Tue Sep 22 22:59:28 +0000 2026"
źródło: "https://x.com/teortaxesTex/status/2102533265265500175"
kategoria: "Architektura modeli / Cel treningowy / Mechanistyczna interpretowalność"
tagi:
  - teortaxestex
  - ai-engineering
  - wpis-atomowy
---

# MTP to ślepy zaułek — liczy się efektywna głębokość obwodu (effective circuit depth)

- **Autor:** [[teortaxesTex — Indeks|@teortaxesTex]] | **Data:** `Tue Sep 22 22:59:28 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102533265265500175)
- **Konwersacja:** Odpowiedź w dyskusji (@rudzinskimaciej)
- **Kluczowe pojęcia:** [[Architektura KV Cache i Rozumowanie Latentne|Multi-Token Prediction (MTP)]] [[Harness|Next-Token Prediction]] [[Harness|Effective Circuit Depth]] [[Harness|Residual Stream]] [[Harness|Mechanistic Interpretability]] [[Harness|Look-ahead w aktywacjach]] [[Harness|Architektura transformera]]

---

## Kontekst i problem
Dyskusja pod wpisem o architekturze transformerów i celach treningowych. Autor odpiera argument, że Multi-Token Prediction (MTP) jest kluczowym mechanizmem poprawiającym jakość modelu. Twierdzi, że sam cel przewidywania pojedynczego tokenu (single-token prediction) wystarcza, aby aktywacje wewnętrznych warstw już 'patrzyły w przyszłość' (look ahead) — czyli reprezentacje pośrednie kodują informację o tokenach jeszcze nie wygenerowanych. Prawdziwym, nierozwiązanym problemem nie jest więc cel treningowy, lecz efektywna głębokość obwodu obliczeniowego: ile warstw sekwencyjnie realnie uczestniczy w transformacji reprezentacji, a ile jest pomijanych (np. przez residual stream, attention sinks, czy redundancję).

## Rada inżynierska
Nie traktuj MTP (Multi-Token Prediction) jako źródła zdolności 'patrzenia w przyszłość' — to efekt uboczny, obecny już przy zwykłym next-token prediction. Zamiast optymalizować cel treningowy pod kątem look-ahead, mierz i optymalizuj EFEKTYWNĄ GŁĘBOKOŚĆ OBWODU: ile warstw faktycznie wnosi nieliniową transformację do przepływu informacji. Praktycznie: (1) diagnozuj redundantne warstwy przez ablację/analizę residual stream, (2) rozróżniaj głębokość nominalną (liczba warstw) od głębokości efektywnej (liczba warstw istotnych dla danego zadania), (3) przy projektowaniu architektury pytaj 'jak głęboko musi sięgnąć obliczenie', a nie 'ile tokenów przewidujemy naraz'.

## Uwaga / Anty-wzorzec
Anty-wzorzec: traktowanie MTP jako magicznego przełącznika zdolności planowania/look-ahead i przypisywanie mu zasług za poprawę jakości, gdy realnym ograniczeniem jest głębokość obwodu. Mylenie celu treningowego (co przewidujemy) z pojemnością obliczeniową (jak głęboko model przetwarza) prowadzi do błędnych wniosków o źródle zdolności modelu i do marnowania budżetu treningowego na mechanizmy, które nie adresują wąskiego gardła.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Autor podważa powszechny konsensus branżowy, że Multi-Token Prediction (stosowany m.in. w DeepSeek-V3) jest istotnym ulepszeniem celu treningowego poprawiającym jakość i zdolności planowania. Teza: MTP to 'red herring' — look-ahead w aktywacjach wynika już z samego next-token prediction, a prawdziwym problemem badawczym jest efektywna głębokość obwodu, nie cel treningowy. Do rozstrzygnięcia: czy MTP wnosi wartość niezależną od zwykłego NTP, czy jest jedynie kosztowną redundancją.

## Oryginalny cytat
> *"MTP is a red herring. Single token prediction objective is sufficient for activations to already "look ahead"
my question is about *effective* circuit depth"*
