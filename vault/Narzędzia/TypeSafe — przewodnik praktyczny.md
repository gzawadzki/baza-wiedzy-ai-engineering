---
typ: narzędzie
aliases: [TypeSafe AI, System One, przewodnik TypeSafe]
tagi: [agenci, automatyzacja, klasyfikacja, routing, weryfikacja]
źródła:
  - "[TypeSafe — System One](https://docs.typesafe.ai/concepts/system-one)"
  - "[TypeSafe — How to build](https://docs.typesafe.ai/concepts/how-to-build-with-system-one)"
  - "[TypeSafe — State](https://docs.typesafe.ai/concepts/state)"
  - "[TypeSafe — Primitives](https://docs.typesafe.ai/primitives)"
  - "[TypeSafe — Confidence](https://docs.typesafe.ai/confidence)"
  - "[TypeSafe — Patterns](https://docs.typesafe.ai/patterns)"
  - "[TypeSafe — Models](https://docs.typesafe.ai/models)"
  - "[TypeSafe — API](https://docs.typesafe.ai/api)"
  - "[TypeSafe — Cookbooks](https://docs.typesafe.ai/cookbooks)"
  - "[TypeSafe — Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13)"
sprawdzono: 2026-09-22
---

# TypeSafe — przewodnik praktyczny

## Zacznij od decyzji, nie od modelu

1. Nazwij pojedynczy osąd, którego nie da się pewnie obliczyć zwykłym kodem.
2. Zbierz tylko stan potrzebny do tego osądu.
3. Wybierz typ wyniku: `Noul`, `Choice` albo `Score`.
4. Wyślij razem pytania niezależne od siebie.
5. W kodzie zastosuj reguły, progi i skutki uboczne.
6. Niepewne lub ryzykowne przypadki skieruj do człowieka albo modelu rozumującego.
7. Zmierz jakość całego procesu na własnych danych przed automatyzacją.

