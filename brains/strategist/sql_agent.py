import re
from pathlib import Path
from openai import OpenAI
from shared.config import OPENAI_API_KEY, CHAT_MODEL

PROJECT_ROOT = Path(__file__).parent.parent.parent
_SYSTEM_PROMPT_PATH = PROJECT_ROOT / "prompts" / "sql_system.txt"

client = OpenAI(api_key=OPENAI_API_KEY)


def _load_system_prompt() -> str:
    return _SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


def generate_sql(user_question: str) -> str:
    system_prompt = _load_system_prompt()

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question},
        ],
    )

    raw = response.choices[0].message.content or ""
    raw = raw.strip()

    if not raw:
        raise ValueError("The model returned an empty response. Please rephrase your question.")

    # Strip markdown code fences if present
    raw = re.sub(r"^```sql\s*", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    raw = raw.strip()

    if not raw:
        raise ValueError("The model returned an empty SQL statement after stripping code fences.")

    return raw
