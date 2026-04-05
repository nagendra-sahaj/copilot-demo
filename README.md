# Copilot Demo

A multi-brain analytics and RAG system demonstrating AI copilot patterns for enterprise data. Built for a conference talk — uses hypothetical client, issue, and feature data with three specialised AI brains powered by GPT-4o.

## Brains

- **Strategist** — Natural language → SQL analytics with Plotly visualisation (bar, pie, line, table) and AI summaries
- **Resolver** — Operational RAG: ask anything about client issues — summaries, patterns, or resolution guidance based on similar historical cases
- **Navigator** — Documentation RAG: how-to answers from markdown docs with step-by-step guidance; responds with "I don't know" when the answer isn't in the docs

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key

## Setup

### 1. Install dependencies

```bash
uv venv
source .venv/bin/activate
uv sync
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Seed the database

```bash
# Creates DuckDB with all hypothetical data (clients, issues, features, feedback)
uv run python data/seed.py

# Embeds issues into ChromaDB for Resolver brain
uv run python data/seed_resolver.py

# Add your markdown docs to data/docs/ first, then:
uv run python data/seed_navigator.py
```

### 4. Run the app

```bash
uv run streamlit run app/main.py
```

Open http://localhost:8501

## Navigator documentation

`data/docs/` already contains UAT and FB360 guides. To add more documentation, place additional `.md` files in that directory using `##` headings to divide content into sections, then re-seed:

```bash
rm -rf db/chroma_db && uv run python data/seed_navigator.py
```

## Re-seeding

Delete the relevant files and re-run:

```bash
# Re-seed DuckDB
rm db/strategist.duckdb && uv run python data/seed.py

# Re-seed ChromaDB (both Resolver and Navigator)
rm -rf db/chroma_db
uv run python data/seed_resolver.py
uv run python data/seed_navigator.py
```

## Project structure

```
copilot-demo/
├── app/            # Streamlit entry point and page modules
├── brains/         # AI brain implementations
│   ├── strategist/ # NL→SQL pipeline
│   ├── resolver/   # Issue RAG pipeline
│   └── navigator/  # Docs RAG pipeline
├── data/           # Seed scripts and documentation
├── db/             # DuckDB and ChromaDB (generated)
├── prompts/        # System prompts for each brain
├── schema/         # DuckDB schema SQL
└── shared/         # Config and shared UI components
```
