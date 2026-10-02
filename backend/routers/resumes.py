from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models import Resume
from backend.services.file_parser import validate_upload
from backend.services.resume_service import process_resume, resume_to_dict
from backend.utils.security import get_current_user

router = APIRouter(prefix="/api/resumes", tags=["Resumes"])


@router.post("/upload", summary="Upload and analyze a PDF or DOCX resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    content = await file.read()
    suffix = validate_upload(file, content)
    resume = await process_resume(
        db, user.id, file.filename or "resume", suffix, content
    )
    return resume_to_dict(resume)


@router.get("", summary="List current user's resumes")
def list_resumes(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return [
        resume_to_dict(r)
        for r in db.query(Resume)
        .filter(Resume.user_id == user.id)
        .order_by(Resume.created_at.desc())
        .all()
    ]


@router.get("/{resume_id}", summary="Get a resume")
def get_resume(
    resume_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    resume = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.user_id == user.id)
        .first()
    )
    if not resume:
        from fastapi import HTTPException

        raise HTTPException(404, "Resume not found")
    return resume_to_dict(resume)
