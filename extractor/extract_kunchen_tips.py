#!/usr/bin/env python3
"""
Ekstraktor porad i wskazówek Kuna Chena (@kunchenguid) z X/Twittera.
Wykorzystuje Apify (apidojo/tweet-scraper) do pobrania wpisów i komentarzy,
a następnie LLM do destylacji wiedzy i zapisu w formacie Markdown dla Obsidiana.
"""

import os
import sys
import re
import json
import logging
import argparse
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Zapewnienie poprawnego kodowania UTF-8 na Windowsie
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Inicjalizacja trwałego logowania operacji
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
STATE_LOGS_DIR = PROJECT_ROOT / "state" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
STATE_LOGS_DIR.mkdir(parents=True, exist_ok=True)

FETCH_LOG_FILE = LOGS_DIR / "fetch.log"
FETCH_JSONL_FILE = LOGS_DIR / "fetch.jsonl"
STATE_FETCH_LOG_FILE = STATE_LOGS_DIR / "fetch.log"
STATE_FETCH_JSONL_FILE = STATE_LOGS_DIR / "fetch.jsonl"

logger = logging.getLogger("extractor")
logger.setLevel(logging.INFO)
if not logger.handlers:
    _log_format = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    _ch = logging.StreamHandler(sys.stdout)
    _ch.setFormatter(_log_format)
    logger.addHandler(_ch)

    _fh1 = logging.FileHandler(FETCH_LOG_FILE, encoding="utf-8")
    _fh1.setFormatter(_log_format)
    logger.addHandler(_fh1)

    _fh2 = logging.FileHandler(STATE_FETCH_LOG_FILE, encoding="utf-8")
    _fh2.setFormatter(_log_format)
    logger.addHandler(_fh2)


