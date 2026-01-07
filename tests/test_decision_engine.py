"""Unit tests for reasoning.decision_engine module."""
import pytest
from reasoning.decision_engine import final_decision


class TestFinalDecisionBasic:
    """Test basic decision logic."""

    def test_decision_consistent_low_score(self):
        """Test consistent decision with low contradiction score."""
        decision = final_decision(0.3)
        assert decision == 1  # Consistent

    def test_decision_inconsistent_high_score(self):
        """Test inconsistent decision with high contradiction score."""
        decision = final_decision(0.8)
        assert decision == 0  # Inconsistent

    def test_decision_at_threshold(self):
        """Test decision at threshold boundary."""
        decision = final_decision(0.6)
        assert decision == 0  # Inconsistent (>= threshold)

    def test_decision_just_below_threshold(self):
        """Test decision just below threshold."""
        decision = final_decision(0.59)
        assert decision == 1  # Consistent


class TestFinalDecisionEdgeCases:
    """Test edge cases."""

    def test_decision_zero_score(self):
        """Test decision with zero contradiction score."""
        decision = final_decision(0.0)
        assert decision == 1  # Consistent

    def test_decision_perfect_score(self):
        """Test decision with perfect contradiction score."""
        decision = final_decision(1.0)
        assert decision == 0  # Inconsistent

    def test_decision_negative_score(self):
        """Test decision with negative score (shouldn't happen but should handle)."""
        decision = final_decision(-0.5)
        assert decision == 1  # Consistent


class TestFinalDecisionCustomThreshold:
    """Test with custom thresholds."""

    def test_decision_custom_threshold_high(self):
        """Test decision with high custom threshold."""
        decision = final_decision(0.5, threshold=0.8)
        assert decision == 1  # Consistent (0.5 < 0.8)

    def test_decision_custom_threshold_low(self):
        """Test decision with low custom threshold."""
        decision = final_decision(0.5, threshold=0.2)
        assert decision == 0  # Inconsistent (0.5 >= 0.2)

    def test_decision_custom_threshold_zero(self):
        """Test decision with zero threshold."""
        decision = final_decision(0.0, threshold=0.0)
        assert decision == 0  # Inconsistent (0.0 >= 0.0)

    def test_decision_custom_threshold_one(self):
        """Test decision with threshold of 1."""
        decision = final_decision(0.99, threshold=1.0)
        assert decision == 1  # Consistent (0.99 < 1.0)


class TestFinalDecisionConsistency:
    """Test consistency and determinism."""

    def test_same_input_same_output(self):
        """Test that same input produces same output."""
        score = 0.45
        result1 = final_decision(score)
        result2 = final_decision(score)
        assert result1 == result2

    def test_monotonic_behavior(self):
        """Test that decision changes appropriately with increasing score."""
        # Lower scores should be consistent
        assert final_decision(0.1) == 1
        assert final_decision(0.3) == 1
        assert final_decision(0.5) == 1
        # Higher scores should be inconsistent
        assert final_decision(0.7) == 0
        assert final_decision(0.9) == 0
