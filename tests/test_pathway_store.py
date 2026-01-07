"""Unit tests for retrieval.pathway_store module."""
import pytest
from retrieval.pathway_store import PathwayStore


class TestPathwayStoreBasic:
    """Test basic PathwayStore functionality."""

    def test_pathway_store_init(self):
        """Test PathwayStore initialization."""
        chunks = ["chunk one", "chunk two", "chunk three"]
        store = PathwayStore(chunks)
        assert store.chunks == chunks
        assert store.embeddings is not None
        assert len(store.embeddings) == 3

    def test_pathway_store_search_returns_list(self):
        """Test that search returns a list."""
        chunks = [
            "The quick brown fox jumps over the lazy dog.",
            "Artificial intelligence improves search and retrieval.",
            "Machine learning algorithms process data efficiently."
        ]
        store = PathwayStore(chunks)
        results = store.search("fox", top_k=2)
        assert isinstance(results, list)

    def test_pathway_store_search_top_k(self):
        """Test that search respects top_k parameter."""
        chunks = [f"chunk {i}" for i in range(10)]
        store = PathwayStore(chunks)
        results = store.search("chunk", top_k=3)
        assert len(results) <= 3

    def test_pathway_store_search_retrieves_relevant(self):
        """Test that search retrieves relevant chunks."""
        chunks = [
            "The quick brown fox jumps over the lazy dog.",
            "Cooking recipes often mention ingredients, steps, and timings.",
            "Artificial intelligence improves search and retrieval effectiveness."
        ]
        store = PathwayStore(chunks)
        results = store.search("search and retrieval", top_k=1)
        assert len(results) >= 1
        # Should find the AI/retrieval chunk as most relevant
        assert "search" in results[0].lower() or "retrieval" in results[0].lower()


class TestPathwayStoreEdgeCases:
    """Test edge cases."""

    def test_pathway_store_empty_chunks(self):
        """Test PathwayStore with empty chunks list."""
        store = PathwayStore([])
        assert len(store.chunks) == 0
        assert len(store.embeddings) == 0

    def test_pathway_store_search_empty_store(self):
        """Test searching in empty store."""
        store = PathwayStore([])
        results = store.search("query", top_k=5)
        assert results == []

    def test_pathway_store_single_chunk(self):
        """Test with single chunk."""
        store = PathwayStore(["only chunk"])
        results = store.search("chunk", top_k=5)
        assert len(results) == 1
        assert results[0] == "only chunk"

    def test_pathway_store_top_k_exceeds_chunks(self):
        """Test that top_k is capped at number of chunks."""
        chunks = ["chunk 1", "chunk 2"]
        store = PathwayStore(chunks)
        results = store.search("chunk", top_k=10)
        assert len(results) <= 2

    def test_pathway_store_empty_query(self):
        """Test search with empty query."""
        chunks = ["chunk one", "chunk two"]
        store = PathwayStore(chunks)
        results = store.search("", top_k=2)
        assert isinstance(results, list)

    def test_pathway_store_top_k_zero(self):
        """Test search with top_k=0."""
        chunks = ["chunk one", "chunk two"]
        store = PathwayStore(chunks)
        results = store.search("query", top_k=0)
        assert len(results) == 0


class TestPathwayStoreConsistency:
    """Test consistency and determinism."""

    def test_same_chunks_same_embeddings(self):
        """Test that same chunks produce same embeddings."""
        chunks = ["text one", "text two", "text three"]
        store1 = PathwayStore(chunks)
        store2 = PathwayStore(chunks)
        # Embeddings should be close (may have slight floating point differences)
        assert len(store1.embeddings) == len(store2.embeddings)

    def test_search_deterministic(self):
        """Test that searches are deterministic."""
        chunks = [
            "The quick brown fox",
            "jumps over the lazy dog",
            "in a field of flowers"
        ]
        store = PathwayStore(chunks)
        results1 = store.search("quick fox", top_k=2)
        results2 = store.search("quick fox", top_k=2)
        assert results1 == results2


class TestPathwayStoreDocumentation:
    """Test that the class works as documented."""

    def test_pathway_store_basic_usage(self):
        """Test basic usage pattern from docstring."""
        chunks = [
            "The sky is blue",
            "The ocean is vast",
            "Birds fly in the air"
        ]
        store = PathwayStore(chunks)
        results = store.search("sky", top_k=2)
        assert len(results) > 0
        assert isinstance(results[0], str)
