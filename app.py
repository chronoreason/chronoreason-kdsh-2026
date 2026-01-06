import streamlit as st
from src.ingestion.chunker import chunk_text
from src.retrieval.pathway_store import PathwayStore
from src.reasoning.claim_extractor import extract_claims
from src.reasoning.claim_validator import validate_claim
from src.reasoning.contradiction_score import contradiction_score
from src.reasoning.decision_engine import final_decision

st.title("ChronoReason 🧠⏳")

story_file = st.file_uploader("Upload Story", type=["txt"])
backstory_file = st.file_uploader("Upload Backstory", type=["txt"])

if story_file and backstory_file:
    story = story_file.read().decode()
    backstory = backstory_file.read().decode()

    chunks = chunk_text(story)
    store = PathwayStore(chunks)
    claims = extract_claims(backstory)

    validations = []
    for claim in claims:
        evidence = store.search(claim)
        validations.append(validate_claim(claim, evidence))

    score = contradiction_score(validations)
    decision = final_decision(score)

    st.metric("Contradiction Score", score)
    st.success("CONSISTENT ✅" if decision == 1 else "INCONSISTENT ❌")
