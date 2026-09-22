---
typ: narzędzie
aliases: [TypeSafe Jev, System One Model]
tagi: [agenci, automatyzacja, klasyfikacja, routing]
źródła:
  - "[TypeSafe — Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)"
  - "[TypeSafe — AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer)"
  - "[TypeSafe — Primitives](https://docs.typesafe.ai/primitives)"
  - "[TypeSafe — Confidence](https://docs.typesafe.ai/confidence)"
  - "[TypeSafe — Patterns](https://docs.typesafe.ai/patterns)"
  - "[OpenRouter — Jev 1.13](https://openrouter.ai/typesafe/jev-1.13/api)"
sprawdzono: 2026-09-22
---

# Jev

Jev to model decyzji firmy TypeSafe. Zamiast generować swobodny tekst zwraca z góry określone, typowane odpowiedzi wraz z prawdopodobieństwami. TypeSafe określa tę klasę modeli jako **System One Models**: mają szybko podejmować wąskie decyzje wewnątrz oprogramowania, podczas gdy LLM pozostaje narzędziem do generowania, rozumowania i pracy z nieograniczonym tekstem.

## Machine-native intelligence

TypeSafe projektuje Jev pod komunikację maszyna–maszyna, a nie pod rozmowę z człowiekiem. Pożądane cechy to struktura, niezawodność, obserwowalność, testowalność, szybkość, spójność i niski koszt. Model ma dostarczać wąski osąd, który kod może sprawdzić i wykorzystać, zamiast próbować rozwiązać całe zadanie jednym generowanym tekstem.

| Metoda | Optymalizuje model pod | Typowe zastosowanie |
| --- | --- | --- |
| RLHF | odpowiedzi preferowane przez ludzi | chatboty i modele instrukcyjne |
| RLVR | nagrody możliwe do programowego zweryfikowania | rozumowanie, matematyka, kod |
| RLCD | skalibrowane decyzje i prawdopodobieństwa | automatyzacje sterowane przez kod |

**RLCD** (*reinforcement learning for calibrated decisions*) jest podejściem TypeSafe. Kalibracja dotyczy zbioru predykcji: jeśli dobrze skalibrowany model nadaje wielu zdarzeniom prawdopodobieństwo 0,8, około 80% z nich powinno zajść. Nie jest to gwarancja poprawności pojedynczej odpowiedzi.

## Interfejs

Jev odpowiada trzema prymitywami:

1. **Noul** — prawdopodobieństwo odpowiedzi „tak” dla pojedynczego warunku; nie ma osobnego pola `confidence`.
2. **Choice** — wybór jednej pozycji z podanego zbioru wraz z rozkładem `probabilities` i polem `confidence`.
3. **Score** — ocena na opisanej, uporządkowanej skali wraz z legendą poziomów, rozkładem i `confidence`.

To nie jest zamiennik modelu generatywnego. Kod definiuje możliwe odpowiedzi i steruje przepływem, a Jev dostarcza semantyczny osąd tam, gdzie zwykłe reguły nie wystarczają.

### Jak formułować pytania

- Jedno pytanie powinno opisywać jeden szybki, spójny osąd. Zamiast „oceń zgłoszenie”, osobno pytaj o pilność, frustrację i kompletność danych.
- `instructions` musi zawierać pełne znaczenie pytania. Identyfikator pytania służy tylko kodowi i nie jest wysyłany do modelu.
- `criteria` definiuje dostępne opcje `Choice`, poziomy `Score` albo doprecyzowanie odpowiedzi `Noul`.
- `Choice` powinien mieć opcję „inne” albo „żadne”, jeśli lista może być niepełna. Model nie wybierze wartości, której nie dostał.
- Niezależne pytania nad tym samym stanem należy wysłać razem. Są oceniane równolegle i nie widzą swoich odpowiedzi.
- Drugie wywołanie ma sens dopiero wtedy, gdy wcześniejsza odpowiedź jest potrzebna do pobrania nowych danych, zbudowania nowego stanu albo wyznaczenia kolejnych opcji.

## Prawdopodobieństwo i confidence

