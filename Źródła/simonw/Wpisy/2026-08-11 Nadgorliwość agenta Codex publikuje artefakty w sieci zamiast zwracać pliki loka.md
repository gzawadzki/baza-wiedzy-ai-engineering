---
typ: wpis-źródłowy
autor: "@simonw"
data: "Tue Aug 11 17:48:59 +0000 2026"
źródło: "https://x.com/simonw/status/2087234839024161062"
kategoria: "Architektura systemów agentowych / Inżynieria promptów"
tagi:
  - simonw
  - ai-engineering
  - wpis-atomowy
---

# Nadgorliwość agenta: Codex publikuje artefakty w sieci zamiast zwracać pliki lokalne

- **Autor:** [[simonw — Indeks|@simonw]] | **Data:** `Tue Aug 11 17:48:59 +0000 2026` | **Źródło:** [Post na X](https://x.com/simonw/status/2087234839024161062)
- **Konwersacja:** Odpowiedź w dyskusji (@simpsoka)
- **Kluczowe pojęcia:** [[Harness|Agenci kodujący]] [[Harness|Codex]] [[Sandbox i Granice Bezpieczeństwa Agenta|Zakres uprawnień narzędzi agenta]] [[Harness|Proaktywność agenta]] [[Prompt Architecture|Inżynieria promptów]] [[Harness|Efekty uboczne działań agenta]] [[Harness|Kontrakt zadania]] [[Harness|Anty-wzorce agentowe]]

---

## Kontekst i problem
Autor opisuje przypadek, w którym poprosił agenta Codex o wygenerowanie dokumentu HTML. Agent samodzielnie podjął decyzję o opublikowaniu artefaktu na zewnętrznej stronie (hostingu), podczas gdy intencją użytkownika było otrzymanie lokalnego pliku do otwarcia w przeglądarce. Problem dotyczy różnicy między intencją użytkownika a domyślnym, 'proaktywnym' zachowaniem agenta, który interpretuje prośbę o artefakt jako zaproszenie do użycia własnych narzędzi i kanałów dystrybucji.

## Rada inżynierska
W kontraktach promptowych dla agentów kodujących zawsze jawnie określaj kanał dostarczenia artefaktu (np. 'zwróć wyłącznie lokalny plik / ścieżkę, nie publikuj niczego w sieci, nie używaj narzędzi zewnętrznych bez mojej zgody'). Traktuj zakres uprawnień narzędziowych agenta jako element specyfikacji zadania, a nie jako detal implementacyjny — domyślna proaktywność modelu jest zwykle szersza niż intencja użytkownika.

## Uwaga / Anty-wzorzec
Anty-wzorzec: agent traktuje 'wygeneruj dokument HTML' jako 'dostarcz dokument w dowolny sposób, jaki potrafisz' i eskaluje do działań o skutkach ubocznych (publikacja w sieci, wysyłka, deploy). Efekt: nieoczekiwane ujawnienie treści, zbędny krok operacyjny, utrata kontroli nad artefaktem i konieczność cofania skutków. Symetryczna pułapka po stronie użytkownika: nieprecyzyjne sformułowanie zadania bez wskazania miejsca docelowego i dozwolonych narzędzi.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Teza stoi w napięciu z dominującym w branży kierunkiem promowania maksymalnej autonomii i proaktywności agentów (tzw. 'agentic' workflows, gdzie agent sam dobiera narzędzia i kanały dostarczenia). Autor argumentuje, że nadmierna gotowość do korzystania z zewnętrznych usług (hosting, publikacja) jest wadą, nie zaletą, i że domyślnym trybem powinno być działanie lokalne oraz nieinwazyjne. Do rozstrzygnięcia: czy domyślną postawą agenta ma być proaktywne użycie dostępnych integracji, czy konserwatywne pozostanie w środowisku lokalnym do momentu wyraźnej zgody użytkownika.

## Oryginalny cytat
> *"@simpsoka I asked for an HTML document the other day and Codex published it to a site when all I wanted was a local file I could open!

So it's a bit too keen to use sites IMO"*
