from pathlib import Path
from openai import OpenAI
from shared.config import OPENAI_API_KEY, CHAT_MODEL

PROJECT_ROOT = Path(__file__).parent.parent.parent
_PROMPT_PATH = PROJECT_ROOT / "prompts" / "resolver_system.txt"

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(query: str, retrieved_docs: list[dict]) -> str:
    system_prompt = _PROMPT_PATH.read_text(encoding="utf-8")

    context = "\n---\n".join(doc["parent_text"] for doc in retrieved_docs)

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0,
        max_tokens=1000,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Query: {query}\n\nContext documents:\n{context}",
            },
        ],
    )

    return (response.choices[0].message.content or "").strip()
