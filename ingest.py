"""
Document Ingestion + Chunking  (planning.md — Stage 1 & 2)

Loads all .txt files from documents/, splits each into overlapping chunks of
300 words / 50-word overlap, and attaches source metadata to each chunk.

Usage (standalone verification):
    python ingest.py
"""

import os
import re
from pathlib import Path
from typing import Generator

DOCS_DIR = Path(__file__).parent / "documents"
CHUNK_SIZE = 300   # words (≈ tokens for sentence-transformers)
CHUNK_OVERLAP = 50


def _source_label(filename: str) -> str:
    """Map filename to a human-readable source label used as metadata prefix."""
    mapping = {
        "asa_greekrank": "GreekRank reviews — Alpha Sigma Alpha at Drexel",
        "dphie_greekrank": "GreekRank reviews — Delta Phi Epsilon at Drexel",
        "dz_greekrank": "GreekRank reviews — Delta Zeta at Drexel",
        "phisig_greekrank": "GreekRank reviews — Phi Sigma Sigma at Drexel",
        "asa_about": "Alpha Sigma Alpha official information and Drexel chapter",
        "dphie_about": "Delta Phi Epsilon official information and Drexel chapter",
        "dz_about": "Delta Zeta official information and Drexel chapter",
        "dg_about": "Delta Gamma official information and Drexel chapter",
        "phisig_about": "Phi Sigma Sigma official information and Drexel chapter",
        "reddit_sororities": "Reddit r/Drexel — student discussions about sororities",
        "drexel_recruitment_official": "Drexel University official Greek Life page — Panhellenic recruitment",
        "recruitment_2026": "Drexel Panhellenic recruitment schedule Fall 2026",
        "drexel_phc": "Drexel Panhellenic Council — recognized sororities and contacts",
        "cc_drexel_sorority": "College Confidential forum — Drexel sorority discussion",
    }
    stem = Path(filename).stem
    return mapping.get(stem, stem)


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> Generator[str, None, None]:
    """
    Split text into overlapping word-based chunks.

    Yields chunks of `chunk_size` words with `overlap` words carried over
    from the previous chunk so context is not lost at boundaries.
    """
    words = text.split()
    if not words:
        return
    start = 0
    while start < len(words):
        end = start + chunk_size
        yield " ".join(words[start:end])
        if end >= len(words):
            break
        start += chunk_size - overlap


def load_chunks() -> list[dict]:
    """
    Load all documents, chunk them, and return a list of chunk records.

    Each record:
        {
            "text": str,             # raw chunk text
            "embed_text": str,       # metadata-prepended text used for embedding
            "source": str,           # human-readable source label
            "filename": str,         # original filename
            "chunk_index": int,      # 0-based position within the document
        }
    """
    chunks = []
    for path in sorted(DOCS_DIR.glob("*.txt")):
        if path.name == ".gitkeep":
            continue
        raw = path.read_text(encoding="utf-8")
        # Strip the source-header line written by clean_docs.py so it
        # doesn't pollute every chunk, but capture it for metadata.
        lines = raw.splitlines()
        if lines and lines[0].startswith("Source:"):
            raw = "\n".join(lines[1:]).strip()

        source = _source_label(path.name)

        for idx, chunk in enumerate(chunk_text(raw)):
            # Prepend metadata before embedding (per planning.md)
            embed_text = f"Source: {source}\n{chunk}"
            chunks.append(
                {
                    "text": chunk,
                    "embed_text": embed_text,
                    "source": source,
                    "filename": path.name,
                    "chunk_index": idx,
                }
            )
    return chunks


if __name__ == "__main__":
    chunks = load_chunks()
    # Group by filename for a quick summary
    from collections import Counter
    counts = Counter(c["filename"] for c in chunks)
    print(f"Total chunks: {len(chunks)}\n")
    print(f"{'File':<40} {'Chunks':>6}")
    print("-" * 48)
    for fname, n in sorted(counts.items()):
        print(f"{fname:<40} {n:>6}")

    # Spot-check: print first chunk of asa_greekrank
    sample = next(c for c in chunks if c["filename"] == "asa_greekrank.txt")
    print("\n── Sample embed_text (asa_greekrank chunk 0) ──")
    print(sample["embed_text"][:600])
