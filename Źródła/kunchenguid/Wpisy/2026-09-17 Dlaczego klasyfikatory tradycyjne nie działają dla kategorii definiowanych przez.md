---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Thu Sep 17 15:35:36 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2100609623531421915"
kategoria: "Architektura systemów agentowych / Inżynieria kontekstu"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Dlaczego klasyfikatory tradycyjne nie działają dla kategorii definiowanych przez użytkownika

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Thu Sep 17 15:35:36 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2100609623531421915)
- **Konwersacja:** Odpowiedź w dyskusji (@winterspeak)
- **Kluczowe pojęcia:** [[Harness|Dynamiczna klasyfikacja in-context]] [[Harness|Open-label classification]] [[Harness|Zero-shot i few-shot klasyfikacja LLM]] [[Harness|Kategorie definiowane przez użytkownika]] [[Harness|Kiedy LLM zamiast klasyfikatora ML]]

---

## Kontekst i problem
Autor odpowiada na sugestię @winterspeak, że problem klasyfikacji można rozwiązać tradycyjnym klasyfikatorem (np. nadzorowanym modelem ML). Wyjaśnia, że w jego przypadku kategorie są definiowane przez użytkownika i są całkowicie dowolne (freeform), co czyni klasyfikator trenowany z góry bezużytecznym — nie da się wytrenować jednego modelu pokrywającego wszystkie możliwe kategorie każdego użytkownika, ani oczekiwać, że każdy użytkownik wytrenuje własny model.

## Rada inżynierska
Gdy kategorie/etykiety są definiowane dynamicznie przez użytkownika i są dowolne (freeform), NIE używaj klasyfikatora nadzorowanego ani stałego zestawu klas — zamiast tego klasyfikację realizuj przez model językowy warunkowany kontekstem (prompt/few-shot/embeddings zależne od definicji użytkownika). Klasyfikacja musi być rozwiązywana jako zadanie in-context, a nie jako trenowany model offline.

## Uwaga / Anty-wzorzec
Anty-wzorzec: zakładanie, że tradycyjny klasyfikator (fixed-label ML) rozwiąże problem klasyfikacji w systemie z otwartym zbiorem kategorii. Prowadzi to do dwóch ślepych uliczek: (1) próby wytrenowania uniwersalnego modelu dla wszystkich użytkowników — niemożliwe przy dowolnych, prywatnych taksonomiach; (2) przerzucanie ciężaru treningu na użytkownika — nieakceptowalne UX i kosztowo nieefektywne.

## Oryginalny cytat
> *"@winterspeak not exactly - if you think about the use case i have here, the categories are user-defined and completely freeform

there’s no way i can train a traditional classifier that will work for every user, and there’s no way every user will train their own classifier"*
