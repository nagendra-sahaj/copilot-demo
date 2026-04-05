import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import chromadb
from openai import OpenAI
from shared.config import OPENAI_API_KEY, CHROMA_PATH, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

DOCS_DIR = PROJECT_ROOT / "data" / "docs"


def _embed_batch(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]


def _split_by_headings(content: str, min_length: int = 100) -> list[dict]:
    chunks = []
    current_heading = "Introduction"
    current_lines = []

    for line in content.splitlines():
        if line.startswith("## "):
            if current_lines:
                chunk_text = "\n".join(current_lines).strip()
                if len(chunk_text) >= min_length:
                    chunks.append({"heading": current_heading, "text": chunk_text})
            current_heading = line.lstrip("#").strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        chunk_text = "\n".join(current_lines).strip()
        if len(chunk_text) >= min_length:
            chunks.append({"heading": current_heading, "text": chunk_text})

    return chunks


def main():
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    existing = [c.name for c in chroma_client.list_collections()]
    if "navigator_docs" in existing:
        col = chroma_client.get_collection("navigator_docs")
        if col.count() > 0:
            print("Navigator index already exists. Delete db/chroma_db to re-index.")
            return

    if not DOCS_DIR.exists():
        print(f"ERROR: Documentation directory not found: {DOCS_DIR}")
        print("Create the directory and add .md files before running this script.")
        return

    md_files = list(DOCS_DIR.glob("*.md"))
    if not md_files:
        print(f"ERROR: No .md files found in {DOCS_DIR}")
        print("Add markdown documentation files to data/docs/ before running this script.")
        print("Each file should use ## headings to divide content into sections.")
        return

    collection = chroma_client.get_or_create_collection(
        "navigator_docs",
        metadata={"hnsw:space": "cosine"},
    )

    all_ids = []
    all_texts = []
    all_metas = []
    total_files = 0

    for md_file in md_files:
        source_file = md_file.stem
        content = md_file.read_text(encoding="utf-8")
        chunks = _split_by_headings(content)

        for chunk_index, chunk in enumerate(chunks):
            all_ids.append(f"{source_file}_{chunk_index}")
            all_texts.append(chunk["text"])
            all_metas.append({
                "source_file": source_file,
                "heading": chunk["heading"],
                "chunk_index": chunk_index,
            })

        total_files += 1

    if not all_texts:
        print("ERROR: No valid chunks extracted from documentation files.")
        print("Ensure your .md files contain ## headings and sufficient content.")
        return

    # Embed in batches of 20
    batch_size = 20
    all_embeddings = []
    for i in range(0, len(all_texts), batch_size):
        batch = all_texts[i : i + batch_size]
        embeddings = _embed_batch(batch)
        all_embeddings.extend(embeddings)

    # Upsert into ChromaDB
    upsert_batch = 50
    for i in range(0, len(all_ids), upsert_batch):
        collection.upsert(
            ids=all_ids[i : i + upsert_batch],
            documents=all_texts[i : i + upsert_batch],
            embeddings=all_embeddings[i : i + upsert_batch],
            metadatas=all_metas[i : i + upsert_batch],
        )

    print(f"✓ Navigator index ready: {total_files} files → {len(all_ids)} chunks")


if __name__ == "__main__":
    main()
