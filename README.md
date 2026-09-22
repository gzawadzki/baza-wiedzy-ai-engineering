# AI Engineering Knowledge Repository and Intelligence Pipeline

Wiedza o inżynierii systemów AI, architekturze kontekstu i orkiestracji agentów w Obsidianie z automatycznym modułem ekstrakcji z X/Twittera.

## Struktura projektu

- `extractor/` — skrypt Python pobierający tweety przez Apify, z wielowymiarowym filtrem TypeSafe Jev (Score + Choice) oraz równoległą analizą DeepSeek / LLM.
- `Pojęcia/`, `Narzędzia/`, `Procesy/`, `Zasady/`, `Źródła/` — bezpośrednia zawartość skarbca Obsidiana (`00 Start.md` jako punkt wejścia).

## Uruchomienie ekstraktora

```bash
cd extractor
pip install -r requirements.txt
cp .env.example .env
python extract_kunchen_tips.py --analyze-only
```
