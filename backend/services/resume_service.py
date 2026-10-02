import json
from pathlib import Path
from backend.agents.resume_analyzer import ResumeAnalyzerAgent
from backend.services.file_parser import extract_text, save_file
from backend.models import Resume


async def process_resume(
    db, user_id: int, original_filename: str, suffix: str, content: bytes
) -> Resume:
    raw_text = extract_text(content, suffix)
    stored = save_file(content, suffix)
    data = await ResumeAnalyzerAgent().analyze(raw_text)
    resume = Resume(
        user_id=user_id,
        original_filename=original_filename,
        stored_filename=stored,
        file_type=suffix[1:],
        raw_text=raw_text,
        full_name=data.get("full_name", ""),
        email=data.get("email", ""),
        phone=data.get("phone", ""),
        education_json=json.dumps(data.get("education", [])),
        experience_json=json.dumps(data.get("experience", [])),
        technical_skills_json=json.dumps(data.get("technical_skills", [])),
        soft_skills_json=json.dumps(data.get("soft_skills", [])),
        summary=data.get("summary", ""),
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


def resume_to_dict(resume: Resume) -> dict:
    return {
        "id": resume.id,
        "original_filename": resume.original_filename,
        "file_type": resume.file_type,
        "full_name": resume.full_name,
        "email": resume.email,
        "phone": resume.phone,
        "education": json.loads(resume.education_json or "[]"),
        "experience": json.loads(resume.experience_json or "[]"),
        "technical_skills": json.loads(resume.technical_skills_json or "[]"),
        "soft_skills": json.loads(resume.soft_skills_json or "[]"),
        "summary": resume.summary,
    }
