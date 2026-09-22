---
typ: pojęcie
aliases: [ICM, Model Workspace Protocol, MWP]
tagi: [agenci, kontekst, workflow, human-in-the-loop]
źródła:
  - "[Van Clief i McDermott — Interpretable Context Methodology](https://arxiv.org/abs/2603.16021)"
  - "[Oficjalne repozytorium ICM](https://github.com/RinDig/Interpretable-Context-Methodology)"
sprawdzono: 2026-09-22
---

# Interpretable Context Methodology

**Interpretable Context Methodology (ICM)** to zaproponowana przez Jake'a Van Cliefa i Davida McDermotta metoda budowania sekwencyjnych workflow agentowych za pomocą struktury folderów, plików Markdown i małych lokalnych skryptów. Zamiast kodować osobne role „researchera”, „planisty” i „redaktora”, jeden sprawny model w [[Harness|harnessie]] czyta inną instrukcję i inny wycinek kontekstu na każdym etapie. Autorzy streszczają to jako **„folder structure as agent architecture”**.

Nazwa w transkrypcji została przekręcona: autorem jest **Jake Van Clief**, nie „Jake Van Clee”. Oficjalny tytuł artykułu rozwija skrót jako *Interpretable Context Methodology*. Wewnątrz publikacji architektura bywa też nazywana **Model Workspace Protocol (MWP)**; to protokół implementujący ideę ICM, a nie rozwinięcie skrótu ICM.