def log_event(event_type: str, data: Dict[str, Any]):
    """Zapisuje ustrukturyzowany rekord audytowy w formacie JSONL."""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event_type,
        **data,
    }
    line = json.dumps(record, ensure_ascii=False) + "\n"
    try:
        with open(FETCH_JSONL_FILE, "a", encoding="utf-8") as f:
            f.write(line)
        with open(STATE_FETCH_JSONL_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception as exc:
        logger.warning(f"Błąd zapisu JSONL logu: {exc}")


from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator

# Załaduj zmienne środowiskowe z pliku scripts/.env lub .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "~deepseek/deepseek-flash-latest")
TYPESAFE_API_KEY = os.getenv("TYPESAFE_API_KEY")
TYPESAFE_BASE_URL = os.getenv("TYPESAFE_BASE_URL", "https://api.typesafe.ai")
JEV_MODEL = os.getenv("JEV_MODEL", "jev-latest")
JEV_SCORE_THRESHOLD = float(os.getenv("JEV_SCORE_THRESHOLD", "1.35"))
JEV_BATCH_SIZE = int(os.getenv("JEV_BATCH_SIZE", "20"))
MAX_LLM_WORKERS = int(os.getenv("MAX_LLM_WORKERS", "4"))
DEFAULT_HANDLE = os.getenv("TWITTER_HANDLE", "kunchenguid")
CACHE_FILE = Path(__file__).parent / f"{DEFAULT_HANDLE}_raw_tweets.json"


# Model struktury wyjściowej dla pojedynczego wpisu
class ExtractedTip(BaseModel):
    is_valuable: bool = Field(
        description="True, jeśli wpis zawiera merytoryczną radę, tip techniczny, przestrogę, wyjaśnienie architektury lub wgląd w zachowanie modeli. False dla small talku, krótkich podziękowań, memów."
    )
    title: Optional[str] = Field(
        default=None,
        description="Zwięzły, techniczny tytuł porady lub problemu (po polsku)."
    )
    category: Optional[str] = Field(
        default=None,
        description="Kategoria: np. 'Architektura promptów', 'Harnessy i weryfikacja', 'Pętle agentowe', 'Kontekst i drift', 'Ewaluacja i modele', 'Narzędzia i implementacja'."
    )
    context_summary: Optional[str] = Field(
        default=None,
        description="Kontekst: na co odpowiada autor lub jaki problem rozwiązuje (szczególnie istotne przy komentarzach pod wpisami innych)."
    )
    tip: Optional[str] = Field(
        default=None,
        description="Konkretna, zdatna do wdrożenia rada lub reguła inżynierska (po polsku)."
    )
    pitfall: Optional[str] = Field(
        default=None,
        description="Anty-wzorzec, pułapka lub błąd, przed którym ostrzega (jeśli dotyczy, po polsku)."
    )
    has_conflict: bool = Field(
        default=False,
        description="True, jeśli autor prezentuje tezę sporną, podważa powszechne przekonanie branżowe, zmienia wcześniejsze zdanie lub jego teza stoi w sprzeczności z innymi powszechnymi praktykami inżynierskimi."
    )
    conflict_notes: Optional[str] = Field(
        default=None,
        description="Opis sprzeczności / kontrowersji do rozstrzygnięcia przez inżyniera (np. 'Autor zaleca X wbrew powszechnemu Y ze względu na Z')."
    )
    vault_links: List[str] = Field(
        default_factory=list,
        description=(
            "Sugerowane linki do pojęć w Obsidianie z bazy wiedzy, np.: "
            "['[[Harness]]', '[[Weryfikator]]', '[[Interpretable Context Methodology]]', '[[Jev]]', "
            "'[[Test-Time Compute i Reasoning Tokens]]', '[[Sandbox i Granice Bezpieczeństwa Agenta]]', "
            "'[[Kaskady Modeli i Routing Pewności]]', '[[Dynamiczne Skille i Metaprogramowanie Agenta]]', "
            "'[[Architektura KV Cache i Rozumowanie Latentne]]', '[[Context Compaction]]', "
            "'[[Bezpieczny punkt kompaktowania]]', '[[Persistencja stanu agenta]]', "
            "'[[Firstmate i Agenci Wykonawczy]]', '[[Rework Rate]]', '[[Eval Set z realnych sesji]]', "
            "'[[Selektywna weryfikacja kodu]]', '[[Stabilność modeli i przestrzeganie promptu]]', "
            "'[[Prompt Architecture]]']. Używaj wyłącznie trafnych pojęć z listy lub stwórz precyzyjne nowe."
        )
    )
    original_quote: Optional[str] = Field(
        default=None,
        description="Kluczowy fragment wypowiedzi w oryginalnym brzmieniu (język angielski)."
    )

    @field_validator("vault_links", mode="before")
    @classmethod
    def normalize_vault_links(cls, value: Any) -> List[str]:
        """Toleruje drobne błędy JSON modeli OpenAI-compatible, np. zagnieżdżone listy."""
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        if not isinstance(value, list):
            return []

        links: List[str] = []
        for item in value:
            if isinstance(item, str):
                links.append(item)
            elif isinstance(item, list):
                links.extend(str(nested) for nested in item if isinstance(nested, str))
        return links


def fetch_tweets_from_apify(
    handle: str, max_items: int = 80, until_date: Optional[str] = None, since_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Pobiera tweety i komentarze danego użytkownika przez Apify z trwałym logowaniem audytowym."""
    if not APIFY_API_TOKEN:
        raise ValueError(
            "Brak APIFY_API_TOKEN. Ustaw go w pliku .env lub zmiennych środowiskowych."
        )

    from apify_client import ApifyClient

    query = f"from:{handle}"
    if since_date:
        query += f" since:{since_date}"
    if until_date:
        query += f" until:{until_date}"

    logger.info(f"Łączenie z Apify (@{handle}) | query='{query}' | limit={max_items}")
    log_event("apify_fetch_started", {
        "handle": handle,
        "query": query,
        "limit": max_items,
        "since": since_date,
        "until": until_date,
    })

    client = ApifyClient(APIFY_API_TOKEN)
    actor_id = "scrape.badger/twitter-tweets-scraper"
    run_input = {
        "mode": "Advanced Search",
        "query": query,
        "query_type": "Latest",
        "max_results": max_items,
    }

    t0 = datetime.now()
    try:
        run = client.actor(actor_id).call(run_input=run_input)
    except Exception as exc:
        logger.error(f"Błąd uruchomienia aktora {actor_id}: {exc}")
        log_event("apify_fetch_error", {"handle": handle, "query": query, "error": str(exc)})
        raise

    dataset_id = getattr(run, "default_dataset_id", None)
    if not dataset_id and isinstance(run, dict):
        dataset_id = run.get("defaultDatasetId")

    if not dataset_id:
        raise RuntimeError("Nie udało się uzyskać identyfikatora datasetu z Apify.")

    dataset_items = list(client.dataset(dataset_id).iterate_items())
    dur = (datetime.now() - t0).total_seconds()

    logger.info(f"Pobrano {len(dataset_items)} surowych rekordów dla @{handle} w {dur:.2f}s (dataset: {dataset_id})")
    log_event("apify_fetch_completed", {
        "handle": handle,
        "query": query,
        "dataset_id": dataset_id,
        "items_count": len(dataset_items),
        "duration_seconds": round(dur, 2),
    })

    return dataset_items


def normalize_tweet(item: Dict[str, Any], handle: str) -> Optional[Dict[str, Any]]:
    """Normalizuje format tweeta z Apify do jednolitego schematu."""
    text = (
        item.get("full_text")
        or item.get("text")
        or item.get("displayText")
        or ""
    ).strip()

    # Odrzucenie pustych, czystych retweetów bez komentarza lub zbyt krótkich wpisów
    if not text or len(text) < 15:
        return None
    if text.startswith("RT @"):
        return None

    tweet_id = str(item.get("id") or item.get("id_str") or item.get("tweet_id") or "")
    url = (
        item.get("url")
        or item.get("twitterUrl")
        or (f"https://x.com/{handle}/status/{tweet_id}" if tweet_id else "")
    )
    created_at = (
        item.get("createdAt")
        or item.get("created_at")
        or datetime.now().strftime("%Y-%m-%d")
    )

    # Detekcja czy wpis to odpowiedź / komentarz
    in_reply_to_id = item.get("in_reply_to_status_id") or item.get("inReplyToStatusId")
    in_reply_to_user = (
        item.get("in_reply_to_screen_name")
        or item.get("inReplyToUsername")
        or (item.get("replyTo") or {}).get("username")
        or ""
    )
    conversation_id = item.get("conversation_id")

    is_reply = bool(
        in_reply_to_id
        or (conversation_id and str(conversation_id) != str(tweet_id))
        or in_reply_to_user
    )

    parent_text = (
        (item.get("replyTo") or {}).get("text")
        or (item.get("replyTo") or {}).get("full_text")
        or item.get("inReplyToText")
        or item.get("quotedText")
        or (item.get("quotedTweet") or {}).get("text")
        or ""
    )

    return {
        "id": tweet_id,
        "url": url,
        "date": created_at,
        "text": text,
        "is_reply": is_reply,
        "parent_user": in_reply_to_user,
        "parent_text": parent_text,
        "likes": item.get("favorite_count", item.get("likeCount", 0)),
        "retweets": item.get("retweet_count", item.get("retweetCount", 0)),
    }


def evaluate_with_jev(tweets: List[Dict[str, Any]], min_score: float = 1.35) -> List[Tuple[Dict[str, Any], float, str]]:
    """Używa Jev (TypeSafe System One) z dwuwymiarową oceną: Score (gęstość techniczna) + Choice (kategoria/odrzucenie)."""
    if not TYPESAFE_API_KEY:
        print("[*] Brak TYPESAFE_API_KEY — pomijam filtr Jev i kieruję wszystkie rekordy do analizy LLM.")
        return [(tweet, 2.0, "general") for tweet in tweets]

    selected: List[Tuple[Dict[str, Any], float, str]] = []
    endpoint = f"{TYPESAFE_BASE_URL.rstrip('/')}/v1/systemone"

    for start in range(0, len(tweets), JEV_BATCH_SIZE):
        batch = tweets[start:start + JEV_BATCH_SIZE]
        state = {
            "tweets": [
                {
                    "date": tw["date"],
                    "url": tw["url"],
                    "text": tw["text"],
                    "is_reply": tw["is_reply"],
                    "parent_user": tw.get("parent_user") or "",
                    "parent_text": tw.get("parent_text") or "",
                }
                for tw in batch
            ]
        }
        
        # Zgodnie z zasadami TypeSafe:
        # 1. Score do gradacji użyteczności inżynierskiej (poziomy o konkretnym znaczeniu)
        # 2. Choice do klasyfikacji domeny merytorycznej lub odrzucenia (w tym opcja no-match: none_of_these)
        questions = {}
        for i in range(len(batch)):
            questions[f"score_{i}"] = {
                "type": "score",
                "instructions": (
                    f"Rate the substantive engineering utility of `tweets[{i}]` for an AI Engineering knowledge base. "
                    "Evaluate whether it delivers concrete architectural rules, model behavioral insights, "
                    "agent harness practices, context window tactics, evaluation/eval methodology, or verifiable production anti-patterns."
                ),
                "criteria": [
                    "No technical utility: casual chatter, social gratitude, generic reaction, promotional, or empty meme.",
                    "Marginal technical utility: broad opinion, high-level commentary, or non-actionable observation.",
                    "High technical utility: concrete heuristic, specific architectural rule, failure mode analysis, evaluation design, or actionable engineering guidance."
                ],
            }
            questions[f"topic_{i}"] = {
                "type": "choice",
                "instructions": f"Identify the primary technical subject matter discussed in `tweets[{i}]`.",
                "criteria": {
                    "context_compaction": "Context window limits, session compaction, safe checkpoints, tool output pruning, caching.",
                    "agent_orchestration": "Multi-agent systems, Firstmate, leaf node agents, task routing, coordination tradeoffs.",
                    "prompt_and_models": "Prompt architecture, system prompt adherence, model spikiness vs stability, evaluation metrics.",
                    "verification_and_harness": "Harness engineering, code review rules, step-by-step verification, test bypass prevention.",
                    "evals_and_debugging": "LLM evaluation methodology, real vs synthetic eval sets, error analysis, LLM-as-a-judge failure modes, fine-tuning evals.",
                    "security_and_tools": "Prompt injection, security boundaries, sandboxing, tool calling, CLI harness, agent tooling.",
                    "embodied_and_models": "Embodied AI, world models, multimodal models, reasoning capabilities, training paradigms.",
                    "none_of_these": "Not technical, trivial social comment, off-topic, or lacks substantive AI engineering substance."
                }
            }

        payload = json.dumps({"model": JEV_MODEL, "state": state, "questions": questions}).encode("utf-8")
        request = urllib.request.Request(
            endpoint,
            data=payload,
            headers={
                "Authorization": f"Bearer {TYPESAFE_API_KEY}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            },
            method="POST",
        )

        print(f"[*] Jev ocenia wielowymiarowo batch {start + 1}-{start + len(batch)} / {len(tweets)}...")
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Błąd TypeSafe/Jev HTTP {e.code}: {body}") from e

        answers = data.get("answers", {})
        for i, tw in enumerate(batch):
            score_ans = answers.get(f"score_{i}", {})
            topic_ans = answers.get(f"topic_{i}", {})

            score_val = float(score_ans.get("score", 0.0))
            topic_choice = topic_ans.get("choice", "none_of_these")
            topic_confidence = float(topic_ans.get("confidence", 0.0))

            # Kompozycja osądów: odrzucamy rekordy poniżej progu jakości lub sklasyfikowane jako nietechniczne
            if score_val >= min_score and topic_choice != "none_of_these":
                selected.append((tw, score_val, topic_choice))

    print(f"[+] Jev wyselekcjonował {len(selected)} / {len(tweets)} wpisów (Score >= {min_score:.2f} & Choice != none_of_these).")
    return selected


def analyze_with_llm(tweet: Dict[str, Any], handle: str = "autor") -> Optional[ExtractedTip]:
    """Wysyła pojedynczy wpis/komentarz do LLM w celu ekstrakcji porady."""
    if not OPENAI_API_KEY:
        raise ValueError("Brak OPENAI_API_KEY w pliku .env lub zmiennych środowiskowych.")

    from openai import OpenAI

    client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
    )

    system_prompt = f"""Jesteś starszym inżynierem AI analizującym wpisy i komentarze autora @{handle} na Twitterze/X.
Wpisy mogą być w języku ANGIELSKIM, CHIŃSKIM (uproszczonym/tradycyjnym) lub polskim.
Twoim celem jest wyciągnięcie GĘSTEJ, PRAKTYCZNEJ WIEDZY inżynierskiej do bazy wiedzy w Obsidianie w JĘZYKU POLSKIM:
- Konkretne zasady tworzenia promptów i kompilacji (prompt architecture),
- Obserwacje zachowania modeli (drift, saturation, MoE, attention, latency, token throughput),
- Architektura harnessów, systemów agentowych, zewnętrznych weryfikatorów,
- Inżynieria kontekstu, zarządzanie pamięcią, cache i benchmarking,
- Wykrywanie anty-wzorców (co ludzie robią źle).

ZASADA WIELOJĘZYCZNOŚCI:
Jeśli wpis jest po chińsku lub angielsku, przetłumacz i zsyntetyzuj jego sens na precyzyjny, profesjonalny język polski inżynierii oprogramowania. Cytat (`original_quote`) pozostaw w oryginalnym brzmieniu (po chińsku lub angielsku).

ZASADA AKTUALNOŚCI I KWESTII SPORNYCH:
1. Jeżeli wnioski stoją w sprzeczności z wcześniejszymi wpisami, uznaj, że nowszy wpis odzwierciedla zaktualizowany stan wiedzy.
2. Jeśli autor podważa powszechny konsensus branżowy, krytykuje popularne podejście lub formułuje tezę kontrowersyjną, ustaw `has_conflict: true` i opisz w `conflict_notes` istotę sporu do rozstrzygnięcia.

Zignoruj:
- Zwykły small talk, krótkie potwierdzenia ("Yes", "cool", "ty"),
- Wpisy o charakterze czysto towarzyskim lub marketingowym bez szczegółów technicznych.

Zwróć odpowiedź w formacie JSON zgodnym ze schematem."""

    # Budowa kontekstu wiadomości
    user_content = f"Autor: @{handle}\nData wpisu: {tweet['date']}\nLink: {tweet['url']}\n"
    if tweet["is_reply"]:
        user_content += f"TYP: Komentarz / Odpowiedź pod wpisem innego użytkownika (@{tweet['parent_user'] or 'unknown'})\n"
        if tweet["parent_text"]:
            user_content += f"TREŚĆ POSTA NADRZĘDNEGO (na co odpowiada autor):\n\"{tweet['parent_text']}\"\n\n"
        else:
            user_content += "(Brak bezpośredniej treści posta nadrzędnego, oceń kontekst z samej odpowiedzi)\n\n"
    else:
        user_content += f"TYP: Autorski wpis / wątek @{handle}\n\n"

    user_content += f"TREŚĆ WPISU @{handle}:\n\"{tweet['text']}\"\n"

    # Wywołanie modelu
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.1,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": user_content
                + '\nZwróć JSON z polami:\n'
                '{\n'
                '  "is_valuable": true/false,\n'
                '  "title": "Zwięzły techniczny tytuł po polsku",\n'
                '  "category": "Kategoria tematyczna",\n'
                '  "context_summary": "Kontekst / jaki problem rozwiązuje",\n'
                '  "tip": "Główna rada / reguła inżynierska po polsku",\n'
                '  "pitfall": "Anty-wzorzec lub pułapka (opcjonalnie)",\n'
                '  "has_conflict": true/false,\n'
                '  "conflict_notes": "Zwięzły opis kwestii spornej / sprzeczności (jeśli dotyczy)",\n'
                '  "vault_links": ["[[Pojęcie]]"],\n'
                '  "original_quote": "Oryginalny cytat po angielsku"\n'
                '}',
            },
        ],
    )

    try:
        data = json.loads(response.choices[0].message.content)
        return ExtractedTip(**data)
    except Exception as e:
        print(f"[!] Błąd parsowania odpowiedzi modelu: {e}")
        return None


def slugify_title(title: str) -> str:
    """Tworzy bezpieczną nazwę pliku z tytułu porady."""
    # Usuwamy niedozwolone znaki dla systemów plików i Obsidiana (: / \ ? * < > | " # ^ [ ])
    clean = re.sub(r'[\/:*?"<>|#^\[\]]', '', title)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean[:80] if len(clean) > 80 else clean


def collect_all_notes(notes_dir: Path) -> List[Dict[str, Any]]:
    """Odczytuje wszystkie istniejące notatki atomowe z folderu, aby zachować spójność indeksu."""
    all_notes = []
    for p in sorted(notes_dir.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        m_title = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        m_cat = re.search(r"kategoria:\s*\"?([^\n\"]+)\"?", text)
        m_url = re.search(r"źródło:\s*\"?([^\n\"]+)\"?", text)
        m_conf = re.search(r"## ⚡ Kwestia sporna / do rozstrzygnięcia\s*\n+([^\n#]+)", text)
        m_links = re.search(r"- \*\*Kluczowe pojęcia:\*\*\s*(.+)$", text, re.MULTILINE)

        title = m_title.group(1).strip() if m_title else p.stem
        cat = m_cat.group(1).strip() if m_cat else "Inne obserwacje"
        url = m_url.group(1).strip() if m_url else ""
        conf = m_conf.group(1).strip() if m_conf else None
        links_str = f" ({m_links.group(1).strip()})" if m_links else ""

        all_notes.append({
            "note_stem": p.stem,
            "title": title,
            "category": cat,
            "url": url,
            "conflict": conf,
            "links_str": links_str,
        })
    return all_notes


def generate_obsidian_markdown(
    results: List[Dict[str, Any]], output_path: Path, handle: str
):
    """Generuje strukturę Zettelkasten: atomowe notatki per wpis oraz aktualizuje główny indeks autora."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Tworzymy folder autora w Źródła/<handle>/ oraz podfolder Wpisy/
    author_dir = output_path.parent / handle
    notes_dir = author_dir / "Wpisy"
    notes_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generujemy poszczególne atomowe notatki
    for item in results:
        t: ExtractedTip = item["tip_obj"]
        raw = item["tweet"]

        title = t.title or "Wskazówka inżynierska"
        slug = slugify_title(title)
        
        # Formatowanie daty do prefiksu (np. 2026-09-20)
        date_str = str(raw.get("date", ""))
        date_prefix = ""
        try:
            parsed_date = datetime.strptime(date_str, "%a %b %d %H:%M:%S %z %Y")
            date_prefix = parsed_date.strftime("%Y-%m-%d ")
        except Exception:
            if len(date_str) >= 10 and date_str[:4].isdigit():
                date_prefix = date_str[:10] + " "

        filename = f"{date_prefix}{slug}.md"
        file_path = notes_dir / filename

        note_lines = []
        note_lines.append("---")
        note_lines.append(f"typ: wpis-źródłowy")
        note_lines.append(f"autor: \"@{handle}\"")
        note_lines.append(f"data: \"{raw['date']}\"")
        note_lines.append(f"źródło: \"{raw['url']}\"")
        note_lines.append(f"kategoria: \"{t.category or 'Inżynieria AI'}\"")
        note_lines.append("tagi:")
        note_lines.append(f"  - {handle.lower()}")
        note_lines.append("  - ai-engineering")
        note_lines.append("  - wpis-atomowy")
        note_lines.append("---\n")

        note_lines.append(f"# {title}\n")
        note_lines.append(f"- **Autor:** [[{handle} — Indeks|@{handle}]] | **Data:** `{raw['date']}` | **Źródło:** [Post na X]({raw['url']})")
        if raw["is_reply"]:
            note_lines.append(f"- **Konwersacja:** Odpowiedź w dyskusji (@{raw['parent_user'] or 'wątek'})")
        
        if t.vault_links:
            note_lines.append(f"- **Kluczowe pojęcia:** {' '.join(t.vault_links)}")
        
        note_lines.append("\n---\n")

        if t.context_summary:
            note_lines.append(f"## Kontekst i problem\n{t.context_summary}\n")

        if t.tip:
            note_lines.append(f"## Rada inżynierska\n{t.tip}\n")

        if t.pitfall:
            note_lines.append(f"## Uwaga / Anty-wzorzec\n{t.pitfall}\n")

        if t.has_conflict and t.conflict_notes:
            note_lines.append(f"## ⚡ Kwestia sporna / do rozstrzygnięcia\n{t.conflict_notes}\n")

        if t.original_quote:
            note_lines.append(f"## Oryginalny cytat\n> *\"{t.original_quote}\"*\n")

        file_path.write_text("\n".join(note_lines), encoding="utf-8")

    # 2. Generujemy zbiorczy główny indeks autora ze wszystkich notatek w folderze
    index_file = author_dir / f"{handle} — Indeks.md"
    all_notes = collect_all_notes(notes_dir)
    
    # Grupowanie według kategorii do indeksu
    by_category: Dict[str, List[Dict[str, Any]]] = {}
    for item in all_notes:
        by_category.setdefault(item["category"], []).append(item)

    idx_lines = []
    idx_lines.append("---")
    idx_lines.append("typ: indeks-autora")
    idx_lines.append(f"autor: \"@{handle}\"")
    idx_lines.append(f"źródło: \"https://x.com/{handle}\"")
    idx_lines.append(f"wygenerowano: \"{now_str}\"")
    idx_lines.append("tagi:")
    idx_lines.append(f"  - {handle.lower()}")
    idx_lines.append("  - ai-engineering")
    idx_lines.append("  - indeks")
    idx_lines.append("---\n")

    idx_lines.append(f"# @{handle} — Indeks Bazy Wiedzy\n")
    idx_lines.append(
        f"> Baza wiedzy wyekstrahowana z wypowiedzi i dyskusji inżynierskich **@{handle}**. "
        f"Zawiera **{len(all_notes)}** wyodrębnionych, atomowych notatek inżynierskich.\n"
    )

    # Sekcja sporów
    conflicts = [it for it in all_notes if it["conflict"]]
    if conflicts:
        idx_lines.append("## ⚠️ Kwestie sporne i rozbieżności do rozstrzygnięcia\n")
        idx_lines.append("> Tezy podważające powszechne przekonania branżowe lub prezentujące odmienne podejście:\n")
        for it in conflicts:
            idx_lines.append(f"- **[[{it['note_stem']}|{it['title']}]]** — {it['conflict']}")
        idx_lines.append("\n---\n")

    idx_lines.append("## Spis tematów i notatek\n")
    for cat, items in sorted(by_category.items()):
        idx_lines.append(f"### {cat} ({len(items)})\n")
        for it in items:
            idx_lines.append(f"- [[{it['note_stem']}|{it['title']}]] — [Post na X]({it['url']}){it['links_str']}")
        idx_lines.append("")

    index_file.write_text("\n".join(idx_lines), encoding="utf-8")
    print(f"[+] Zapisano {len(results)} nowych notatek atomowych w: {notes_dir}")
    print(f"[+] Zaktualizowano indeks autora ({len(all_notes)} łącznie) w: {index_file}")


def run_account_pipeline(raw_items: List[Dict[str, Any]], args: argparse.Namespace) -> None:
    """OCR i wątek, filtr lokalnego CLM oraz Jev, kategoria, ekstrakcja Space Bunny."""
    from kb_pipeline.account_run import analyze_loaded
    from kb_pipeline.live_adapters import (
        make_categorizer,
        make_jev,
        make_local_filter,
        make_summarizer,
        require_runtime_config,
    )
    from kb_pipeline.notes import write_staging
    from kb_pipeline.period import in_period, parse_day

    if args.analyze_only and not args.since and not args.until:
        raise SystemExit("Podaj okres: --since YYYY-MM-DD i opcjonalnie --until YYYY-MM-DD.")
    config = require_runtime_config()
    since = parse_day(args.since) if args.since else None
    until = parse_day(args.until) if args.until else None
    window = [
        item for item in raw_items
        if not str(item.get("full_text") or item.get("text") or "").startswith("RT @")
        and in_period(item, since=since, until=until)
    ]
    print(
        f"[*] Pipeline: okres={args.since or '*'}..{args.until or '*'} | "
        f"lokalny CLM={config['local_model']} | ekstrakcja={config['extraction_model']} | "
        f"wpisy={len(window)}"
    )
    local_filter = make_local_filter(config["local_base"], config["local_key"], config["local_model"])
    categorize = make_categorizer(config["local_base"], config["local_key"], config["local_model"])
    summarize = make_summarizer(config["extraction_base"], config["extraction_key"], config["extraction_model"])
    jev = make_jev(config["jev_model"])
    fetch_status = None
    if not args.analyze_only:
        from kb_pipeline.apify_x import fetch_status as fetch_status
    results = analyze_loaded(
        window,
        handle=args.handle,
        known_items=raw_items,
        local_filter=local_filter,
        jev_evaluate=jev,
        categorize=categorize,
        summarize=summarize,
        fetch_status=fetch_status,
    )
    notes_dir = (
        Path(args.output).parent / args.handle / "Wpisy"
        if args.output
        else Path(__file__).resolve().parent.parent / "Źródła" / args.handle / "Wpisy"
    )
    written = write_staging([item for item in results if item.status == "extract"], args.handle, notes_dir)
    output_path = Path(args.output) if args.output else Path(__file__).resolve().parent.parent / "Źródła" / "indeks.md"
    if written or notes_dir.exists():
        generate_obsidian_markdown([], output_path, args.handle)
    counts = {status: sum(item.status == status for item in results) for status in ("extract", "reject", "defer", "error")}
    print(f"[+] Zapisano {len(written)} notatek. extract={counts['extract']} reject={counts['reject']} defer={counts['defer']} error={counts['error']}")


def main():
    parser = argparse.ArgumentParser(
        description="Ekstrakcja porad Kuna Chena (@kunchenguid) z X/Twittera do Obsidiana."
    )
    parser.add_argument(
        "--handle",
        default=DEFAULT_HANDLE,
        help=f"Uchwyt na X (domyślnie: {DEFAULT_HANDLE})",
    )
    parser.add_argument(
        "--max-tweets",
        type=int,
        default=int(os.getenv("MAX_TWEETS", "80")),
        help="Maksymalna liczba tweetów do pobrania z Apify (domyślnie: 80)",
    )
    parser.add_argument(
        "--fetch-only",
        action="store_true",
        help="Tylko pobierz tweety z Apify i zapisz do pliku cache JSON (bez analizy LLM)",
    )
    parser.add_argument(
        "--analyze-only",
        action="store_true",
        help="Użyj istniejącego pliku cache JSON i wykonaj tylko analizę LLM (bez odpytywania Apify)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Ścieżka pliku wyjściowego w Obsidianie (domyślnie generowana z nazwy handle)",
    )
    parser.add_argument(
        "--since",
        default=None,
        help="Data początkowa w formacie YYYY-MM-DD (np. 2026-08-01)",
    )
    parser.add_argument(
        "--until",
        default=None,
        help="Data graniczna wstecz w formacie YYYY-MM-DD (np. 2026-09-01)",
    )
    parser.add_argument(
        "--skip-jev",
        action="store_true",
        help="Pomiń filtr Jev i wyślij wszystkie znormalizowane wpisy do LLM",
    )
    parser.add_argument(
        "--jev-threshold",
        type=float,
        default=JEV_SCORE_THRESHOLD,
        help=f"Próg minimalnego Score Jev dla wartościowych wpisów (skala 0-2, domyślnie: {JEV_SCORE_THRESHOLD})",
    )
    parser.add_argument(
        "--llm-workers",
        type=int,
        default=MAX_LLM_WORKERS,
        help=f"Liczba równoległych wywołań LLM/DeepSeek (domyślnie: {MAX_LLM_WORKERS})",
    )
    parser.add_argument(
        "--legacy",
        action="store_true",
        help="Stary filtr Jev Score i ekstrakcja jednym modelem, bez OCR i lokalnego CLM",
    )

    args = parser.parse_args()
    cache_path = Path(__file__).parent / f"{args.handle}_raw_tweets.json"

    raw_items = []

    # 1. Pobieranie lub wczytanie z cache
    if args.analyze_only:
        if not cache_path.exists():
            print(f"[!] Błąd: Brak pliku cache {cache_path}. Uruchom bez --analyze-only.")
            sys.exit(1)
        print(f"[*] Wczytywanie tweetów z cache: {cache_path}")
        with open(cache_path, "r", encoding="utf-8") as f:
            raw_items = json.load(f)
    else:
        # Automatyczne wykrycie okna od ostatniego pobrania, jeśli flaga --since nie została jawnie podana
        if not args.since and cache_path.exists():
            try:
                cached_items = json.loads(cache_path.read_text(encoding="utf-8"))
                latest_dt = None
                for it in cached_items:
                    c = it.get("created_at") or it.get("createdAt")
                    if c:
                        try:
                            dt = datetime.strptime(c, "%a %b %d %H:%M:%S %z %Y")
                        except Exception:
                            try:
                                dt = datetime.fromisoformat(c.replace("Z", "+00:00"))
                            except Exception:
                                continue
                        if latest_dt is None or dt > latest_dt:
                            latest_dt = dt
                if latest_dt:
                    args.since = latest_dt.strftime("%Y-%m-%d")
                    logger.info(f"Okno od ostatniego pobrania (@{args.handle}): since={args.since} (najnowszy wpis: {latest_dt.isoformat()})")
            except Exception as e:
                logger.warning(f"Nie udało się odczytać daty ostatniego pobrania: {e}")

        raw_items = fetch_tweets_from_apify(args.handle, args.max_tweets, until_date=args.until, since_date=args.since)
        existing_raw = []
        if cache_path.exists():
            try:
                existing_raw = json.loads(cache_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        before_cnt = len(existing_raw)
        merged_by_id = {}
        for item in existing_raw + raw_items:
            tid = str(item.get("id") or item.get("id_str") or item.get("tweet_id") or "")
            if tid:
                merged_by_id[tid] = item
            else:
                merged_by_id[str(len(merged_by_id))] = item
        
        all_raw_items = list(merged_by_id.values())
        new_cnt = len(all_raw_items) - before_cnt
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(all_raw_items, f, ensure_ascii=False, indent=2)
        logger.info(f"Zapisano cache: {cache_path} (+{new_cnt} nowych, łącznie: {len(all_raw_items)}).")
        log_event("cache_saved", {
            "handle": args.handle,
            "cache_file": cache_path.name,
            "before_count": before_cnt,
            "new_count": new_cnt,
            "total_count": len(all_raw_items),
        })

        if args.fetch_only:
            logger.info("Zakończono etap pobierania (--fetch-only). Zapisano logi.")
            return

    # Filtrowanie daty (--since) w trybie analizy
    if args.since:
        filtered_items = []
        since_val = args.since.strip()
        for item in raw_items:
            created = item.get("created_at") or item.get("createdAt")
            if not created:
                continue
            item_dt = None
            try:
                item_dt = datetime.strptime(created, "%a %b %d %H:%M:%S %z %Y")
            except Exception:
                try:
                    item_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                except Exception:
                    pass
            if item_dt:
                if len(since_val) == 10 and since_val.count("-") == 2:
                    if item_dt.strftime("%Y-%m-%d") >= since_val:
                        filtered_items.append(item)
                else:
                    try:
                        since_dt = datetime.fromisoformat(since_val.replace("Z", "+00:00"))
                        if not since_dt.tzinfo:
                            from datetime import timezone
                            since_dt = since_dt.replace(tzinfo=timezone.utc)
                        if item_dt >= since_dt:
                            filtered_items.append(item)
                    except Exception:
                        if created >= since_val:
                            filtered_items.append(item)
            elif created >= since_val:
                filtered_items.append(item)
        print(f"[*] Przefiltrowano wpisy wg --since {args.since}: {len(filtered_items)} / {len(raw_items)}")
        raw_items = filtered_items

    # Pomijamy wpisy, które już zostały wcześniej wyekstrahowane do notatek
    notes_dir = (
        Path(args.output).parent / args.handle / "Wpisy"
        if args.output
        else Path(__file__).resolve().parent.parent / "Źródła" / args.handle / "Wpisy"
    )
    if notes_dir.exists():
        existing_urls = set()
        for p in notes_dir.glob("*.md"):
            txt = p.read_text(encoding="utf-8")
            m_url = re.search(r"źródło:\s*\"?([^\n\"]+)\"?", txt)
            if m_url:
                existing_urls.add(m_url.group(1).strip())
        before_cnt = len(raw_items)
        raw_items = [
            it for it in raw_items
            if (it.get("url") or it.get("twitterUrl") or f"https://x.com/{args.handle}/status/{it.get('id') or it.get('id_str')}") not in existing_urls
        ]
        if before_cnt != len(raw_items):
            print(f"[*] Pominięto {before_cnt - len(raw_items)} wpisów już istniejących w bazie. Do analizy: {len(raw_items)}")

    if not raw_items:
        print("[*] Brak nowych wpisów do analizy. Wszystkie wpisy z tego zakresu są już w bazie wiedzy.")
        return

    if not args.legacy:
        run_account_pipeline(raw_items, args)
        return

    # 2. Normalizacja
    normalized_tweets = []
    for item in raw_items:
        norm = normalize_tweet(item, args.handle)
        if norm:
            normalized_tweets.append(norm)

    print(f"[*] Przesortowano {len(normalized_tweets)} merytorycznych wpisów do analizy...")

    # 3. Wielowymiarowy filtr TypeSafe Jev (Score + Choice)
    if args.skip_jev:
        candidates = [(tw, 2.0, "unfiltered") for tw in normalized_tweets]
        print("[*] Pominięto filtr Jev (--skip-jev).")
    else:
        candidates = evaluate_with_jev(normalized_tweets, min_score=args.jev_threshold)

    # 4. Równoległa analiza przez LLM / DeepSeek
    valuable_results = []
    workers = max(1, args.llm_workers)
    print(f"[*] Analiza LLM {len(candidates)} kandydatów równolegle (workers={workers}, model={MODEL_NAME})...")

    def analyze_candidate(candidate: Tuple[Dict[str, Any], float, str]) -> Optional[Dict[str, Any]]:
        tw, jev_score, jev_topic = candidate
        tip_obj = analyze_with_llm(tw, handle=args.handle)
        if tip_obj and tip_obj.is_valuable:
            return {"tweet": tw, "tip_obj": tip_obj, "jev_score": jev_score, "jev_topic": jev_topic}
        return None

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_candidate = {executor.submit(analyze_candidate, candidate): candidate for candidate in candidates}
        total = len(future_to_candidate)
        for idx, future in enumerate(as_completed(future_to_candidate), 1):
            tw, jev_score, jev_topic = future_to_candidate[future]
            try:
                result = future.result()
            except Exception as e:
                print(f"[{idx}/{total}] [!] Błąd analizy wpisu ({tw['url']}): {e}")
                continue

            if result:
                title = result["tip_obj"].title
                category = result["tip_obj"].category
                print(f"[{idx}/{total}] -> [Wartościowy] {title} ({category}) | JevScore={jev_score:.2f} [{jev_topic}]")
                valuable_results.append(result)
            else:
                print(f"[{idx}/{total}] -> Pominięto po LLM ({tw['url']}) | JevScore={jev_score:.2f} [{jev_topic}]")

    print(f"\n[+] Znaleziono {len(valuable_results)} wartościowych wskazówek z {len(normalized_tweets)} wpisów.")

    # Zachowaj chronologiczny porządek (najnowsze na górze)
    valuable_results.sort(key=lambda item: item["tweet"].get("date", ""), reverse=True)

    # 5. Normalizacja linków Obsidianowych do kanonicznych pojęć
    root_dir = Path(__file__).parent.parent
    canonical_files = {f.stem.lower(): f.stem for f in root_dir.glob("Pojęcia/*.md")}
    canonical_files.update({f.stem.lower(): f.stem for f in root_dir.glob("Narzędzia/*.md")})
    canonical_files.update({f.stem.lower(): f.stem for f in root_dir.glob("Procesy/*.md")})

    concept_rules = {
        "reasoning": "Test-Time Compute i Reasoning Tokens",
        "compute": "Test-Time Compute i Reasoning Tokens",
        "overthinking": "Test-Time Compute i Reasoning Tokens",
        "token throughput": "Test-Time Compute i Reasoning Tokens",
        "sandbox": "Sandbox i Granice Bezpieczeństwa Agenta",
        "bezpieczeństw": "Sandbox i Granice Bezpieczeństwa Agenta",
        "uprawnień": "Sandbox i Granice Bezpieczeństwa Agenta",
        "izolacj": "Sandbox i Granice Bezpieczeństwa Agenta",
        "kaskad": "Kaskady Modeli i Routing Pewności",
        "cascade": "Kaskady Modeli i Routing Pewności",
        "dobór modeli": "Kaskady Modeli i Routing Pewności",
        "routing": "Kaskady Modeli i Routing Pewności",
        "skill": "Dynamiczne Skille i Metaprogramowanie Agenta",
        "kv cache": "Architektura KV Cache i Rozumowanie Latentne",
        "latent": "Architektura KV Cache i Rozumowanie Latentne",
        "multi-token": "Architektura KV Cache i Rozumowanie Latentne",
        "mtp": "Architektura KV Cache i Rozumowanie Latentne",
        "compaction": "Context Compaction",
        "kompakcj": "Context Compaction",
        "kontekst": "Context Compaction",
        "context window": "Context Compaction",
        "bezpieczny punkt": "Bezpieczny punkt kompaktowania",
        "checkpoint": "Bezpieczny punkt kompaktowania",
        "persistencj": "Persistencja stanu agenta",
        "trwały stan": "Persistencja stanu agenta",
        "firstmate": "Firstmate Agent",
        "leaf node": "Firstmate i Agenci Wykonawczy",
        "sub-agent": "Firstmate i Agenci Wykonawczy",
        "subagent": "Firstmate i Agenci Wykonawczy",
        "rework": "Rework Rate",
        "eval": "Eval Set z realnych sesji",
        "ground truth": "Eval Set z realnych sesji",
        "etykietowan": "Eval Set z realnych sesji",
        "code review": "Code Review",
        "weryfikacj": "Weryfikacja krokowa",
        "weryfikator": "Weryfikator",
        "bypass": "CI Check Bypass Confirmation",
        "system prompt": "Stabilność modeli i przestrzeganie promptu",
        "stabilność": "Stabilność modeli i przestrzeganie promptu",
        "prompt architecture": "Prompt Architecture",
        "prompt": "Prompt Architecture",
        "cache": "Prompt Architecture",
        "jev": "Jev",
        "typesafe": "TypeSafe — przewodnik praktyczny",
        "harness": "Harness",
    }

    def resolve_concept(link_text: str) -> str:
        clean = link_text.strip().replace("[[", "").replace("]]", "")
        if clean.lower() in canonical_files:
            return canonical_files[clean.lower()]
        lower_c = clean.lower()
        for k, dest in concept_rules.items():
            if k in lower_c:
                return dest
        return "Harness"

    for item in valuable_results:
        tip: ExtractedTip = item["tip_obj"]
        normalized_links = []
        for l in tip.vault_links:
            dest = resolve_concept(l)
            clean_name = l.strip().replace("[[", "").replace("]]", "")
            if dest == clean_name:
                normalized_links.append(f"[[{dest}]]")
            else:
                normalized_links.append(f"[[{dest}|{clean_name}]]")
        tip.vault_links = list(dict.fromkeys(normalized_links))

    # 6. Generowanie Markdown do Obsidiana
    if args.output:
        output_file = root_dir / args.output
    else:
        output_file = root_dir / f"Źródła/{args.handle} — Baza Wskazówek i Komentarzy.md"
    generate_obsidian_markdown(valuable_results, output_file, args.handle)


if __name__ == "__main__":
    main()