`probabilities` opisuje rozkład prawdopodobieństwa między opcjami `Choice` albo poziomami `Score`. `confidence` streszcza koncentrację tego rozkładu liczbą od 0 do 1: wyraźny zwycięzca daje wartość wysoką, a płaski rozkład — niską. Nie jest to miara prawdziwości całego workflow ani zgoda na wykonanie ryzykownej akcji.

Dla `Noul` sama wartość od 0 do 1 jest prawdopodobieństwem odpowiedzi „tak”. Wynik bliski 0,5 oznacza podobne prawdopodobieństwo „tak” i „nie”, a nie średnie natężenie cechy.

Kod powinien mapować niepewność na zachowanie:

1. **Wysoka pewność** — wykonaj niskiego ryzyka akcję automatycznie.
2. **Średnia pewność** — zbierz dodatkowe dane, poproś o potwierdzenie albo oznacz do przeglądu.
3. **Niska pewność** — nie zgaduj; eskaluj do człowieka lub innego systemu.

Progi zależą od skutków błędu. Pokazanie niewłaściwego widoku może mieć niższy próg niż zatwierdzenie operacji finansowej. Wartości progów trzeba ustalić na reprezentatywnych danych i monitorować po wdrożeniu.

## Wzorzec użycia z LLM

1. Kod zbiera stan i formułuje wąskie pytania.
2. Jev klasyfikuje, ocenia albo wybiera trasę.
3. Kod stosuje próg pewności i wykonuje bezpieczną akcję.
4. Przypadki niepewne trafiają do człowieka lub modelu generatywnego, np. Claude'a albo Codexa.

Takie połączenie rozdziela szybkie, masowe decyzje od droższego generowania i rozumowania. Progi trzeba skalibrować na własnych danych; typowany wynik nie gwarantuje prawdziwości decyzji.

## Wzorce architektoniczne TypeSafe

| Wzorzec | Mechanizm | Korzyść |
| --- | --- | --- |
| **Speculative Fan-Out** | wyślij w jednym wywołaniu wszystkie niezależne pytania, także warunkowe; kod wykorzysta tylko potrzebne wyniki | szybkość i koszt |
| **Confidence-Gated Routing** | użyj zarówno wybranej odpowiedzi, jak i jej pewności do wyboru następnej ścieżki | bezpieczeństwo i niezawodność |
| **Composite Scoring** | oceń kilka niezależnych wymiarów, a następnie połącz je wagami i regułami w kodzie | testowalność i elastyczność |
| **Intent Routing** | rozpoznaj intencję i przekaż zadanie do konkretnego handlera, narzędzia albo modelu | szybkość i koszt |

Wagi, progi i zasady pozostają w kodzie. Dzięki temu można zmieniać politykę bez ponownego pytania modelu, o ile stan i znaczenie surowych ocen się nie zmieniły.

## Zastosowania

### Agentic engineering

- **Routing modeli** — wybór tańszego lub mocniejszego modelu zależnie od zadania i ryzyka.
- **Routing skilli** — wybór właściwego skilla z dużego katalogu na podstawie opisu zadania.
- **Weryfikacja** — szybki test konkretnego twierdzenia lub wyniku przed przekazaniem go dalej.

Routing nie jest jednak „darmową optymalizacją”. Trzeba mierzyć jakość całego zadania, koszt dodatkowego wywołania i opóźnienie, a przy niskiej pewności stosować bezpieczny model domyślny.

### Automatyzacje biznesowe

- triage wiadomości, leadów i zgłoszeń wsparcia,
- wykrywanie spamu, nadużyć i podejrzanych faktur,
- moderacja treści,
- klasyfikacja próśb o zwrot,
- ocena ryzyka odejścia klienta.

Najlepszy kandydat to duży strumień podobnych obiektów, dla których trzeba wielokrotnie odpowiedzieć na jasno zdefiniowane pytanie biznesowe.

### Funkcje aplikacji

- reranking kandydatów w wyszukiwaniu semantycznym,
- wybór właściwego elementu strony do ukrycia, np. reklamy lub banera,
- ekstrakcja przez wybór spośród wartości znalezionych wcześniej przez kod,
- decyzje interfejsu zależne od bieżącego stanu aplikacji.

