import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import duckdb
import chromadb
from openai import OpenAI
from shared.config import OPENAI_API_KEY, DB_PATH, CHROMA_PATH, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def _embed_batch(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]


def main():
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    existing = [c.name for c in chroma_client.list_collections()]
    if "resolver_issues" in existing:
        col = chroma_client.get_collection("resolver_issues")
        if col.count() > 0:
            print("Resolver index already exists. Delete db/chroma_db to re-index.")
            return

    conn = duckdb.connect(DB_PATH, read_only=True)
    try:
        rows = conn.execute("""
            SELECT i.issue_id, i.title, i.client_id, i.category, i.severity,
                   i.status, i.created_date, i.revenue_impact_usd,
                   i.description, i.business_impact_description,
                   i.resolution_notes, c.client_name, c.industry, c.tier
            FROM issues i
            JOIN clients c ON i.client_id = c.client_id
        """).fetchall()
        columns = [
            "issue_id", "title", "client_id", "category", "severity",
            "status", "created_date", "revenue_impact_usd",
            "description", "business_impact_description",
            "resolution_notes", "client_name", "industry", "tier",
        ]
        issues = [dict(zip(columns, row)) for row in rows]
    finally:
        conn.close()

    collection = chroma_client.get_or_create_collection(
        "resolver_issues",
        metadata={"hnsw:space": "cosine"},
    )

    all_ids = []
    all_texts = []
    all_metas = []

    for idx, issue in enumerate(issues):
        resolution_text = issue["resolution_notes"] if issue["resolution_notes"] else "Issue not yet resolved."

        parent_text = (
            f"ISSUE: {issue['title']}\n"
            f"CLIENT: {issue['client_name']} | INDUSTRY: {issue['industry']} | TIER: {issue['tier']} tier\n"
            f"CATEGORY: {issue['category']} | SEVERITY: {issue['severity']} | STATUS: {issue['status']}\n"
            f"REVENUE IMPACT: ${issue['revenue_impact_usd']:,}\n"
            f"CREATED: {issue['created_date']}\n\n"
            f"DESCRIPTION:\n{issue['description']}\n\n"
            f"BUSINESS IMPACT:\n{issue['business_impact_description']}\n\n"
            f"RESOLUTION NOTES:\n{resolution_text}"
        )

        raw_chunks = parent_text.split("\n\n")
        chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 80]

        for n, chunk in enumerate(chunks):
            all_ids.append(f"{issue['issue_id']}_chunk_{n}")
            all_texts.append(chunk)
            all_metas.append({
                "issue_id": issue["issue_id"],
                "client_name": issue["client_name"],
                "severity": issue["severity"],
                "status": issue["status"],
                "category": issue["category"],
                "revenue_impact_usd": int(issue["revenue_impact_usd"]),
                "chunk_type": "child",
                "parent_text": parent_text,
            })

        if (idx + 1) % 50 == 0:
            print(f"  Processed {idx + 1}/{len(issues)} issues...")

    # Embed in batches of 50
    batch_size = 50
    all_embeddings = []
    for i in range(0, len(all_texts), batch_size):
        batch = all_texts[i : i + batch_size]
        embeddings = _embed_batch(batch)
        all_embeddings.extend(embeddings)

    # Upsert into ChromaDB in batches
    upsert_batch = 100
    for i in range(0, len(all_ids), upsert_batch):
        collection.upsert(
            ids=all_ids[i : i + upsert_batch],
            documents=all_texts[i : i + upsert_batch],
            embeddings=all_embeddings[i : i + upsert_batch],
            metadatas=all_metas[i : i + upsert_batch],
        )

    print(f"✓ Resolver index ready: {len(issues)} issues → {len(all_ids)} chunks")


if __name__ == "__main__":
    main()
