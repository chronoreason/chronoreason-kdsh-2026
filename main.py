from src.ingestion.chunker import chunk_text
from src.retrieval.pathway_store import PathwayStore
from src.reasoning.claim_extractor import extract_claims
from src.reasoning.claim_validator import validate_claim
from src.reasoning.contradiction_score import contradiction_score
from src.reasoning.decision_engine import final_decision

with open("data/sample/story.txt") as f:
    story = f.read()

with open("data/sample/backstory.txt") as f:
    backstory = f.read()

chunks = chunk_text(story)
store = PathwayStore(chunks)
claims = extract_claims(backstory)

validations = []

for claim in claims:
    evidence = store.search(claim)
    result = validate_claim(claim, evidence)
    validations.append(result)

score = contradiction_score(validations)
decision = final_decision(score)

print("Contradiction Score:", score)
print("Final Decision:", "CONSISTENT" if decision == 1 else "INCONSISTENT")
