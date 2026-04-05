import chromadb
from openai import OpenAI
from shared.config import OPENAI_API_KEY, CHROMA_PATH, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def _embed(text: str) -> list[float]:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def retrieve(
    query: str,
    n_results: int = 8,
    severity: str = None,
    status: str = None,
    category: str = None,
) -> list[dict]:
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = chroma_client.get_collection("resolver_issues")

    query_embedding = _embed(query)

    where_conditions = []
    if severity:
        where_conditions.append({"severity": {"$eq": severity}})
    if status:
        where_conditions.append({"status": {"$eq": status}})
    if category:
        where_conditions.append({"category": {"$eq": category}})

    where = None
    if len(where_conditions) == 1:
        where = where_conditions[0]
    elif len(where_conditions) > 1:
        where = {"$and": where_conditions}

    kwargs = dict(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )
    if where:
        kwargs["where"] = where

    results = collection.query(**kwargs)

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    raw = []
    for doc, meta, dist in zip(docs, metas, distances):
        raw.append({
            "issue_id": meta.get("issue_id", ""),
            "client_name": meta.get("client_name", ""),
            "severity": meta.get("severity", ""),
            "status": meta.get("status", ""),
            "category": meta.get("category", ""),
            "revenue_impact_usd": meta.get("revenue_impact_usd", 0),
            "matched_chunk": doc,
            "parent_text": meta.get("parent_text", doc),
            "distance": dist,
        })

    # Deduplicate by issue_id, keeping lowest distance
    seen: dict[str, dict] = {}
    for item in raw:
        iid = item["issue_id"]
        if iid not in seen or item["distance"] < seen[iid]["distance"]:
            seen[iid] = item

    return list(seen.values())
