from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models import Resume
from backend.services.resume_service import resume_to_dict
from backend.agents.career_advisor import CareerAdvisorAgent
from backend.schemas import CareerQuestion
from backend.utils.security import get_current_user

router = APIRouter(prefix="/api/career", tags=["Career Advisor & RAG"])


@router.post("/ask", summary="Ask a RAG-based career question")
async def ask(
    data: CareerQuestion, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    resume = None
    if data.resume_id:
        r = (
            db.query(Resume)
            .filter(Resume.id == data.resume_id, Resume.user_id == user.id)
            .first()
        )
        if r:
            resume = resume_to_dict(r)
    return await CareerAdvisorAgent().advise(data.question, resume)
