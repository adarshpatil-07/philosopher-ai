import uuid
import chromadb
from sentence_transformers import SentenceTransformer
from app.config import CHROMA_DIR, EMBED_MODEL

_model = SentenceTransformer(EMBED_MODEL)
_client = chromadb.PersistentClient(path=CHROMA_DIR)

BATCH_SIZE = 500


def _collection(persona: str):
    # One collection per persona, so Kafka only searches Kafka's books
    return _client.get_or_create_collection(
        name=f"persona_{persona}",
        metadata={"hnsw:space": "cosine"},
    )


def add_chunks(persona: str, chunks: list[dict]) -> int:
    col = _collection(persona)
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]
        texts = [c["text"] for c in batch]
        embeddings = _model.encode(texts).tolist()
        col.add(
            ids=[str(uuid.uuid4()) for _ in batch],
            documents=texts,
            embeddings=embeddings,
            metadatas=[{"book": c["book"], "page": c["page"]} for c in batch],
        )
    return len(chunks)


def search(persona: str, query: str, k: int = 4) -> list[dict]:
    col = _collection(persona)
    if col.count() == 0:
        return []
    query_emb = _model.encode([query]).tolist()
    res = col.query(query_embeddings=query_emb, n_results=k)
    results = []
    for doc, meta in zip(res["documents"][0], res["metadatas"][0]):
        results.append({"text": doc, "book": meta["book"], "page": meta["page"]})
    return results


def list_books(persona: str) -> list[str]:
    metas = _collection(persona).get(include=["metadatas"])["metadatas"]
    return sorted({m["book"] for m in metas})


def delete_book(persona: str, book: str) -> None:
    _collection(persona).delete(where={"book": book})