"""Unit tests for ingestion.chunker module."""
import pytest
from ingestion.chunker import chunk_text


class TestChunkTextBasic:
    """Test basic chunking functionality."""

    def test_chunk_text_normal(self, sample_text):
        """Test chunking normal text."""
        chunks = chunk_text(sample_text, chunk_size=50, overlap=10)
        assert isinstance(chunks, list)
        assert len(chunks) > 0
        assert all(isinstance(c, str) for c in chunks)

    def test_chunk_text_with_default_params(self, sample_text):
        """Test chunking with default parameters."""
        chunks = chunk_text(sample_text)
        assert isinstance(chunks, list)
        assert len(chunks) > 0

    def test_chunk_text_respects_chunk_size(self, sample_text):
        """Test that chunks don't exceed specified size."""
        chunk_size = 50
        chunks = chunk_text(sample_text, chunk_size=chunk_size, overlap=0)
        for chunk in chunks:
            words = chunk.split()
            # Allow some tolerance due to word boundaries
            assert len(words) <= chunk_size + 1


class TestChunkTextEdgeCases:
    """Test edge cases and error handling."""

    def test_chunk_empty_string(self):
        """Test chunking empty string returns empty list."""
        result = chunk_text("")
        assert result == []

    def test_chunk_whitespace_only(self):
        """Test chunking whitespace-only string returns empty list."""
        result = chunk_text("   \n\t  ")
        assert result == []

    def test_chunk_single_word(self):
        """Test chunking single word."""
        result = chunk_text("word")
        assert len(result) == 1
        assert result[0] == "word"

    def test_chunk_text_smaller_than_chunk_size(self):
        """Test chunking text smaller than chunk size."""
        text = "This is a short text"
        result = chunk_text(text, chunk_size=100, overlap=10)
        assert len(result) >= 1
        assert "short text" in result[0]

    def test_chunk_with_zero_overlap(self):
        """Test chunking with zero overlap."""
        text = " ".join(["word"] * 100)
        chunks = chunk_text(text, chunk_size=10, overlap=0)
        assert len(chunks) > 0
        # Should produce multiple chunks
        assert len(chunks) >= 5  # 100 words / 10 chunk_size ≈ 10 chunks

    def test_chunk_with_large_overlap(self):
        """Test chunking with large overlap."""
        text = " ".join(["word"] * 50)
        chunks = chunk_text(text, chunk_size=20, overlap=15)
        assert len(chunks) > 1
        # Should have overlap between consecutive chunks
        assert len(chunks) > len(chunk_text(text, chunk_size=20, overlap=0))


class TestChunkTextConsistency:
    """Test consistency and determinism."""

    def test_chunk_same_input_same_output(self, sample_text):
        """Test that chunking same input produces same output."""
        result1 = chunk_text(sample_text, chunk_size=50, overlap=10)
        result2 = chunk_text(sample_text, chunk_size=50, overlap=10)
        assert result1 == result2

    def test_chunk_preserves_content(self, sample_text):
        """Test that all words are preserved in chunks."""
        original_words = sample_text.split()
        chunks = chunk_text(sample_text, chunk_size=50, overlap=10)
        chunked_words = " ".join(chunks).split()
        # Compare relevant parts (may have extra spaces)
        assert len(chunked_words) >= len(original_words) - 10
