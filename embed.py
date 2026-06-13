"""
Embedding + Vector Store  (planning.md — Stage 3)

Loads chunks from ingest.py, embeds each chunk's metadata-prepended text
with all-MiniLM-L6-v2 (sentence-transformers), and persists in ChromaDB.

Usage:
    python embed.py          # build / rebuild the vector store
"""

import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from pathlib import Path

from ingest import load_chunks

CHROMA_DIR = str(Path(__file__).parent / "chroma_db")
COLLECTION_NAME = "drexel_panhellenic"
EMBED_MODEL = "all-MiniLM-L6-v2"
BATCH_SIZE = 64   # embed in batches to avoid memory spikes on large corpora


def build_vector_store(reset: bool = False) -> chromadb.Collection:
    """
    Embed all chunks and upsert into ChromaDB.

    Args:
        reset: if True, delete and recreate the collection from scratch.

    Returns:
        The ChromaDB collection.
    """
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
            print(f"Deleted existing collection '{COLLECTION_NAME}'")
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks from documents/")

    model = SentenceTransformer(EMBED_MODEL)
    print(f"Embedding with {EMBED_MODEL} …")

    # Embed in batches
    for batch_start in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[batch_start : batch_start + BATCH_SIZE]

        embed_texts = [c["embed_text"] for c in batch]
        embeddings = model.encode(embed_texts, show_progress_bar=False).tolist()

        collection.upsert(
            ids=[
                f"{c['filename']}_chunk{c['chunk_index']}"
                for c in batch
            ],
            embeddings=embeddings,
            documents=[c["text"] for c in batch],      # raw text stored for display
            metadatas=[
                {
                    "source": c["source"],
                    "filename": c["filename"],
                    "chunk_index": c["chunk_index"],
                }
                for c in batch
            ],
        )
        end = min(batch_start + BATCH_SIZE, len(chunks))
        print(f"  Upserted chunks {batch_start + 1}–{end}")

    total = collection.count()
    print(f"\nVector store ready — {total} vectors in '{COLLECTION_NAME}'")
    return collection


if __name__ == "__main__":
    build_vector_store(reset=True)
