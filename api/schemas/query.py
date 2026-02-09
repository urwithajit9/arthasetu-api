from ninja import Schema
from typing import List, Optional

class QueryRequest(Schema):
    query: str
    top_k: int = 5

class SourceContext(Schema):
    content: str
    doc_level: str
    metadata: Optional[dict] = None

class QueryResponse(Schema):
    answer: str
    sources: List[SourceContext]
