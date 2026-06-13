"""
Retrieval  (planning.md — Stage 4)

Provides retrieve() — given a natural-language query, embeds it with the
same model used at index time and returns the top-k most similar chunks
from ChromaDB (cosine similarity, k=5 by default).

Usage (standalone test):
    python retrieve.py "What are students saying about Delta Zeta?"
"""

import sys
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

CHROMA_DIR = str(Path(__file__).parent / "chroma_db")
COLLECTION_NAME = "drexel_panhellenic"
EMBED_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5

# Module-level singletons so callers (generate.py) don't reload the model
# on every call.
_model: SentenceTransformer | None = None
_collection: chromadb.Collection | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def _get_collection() -> chromadb.Collection:
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = client.get_collection(COLLECTION_NAME)
    return _collection


def retrieve(query: str, k: int = TOP_K) -> list[dict]:
    """
    Embed `query` and return the top-k chunks by cosine similarity.

    Returns a list of dicts, each with:
        "text"        — the chunk text
        "source"      — human-readable source label
        "filename"    — original filename
        "chunk_index" — position within the document
        "distance"    — cosine distance (lower = more similar)
    """
    model = _get_model()
    collection = _get_collection()

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append(
            {
                "text": doc,
                "source": meta["source"],
                "filename": meta["filename"],
                "chunk_index": meta["chunk_index"],
                "distance": dist,
            }
        )

    return chunks


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else (
        "What do students say about Delta Zeta at Drexel?"
    )
    print(f"Query: {query}\n")
    results = retrieve(query)
    for i, r in enumerate(results, 1):
        print(f"[{i}] {r['source']}  (chunk {r['chunk_index']}, dist={r['distance']:.4f})")
        print(r["text"][:300])
        print()
