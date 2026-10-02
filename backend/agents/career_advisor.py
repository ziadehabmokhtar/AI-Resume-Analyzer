from backend.rag.service import RAGService
from backend.services.ai_client import AIClient


class CareerAdvisorAgent:
    name = "Career Advisor Agent"

    def __init__(self):
        self.rag = RAGService()
        self.ai = AIClient()

    async def advise(self, question: str, resume: dict | None = None):
        context = str(resume or {})
        return await self.rag.answer(question, context)

    async def improvement(self, resume: dict, job: dict | None = None):
        query = (
            "resume improvement missing skills certifications learning resources "
            + str(job or {})
        )
        result = await self.rag.answer(query, str(resume))
        fallback = {"answer": result["answer"], "sources": result["sources"]}
        return fallback
