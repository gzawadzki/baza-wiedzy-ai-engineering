---
typ: pojęcie
aliases: [Step-by-step verification, Weryfikacja pośrednia]
tagi: [weryfikacja, jakosc, harness, agenci]
źródła:
  - "[[Kun Chen — Baza Wskazówek i Komentarzy]]"
---

# Weryfikacja krokowa

**Weryfikacja krokowa** to podejście architektoniczne, w którym poprawność działania agenta jest sprawdzana na bieżąco po każdym atomowym podkroku, zamiast jednorazowej walidacji dopiero na samym końcu długiego łańcucha wykonania.

## Zasada działania

1. Agent dzieli zadanie na sekwencję kroków.
2. Po wykonaniu pojedynczego kroku (np. edycja jednego pliku, migracja schematu) następuje natychmiastowe uruchomienie szybkiego testu, lintera lub osądu weryfikatora.
3. Jeśli krok zawodzi, naprawa następuje w obrębie małego kontekstu tego kroku, zapobiegając nawarstwianiu się błędów.

## Selektywność weryfikacji

Weryfikacja krokowa nie oznacza ślepego sprawdzania wszystkiego. Stosuje się [[Selektywna weryfikacja kodu|selektywną weryfikację kodu]] — tylko krytyczne lub nieodwracalne zmiany wymagają twardych blokad wykonania.

## Powiązane

- [[Weryfikator]]
- [[Selektywna weryfikacja kodu]]
- [[Harness]]
