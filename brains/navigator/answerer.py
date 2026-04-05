from pathlib import Path
from openai import OpenAI
from shared.config import OPENAI_API_KEY, CHAT_MODEL

PROJECT_ROOT = Path(__file__).parent.parent.parent
_PROMPT_PATH = PROJECT_ROOT / "prompts" / "navigator_system.txt"

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(query: str, retrieved_docs: list[dict]) -> str:
    system_prompt = _PROMPT_PATH.read_text(encoding="utf-8")

    context_parts = []
    for doc in retrieved_docs:
        context_parts.append(
            f"Source: {doc['source_file']} — {doc['heading']}\n{doc['content']}"
        )
    context = "\n---\n".join(context_parts)

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0,
        max_tokens=800,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Question: {query}\n\nDocumentation context:\n{context}",
            },
        ],
    )

    return (response.choices[0].message.content or "").strip()
