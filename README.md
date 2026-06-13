
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
Which one is best sorority?

**What the system returned:**
According to GreekRank reviews, several reviewers say Delta Zeta (DZ) and Phi Sigma Sigma (Phi Sig) are top contenders for the best sorority at Drexel. DZ has a high rating of 4.8-5.0 TOP TIER across multiple reviews, with reviewers praising their friendly and down-to-earth nature, strong sisterhood, and involvement in philanthropy. Phi Sig also has a high rating of 4.0-5.0 TOP TIER, with reviewers praising their fun and outgoing personalities, strong sisterhood, and involvement in philanthropy.

**Root cause (tied to a specific pipeline stage):**

 The expected answer mentions Phi Sig, DZ, and DPhiE. The system returned only Phi Sig. This is not a hallucination — Phi Sig does have 5.0 TOP TIER reviews in the corpus — but it is an incomplete answer. The system cannot compare all five sororities at once because retrieval only surfaces 8 chunks at a time, so whichever sorority's review chunks score highest for that specific query wins. Running the same question twice can return different sororities depending on which chunks rank in the top 8. This is a known limitation of fixed top-k retrieval for comparative questions.


**What you would change to fix it:**
Create a separate document for the rating isntead of depending to whichever 8 chuck rates the highest, it will give wrong answer always, also have to keep in mind that sororitites are sometimes biased.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The spec made it easy to prompt AI to implement the chunking function — I gave Claude the chunk size (300 tokens) and overlap (50 tokens) from the spec and it translated them directly into code without me having to explain the logic.
**One way your implementation diverged from the spec, and why:**

---The spec said to use local .txt files but didn't plan for a separate cleaning step. During implementation I ended up adding clean_docs.py as a whole extra stage between loading and chunking because the raw files had too much noise — cookie banners, nav menus, GreekRank UI fragments — that would have polluted the chunks.

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*he 5 evaluation questions from planning.md to test the retrieval system — questions like "how many days does recruitment last" and "is it free to rush"
- *What it produced:*Mostly "I don't have enough information to answer that" responses for the majority of questions because the retrieved chunks weren't containing the right content — the system was pulling tangentially related chunks that mentioned recruitment but not the specific facts the questions were asking for
- *What I changed or overrode:*
I kept adding more information as I realized it wasn't enough — the system kept saying it didn't have enough information to answer so I went back and rewrote the questions to be broader and closer to how students actually talk in the reviews and Reddit posts until it started returning real answers.

**Instance 2**

- *What I gave the AI:*
I first tried to scrape the information directly from websites but I could not get it to work so I manually copied the text instead and gave it those .txt files to write the cleaning script
- *What it produced:*
It would give wrong information and didn't understand some things — every answer came with huge blocks of sources attached to it making the output really long and hard to read, and the introductions it wrote were bad and didn't flow naturally, they were too formal and stiff
- *What I changed or overrode:*
I went in and modified the introductions myself to make them shorter and sound more natural. I also trimmed down the sources it was attaching to every single answer because they were overwhelming and not all of them were even relevant.