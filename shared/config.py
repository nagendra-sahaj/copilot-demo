import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent

load_dotenv(PROJECT_ROOT / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is not set. "
        "Copy .env.example to .env and add your OpenAI API key."
    )

_db_path_raw = os.getenv("DB_PATH", "db/strategist.duckdb")
DB_PATH = str(PROJECT_ROOT / _db_path_raw) if not Path(_db_path_raw).is_absolute() else _db_path_raw

_chroma_path_raw = os.getenv("CHROMA_PATH", "db/chroma_db")
CHROMA_PATH = str(PROJECT_ROOT / _chroma_path_raw) if not Path(_chroma_path_raw).is_absolute() else _chroma_path_raw

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o"

PRIMARY_COLOUR = "#1D9E75"

SEVERITY_COLOURS = {
    "Critical": "#E24B4A",
    "High": "#D85A30",
    "Medium": "#BA7517",
    "Low": "#1D9E75",
}
