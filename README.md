# ChronoReason – Kharagpur Data Science Hackathon 2026

ChronoReason is an AI system that determines whether a hypothetical
character backstory is causally and logically consistent with a full-length
novel (100k+ words).

This project focuses on long-context reasoning, evidence aggregation,
and temporal causal analysis rather than surface-level text generation.

---

## Problem Statement
Large language models often fail to maintain global consistency over long
narratives. Earlier events impose constraints that affect later outcomes.
This project reframes the challenge as a structured reasoning and
classification task.

---

## Our Approach
1. Extract factual claims from the hypothetical backstory
2. Chunk and embed the full novel
3. Retrieve evidence using Pathway vector search
4. Validate each claim against multiple passages
5. Build event → effect timelines
6. Compute a contradiction strength score
7. Produce a final consistency decision

---

## Key Features
- Evidence-based reasoning
- Long-context handling using Pathway
- Temporal event–effect graphs
- Quantitative contradiction scoring
- Explainable outputs for judges

---

## Tech Stack
- Python
- Pathway
- Streamlit
- Sentence Transformers
- OpenAI API
- NetworkX, Matplotlib

---

## How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