Jev przyjmuje tekstowy stan. Przykład „wyszukiwania obrazów po znaczeniu” wymaga więc wcześniejszego opisu, OCR albo innych metadanych obrazu; sam model nie analizuje obrazu.

## Dostęp i koszt

Model jest dostępny bezpośrednio przez TypeSafe oraz przez [[LM Studio i OpenRouter|OpenRouter]]. Według dokumentacji sprawdzonej 22 września 2026 r. Jev 1.13 kosztuje **0,042 USD za milion tokenów wejściowych**, a tokeny wyjściowe są rozliczane po **0 USD**.

Limit kontekstu ma dwie części:

- 64 tys. tokenów na całe wywołanie: stan i wszystkie pytania,
- 32 tys. tokenów na stan i pojedyncze najdłuższe pytanie.

Jev przetwarza stan raz, a pytania ocenia równolegle. Bezpośrednie API używa `POST /v1/systemone`; SDK domyślnie wybierają alias `jev-latest`. Alias może zostać przesunięty na nowszą wersję, dlatego workflow ze skalibrowanymi progami powinien przypinać wersję i logować pole `model` z odpowiedzi. Limity przepustowości są obecnie dynamiczne, a cennik i dostępność mogą się zmienić.

TypeSafe podaje dla własnych workflow wyniki do około **193,6× szybciej** i **444,6× taniej** od porównywanych LLM-ów. To benchmark producenta, zależny od konstrukcji zadania, lokalizacji klienta i sposobu pomiaru; nie należy przenosić go bez testów na własny proces.

## Ograniczenia Jev 1.13

- Obsługuje wyłącznie tekst: ciągi, obiekty JSON i tablice wartości tekstowych. Obraz, audio i wideo trzeba wcześniej przetworzyć do tekstu lub pól strukturalnych.
- Najlepsza jakość jest obecnie dla języka angielskiego. Inne języki są obsługiwane, ale wymagają osobnej walidacji na danych docelowych.
- Nie należy zlecać modelowi arytmetyki, liczenia, porównywania dat ani precyzyjnych operacji numerycznych. Te kroki należą do kodu.
- Długie stany pełne nieistotnych informacji pogarszają jakość. Najpierw wyszukaj i odfiltruj dane, potem pytaj model.
- Model interpretuje instrukcje literalnie i gorzej radzi sobie z wieloma poziomami pośrednictwa, sprzecznymi kryteriami i podwójnymi negacjami.
- Stan nie jest automatycznie traktowany jako potencjalnie wrogi. Dane pochodzące od użytkownika trzeba testować pod kątem prompt injection i manipulacji klasyfikacją.
- Wyniki równoważnie brzmiących pytań zadanych jako `Noul` i `Choice` nie muszą być arytmetycznie zgodne. Progi stroi się osobno dla każdego prymitywu i sformułowania.
- Jev nie generuje tekstu, kodu ani uzasadnień. Gdy odpowiedź nie ma zamkniętego zbioru kandydatów, potrzebny jest model generatywny.

## Ważne sprostowania do transkrypcji

- Współzałożyciel TypeSafe, **Diogo Almeida**, współtworzył RLHF, metodę wykorzystaną przy trenowaniu InstructGPT i ChatGPT. Określenie „współwynalazca ChatGPT” z transkrypcji jest więc skrótem, a nie precyzyjnym opisem jego roli.
- „Fable” i „Astra” w materiale są nazwami modeli porównawczych, a nie opisem wszystkich tradycyjnych LLM-ów.
- „Brak halucynacji” u producenta oznacza brak dowolnie wygenerowanych wartości poza zdefiniowanym typem. Model nadal może wybrać błędną odpowiedź.

## Powiązane

- [[TypeSafe i Jev — wywiad z Diogo Almeidą]]
- [[TypeSafe — przewodnik praktyczny]]
- [[Harness]]
- [[Harnessy]]
- [[Praca z harnessem]]
- [[LM Studio i OpenRouter]]
- [[Weryfikator]]
