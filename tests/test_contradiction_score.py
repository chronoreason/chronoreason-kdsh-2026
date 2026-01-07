"""Unit tests for reasoning.contradiction_score module."""
import pytest
from reasoning.contradiction_score import contradiction_score


class TestContradictionScoreBasic:
    """Test basic contradiction scoring."""

    def test_contradiction_score_all_support(self, validations_all_support):
        """Test score when all validations support."""
        score = contradiction_score(validations_all_support)
        assert score == 0.0

    def test_contradiction_score_all_contradict(self, validations_all_contradict):
        """Test score when all validations contradict."""
        score = contradiction_score(validations_all_contradict)
        assert score == 1.0

    def test_contradiction_score_mixed(self, validations_mixed):
        """Test score with mixed validations."""
        score = contradiction_score(validations_mixed)
        assert 0.0 < score < 1.0

    def test_contradiction_score_with_neutral(self):
        """Test that neutral adds 0.5 to score."""
        validations = ["neutral", "neutral", "neutral"]
        score = contradiction_score(validations)
        expected = (0.5 + 0.5 + 0.5) / 3
        assert abs(score - expected) < 0.01


class TestContradictionScoreEdgeCases:
    """Test edge cases."""

    def test_contradiction_score_empty_list(self):
        """Test score with empty validation list."""
        result = contradiction_score([])
        assert result == 0.0

    def test_contradiction_score_single_support(self):
        """Test score with single support."""
        score = contradiction_score(["support"])
        assert score == 0.0

    def test_contradiction_score_single_contradict(self):
        """Test score with single contradict."""
        score = contradiction_score(["contradict"])
        assert score == 1.0

    def test_contradiction_score_single_neutral(self):
        """Test score with single neutral."""
        score = contradiction_score(["neutral"])
        assert score == 0.5

    def test_contradiction_score_one_contradict_many_support(self):
        """Test score with mostly support and one contradict."""
        validations = ["support"] * 9 + ["contradict"]
        score = contradiction_score(validations)
        expected = 1.0 / 10
        assert abs(score - expected) < 0.01


class TestContradictionScoreRanges:
    """Test that scores stay within valid ranges."""

    def test_score_between_0_and_1(self, validations_mixed):
        """Test that score is always between 0 and 1."""
        for _ in range(10):
            score = contradiction_score(validations_mixed)
            assert 0.0 <= score <= 1.0

    def test_score_capped_at_1(self):
        """Test that score is capped at 1.0."""
        validations = ["contradict"] * 100
        score = contradiction_score(validations)
        assert score == 1.0

    def test_many_neutral_values(self):
        """Test with many neutral values."""
        validations = ["neutral"] * 100
        score = contradiction_score(validations)
        assert abs(score - 0.5) < 0.01


class TestContradictionScoreConsistency:
    """Test consistency and determinism."""

    def test_same_input_same_output(self, validations_mixed):
        """Test that same input produces same output."""
        result1 = contradiction_score(validations_mixed)
        result2 = contradiction_score(validations_mixed)
        assert result1 == result2

    def test_order_invariant_for_same_values(self):
        """Test that order doesn't matter (it should, actually, but consistency is key)."""
        validations1 = ["support", "contradict", "neutral"]
        validations2 = ["contradict", "support", "neutral"]
        # Same values in different order should give same score
        score1 = contradiction_score(validations1)
        score2 = contradiction_score(validations2)
        assert score1 == score2
