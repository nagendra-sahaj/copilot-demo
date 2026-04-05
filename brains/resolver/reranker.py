from openai import OpenAI
from shared.config import OPENAI_API_KEY, CHAT_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

_SYSTEM_PROMPT = (
    "You are a relevance scoring assistant. Score how relevant the following "
    "issue document is to the user query. Return ONLY a float between 0.0 and 1.0. "
    "Nothing else."
)


def rerank(query: str, results: list[dict], top_k: int = 3) -> list[dict]:
    scored = []
    for result in results:
        snippet = result["matched_chunk"][:500]
        try:
            response = client.chat.completions.create(
                model=CHAT_MODEL,
                temperature=0,
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Query: {query}\n\nDocument snippet: {snippet}",
                    },
                ],
            )
            raw_score = (response.choices[0].message.content or "0.0").strip()
            score = float(raw_score)
        except (ValueError, TypeError):
            score = 0.0

        result = dict(result)
        result["relevance_score"] = max(0.0, min(1.0, score))
        scored.append(result)

    scored.sort(key=lambda x: x["relevance_score"], reverse=True)
    return scored[:top_k]