TypeSafe opisuje ten układ jako **AI-powered software**: kod pozostaje właścicielem przepływu, a model System One dostarcza małe, typowane osądy nad tekstem. [[Jev]] nie pisze odpowiedzi, kodu ani uzasadnień i nie zastępuje modelu napędzającego [[Harnessy|harness]]. [Źródła: [System One](https://docs.typesafe.ai/concepts/system-one), [How to build with TypeSafe](https://docs.typesafe.ai/concepts/how-to-build-with-system-one), [Jev with coding agents](https://docs.typesafe.ai/introduction/coding-agents)]

## Model mentalny

| Warstwa | Odpowiedzialność |
| --- | --- |
| kod | walidacja, obliczenia, wyszukiwanie dokładne, kontrola przepływu, skutki uboczne |
| System One / Jev | semantyczny osąd nad tekstem: wybór, ocena albo prawdopodobieństwo „tak” |
| LLM rozumujący | generowanie, złożone rozumowanie, obsługa niejednoznacznych wyjątków |
| człowiek | decyzje wysokiego ryzyka, przypadki bez wystarczających danych, audyt |

System One przyjmuje tekstowy `state` oraz mapę niezależnych pytań, a zwraca ustrukturyzowane odpowiedzi i prawdopodobieństwa. Typowany format eliminuje parsowanie swobodnego tekstu, ale **nie gwarantuje prawdziwości decyzji**. Kalibracja jest własnością zbioru predykcji, nie obietnicą poprawności pojedynczego wyniku. [Źródła: [System One](https://docs.typesafe.ai/concepts/system-one), [AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer), [How to build](https://docs.typesafe.ai/concepts/how-to-build-with-system-one)]

## State: co model ma wiedzieć

`state` może być napisem, obiektem JSON albo tablicą wartości tekstowych. Przy złożonych rekordach lepszy jest nazwany, zagnieżdżony JSON: oddziel wiadomość, politykę, dane klienta i wyniki wyszukiwania. W instrukcjach można wskazywać ścieżki, np. `` `ticket.message` ``, aby usunąć dwuznaczność. Identyfikator pytania służy wyłącznie aplikacji i nie jest przekazywany modelowi, więc pełne znaczenie musi znaleźć się w `instructions`. [Źródła: [State](https://docs.typesafe.ai/concepts/state), [API](https://docs.typesafe.ai/api), [How to build](https://docs.typesafe.ai/concepts/how-to-build-with-system-one)]

Praktyczna polityka stanu:

1. Najpierw pobierz i odfiltruj kandydatów w kodzie.
2. Przekaż aktualne fakty i reguły domenowe; nie zakładaj, że model zna ich bieżącą wersję.
3. Usuń pola niezwiązane z pytaniem — długi, rozpraszający kontekst pogarsza trafność.
4. Traktuj treść użytkownika jak dane potencjalnie wrogie; Jev 1.13 nie izoluje automatycznie prompt injection zawartego w stanie.
5. Dla obrazu, audio lub wideo najpierw przygotuj OCR, transkrypcję albo metadane, ponieważ Jev 1.13 obsługuje tylko tekst.

Te reguły wynikają zarówno z ogólnego przewodnika, jak i z listy znanych ograniczeń Jev 1.13. [Źródła: [State](https://docs.typesafe.ai/concepts/state), [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13), [Models](https://docs.typesafe.ai/models)]

## Trzy prymitywy

| Potrzeba | Prymityw | Wynik | Użyj, gdy |
| --- | --- | --- | --- |
| czy warunek zachodzi | `Noul` | `noul` od 0 do 1 = P(„tak”) | etykiety nie wykluczają się albo potrzebna jest niezależna bramka |
| wybór jednej opcji | `Choice` | zwycięska opcja, rozkład po opcjach, `confidence` | odpowiedzi konkurują i dokładnie jedna ma wygrać |
| stopień cechy | `Score` | wartość oczekiwana na opisanej skali, legenda, rozkład, `confidence` | potrzebny jest uporządkowany wymiar, próg lub ranking |

`Choice` przyjmuje maksymalnie 255 opcji. Gdy żadna nie musi pasować, dodaj jawne „inne” lub „brak dopasowania”. `Score` przyjmuje od 2 do 10 opisanych poziomów; poziomy powinny opisywać konkretne sytuacje, a nie same liczby. `Noul` nie ma osobnego `confidence`, bo jego wartość jest już prawdopodobieństwem odpowiedzi „tak”. [Źródła: [Primitives](https://docs.typesafe.ai/primitives), [Choice](https://docs.typesafe.ai/primitives/choice), [Score](https://docs.typesafe.ai/primitives/score), [Noul](https://docs.typesafe.ai/primitives/noul), [API](https://docs.typesafe.ai/api)]

### Jak pisać pytania

1. Jedno pytanie = jeden osąd przydatny niezależnie od pozostałych.
2. Napisz dokładny warunek w `instructions`; Jev 1.13 czyta literalnie.
3. W `criteria` opisz granice, wykluczenia i przypadki brzegowe.
4. Dopilnuj, aby instrukcja i kryteria mówiły to samo; nie odwracaj sztucznie znaczenia `true` i `false`.
5. Jeśli kilka etykiet może być prawdziwych naraz, użyj kilku `Noul`, a nie jednego `Choice`.
6. Jeśli wynik ma być źródłową wartością, najpierw znajdź kandydatów w kodzie, a potem pozwól modelowi wybrać; model nie wybierze wartości, której nie dostał.
7. Gdy po błędzie tłumaczysz „co naprawdę miałem na myśli”, przenieś to wyjaśnienie do pytania lub kryteriów.

Pola `instructions` i `criteria` mogą być tekstem albo strukturą JSON, co pomaga rozdzielić regułę, porównywany obiekt i dane pomocnicze. [Źródła: [Advanced structure](https://docs.typesafe.ai/primitives/advanced), [How to build](https://docs.typesafe.ai/concepts/how-to-build-with-system-one), [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13)]

## Probability a confidence

`probabilities` to rozkład po opcjach `Choice` albo poziomach `Score`. `confidence` streszcza, jak skoncentrowany jest ten rozkład: wysoka wartość oznacza wyraźnego zwycięzcę, a niska — konkurujące odpowiedzi. Nie mówi, czy cały workflow jest bezpieczny ani czy wolno wykonać akcję. Wybór między dwoma równie dobrymi, nieszkodliwymi wariantami może mieć niskie `confidence` i nadal być użyteczny. [Źródło: [Confidence](https://docs.typesafe.ai/confidence)]

Dla `Noul` wartość około 0,5 oznacza podobne prawdopodobieństwo „tak” i „nie”, a nie średnie natężenie cechy. Nie przenoś progu dostrojonego dla `Noul` na `Choice`: te prymitywy odpowiadają na różne pytania i nie muszą spełniać intuicyjnych tożsamości, np. P(A) + P(nie-A) = 1 między dwoma osobnymi wywołaniami. [Źródła: [Noul](https://docs.typesafe.ai/primitives/noul), [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13)]

### Polityka działania

1. Określ koszt fałszywego pozytywu i fałszywego negatywu.
2. Ustal osobne progi dla automatyzacji, przeglądu i odrzucenia.
3. Dla niewinnej preferencji wybierz maksimum rozkładu; nie dodawaj progu bez potrzeby.
4. Dla działania ryzykownego wymagaj dodatkowych warunków deterministycznych albo zatwierdzenia.
5. Strojenie wykonaj na reprezentatywnym zbiorze z etykietami, a po wdrożeniu monitoruj pokrycie automatyzacji i błędy.

Dokumentacja pokazuje progi w przykładach, ale podkreśla, że zależą od konsekwencji i danych konkretnego systemu. [Źródła: [Confidence](https://docs.typesafe.ai/confidence), [Confidence-gated routing](https://docs.typesafe.ai/patterns/confidence-routing)]

## Wzorce architektoniczne

### Speculative fan-out

Wyślij w jednym żądaniu wszystkie niezależne pytania nad tym samym stanem, także pytania potrzebne tylko w niektórych gałęziach. Model ocenia je równolegle, a kod wykorzystuje właściwy wynik. Drugie wywołanie jest potrzebne dopiero wtedy, gdy pierwsza odpowiedź służy do pobrania nowych danych, utworzenia nowych opcji albo zbudowania kolejnego stanu. [Źródło: [Speculative fan-out](https://docs.typesafe.ai/patterns/fan-out)]

### Confidence-gated routing

Najpierw ustal „co” poprzez wybór lub ocenę, a potem „czy działać” poprzez pewność i ryzyko. Typowy przepływ to: automatyzacja dla mocnego sygnału, przegląd dla strefy pośredniej i eskalacja dla słabego sygnału. [[Weryfikator]] może realizować tę bramkę przed kosztowną albo nieodwracalną akcją. [Źródło: [Confidence-gated routing](https://docs.typesafe.ai/patterns/confidence-routing)]

### Composite scoring

Rozbij szeroki osąd na kilka wymiarów, oceń je niezależnymi `Score`, znormalizuj i połącz wagami w kodzie. Surowe wyniki pozostają widoczne, a zmianę polityki można wdrożyć przez zmianę wag bez ponownej inferencji, jeśli stan i znaczenie pytań się nie zmieniły. Reguła „jakiekolwiek poważne naruszenie” wymaga jednak osobnych bramek, a nie średniej, która może rozmyć alarm. [Źródło: [Composite scoring](https://docs.typesafe.ai/patterns/composite-scoring)]

### Intent routing

Jedno wywołanie może równolegle rozpoznać intencję i złożoność, po czym kod kieruje prosty przypadek do deterministycznego handlera, trudniejszy do specjalistycznego LLM, a niepewny do człowieka. To dobre miejsce na połączenie TypeSafe z [[Praca z harnessem|pracą z harnessem]], lecz Jev jest routerem wewnątrz systemu, nie zamiennikiem modelu agenta. [Źródła: [Intent routing](https://docs.typesafe.ai/patterns/intent-routing), [Jev with coding agents](https://docs.typesafe.ai/introduction/coding-agents)]

## Najbardziej przenośne cookbooki

| Problem | Przepis TypeSafe | Wzorzec do skopiowania |
| --- | --- | --- |
| wiele pytań do dużego dokumentu | [Parallel questions](https://docs.typesafe.ai/cookbooks/parallel_questions) | stan wyślij raz, pytania zbatchuj; mierz koszt i czas całego żądania |
| wybór funkcji i argumentów | [Function calling](https://docs.typesafe.ai/cookbooks/function_calling) | funkcję i zamknięte argumenty przedstaw jako typowane wybory; walidację i wywołanie zachowaj w kodzie |
| wybór skilla z dużego katalogu | [Skill suggestion](https://docs.typesafe.ai/cookbooks/skill_suggestion) | szeroki ranking → krótka lista → ponowna weryfikacja pełnych opisów → możliwość wyboru „żaden” |
| filtrowanie kontekstu RAG | [Classifying RAG passages](https://docs.typesafe.ai/cookbooks/classifying_rag_passages) | retrieval tworzy kandydatów, Jev ocenia ich użyteczność, kod wybiera fragmenty dla LLM |
| kontrola cytowań | [Double-checking citations](https://docs.typesafe.ai/cookbooks/citation_check) | sprawdź konkretną tezę względem jej źródłowego kontekstu, zamiast pytać ogólnie „czy odpowiedź jest dobra” |
| guardraile wejścia i wyjścia | [Guardrails for LLMs](https://docs.typesafe.ai/cookbooks/llm_guardrails) | osobne prawdopodobieństwa zagrożeń i poziom ciężkości → pass, review, block lub route |
| tania ekstrakcja z eskalacją | [SDE cascade](https://docs.typesafe.ai/cookbooks/sde_cascade) | tani ekstraktor → bateria weryfikacji per pole → eskalacja do mocnego modelu, gdy dowolna poważna flaga przekroczy próg |
| ekstrakcja wartości bez generowania | [Pre-parsed value extraction](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook) | regex/parser znajduje kandydatów, Jev wybiera właściwy span, kod kopiuje i normalizuje wartość |
| klasyfikacja hierarchiczna | [Classification using confidence](https://docs.typesafe.ai/cookbooks/classification_using_confidence) | przy wysokiej pewności zwróć kategorię szczegółową, przy niskiej — poprawną kategorię nadrzędną |

Cookbooki są studiami przypadku producenta, a ich zbiory, modele porównawcze, progi i wyniki nie są gwarancją dla innej domeny. Przykładowo TypeSafe raportuje w cookbooku o batchingu 10× krótszy czas i 12,2× niższy koszt dla 13 pytań do jednego dużego dokumentu; korzyść wynikała głównie z niewysyłania tego samego stanu 13 razy. W cookbooku wyboru skilli producent raportuje spadek błędnych załadowań z 16,8% do 7,3% na własnym eksperymencie z katalogiem Hermes. Oba wyniki trzeba odtworzyć na swoim obciążeniu. [Źródła: [Parallel questions](https://docs.typesafe.ai/cookbooks/parallel_questions), [Skill suggestion](https://docs.typesafe.ai/cookbooks/skill_suggestion)]

## API, SDK i model

- Główny endpoint HTTP: `POST https://api.typesafe.ai/v1/systemone`; lista dostępnych modeli: `GET /v1/models`.
- Python: pakiet `typesafe-sdk`, Python 3.10 lub nowszy; klient synchroniczny i asynchroniczny.
- JavaScript/TypeScript: pakiet `@typesafe-ai/sdk`, Node.js 20 lub nowszy.
- Klucz API należy przechowywać po stronie serwera, np. w `TYPESAFE_API_KEY`, nie w kodzie przeglądarki.
- Odpowiedź zawiera wersjonowane pole `model`, mapę `answers` oraz `usage` z tokenami wejścia i wyjścia.
- SDK domyślnie stosują retry z backoffem i respektują `retry-after`; przy bezpośrednim HTTP trzeba obsłużyć co najmniej `401`, `422`, `429` oraz `529`.

[Źródła: [API reference](https://docs.typesafe.ai/api), [Python SDK](https://docs.typesafe.ai/sdk/python), [JavaScript SDK](https://docs.typesafe.ai/sdk/javascript), [Models](https://docs.typesafe.ai/models)]

### Jev 1.13: parametry operacyjne

| Właściwość | Stan na 2026-09-22 |
| --- | --- |
| wersjonowany model | `jev-1.13.0` |
| alias stabilny | `jev-latest` |
| alias najnowszej kompilacji | `jev-preview` — obecnie wskazuje tę samą wersję co `jev-latest` |
| kontekst żądania | 64 tys. tokenów łącznie; dodatkowo limit 32 tys. dla `state` + najdłuższego pytania |
| wejście | tylko tekst: string, obiekt JSON lub tablica tekstów |
| język | angielski jest podstawowym i najlepiej działającym językiem treningowym; polski trzeba ocenić na własnym korpusie |
| rozliczenie producenta | 0,042 USD za milion tokenów wejściowych; tokeny wyjściowe bez opłaty |

Alias może bez zmiany kodu zacząć wskazywać nową wersję, a wtedy wyniki i kalibracja progów mogą się zmienić. Do procesu produkcyjnego ze strojonymi progami przypnij identyfikator wersji, loguj `response.model`, a migrację wykonuj jawnie. Limity szybkości według producenta zmieniają się dynamicznie, więc nie utrwalaj ich jako stałej architektonicznej. Dostęp przez [[LM Studio i OpenRouter|OpenRouter]] jest osobną ścieżką integracji; ten przewodnik opisuje bezpośrednie API TypeSafe. [Źródło: [Models](https://docs.typesafe.ai/models)]

## Znane ograniczenia Jev 1.13

| Nie używaj modelu do | Zrób zamiast tego |
| --- | --- |
| arytmetyki i precyzyjnych obliczeń | policz w kodzie |
| liczenia znaków, wystąpień lub elementów | wykryj elementy parserem, oceń semantycznie osobno, zsumuj w kodzie |
| porównywania dat i czasu | wyodrębnij składniki jako zamknięte wybory, zbuduj datę i porównaj w kodzie |
| rekonstrukcji dokładnej liczby ze `Score` | użyj opisanych progów semantycznych, nie interpolacji liczbowej |
| wielohopowego rozumowania i podwójnych negacji | uprość instrukcję i rozbij zadanie |
| generowania tekstu | użyj LLM generatywnego |
| analizy ogromnego, nieprzefiltrowanego stanu | retrieve/filter w kodzie, potem oceń krótką listę |
| zakładania odporności na prompt injection | testuj adversarial cases i ogranicz stan |

Jev 1.13 może też zwrócić różne liczby dla semantycznie podobnego `Noul` i binarnego `Choice`; nie wymuszaj między osobnymi pytaniami intuicyjnych zależności matematycznych. Lista ograniczeń jest wersjonowana i według TypeSafe część problemów może zniknąć w kolejnych wydaniach. [Źródło: [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13)]

## Checklista wdrożenia

1. **Zdefiniuj wynik biznesowy:** jaka akcja ma zależeć od osądu i jaki jest koszt błędu?
2. **Zbuduj baseline:** prosta reguła, człowiek lub obecny LLM daje punkt odniesienia.
3. **Zaprojektuj stan:** tylko potrzebne fakty, jawne źródło i wersja polityki.
4. **Rozbij pytania:** niezależne wymiary zamiast jednego „oceń wszystko”.
5. **Dodaj brak dopasowania:** nie zmuszaj `Choice` do fałszywej pewności.
6. **Oddziel model od polityki:** progi, wagi i skutki uboczne trzymaj w kodzie.
7. **Zaprojektuj awarie:** timeout, `429`, `529`, brak odpowiedzi, niska pewność i ręczny fallback.
8. **Waliduj na danych domenowych:** szczególnie po polsku, na przypadkach granicznych i wrogich.
9. **Mierz system:** jakość, pokrycie automatyzacji, koszt, latency i koszt eskalacji.
10. **Przypnij wersję:** po strojeniu progów; nowy model wprowadź przez ponowną ewaluację.
11. **Loguj audytowalnie:** wersję modelu, skrót stanu, pytania, surowe rozkłady, decyzję kodu i wynik rzeczywisty — zgodnie z zasadami prywatności.

To jest synteza praktyk zalecanych przez TypeSafe; szczegóły retencji i zgodności trzeba sprawdzić w aktualnych dokumentach prawnych przed wysłaniem danych wrażliwych. [Źródła: [How to build](https://docs.typesafe.ai/concepts/how-to-build-with-system-one), [Confidence](https://docs.typesafe.ai/confidence), [Models](https://docs.typesafe.ai/models), [Legal](https://docs.typesafe.ai/legal)]

## TypeSafe w agentach i harnessach

Jev nie jest modelem czatu ani code completion. Agent nadal potrzebuje LLM, które generuje tekst, wywołuje narzędzia i edytuje pliki. TypeSafe może jednak działać **wewnątrz** narzędzia budowanego przez agenta: wybrać handler, model lub skill, ocenić ryzyko, przefiltrować kontekst i zweryfikować wynik. To uzupełnia, a nie zastępuje, praktyki z [[Harnessy]] i [[Praca z harnessem]]. [Źródło: [Jev with coding agents](https://docs.typesafe.ai/introduction/coding-agents)]

TypeSafe publikuje także skill dla Claude Code, Codexa i innych środowisk. Skill dostarcza agentowi aktualny kontrakt API oraz wzorce projektowe, lecz nie „podłącza Jev jako mózgu agenta”. Producent zaleca trzymać pytania i progi w jednym łatwym do przeglądu miejscu oraz weryfikować założenia wygenerowane przez agenta. [Źródło: [Agent skill](https://docs.typesafe.ai/agent-skill)]

## Powiązane

- [[TypeSafe i Jev — wywiad z Diogo Almeidą]]
- [[Jev]]
- [[Harnessy]]
- [[Praca z harnessem]]
- [[Weryfikator]]
- [[LM Studio i OpenRouter]]
