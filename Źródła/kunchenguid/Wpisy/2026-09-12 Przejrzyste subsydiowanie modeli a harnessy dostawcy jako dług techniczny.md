---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Sat Sep 12 19:22:48 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2098854862788440308"
kategoria: "Ekonomia i strategia dostawców modeli / Architektura harnessów"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Przejrzyste subsydiowanie modeli a harnessy dostawcy jako dług techniczny

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Sat Sep 12 19:22:48 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2098854862788440308)
- **Kluczowe pojęcia:** [[Harness]] [[Harness|Model-agnostic harness]] [[Harness|Vendor lock-in]] [[Harness|Zbieranie danych treningowych]] [[Harness|Przejrzystość subsydiowania modeli]] [[Context Compaction|Inżynieria kontekstu]]

---

## Kontekst i problem
Autor komentuje praktykę dostawców modeli (np. Anthropic, OpenAI), którzy oferują atrakcyjne ceny tylko w połączeniu z własnym harnessem, który przy okazji po cichu zbiera dane lub wysyła kod użytkownika. Kontrastuje to z modelem cenowym Meta (muse spark), gdzie subsydiowanie jest jawnie oznaczone dla określonego tieru kontrybutorów, a zbieranie danych jest opcjonalne i wycenione. Problem: użytkownik płaci za niższą cenę utratą kontroli nad danymi i fragmentacją własnego środowiska pracy.

## Rada inżynierska
Traktuj harness jako warstwę wymienną, a nie część umowy z dostawcą modelu: buduj setup wokół harnessów niezależnych od dostawcy (pi, opencode, hermes, openclaw, Claude Code, Codex), które można skonfigurować pod dowolny model. Od dostawcy wymagaj rozdzielenia dwóch decyzji: (1) ile kosztuje token, (2) czy i kiedy zbierane są dane treningowe — oraz jawnej wyceny tej wymiany. Subsydiowanie powinno być etykietowane per tier (np. tier kontrybutora), a nie ukryte w regulaminie harnessa.

## Uwaga / Anty-wzorzec
Uzależnienie się od harnessa dostawcy tylko po to, by dostać lepszą cenę: prowadzi to do vendor lock-in, ukrytego eksfiltrowania kodu i danych, fragmentacji toolchainu (własne pluginy, konfiguracja, CI) oraz długu technicznego po stronie dostawcy, który nie wnosi realnej wartości ponad istniejące, dojrzałe harnessy. Brak jasnej informacji, kiedy dane są zbierane, a kiedy nie, uniemożliwia świadomą decyzję.

## ⚡ Kwestia sporna / do rozstrzygnięcia
Teza stoi w sprzeczności z dominującym konsensusem branżowym, w którym dostawcy modeli wiążą korzystną cenę z użyciem własnego harnessa i domyślnym zbieraniem danych ('data-for-discount'). Autor twierdzi, że subsydiowanie da się rozdzielić od harnessa i że harness dostawcy jest długiem technicznym, a nie przewagą — do rozstrzygnięcia: czy istnieje ekonomicznie trwały model sprzedaży modeli bez pośrednictwa własnego harnessa, oraz czy niezależne harnessy rzeczywiście pokrywają pełen zakres funkcji (np. specyficzne narzędzia, pamięć, cache promptów) oferowanych przez harnessy pierwszej strony.

## Oryginalny cytat
> *""every model provider should learn from meta's pricing model for muse spark, with fully transparent subsidization labeled for the contributor tier

stop doing "in order to use our model at a good price, you must use our harness which secretly collects your data and/or upload your codebase"

meta clearly proved there's a way to collect training data without relying on a harness. just be transparent about when you collect data vs not, clearly communicate how much the data is worth, and give the choice to the user

and i really don't need your harness. i already have SO MANY state of the art harnesses to pick from. pi, opencode, hermes, openclaw, and even claude code and codex can be configured to use any model. your own harness is a tech debt that fragments my setup and doesn't add much value""*
