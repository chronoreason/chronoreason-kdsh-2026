import pathway as pw
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

class PathwayStore:
    def __init__(self, chunks):
        """
        chunks: List[str]
        """
        self.chunks = chunks
        self.table = self._build_table(chunks)

    def _build_table(self, chunks):
        # Create Pathway table
        table = pw.Table.from_rows(
            [(i, chunk) for i, chunk in enumerate(chunks)],
            schema=["id", "text"]
        )

        # Add embedding column
        table = table.select(
            table.id,
            table.text,
            embedding=pw.apply(
                lambda x: model.encode(x).tolist(),
                table.text
            )
        )

        return table

    def search(self, query, top_k=3):
        query_embedding = model.encode(query).tolist()

        # Compute cosine similarity inside Pathway
        scored = self.table.select(
            self.table.text,
            score=pw.apply(
                lambda emb: sum(a * b for a, b in zip(emb, query_embedding)),
                self.table.embedding
            )
        )

        # Sort by similarity
        top_results = scored.sort(
            scored.score, reverse=True
        ).limit(top_k)

        # Collect results
        return [row["text"] for row in top_results.collect()]
