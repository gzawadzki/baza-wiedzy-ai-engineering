---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Mon Sep 21 03:34:19 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2101877657927655730"
kategoria: "Inżynieria kontekstu / zarządzanie pamięcią agenta"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Kompakcja kontekstu sterowana sygnałem agenta zamiast ręcznego triggera

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Mon Sep 21 03:34:19 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101877657927655730)
- **Konwersacja:** Odpowiedź w dyskusji (@kunchenguid)
- **Kluczowe pojęcia:** [[Context Compaction]] [[Context Compaction|Zarządzanie kontekstem agenta]] [[Harness|Harness agentowy]] [[Harness|Event-driven triggers w agentach]] [[Harness|Degradacja jakości przy przepełnionym kontekście]]

---

## Kontekst i problem
Wpis jest odpowiedzią pod dyskusją o strategiach kompakcji (compaction) okna kontekstowego w harnessach agentowych. Autor zestawia alternatywę wobec ręcznego/zaplanowanego wywoływania kompakcji: pozostawienie decyzji o momencie kompakcji samemu systemowi/agentowi (tu nazwanemu 'Jev'), który sygnalizuje, kiedy kontekst wymaga redukcji.

## Rada inżynierska
Zamiast sztywnego progu (np. 'kompaktuj co N tokenów' lub ręcznego wywołania przez użytkownika), wpuść do harnessu mechanizm, w którym agent sam wykrywa narastające przeciążenie kontekstu i emituje sygnał do kompakcji. To podejście event-driven lepiej dopasowuje się do realnego tempa zapełniania kontekstu i unika albo przedwczesnej utraty informacji, albo degradacji jakości przez przepełnione okno.

## Uwaga / Anty-wzorzec
Ryzyko: oddanie decyzji o kompakcji w ręce samego modelu bez zewnętrznego weryfikatora może prowadzić do zbyt późnej lub zbyt agresywnej kompakcji (utrata istotnego stanu zadania). Wymaga to obserwowalności (metryki zużycia kontekstu, logi triggerów) i fallbacku na próg twardy.

## Oryginalny cytat
> *"oh alternatively, which is what i do right now - let Jev tell you when to compact"*
