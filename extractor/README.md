# Ekstraktor porad Kuna Chena (@kunchenguid)

Narzędzie do automatycznego pobierania autorskich wpisów oraz technicznych komentarzy (replies) **Kuna Chena** (@kunchenguid) z Twittera/X przez **Apify**, ich merytorycznej analizy przez LLM oraz zapisu do bazy wiedzy Obsidiana.

---

## 1. Instalacja zależności

Wymagany Python 3.10+:

```bash
pip install -r scripts/requirements.txt
```

---

## 2. Konfiguracja (`scripts/.env`)

Skopiuj plik szablonu:
```bash
cp scripts/.env.example scripts/.env
```

Wypełnij plik `scripts/.env`:
```ini
# Token Apify (darmowy, z https://console.apify.com/account#/integrations)
APIFY_API_TOKEN=apify_api_xxx

# Konfiguracja LLM (OpenRouter, OpenAI lub LM Studio)
OPENAI_API_KEY=twoj_klucz_api
OPENAI_BASE_URL=https://openrouter.ai/api/v1
MODEL_NAME=deepseek/deepseek-chat
MAX_LLM_WORKERS=4

# Jev / TypeSafe jako szybki filtr przed DeepSeek
TYPESAFE_API_KEY=twoj_typesafe_api_key
JEV_MODEL=jev-latest
JEV_VALUABLE_THRESHOLD=0.65
JEV_BATCH_SIZE=25

# Parametry
TWITTER_HANDLE=kunchenguid
MAX_TWEETS=80
```

> **Wskazówka:** Jeśli chcesz użyć lokalnego **LM Studio**:
> ```ini
> OPENAI_BASE_URL=http://localhost:1234/v1
> OPENAI_API_KEY=not-needed
> MODEL_NAME=twoj-model-w-lm-studio
> ```

---

## 3. Uruchomienie

### Standardowe wykonanie (Pobranie + filtr Jev + równoległa analiza DeepSeek/LLM + Eksport Markdown)
```bash
python scripts/extract_kunchen_tips.py
```

Jev najpierw ocenia, które wpisy są warte ekstrakcji (`noul >= JEV_VALUABLE_THRESHOLD`), a dopiero potem kandydaci trafiają równolegle do DeepSeek/LLM (`MAX_LLM_WORKERS`).

### Tryb oszczędzania kredytów / testowania:

1. **Tylko pobranie z Apify do cache JSON** (bez zużywania tokenów LLM):
   ```bash
   python scripts/extract_kunchen_tips.py --fetch-only
   ```
   Zapisze pobrane tweety w `scripts/kunchenguid_raw_tweets.json`.

2. **Tylko analiza z pliku cache** (bez ponownego odpytywania Apify):
   ```bash
   python scripts/extract_kunchen_tips.py --analyze-only
   ```
   Pozwala eksperymentować z progiem Jev, liczbą równoległych wywołań i promptem bez ponownego płacenia za scraping X.

3. **Zmiana równoległości DeepSeek/LLM:**
   ```bash
   python scripts/extract_kunchen_tips.py --analyze-only --llm-workers 8
   ```

4. **Zmiana progu Jev lub pominięcie Jev:**
   ```bash
   python scripts/extract_kunchen_tips.py --analyze-only --jev-threshold 0.75
   python scripts/extract_kunchen_tips.py --analyze-only --skip-jev
   ```

5. **Zmiana liczby pobieranych tweetów:**
   ```bash
   python scripts/extract_kunchen_tips.py --max-tweets 150
   ```

---

## 4. Efekt w Obsidianie

Wynik trafia bezpośrednio do katalogu `Źródła/`:
Plik: `Źródła/Kun Chen — Baza Wskazówek i Komentarzy.md`

Zawiera:
- Podział tematyczny (Architektura promptów, Weryfikacja i harnessy, Kontekst i drift, Pętle agentowe),
- Zrekonstruowany kontekst posta nadrzędnego (dla komentarzy/replies pod wpisami innych),
- Wskazówkę inżynierską i anty-wzorce,
- Bezpośredni link źródłowy do wpisu na X,
- Wikilinki (`[[Harness]]`, `[[Weryfikator]]` itp.) łączące wpisy z Twoją bazą wiedzy.
