import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models import Resume, Job
from backend.services.resume_service import resume_to_dict
from backend.agents.job_matching import JobMatchingAgent
from backend.agents.career_advisor import CareerAdvisorAgent
from backend.utils.security import get_current_user

router = APIRouter(prefix="/api/matching", tags=["Matching & Recommendations"])


@router.post("/resume/{resume_id}/job/{job_id}", summary="Match a resume against a job")
async def match(
    resume_id: int,
    job_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    r = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.user_id == user.id)
        .first()
    )
    j = db.get(Job, job_id)
    if not r:
        raise HTTPException(404, "Resume not found")
    if not j:
        raise HTTPException(404, "Job not found")
    job = {
        "title": j.title,
        "company": j.company,
        "description": j.description,
        "required_skills": json.loads(j.required_skills_json or "[]"),
        "location": j.location,
        "experience_level": j.experience_level,
        "education_required": j.education_required,
    }
    return await JobMatchingAgent().match(resume_to_dict(r), job)


@router.get("/resume/{resume_id}/recommendations", summary="Get job recommendations")
async def recommendations(
    resume_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    r = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.user_id == user.id)
        .first()
    )
    if not r:
        raise HTTPException(404, "Resume not found")
    rd = resume_to_dict(r)
    agent = JobMatchingAgent()
    results = []
    for j in db.query(Job).all():
        jd = {
            "required_skills": json.loads(j.required_skills_json or "[]"),
            "experience_level": j.experience_level,
            "education_required": j.education_required,
        }
        m = agent.calculate(rd, jd)
        results.append(
            {
                "job": {
                    "id": j.id,
                    "title": j.title,
                    "company": j.company,
                    "location": j.location,
                },
                **m,
            }
        )
    return sorted(results, key=lambda x: x["score"], reverse=True)


@router.get(
    "/resume/{resume_id}/improvement", summary="Get resume improvement guidance"
)
async def improvement(
    resume_id: int,
    job_id: int | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    r = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.user_id == user.id)
        .first()
    )
    if not r:
        raise HTTPException(404, "Resume not found")
    rd = resume_to_dict(r)
    job = None
    if job_id:
        j = db.get(Job, job_id)
        if not j:
            raise HTTPException(404, "Job not found")
        job = {
            "title": j.title,
            "required_skills": json.loads(j.required_skills_json or "[]"),
            "description": j.description,
        }
    result = await CareerAdvisorAgent().improvement(rd, job)
    missing = []
    if job:
        missing = JobMatchingAgent().calculate(
            rd, {**job, "experience_level": "Entry Level", "education_required": ""}
        )["missing_skills"]
    return {
        "missing_skills": missing,
        "guidance": result["answer"],
        "sources": result["sources"],
    }
