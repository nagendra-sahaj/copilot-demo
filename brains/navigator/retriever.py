import chromadb
from openai import OpenAI
from shared.config import OPENAI_API_KEY, CHROMA_PATH, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def _embed(text: str) -> list[float]:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def retrieve(query: str, n_results: int = 5) -> list[dict]:
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = chroma_client.get_collection("navigator_docs")

    query_embedding = _embed(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    return [
        {
            "source_file": meta.get("source_file", ""),
            "heading": meta.get("heading", ""),
            "content": doc,
            "distance": dist,
        }
        for doc, meta, dist in zip(docs, metas, distances)
    ]
