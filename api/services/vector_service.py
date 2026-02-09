import os
from django.db import connection
from sentence_transformers import SentenceTransformer


class VectorService:
    _model = None  # Class-level variable to store the singleton instance

    @classmethod
    def get_model(cls):
        """Lazy loader for the SentenceTransformer model."""
        if cls._model is None:
            print("💡 Loading Embedding Model (CPU)...")
            # Force CPU to bypass the CUDA compatibility issue with your GTX 1050
            cls._model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        return cls._model

    def find_context(self, query: str, limit: int = 5):
        # 1. Get embedding using the lazy-loaded model
        model = self.get_model()
        embedding = model.encode(query).tolist()

        # 2. Use Django's managed connection (handles pooling & DNS retries)
        with connection.cursor() as cur:
            cur.execute(
                """
                SELECT content, doc_level
                FROM knowledge_base
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """,
                (embedding, limit),
            )

            rows = cur.fetchall()
            return [{"content": r[0], "doc_level": r[1]} for r in rows]
