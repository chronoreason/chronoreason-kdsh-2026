"""Unit tests for reasoning.timeline_builder module."""
import pytest
from reasoning.timeline_builder import build_timeline


class TestBuildTimelineBasic:
    """Test basic timeline building."""

    def test_build_timeline_normal(self):
        """Test building timeline from evidence."""
        evidence = [
            "Event one happened",
            "Then event two occurred",
            "Finally event three took place"
        ]
        timeline = build_timeline(evidence)
        assert isinstance(timeline, list)
        assert len(timeline) == 3

    def test_build_timeline_structure(self):
        """Test that timeline entries have required fields."""
        evidence = ["Event one", "Event two"]
        timeline = build_timeline(evidence)
        for entry in timeline:
            assert "event" in entry
            assert "time" in entry
            assert "effect" in entry

    def test_build_timeline_preserves_content(self):
        """Test that event text is fully preserved."""
        evidence = ["This is a very long event description that should not be truncated"]
        timeline = build_timeline(evidence)
        assert timeline[0]["event"] == evidence[0]

    def test_build_timeline_sequence_numbering(self):
        """Test that events are sequentially numbered."""
        evidence = ["E1", "E2", "E3", "E4"]
        timeline = build_timeline(evidence)
        for i, entry in enumerate(timeline):
            assert entry["time"] == f"event_{i}"


class TestBuildTimelineEdgeCases:
    """Test edge cases."""

    def test_build_timeline_empty_list(self):
        """Test building timeline from empty evidence list."""
        result = build_timeline([])
        assert result == []

    def test_build_timeline_single_event(self):
        """Test building timeline with single event."""
        evidence = ["Only event"]
        timeline = build_timeline(evidence)
        assert len(timeline) == 1
        assert timeline[0]["event"] == "Only event"

    def test_build_timeline_long_events(self):
        """Test with very long event descriptions."""
        long_event = " ".join(["word"] * 1000)
        evidence = [long_event]
        timeline = build_timeline(evidence)
        assert timeline[0]["event"] == long_event

    def test_build_timeline_special_characters(self):
        """Test with special characters in events."""
        evidence = [
            "Event with!@#$%^&*() special chars",
            "Event with 'quotes' and \"double quotes\"",
            "Event with\nnewlines\nand\ttabs"
        ]
        timeline = build_timeline(evidence)
        for i, entry in enumerate(timeline):
            assert entry["event"] == evidence[i]


class TestBuildTimelineConsistency:
    """Test consistency and determinism."""

    def test_same_input_same_output(self):
        """Test that same input produces same output."""
        evidence = ["Event A", "Event B", "Event C"]
        result1 = build_timeline(evidence)
        result2 = build_timeline(evidence)
        assert result1 == result2

    def test_timeline_order_preserved(self):
        """Test that event order is preserved."""
        evidence = ["First", "Second", "Third", "Fourth"]
        timeline = build_timeline(evidence)
        for i, entry in enumerate(timeline):
            assert entry["event"] == evidence[i]
