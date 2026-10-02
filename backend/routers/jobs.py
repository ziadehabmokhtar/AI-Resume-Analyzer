import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.database.session import get_db
from backend.models import Job
from backend.schemas import JobCreate
from backend.utils.security import get_current_user

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


def out(j):
    return {
        "id": j.id,
        "title": j.title,
        "company": j.company,
        "description": j.description,
        "required_skills": json.loads(j.required_skills_json or "[]"),
        "location": j.location,
        "experience_level": j.experience_level,
        "education_required": j.education_required,
    }


@router.post("", status_code=201, summary="Create a job")
def create_job(
    data: JobCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    job = Job(
        **data.model_dump(exclude={"required_skills"}),
        required_skills_json=json.dumps(data.required_skills),
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return out(job)


@router.get("", summary="Search and list jobs")
def list_jobs(
    q: str | None = Query(None),
    title: str | None = None,
    skills: str | None = None,
    location: str | None = None,
    experience_level: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    query = db.query(Job)
    for term in [q, title, location, experience_level]:
        if term:
            query = query.filter(
                or_(
                    Job.title.ilike(f"%{term}%"),
                    Job.description.ilike(f"%{term}%"),
                    Job.location.ilike(f"%{term}%"),
                )
            )
    jobs = query.order_by(Job.created_at.desc()).all()
    if skills:
        wanted = {x.strip().lower() for x in skills.split(",") if x.strip()}
        jobs = [
            j
            for j in jobs
            if wanted.intersection(
                {x.lower() for x in json.loads(j.required_skills_json or "[]")}
            )
        ]
    return [out(j) for j in jobs]


@router.get("/{job_id}", summary="Get a job")
def get_job(job_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    j = db.get(Job, job_id)
    if not j:
        raise HTTPException(404, "Job not found")
    return out(j)


@router.put("/{job_id}", summary="Update a job")
def update_job(
    job_id: int,
    data: JobCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    j = db.get(Job, job_id)
    if not j:
        raise HTTPException(404, "Job not found")
    for k, v in data.model_dump().items():
        setattr(
            j,
            "required_skills_json" if k == "required_skills" else k,
            json.dumps(v) if k == "required_skills" else v,
        )
    db.commit()
    db.refresh(j)
    return out(j)


@router.delete("/{job_id}", summary="Delete a job")
def delete_job(
    job_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    j = db.get(Job, job_id)
    if not j:
        raise HTTPException(404, "Job not found")
    db.delete(j)
    db.commit()
    return {"message": "Job deleted"}
