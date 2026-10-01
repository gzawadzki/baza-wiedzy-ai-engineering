---
typ: wpis-źródłowy
autor: "@teortaxesTex"
data: "Tue Sep 22 23:46:53 +0000 2026"
źródło: "https://x.com/teortaxesTex/status/2102545198199038197"
kategoria: "Inżynieria kontekstu / Zarządzanie pamięcią / KV cache"
tagi:
  - teortaxestex
  - ai-engineering
  - wpis-atomowy
---

# Kompakcja KV cache po stronie treningu redukuje potrzebę agresywnego zarządzania kontekstem

- **Autor:** [[teortaxesTex — Indeks|@teortaxesTex]] | **Data:** `Tue Sep 22 23:46:53 +0000 2026` | **Źródło:** [Post na X](https://x.com/teortaxesTex/status/2102545198199038197)
- **Konwersacja:** Odpowiedź w dyskusji (@awesome_ruler_)
- **Kluczowe pojęcia:** [[Architektura KV Cache i Rozumowanie Latentne|KV cache]] [[Context Compaction|Inżynieria kontekstu]] [[Context Compaction|Compaction / kompakcja treningowa]] [[Context Compaction|Budżet kontekstu]] [[Test-Time Compute i Reasoning Tokens|Reasoning loop / iteracyjne rozumowanie]] [[Harness|Zarządzanie pamięcią agenta]]

---

## Kontekst i problem
Dyskusja dotyczy opłacalności utrzymywania długiego kontekstu i rozmiaru pamięci podręcznej KV. Wcześniej dominowało założenie, że duży cache KV wymusza agresywne strategie: przycinanie kontekstu, okna przesuwne, kompresję KV, selektywne zapamiętywanie. Autor zauważa, że wraz z postępem w kompakcji na etapie treningu (modele uczą się efektywniej reprezentować stan) oraz przy realnym koszcie ~890 MB na 1M tokenów kontekstu, główny bottleneck zniknął. Wniosek: nie trzeba już wycinać historii ani 'oszczędzać' kontekstu — można po prostu dopisywać kolejne wyjścia i kontynuować rozumowanie.

## Rada inżynierska
Przy planowaniu budżetu kontekstu licz realny koszt KV cache w bajtach na token (tu: ~890 MB / 1M tokenów ≈ ~890 B/token, co sugeruje mocno skwantyzowany/podzielony cache). Jeśli ten koszt jest niski dzięki dobrej kompakcji treningowej, odstąp od heurystyk przycinania i kompresji — pozwól modelowi iterować rozumowanie na pełnym, narastającym kontekście. Utrzymywanie ciągłego 'reasoning with outputs' (dopisywanie wyjść jako kolejnych kroków) jest tańsze niż reinżynieria pamięci.

## Uwaga / Anty-wzorzec
Anty-wzorzec: projektowanie harnessu wokół przestarzałego założenia, że cache KV jest głównym ograniczeniem, i stosowanie agresywnego pruningu/okien przesuwnych, które kasują istotny kontekst, mimo że infrastruktura już to wytrzymuje. Trzymanie się starych optymalizacji kosztem jakości rozumowania to marnowanie potencjału modelu.

## Oryginalny cytat
> *"@awesome_ruler_ @industriaalist @jayden_teoh_ Well, smaller cache doesn't matter much now
we're starting to have good training compaction, and at 890 Mb/1M context, you can just keep reasoning with outputs"*
