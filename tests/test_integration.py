"""Integration tests for the full pipeline."""
import pytest
from ingestion.chunker import chunk_text
from retrieval.pathway_store import PathwayStore
from reasoning.claim_extractor import extract_claims
from reasoning.contradiction_score import contradiction_score
from reasoning.decision_engine import final_decision
from reasoning.timeline_builder import build_timeline


class TestPipelineIntegration:
    """Test the full pipeline working together."""

    def test_pipeline_basic_flow(self, sample_text, sample_backstory):
        """Test complete pipeline with sample data."""
        # Ingest
        chunks = chunk_text(sample_text, chunk_size=100, overlap=20)
        assert len(chunks) > 0

        # Retrieve
        store = PathwayStore(chunks)
        assert store.embeddings.shape[0] > 0

        # Extract claims
        claims = extract_claims(sample_backstory)
        assert len(claims) > 0

        # Validate (mock)
        validations = ["support", "support", "neutral"]
        
        # Score
        score = contradiction_score(validations)
        assert 0.0 <= score <= 1.0

        # Decide
        decision = final_decision(score)
        assert decision in [0, 1]

        # Timeline
        timeline = build_timeline(chunks[:3])
        assert len(timeline) > 0

    def test_pipeline_with_contradictory_backstories(self, sample_text, sample_backstory, contradictory_backstory):
        """Test pipeline with contradictory backstories."""
        chunks = chunk_text(sample_text)
        store = PathwayStore(chunks)

        claims1 = extract_claims(sample_backstory)
        claims2 = extract_claims(contradictory_backstory)

        assert claims1 != claims2

    def test_pipeline_search_and_validate(self, sample_text):
        """Test searching for evidence."""
        chunks = chunk_text(sample_text, chunk_size=50)
        store = PathwayStore(chunks)

        # Search for something
        results = store.search("brave", top_k=3)
        assert isinstance(results, list)

    def test_pipeline_end_to_end(self):
        """Complete end-to-end test with synthetic data."""
        # Create synthetic story
        story = """
        The hero was brave and faced danger.
        He sailed across the ocean to save people.
        He risked his life for others.
        He succeeded in his mission.
        """ * 3

        # Create backstory that supports the story
        backstory_support = """
        The hero was courageous.
        He was willing to sail the ocean.
        He believed in helping others.
        """

        # Full pipeline
        chunks = chunk_text(story, chunk_size=50, overlap=10)
        store = PathwayStore(chunks)

        claims = extract_claims(backstory_support)
        
        # Validate claims (mock validations)
        validations = ["support"] * len(claims) if claims else ["support"]

        score = contradiction_score(validations)
        decision = final_decision(score)

        # Should be consistent (no contradictions)
        assert decision == 1
        assert score < 0.6

    def test_pipeline_with_empty_inputs(self):
        """Test pipeline gracefully handles empty inputs."""
        # Empty story
        chunks = chunk_text("", chunk_size=50)
        assert chunks == []

        # Empty backstory
        claims = extract_claims("")
        assert claims == []

        # Empty validations
        score = contradiction_score([])
        assert score == 0.0

        # Empty timeline
        timeline = build_timeline([])
        assert timeline == []


class TestPipelineRobustness:
    """Test pipeline robustness and error handling."""

    def test_pipeline_with_large_text(self):
        """Test pipeline with large text input."""
        large_text = " ".join(["word"] * 5000)
        chunks = chunk_text(large_text, chunk_size=100)
        assert len(chunks) > 0

        store = PathwayStore(chunks)
        results = store.search("word", top_k=5)
        assert len(results) > 0

    def test_pipeline_with_special_characters(self):
        """Test pipeline with special characters."""
        special_text = "Text with @#$%^&*() and !@#$%^&*()"
        chunks = chunk_text(special_text)
        
        backstory = "Claim @#$ with special chars!"
        claims = extract_claims(backstory)
        assert len(claims) > 0

    def test_pipeline_consistency_across_runs(self):
        """Test that pipeline produces consistent results."""
        text = "The story of a brave hero who sailed the seas."
        backstory = "The hero was brave and sailed."

        # Run pipeline twice
        chunks1 = chunk_text(text)
        claims1 = extract_claims(backstory)
        timeline1 = build_timeline(chunks1)

        chunks2 = chunk_text(text)
        claims2 = extract_claims(backstory)
        timeline2 = build_timeline(chunks2)

        assert chunks1 == chunks2
        assert claims1 == claims2
        assert timeline1 == timeline2
