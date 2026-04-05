import pandas as pd
from openai import OpenAI
from shared.config import OPENAI_API_KEY, CHAT_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

_SYSTEM_PROMPT = (
    "You are a business intelligence assistant. "
    "Summarise the following query results in 2-3 sentences for a Director or VP. "
    "Use business language. Focus on the key insight and any notable outliers. "
    "Do not mention SQL or technical details."
)


def summarise(df: pd.DataFrame, user_question: str) -> str:
    markdown_table = df.head(20).to_markdown(index=False)

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0,
        max_tokens=300,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Question: {user_question}\n\nResults:\n{markdown_table}",
            },
        ],
    )

    return (response.choices[0].message.content or "").strip()
