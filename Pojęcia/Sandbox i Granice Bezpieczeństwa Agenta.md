---
typ: pojęcie
aliases: [Agent Sandbox, Izolacja środowiska, Bezpieczeństwo agenta, Środowisko wykonawcze]
tagi: [bezpieczenstwo, agenci, harness, sandbox, konteneryzacja]
źródła:
  - "[[simonw — Baza Wskazówek i Komentarzy]]"
  - "[[DrJimFan — Baza Wskazówek i Komentarzy]]"
---

# Sandbox i Granice Bezpieczeństwa Agenta

W inżynierii systemów agentowych istnieje fundamentalna zasada bezpieczeństwa: **zaufanie do agenta buduje się przez twardą izolację środowiska wykonawczego (Sandbox), a nie przez instrukcje w system promptcie**.

## Dlaczego system prompt nie zabezpiecza agenta

Próba zabezpieczenia autonomicznego agenta słowami (np. *"nie usuwaj plików poza katalogiem roboczym"* lub *"nie wykonuj niebezpiecznych komend"*):
- Zawsze może zostać przełamana przez **Prompt Injection** ukryty w danych wejściowych (strona internetowa, logi, pliki z kodem).
- Model nie rozróżnia w sposób gwarantowany instrukcji od danych (*data-instruction confusion*).

## Zasady twardego sandboxingu

Według doświadczeń Simona Willisona i Jima Fana:
1. **Izolacja na poziomie systemu operacyjnego:** Kontenery (Docker), mikro-maszyny wirtualne (Firecracker) lub środowiska typu gVisor.
2. **Brak dostępu do sieci produkcyjnej:** Agent uruchamiający kod powinien mieć zablokowany dostęp do wewnętrznych endpointów, zmiennych środowiskowych i kluczy API maszyny-matki.
3. **Safety Envelope i zamrożona telemetria:** W systemach fizycznych lub krytycznych (np. robotyka u DrJimaFana) kod harnessu twardo ogranicza zasięg ruchów i zużycie zasobów (MRU/MTU), ignorując jakiekolwiek polecenia modelu wykraczające poza bezpieczną kopertę.

## Powiązane

- [[Harness]]
- [[Selektywna weryfikacja kodu]]
- [[CI Check Bypass Confirmation]]
