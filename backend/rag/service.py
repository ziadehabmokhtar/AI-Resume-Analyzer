from backend.rag.retriever import KnowledgeBase
from backend.services.ai_client import AIClient


class RAGService:
    def __init__(self):
        self.kb = KnowledgeBase()
        self.ai = AIClient()

    async def answer(self, query: str, resume_context: str = "") -> dict:
        docs = self.kb.retrieve(query, 4)
        context = "\n\n".join(f"[{d['source']}] {d['text']}" for d in docs)
        fallback = "Based on the retrieved knowledge base: " + (
            docs[0]["text"] if docs else "No matching knowledge-base content was found."
        )
        system = "Answer career questions using ONLY the supplied retrieved context when factual claims are made. Clearly say when the context is insufficient. Return a useful concise answer."
        user = f"Question: {query}\nResume context: {resume_context[:4000]}\nRetrieved context:\n{context}"
        answer = await self.ai.generate_text(system, user, fallback)
        return {"answer": answer, "sources": docs}
