---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Fri Sep 18 22:27:31 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2101075672747970901"
kategoria: "Inżynieria kontekstu / Zarządzanie pamięcią agenta"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Auto-compact vs. ręczne mikro-optymalizacje kontekstu w erze szybkiego osądu modeli

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Fri Sep 18 22:27:31 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2101075672747970901)
- **Konwersacja:** Odpowiedź w dyskusji (@seflless)
- **Kluczowe pojęcia:** [[Harness|Auto-compact]] [[Context Compaction|Zarządzanie oknem kontekstowym]] [[Harness|Koszt i latencja osądu modelu]] [[Prompt Architecture|Mikro-optymalizacja promptu]] [[Context Compaction|Inżynieria kontekstu]]

---

## Kontekst i problem
Dyskusja dotyczy strategii zarządzania oknem kontekstowym w systemach agentowych. Autor od dawna rekomendował poleganie na automatycznej kompakcji kontekstu (auto compact) zamiast ręcznego, drobiazgowego dostrajania zawartości promptu. Argumentował, że czas człowieka powinien być przeznaczany na decyzje strategiczne ('co dalej robić'), a nie na mikro-optymalizacje. Jednak wraz z pojawieniem się nowej generacji modeli (określanej jako 'Jev') koszt i czas osądu (judgment) spadły tak drastycznie, że ręczna, świadoma ocena kontekstu stała się tak tania i szybka, iż nie ma już powodu, by z niej rezygnować.

## Rada inżynierska
Domyślnie stosuj automatyczną kompakcję kontekstu (auto compact) i nie marnuj czasu człowieka na ręczne mikro-optymalizacje promptu — priorytetem jest decyzja 'co dalej'. Gdy jednak dostępny model oferuje bardzo szybki i tani osąd (judgment), warto włączyć świadomą, ręczną ocenę kontekstu, ponieważ koszt tej operacji przestał być barierą. Reguła: dobór strategii zarządzania kontekstem powinien zależeć od aktualnego kosztu i latencji osądu modelu, a nie być stały.

## Uwaga / Anty-wzorzec
Anty-wzorzec: traktowanie strategii zarządzania kontekstem jako niezmiennej reguły. Zalecenie 'zawsze auto compact' było słuszne przy wysokim koszcie osądu, ale staje się suboptymalne, gdy osąd jest tani i szybki — wtedy rezygnacja z ręcznej oceny kontekstu oznacza utratę darmowej jakości. Odwrotnie: ręczne mikro-optymalizacje przy drogim osądzie to marnowanie czasu człowieka na zadania, które model rozwiąże sam.

## Oryginalny cytat
> *""just auto compact" has actually been my recommendation all along, because i think our human time should be spent on "what to do next", not these micro optimizations

that changed with Jev. the judgment becomes so fast and cheap that there's no reason not to get it"*
