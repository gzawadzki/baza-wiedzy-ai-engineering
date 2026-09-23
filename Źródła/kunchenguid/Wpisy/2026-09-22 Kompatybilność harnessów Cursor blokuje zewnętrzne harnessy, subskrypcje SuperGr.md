---
typ: wpis-źródłowy
autor: "@kunchenguid"
data: "Tue Sep 22 03:40:58 +0000 2026"
źródło: "https://x.com/kunchenguid/status/2102241720826204224"
kategoria: "Architektura harnessów / Narzędzia agentowe"
tagi:
  - kunchenguid
  - ai-engineering
  - wpis-atomowy
---

# Kompatybilność harnessów: Cursor blokuje zewnętrzne harnessy, subskrypcje SuperGrok nie

- **Autor:** [[kunchenguid — Indeks|@kunchenguid]] | **Data:** `Tue Sep 22 03:40:58 +0000 2026` | **Źródło:** [Post na X](https://x.com/kunchenguid/status/2102241720826204224)
- **Konwersacja:** Odpowiedź w dyskusji (@tanishqk)
- **Kluczowe pojęcia:** [[Harness]] [[Harness|Agent Architecture]] [[Harness|Third-party harness]] [[Harness|Cursor]] [[Harness|SuperGrok]] [[Harness|Agentic Loop]]

---

## Kontekst i problem
Wątek dotyczy możliwości podłączenia własnego (zewnętrznego, third-party) harnessu agentowego do różnych środowisk i modeli. Autor odpowiada na wpis @tanishqk, wskazując różnicę w polityce dostępu między Cursorem a subskrypcją SuperGrok.

## Rada inżynierska
Przy wyborze stacku agentowego weryfikuj nie tylko dostępność modelu, ale i to, czy dany dostawca pozwala na uruchomienie własnego (third-party) harnessu. Cursor celowo ogranicza użycie zewnętrznych harnessów, podczas gdy subskrypcje SuperGrok na to pozwalają — co czyni je praktyczniejszym wyborem, gdy potrzebujesz niestandardowej pętli agentowej, własnego orkiestratora lub zewnętrznego weryfikatora zamiast wbudowanego przepływu dostawcy. Traktuj politykę dostępu do harnessu jako kryterium architektoniczne pierwszego rzędu, nie jako detal konfiguracyjny.

## Uwaga / Anty-wzorzec
Zakładanie, że skoro dany model jest dostępny w narzędziu, to można go swobodnie osadzić we własnym harnessie. Ograniczenia platformy (np. Cursor) potrafią zablokować third-party harness niezależnie od dostępności modelu, co wymusza przeprojektowanie lub migrację stacku.

## Oryginalny cytat
> *"cursor doesn't allow 3p harness but supergrok subs do. i'm using through my supergrok"*
