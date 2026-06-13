"""
Generation  (planning.md — Stage 5)

retrieve() → format context → Groq llama3-8b → answer + sources

The model is given ONLY the retrieved chunks as its knowledge base.
The system prompt forbids it from using any outside knowledge.
If the answer is not in the chunks, it says so explicitly.
"""

import os
import time
from groq import Groq, RateLimitError
from dotenv import load_dotenv
from retrieve import retrieve

load_dotenv()

GROQ_MODEL = "llama-3.1-8b-instant"
TOP_K = 8

SYSTEM_PROMPT = """You are an assistant for prospective students considering Panhellenic sorority recruitment at Drexel University.

STRICT RULES — follow every one of them:
1. Answer ONLY using information explicitly present in the CONTEXT block below.
2. Do NOT use any outside knowledge, training data, or general facts about sororities or Greek life.
3. For opinion or ranking questions, synthesize what the sources actually say (e.g. "Several reviewers say…" or "One Reddit commenter ranked…"). Do not refuse to answer just because opinions differ — summarize them.
4. If the context genuinely contains no relevant information at all, respond with exactly:
   "I don't have enough information in my sources to answer that."
5. Never invent names, events, dates, rankings, or opinions that are not explicitly stated in the context.
6. Every claim in your answer must be traceable to at least one of the numbered [1]–[5] sources in the context.
7. Keep answers concise. Do not pad with filler, caveats, or disclaimers beyond what the rules require.
8. NEVER use bracket labels like "[1]", "[2]", "[3]" in your answer. Instead, naturally weave in a brief source name — use plain phrases like "according to GreekRank reviewers", "on Reddit", "per the official Drexel PHC page", or "according to Wikipedia". Keep it short and conversational, not a formal citation."""


def build_context_block(chunks: list[dict]) -> str:
    """
    Format retrieved chunks into a numbered CONTEXT block for the prompt.
    Each entry shows the source label and the chunk text.
    """
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(
            f"[{i}] SOURCE: {chunk['source']}\n"
            f"{chunk['text'].strip()}"
        )
    return "\n\n".join(parts)


def format_sources(chunks: list[dict]) -> str:
    """Deduplicated source list for display after the answer."""
    seen = []
    for chunk in chunks:
        label = f"{chunk['source']}  (similarity {1 - chunk['distance']:.0%})"
        if label not in seen:
            seen.append(label)
    return "\n".join(f"  [{i+1}] {s}" for i, s in enumerate(seen))


def answer(question: str, k: int = TOP_K) -> dict:
    """
    Full RAG pipeline: retrieve → generate → return answer + sources.

    Returns:
        {
            "answer":  str,          # model's grounded response
            "sources": str,          # formatted source attribution block
            "chunks":  list[dict],   # raw retrieved chunks (for inspection)
        }
    """
    chunks = retrieve(question, k=k)
    context = build_context_block(chunks)

    user_message = (
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {question}"
    )

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": user_message},
                ],
                temperature=0.0,
                max_tokens=512,
            )
            break
        except RateLimitError:
            if attempt == 2:
                raise
            time.sleep(30)   # wait 30 s then retry

    return {
        "answer":  response.choices[0].message.content.strip(),
        "sources": format_sources(chunks),
        "chunks":  chunks,
    }
