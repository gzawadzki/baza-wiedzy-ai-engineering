#!/usr/bin/env python3
"""
Ekstraktor porad i wskazówek Kuna Chena (@kunchenguid) z X/Twittera.
Wykorzystuje Apify (apidojo/tweet-scraper) do pobrania wpisów i komentarzy,
a następnie LLM do destylacji wiedzy i zapisu w formacie Markdown dla Obsidiana.
"""

import os
import sys
import json
import argparse
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Zapewnienie poprawnego kodowania UTF-8 na Windowsie
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

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
        description="Sugerowane linki do pojęć w Obsidianie, np. ['[[Harness]]', '[[Weryfikator]]', '[[Interpretable Context Methodology]]', '[[Jev]]'] jeśli pasują."
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
    """Pobiera tweety i komentarze danego użytkownika przez Apify."""
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

    print(f"[*] Łączenie z Apify w celu pobrania wpisów @{handle} (query: '{query}', limit: {max_items})...")
    client = ApifyClient(APIFY_API_TOKEN)

    # Używamy aktora kompatybilnego w 100% z Apify Free Plan
    actor_id = "scrape.badger/twitter-tweets-scraper"
    run_input = {
        "mode": "Advanced Search",
        "query": query,
        "query_type": "Latest",
        "max_results": max_items,
    }

    print(f"[*] Uruchamianie aktora {actor_id}...")
    run = client.actor(actor_id).call(run_input=run_input)

    # Bezpieczne pobranie dataset_id z obiektu Run lub słownika
    dataset_id = getattr(run, "default_dataset_id", None)
    if not dataset_id and isinstance(run, dict):
        dataset_id = run.get("defaultDatasetId")

    if not dataset_id:
        raise RuntimeError("Nie udało się uzyskać identyfikatora datasetu z Apify.")

    print(f"[*] Pobieranie wyników z datasetu ({dataset_id})...")
    dataset_items = list(client.dataset(dataset_id).iterate_items())

    print(f"[+] Pobrano {len(dataset_items)} surowych rekordów.")
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


def analyze_with_llm(tweet: Dict[str, Any]) -> Optional[ExtractedTip]:
    """Wysyła pojedynczy wpis/komentarz do LLM w celu ekstrakcji porady."""
    if not OPENAI_API_KEY:
        raise ValueError("Brak OPENAI_API_KEY w pliku .env lub zmiennych środowiskowych.")

    from openai import OpenAI

    client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
    )

    system_prompt = """Jesteś starszym inżynierem AI analizującym wpisy i komentarze Kuna Chena (@kunchenguid) na Twitterze/X.
Twoim celem jest wyciągnięcie GĘSTEJ, PRAKTYCZNEJ WIEDZY inżynierskiej do bazy wiedzy w Obsidianie:
- Konkretne zasady tworzenia promptów (prompt architecture),
- Obserwacje zachowania modeli (drift, saturation, reasoning loops),
- Praktyki harnessów, zewnętrznych weryfikatorów, weryfikacji krokowej,
- Wykrywanie anty-wzorców (co ludzie robią źle).

ZASADA AKTUALNOŚCI WIEDZY:
Jeżeli wnioski, obserwacje lub zalecenia stoją w sprzeczności z wcześniejszymi wpisami (np. zmiana zdania na temat modelu, nowe doświadczenia z dłuższą pracą z harnessem, ewolucja podejścia do kontekstu), uznaj, że nowszy wpis odzwierciedla zaktualizowany stan wiedzy i najnowsze ustalenia inżynierskie. Wskaż tę ewolucję w polu `tip` lub `context_summary`.

Zignoruj:
- Zwykły small talk, krótkie potwierdzenia ("Yes, exactly", "Thanks!"),
- Ogólne pytania bez odpowiedzi,
- Wpisy o charakterze czysto towarzyskim lub marketingowym.

Wartościowe są:
- Wnioski z eksperymentów,
- Wskazówki dlaczego dane podejście zawodzi w produkcji,
- Odpowiedzi Kuna Chena prostujące błędy innych programistów.

Jeśli wpis jest odpowiedzią (reply), koniecznie uwzględnij kontekst posta, na który Kun odpowiada.

Zwróć odpowiedź w formacie JSON zgodnym ze schematem."""

    # Budowa kontekstu wiadomości
    user_content = f"Data wpisu: {tweet['date']}\nLink: {tweet['url']}\n"
    if tweet["is_reply"]:
        user_content += f"TYP: Komentarz / Odpowiedź pod wpisem innego użytkownika (@{tweet['parent_user'] or 'unknown'})\n"
        if tweet["parent_text"]:
            user_content += f"TREŚĆ POSTA NADRZĘDNEGO (na co odpowiada Kun Chen):\n\"{tweet['parent_text']}\"\n\n"
        else:
            user_content += "(Brak bezpośredniej treści posta nadrzędnego, oceń kontekst z samej odpowiedzi)\n\n"
    else:
        user_content += "TYP: Autorski wpis / wątek Kuna Chena\n\n"

    user_content += f"TREŚĆ WPISU KUNA CHENA:\n\"{tweet['text']}\"\n"

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


