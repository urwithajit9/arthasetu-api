import os
import psycopg2
from sentence_transformers import SentenceTransformer

class VectorService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.db_url = os.getenv("DATABASE_URL")

    def find_context(self, query: str, limit: int = 5):
        embedding = self.model.encode(query).tolist()
        conn = psycopg2.connect(self.db_url)
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT content, doc_level 
                    FROM knowledge_base 
                    ORDER BY embedding <=> %s::vector 
                    LIMIT %s
                """, (embedding, limit))
                return [{"content": r[0], "doc_level": r[1]} for r in cur.fetchall()]
        finally:
            conn.close()
