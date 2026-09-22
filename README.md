# AI Engineering Knowledge Base & Obsidian Extractor

Wiedza techniczna o inżynierii systemów AI, agentach, architekturze kontekstu oraz narzędzia automatyzacji ekstrakcji wiedzy do formatu Obsidiana.

---

## 🚀 Co znajduje się w repozytorium

### 1. Automatyczny Ekstraktor Wiedzy z X/Twittera (`scripts/`)
Zaawansowany pipeline do destylacji wiedzy inżynierskiej:
- **Apify** do pobierania autorskich wpisów i technicznych komentarzy (replies),
- **TypeSafe Jev** (model System One) jako błyskawiczny filtr wstępny oceniający potencjał merytoryczny wpisu (`noul`),
- **Równoległe wywołania DeepSeek / LLM** (`ThreadPoolExecutor`) do precyzyjnej ekstrakcji reguł, anty-wzorców i cytatów,
- **Automatyczny eksport do Markdown Obsidiana** z kategoryzacją i spójną siecią wikilinków.

Więcej szczegółów w [scripts/README.md](scripts/README.md).

### 2. Vault Obsidiana — Architektura i Pojęcia
Ustrukturyzowana baza pojęć inżynierii agentowej:
- **Architektura kontekstu:** `Context Compaction`, `Bezpieczny punkt kompaktowania`, `Persistencja stanu agenta`, `Interpretable Context Methodology (ICM)`.
- **Systemy agentowe:** `Firstmate i Agenci Wykonawczy`, `CI Check Bypass Confirmation`, `Prompt Architecture`, `Stabilność modeli i przestrzeganie promptu`.
- **Weryfikacja i ewaluacja:** `Rework Rate`, `Selektywna weryfikacja kodu (no-mistakes)`, `Eval Set z realnych sesji`, `Weryfikator`, `Harness`.
- **Modele i narzędzia:** `Jev`, `TypeSafe — przewodnik praktyczny`, `LM Studio i OpenRouter`.

---

## 🛠️ Szybki start ze skryptem

```bash
cd scripts
pip install -r requirements.txt
cp .env.example .env
# uzupełnij klucze w .env (Apify, OpenRouter/DeepSeek, TypeSafe)
python extract_kunchen_tips.py --analyze-only
```

Zacznij przeglądanie bazy od `00 Start.md`.
