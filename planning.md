# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain


Rushing and Greek life at Drexel University — specifically Panhellenic sorority
recruitment. This knowledge is valuable because prospective members rely heavily
on word-of-mouth, scattered Instagram posts, and Reddit threads to understand
what rushing actually looks like at Drexel. Official channels only describe
the process formally; they don't capture chapter culture, what to wear, how
co-op affects involvement, or honest opinions about specific sororities.---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
| 1  | Drexel Panhellenic Instagram  | Recruitment posts, bios, event captions   | @drexelpanhellenic on Instagram |
| 2  | Alpha Sigma Alpha Instagram   | Recruitment posts, chapter culture        | @asadrexel on Instagram         
| 3  | Delta Phi Epsilon Instagram   | Recruitment content, sister spotlights    | @drexeldphie on Instagram       |
| 4  | Delta Zeta Instagram          | Rush posts, event captions                | @drexeldeltazeta on Instagram   |
| 5  | Phi Sigma Sigma Instagram     | Recruitment reels, chapter highlights     | @drexelphisig on Instagram      |
| 6  | Delta Gamma Instagram         | Recruitment posts, chapter culture        | @drexeldg on Instagram          |
| 7  | r/Drexel — rush threads       | Student Q&A and personal rush experiences | reddit.com/r/Drexel             |
| 8  | r/Drexel — Greek life threads | General Greek life discussion and advice  | reddit.com/r/Drexel             |
| 9  | Niche.com Drexel Greek life   | Student-written reviews of Greek life     | niche.com/colleges/drexel-university/greek-life/ |
| 10 | GreekRank.com Drexel          | Candid student reviews of each sorority   | greekrank.com (search: Drexel)  |       |


---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
300
**Overlap:**
50
**Reasoning:**
There should be at least 2-3 sentence, if we make like 200 chunks if someone asks "what do students say about the recruitment process?" the answer might be "they are welcoming" without explaining to which sorority it refers to, overlap is 50 because it should be 1/6 of chunk size
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
Prepend meta data before embedding
**Top-k:**
K = 5
**Production tradeoff reflection:**
It will probably not capture the real opinion, it will get only 5 opinion so not the full picture sometimes
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |  How many days does Panhellenic recruitment last at Drexel? | Recruitment lasts 3 days  |
| 2 | What rounds does Panhellenic recruitment at Drexel consist of?  | Recruitment consists of multiple rounds where PNMs visit each chapter house, getting cut down each round until preference night and bid day |
| 3 | How many times can you rush at Drexel? |  You can rush 2 times per year, once in fall and once in spring. Spring recruitment is usually easier since fewer girls participate |
| 4 | What is considered the best sorority on campus at Drexel?  |  Phi Sigma Sigma and Delta Zeta are frequently mentioned as top tier, with DPhiE praised for being the nicest and most philanthropic |
| 5 | Is it free to rush a sorority at Drexel? | No, there is a $25 non-refundable registration fee to participate in Panhellenic recruitment, plus semester dues once you join a sorority |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.Noisy and opinionated sources:** Instagram captions and Reddit comments
   are informal, sometimes contradictory, and often written with strong
   personal bias. Two students can describe the same sorority very
   differently — one Reddit post might call DPhiE the nicest sorority while
   another says they are cliquey. The system may retrieve conflicting chunks
   and struggle to synthesize a balanced answer without taking sides.

2.Chunks splitting key context:** A Reddit comment might name a sorority
   in one sentence and describe its culture in the next. If those sentences
   fall in different chunks, retrieval may return the description without the
   sorority name, making the answer confusing or impossible to attribute
   correctly. The 50 token overlap helps but will not fully solve this for
   longer comments.
---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---## Architecture

Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation

[Raw .txt files]     [chunk_text()]    [all-MiniLM-L6-v2]     [cosine          [Groq API]
Instagram captions   300 tokens /      sentence-transformers    similarity       llama3-8b
Reddit comments      50 overlap        ChromaDB                 top-k = 5        
 Wikipedia                                                   query → 
GreekRank reviews                                               nearest chunks

## AI Tool Plan


I will give Claude my Chunking Strategy section from this planning.md and
ask it to implement ingest.py with a chunk_text() function using 300 token
chunks and 50 token overlap. I will verify the output by printing chunk
counts per document and spot-checking that no chunk cuts off mid-sentence
and that each chunk contains only one sorority's content where possible.
**Milestone 3 — Ingestion and chunking:**


**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