Źródła: [artykuł i metadane autorów](https://arxiv.org/abs/2603.16021), [oficjalne repozytorium](https://github.com/RinDig/Interpretable-Context-Methodology).

## Rdzeń metody

1. **Jeden etap, jedno zadanie.** Research, redakcja, projekt i publikacja mają osobne granice.
2. **Zwykły tekst jest interfejsem.** Etapy przekazują sobie czytelne pliki zamiast ukrytego stanu w frameworku.
3. **Kontekst ładuje się warstwowo i wybiórczo.** Agent czyta tylko instrukcje, referencje i artefakty potrzebne w bieżącym etapie.
4. **Każdy wynik pośredni jest powierzchnią edycji.** Człowiek może zatrzymać proces, poprawić plik i dopiero wtedy uruchomić następny etap.
5. **Konfiguruje się fabrykę, nie pojedynczy produkt.** Styl, zasady, narzędzia i preferencje zapisuje się raz, a kolejne wykonania dostarczają nowe dane robocze.

To pasuje do [[Manifest|Manifestu]]: Markdown i Git stają się nie tylko dokumentacją, ale również widocznym stanem i interfejsem pracy agenta.

Źródła: [pięć zasad ICM](https://github.com/RinDig/Interpretable-Context-Methodology#design-principles), [artykuł — architektura i kontrakty etapów](https://arxiv.org/html/2603.16021#S3).

## Pięć warstw kontekstu

| Warstwa | Typowa zawartość | Pytanie agenta |
| --- | --- | --- |
| 0 | `CLAUDE.md` lub odpowiednik dla danego [[Harness|harnessa]] | Gdzie jestem? |
| 1 | główny `CONTEXT.md` | Dokąd mam przejść? |
| 2 | `CONTEXT.md` konkretnego etapu | Co mam zrobić i co wczytać? |
| 3 | stałe referencje: styl, reguły, wiedza domenowa, skille | Jakie zasady obowiązują? |
| 4 | artefakty danego przebiegu: nagranie, transkrypcja, wynik poprzedniego etapu | Na czym pracuję? |

Warstwa 2 jest punktem sterowania: kontrakt etapu jawnie wymienia **wejścia, proces i wyjścia**. Foldery `output/` tworzą przekazania między etapami, a numerowane katalogi kodują kolejność. Stałe reguły z warstwy 3 są „fabryką”; zmienne dane i wyniki z warstwy 4 są „produktem”.

Źródła: [kanoniczne konwencje — pięć warstw](https://github.com/RinDig/Interpretable-Context-Methodology/blob/main/_core/CONVENTIONS.md#five-layer-routing-architecture), [kontrakty i handoffy](https://github.com/RinDig/Interpretable-Context-Methodology/blob/main/_core/CONVENTIONS.md#pattern-1-stage-contracts).

## Przykład z transkrypcji

Powtarzalne przetwarzanie wykładu można zapisać jako workspace:

```text
wyklad/
├── CLAUDE.md
├── CONTEXT.md
├── _config/
│   ├── styl.md
│   └── design-system.md
└── stages/
    ├── 01_transkrypcja/output/
    ├── 02_pytania/output/
    ├── 03_materialy/output/
    └── 04_slajdy/output/
```

Nagranie i wyniki danego przebiegu trafiają do warstwy 4. Styl, fonty i zasady prezentacji pozostają w warstwie 3. Agent może wykonać całość albo tylko wskazany etap; człowiek może poprawić transkrypcję czy plan slajdów przed dalszym przetwarzaniem. Powtarzalny workflow powinien mieć wyraźne granice etapów i artefakt, który warto przejrzeć po każdym z nich.

Źródła: [referencyjne workspace'y](https://github.com/RinDig/Interpretable-Context-Methodology/tree/main/workspaces), [kryteria dobrego workspace'u](https://github.com/RinDig/Interpretable-Context-Methodology#what-makes-a-good-workspace).

## Co jest twierdzeniem autorów, a co faktem

**Bezpośrednio wynika z implementacji:** pliki są czytelne i wersjonowalne; można je edytować bez zmiany kodu; struktura repozytorium zawiera działające przykłady i jest udostępniona na licencji MIT. ICM jest więc przenośną konwencją dla [[Praca z harnessem|pracy z harnessem]], a nie osobnym modelem AI.

**Twierdzenia autorów wymagające walidacji lokalnej:** że wybiórczy kontekst obniża koszt, przyspiesza pracę i poprawia jakość; że ten sam workspace jest praktycznie niezależny od modelu; oraz że osoby nietechniczne mogą łatwiej utrzymywać taki system. Artykuł opisuje doświadczenia praktyków, ale sam przyznaje, że obserwacje pochodzą z samoopisów w małej, samozgłaszającej się społeczności. Nie przeprowadzono kontrolowanego porównania ICM z monolitycznym promptem, a testy obejmowały jedną rodzinę modeli Claude.

Wniosek praktyczny: traktuj ICM jako hipotezę architektoniczną i mierz ją na własnym zadaniu — czas, tokeny, liczbę poprawek, poprawność artefaktów i łatwość audytu. Sam układ folderów nie gwarantuje jakości modelu, bezpieczeństwa danych ani poprawności treści.

Źródła: [repozytorium i licencja](https://github.com/RinDig/Interpretable-Context-Methodology), [zagrożenia dla trafności i brak kontrolowanego testu](https://arxiv.org/html/2603.16021#S4.SS6), [otwarte pytania o inne modele](https://arxiv.org/html/2603.16021#S6).

## Gdzie ICM pasuje

Dobry kandydat jest jednocześnie:

1. **sekwencyjny** — etap 2 korzysta z wyniku etapu 1;
2. **powtarzalny** — ten sam proces działa na kolejnych wejściach;
3. **przeglądalny** — człowiek ma sensowny punkt kontroli między etapami;
4. **plikowy** — stan i artefakty można wygodnie utrzymać jako pliki.

Nie jest to zamiennik frameworka przy komunikacji agentów w czasie rzeczywistym, wysokiej współbieżności, kolejkach wielu użytkowników ani złożonym automatycznym routingu i rozgałęzieniach. W takich przypadkach potrzebny jest kod, izolacja stanu i infrastruktura; ICM może nadal opisywać kontekst, ale nie zastąpi warstwy wykonawczej.

Źródła: [gdzie metoda działa i gdzie nie działa](https://arxiv.org/html/2603.16021#S5).

## Reguły wdrożeniowe

1. Zacznij od rzeczywistego, powtarzalnego procesu, nie od abstrakcyjnego „agenta”.
2. Rozpisz naturalne punkty przekazania i kontroli człowieka.
3. Każdemu etapowi daj kontrakt `Inputs → Process → Outputs`; przy pracy kreatywnej dodaj checkpoint i audyt.
4. Oddziel stabilne reguły od danych pojedynczego wykonania.
5. Wskaż jedno kanoniczne miejsce dla każdej reguły; w innych plikach używaj odnośników.
6. Routuj do sekcji, nie automatycznie do całych dużych plików.
7. Mechaniczne operacje — pobieranie, konwersję, walidację formatu, wysyłkę — zostaw skryptom; modelowi powierz osąd i transformację treści.
8. Przetestuj cały przebieg i zachowaj wyniki pośrednie w Git, jeśli polityka danych na to pozwala.

Zobacz też [[Harnessy]] oraz [[Praca z harnessem]].

Źródła: [kanoniczne konwencje ICM](https://github.com/RinDig/Interpretable-Context-Methodology/blob/main/_core/CONVENTIONS.md), [README i zasady kontrybucji](https://github.com/RinDig/Interpretable-Context-Methodology#contributing).