def generate_obsidian_markdown(
    results: List[Dict[str, Any]], output_path: Path, handle: str
):
    """Generuje plik Markdown gotowy do otwarcia w Obsidianie."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Grupowanie według kategorii
    by_category: Dict[str, List[Dict[str, Any]]] = {}
    for res in results:
        tip: ExtractedTip = res["tip_obj"]
        cat = tip.category or "Inne obserwacje"
        by_category.setdefault(cat, []).append(res)

    md = []
    md.append("---")
    md.append(f"autor: @{handle}")
    md.append(f"źródło: https://x.com/{handle}")
    md.append(f"wygenerowano: {now_str}")
    md.append("typ: synteza-wiedzy")
    md.append(f"tagi: [{handle.lower()}, ai-engineering, prompt-engineering, twitter-extract]")
    md.append("---\n")

    md.append(f"# @{handle} — Baza Wskazówek i Komentarzy\n")
    md.append(
        "> Destylacja praktycznych porad, heurystyk inżynierskich i komentarzy technicznych "
        f"z profilu @{handle} na platformie X. Wyciągnięto {len(results)} wartościowych wpisów.\n"
    )

    # Sekcja sporów i rozbieżności
    conflicts = [item for item in results if item["tip_obj"].has_conflict]
    if conflicts:
        md.append("## ⚠️ Kwestie sporne i rozbieżności do rozstrzygnięcia\n")
        md.append("> Wpisy, w których autor podważa powszechne przekonania branżowe lub prezentuje tezy stojące w sprzeczności z innymi praktykami:\n")
        for item in conflicts:
            t: ExtractedTip = item["tip_obj"]
            raw = item["tweet"]
            md.append(f"- **[{t.title or 'Kwestia sporna'}]({raw['url']}):** {t.conflict_notes or t.tip}")
        md.append("\n---\n")

    md.append("## Spis kategorii\n")
    for cat, items in by_category.items():
        md.append(f"- [{cat}](#{cat.lower().replace(' ', '-').replace('/', '')}) ({len(items)})")
    md.append("\n---\n")

    for cat, items in by_category.items():
        md.append(f"## {cat}\n")
        for item in items:
            t: ExtractedTip = item["tip_obj"]
            raw = item["tweet"]

            md.append(f"### {t.title or 'Wskazówka'}\n")
            md.append(f"- **Data:** `{raw['date']}` | **Źródło:** [Post na X]({raw['url']})")
            if raw["is_reply"]:
                md.append(f"- **Rodzaj:** Komentarz w dyskusji (@{raw['parent_user'] or 'dyskusja'})")
            else:
                md.append("- **Rodzaj:** Wpis autorski")

            if t.vault_links:
                links_str = " ".join(t.vault_links)
                md.append(f"- **Powiązane pojęcia:** {links_str}")

            if t.context_summary:
                md.append(f"\n**Kontekst / Problem:**\n{t.context_summary}\n")

            if t.tip:
                md.append(f"**Rada inżynierska:**\n{t.tip}\n")

            if t.pitfall:
                md.append(f"**Uwaga / Anty-wzorzec:**\n{t.pitfall}\n")

            if t.has_conflict and t.conflict_notes:
                md.append(f"**⚡ Kwestia sporna / do rozstrzygnięcia:**\n{t.conflict_notes}\n")

            if t.original_quote:
                md.append(f"> **Cytat:** *\"{t.original_quote}\"*\n")

            md.append("---\n")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print(f"[+] Pomyślnie zapisano notatkę w: {output_path}")


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
        raw_items = fetch_tweets_from_apify(args.handle, args.max_tweets, until_date=args.until, since_date=args.since)
        # Łączymy z istniejącym cache, deduplikując po id
        existing_raw = []
        if cache_path.exists():
            try:
                existing_raw = json.loads(cache_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        merged_by_id = {}
        for item in existing_raw + raw_items:
            tid = str(item.get("id") or item.get("id_str") or item.get("tweet_id") or "")
            if tid:
                merged_by_id[tid] = item
            else:
                merged_by_id[str(len(merged_by_id))] = item
        
        all_raw_items = list(merged_by_id.values())
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(all_raw_items, f, ensure_ascii=False, indent=2)
        print(f"[+] Zapisano zaktualizowany cache: {cache_path} ({len(all_raw_items)} unikalnych wpisów).")

        if args.fetch_only:
            print("[*] Zakończono etap pobierania (--fetch-only).")
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
        tip_obj = analyze_with_llm(tw)
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

    # 5. Generowanie Markdown do Obsidiana
    root_dir = Path(__file__).parent.parent
    if args.output:
        output_file = root_dir / args.output
    else:
        output_file = root_dir / f"Źródła/{args.handle} — Baza Wskazówek i Komentarzy.md"
    generate_obsidian_markdown(valuable_results, output_file, args.handle)


if __name__ == "__main__":
    main()
