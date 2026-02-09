from ninja import Router
from api.schemas.query import QueryRequest, QueryResponse
from api.services.vector_service import VectorService
from api.services.llm_service import LLMService

router = Router()
vector_svc = VectorService()
llm_svc = LLMService()

@router.post("/ask", response=QueryResponse)
def ask(request, payload: QueryRequest):
    sources = vector_svc.find_context(payload.query, limit=payload.top_k)
    context_str = "\n".join([s['content'] for s in sources])
    answer = llm_svc.get_reasoning(payload.query, context_str)
    
    return {"answer": answer, "sources": sources}
