"""Unit tests for reasoning.claim_extractor module."""
import pytest
from reasoning.claim_extractor import extract_claims


class TestExtractClaimsBasic:
    """Test basic claim extraction."""

    def test_extract_claims_normal(self, sample_backstory):
        """Test extracting claims from backstory."""
        claims = extract_claims(sample_backstory)
        assert isinstance(claims, list)
        assert len(claims) > 0
        assert all(isinstance(c, str) for c in claims)

    def test_extract_claims_filters_short_sentences(self):
        """Test that very short sentences are filtered."""
        text = "A. B. This is a proper claim that should be extracted."
        claims = extract_claims(text)
        # Should not include "A" or "B"
        assert not any(c in claims for c in ["A", "B"])

    def test_extract_claims_returns_full_sentence(self, sample_backstory):
        """Test that extracted claims are full sentences."""
        claims = extract_claims(sample_backstory)
        for claim in claims:
            assert len(claim) > 10
            assert len(claim) < 500


class TestExtractClaimsEdgeCases:
    """Test edge cases."""

    def test_extract_claims_empty_string(self):
        """Test extracting from empty string."""
        result = extract_claims("")
        assert result == []

    def test_extract_claims_whitespace_only(self):
        """Test extracting from whitespace-only string."""
        result = extract_claims("   \n\t  ")
        assert result == []

    def test_extract_claims_no_periods(self):
        """Test text with no sentence delimiters."""
        text = "This is a long claim without periods"
        claims = extract_claims(text)
        assert len(claims) >= 1

    def test_extract_claims_multiple_periods(self):
        """Test text with multiple consecutive periods."""
        text = "Claim one... Claim two.. Final claim."
        claims = extract_claims(text)
        assert len(claims) >= 1

    def test_extract_claims_only_short_sentences(self):
        """Test text with only short sentences."""
        text = "A. B. C. D. E."
        claims = extract_claims(text)
        assert claims == []

    def test_extract_claims_max_length_filter(self):
        """Test that very long sentences are filtered."""
        long_sentence = " ".join(["word"] * 600) + "."
        short_sentence = "This is a normal claim."
        text = f"{long_sentence} {short_sentence}"
        claims = extract_claims(text)
        # Long sentence should be filtered
        assert not any(len(c) > 500 for c in claims)


class TestExtractClaimsConsistency:
    """Test consistency and determinism."""

    def test_extract_same_input_same_output(self, sample_backstory):
        """Test that same input produces same output."""
        result1 = extract_claims(sample_backstory)
        result2 = extract_claims(sample_backstory)
        assert result1 == result2

    def test_extract_contradictory_backstories(self, sample_backstory, contradictory_backstory):
        """Test that different backstories produce different claims."""
        claims1 = extract_claims(sample_backstory)
        claims2 = extract_claims(contradictory_backstory)
        # At least some claims should be different
        assert claims1 != claims2
