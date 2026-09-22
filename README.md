# AI Engineering Knowledge Repository and Intelligence Pipeline

Welcome to this comprehensive repository designed to unlock actionable technical paradigms in AI engineering, autonomous agent orchestration, and context curation for Obsidian.

## Repository Architecture

This multi-faceted project is decoupled into two purpose-built directories:

- `extractor/`: An automated pipeline utilizing Apify, TypeSafe Jev (System One classification), and parallelized DeepSeek inference to streamline Twitter insights directly into Markdown.
- `vault/`: A dedicated Obsidian knowledge graph centered on agent harnesses, step-by-step verification, context compaction boundaries, and model stability heuristics.

## Quickstart

### 1. Launching the Extractor

```bash
cd extractor
pip install -r requirements.txt
cp .env.example .env
python extract_kunchen_tips.py --analyze-only
```

### 2. Navigating the Vault

Open the `vault/` directory directly within the Obsidian desktop application. The root index is situated at `vault/00 Start.md`.
