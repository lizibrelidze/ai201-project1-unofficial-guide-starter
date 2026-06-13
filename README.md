# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

It covers Greek life at Drexel University — specifically Panhellenic sorority recruitment.This knowledge is valuable because prospective members rely heavily on word-of-mouth, scattered Instagram posts, and Reddit threads to understand what rushing actually looks like at Drexel.Sometimes it is hard to find the information, so here all the infomations are combined  .

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| #  | Source                                      | Type                        | URL or file path                                                  |
|----|---------------------------------------------|-----------------------------|-------------------------------------------------------------------|
| 1  | GreekRank — Alpha Sigma Alpha at Drexel     | Student reviews             | https://greekrank.com (search: Drexel, Alpha Sigma Alpha)         |
| 2  | GreekRank — Delta Phi Epsilon at Drexel     | Student reviews             | https://greekrank.com (search: Drexel, Delta Phi Epsilon)         |
| 3  | GreekRank — Delta Zeta at Drexel            | Student reviews             | https://greekrank.com (search: Drexel, Delta Zeta)                |
| 4  | GreekRank — Phi Sigma Sigma at Drexel       | Student reviews             | https://greekrank.com (search: Drexel, Phi Sigma Sigma)           |
| 5  | Reddit r/Drexel — sorority threads          | Student forum discussion    | r/Drexel: "What Are The Sororities Like At Drexel?", "sorority qs", "Thoughts on Drexel greek life" |
| 6  | Drexel University official Greek Life page  | Official university source  | https://drexel.edu/studentlife/get_involved/fraternity_sorority_life/ |
| 7  | CampusDirector — Drexel PHC Fall 2026       | Official recruitment page   | documents/recruitment_2026.txt                                    |
| 8  | Drexel Panhellenic Council sorority list    | Official PHC page           | documents/drexel_phc.txt                                          |
| 9  | Alpha Sigma Alpha national + DragonLink     | Official org / chapter page | documents/asa_about.txt                                           |
| 10 | Delta Phi Epsilon national + DragonLink     | Official org / chapter page | documents/dphie_about.txt                                         |
| 11 | Delta Zeta national + DragonLink            | Official org / chapter page | documents/dz_about.txt                                            |
| 12 | Delta Gamma national + DragonLink           | Official org / chapter page | documents/dg_about.txt                                            |
| 13 | Phi Sigma Sigma national + DragonLink       | Official org / chapter page | documents/phisig_about.txt                                        |
| 14 | College Confidential — Drexel sorority thread | Student forum discussion  | collegeconfidential.com: "Drexel sorority?" (2011 thread)         |
| 15 | Wikipedia — Fraternities and sororities     | Background reference        | https://en.wikipedia.org/wiki/Fraternities_and_sororities_in_North_America |
---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 300 words

**Overlap:** 50 words

**Why these choices fit your documents:**

**Final chunk count:** 208 across 15 documents

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | How many days does Panhellenic recruitment last at Drexel?| Recruitment lasts 3 days|According to the Drexel Panhellenic recruitment schedule Fall 2026, recruitment events take place Thursday, October 1 - Saturday, October 3, with Bid Day occurring on October 4. |Relevant |Accurate |
| 2 | What rounds does Panhellenic recruitment at Drexel consist of?|Recruitment consists of multiple rounds where PNMs visit each chapter house, getting cut down each round until preference night and bid day |According to the Drexel Panhellenic recruitment schedule Fall 2026, recruitment events take place from Thursday, October 1 to Saturday, October 3, with Bid Day occurring on October 4. The specific rounds are not explicitly listed, but according to the Drexel University official Greek Life page — Panhellenic recruitment, the rounds typically include: Orientation, Open House Round, Philanthropy Round, Preference Round, then Bid Day.
 |Partially relevant |Accurate |
| 3 | How many times can you rush at Drexel?|You can rush 2 times per year, once in fall and once in spring. Spring recruitment is usually easier since fewer girls participate |According to the Drexel University official Greek Life page — Panhellenic recruitment, you can rush twice per year — once during formal fall recruitment, and again during informal winter or spring recruitment.
 |Relevant |Accurate |
| 4 | What is considered the best sorority on campus at Drexel?|Phi Sigma Sigma and Delta Zeta are frequently mentioned as top tier, with DPhiE praised for being the nicest and most philanthropic |According to GreekRank reviewers, Phi Sigma Sigma is often considered the best sorority on campus at Drexel, with several reviewers giving them a 5.0 TOP TIER rating.
 |Relevant |Accurate |
| 5 | Is it free to rush a sorority at Drexel?|No, there is a $25 non-refundable registration fee to participate in Panhellenic recruitment, plus semester dues once you join a sorority |According to the Drexel University official Greek Life page, the registration fee for Panhellenic Sorority Recruitment is $25, which is non-refundable. |Relevant |Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
