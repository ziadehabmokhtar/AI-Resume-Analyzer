from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.database.session import Base, engine, SessionLocal
from backend.models import User, Resume, Job, MatchResult
from backend.routers import auth, resumes, jobs, matching, career
from backend.utils.config import settings, ROOT_DIR

Base.metadata.create_all(bind=engine)


def seed_jobs():
    db = SessionLocal()
    try:
        if db.query(Job).count() == 0:
            import json

            samples = [
                (
                    "Junior Data Analyst",
                    "Sample Analytics Co.",
                    "Analyze business data, create reports and dashboards, and communicate findings.",
                    ["Python", "SQL", "Pandas", "Excel", "Data Analysis"],
                    "Cairo",
                    "Entry Level",
                    "Bachelor degree",
                ),
                (
                    "Backend Python Developer",
                    "Demo Software Labs",
                    "Build REST APIs with Python and FastAPI, write tests and work with SQL databases.",
                    ["Python", "FastAPI", "REST API", "SQL", "Git"],
                    "Remote",
                    "Junior",
                    "Bachelor degree",
                ),
                (
                    "Machine Learning Intern",
                    "Sample AI Lab",
                    "Prepare datasets and experiment with machine learning models under mentorship.",
                    ["Python", "Pandas", "NumPy", "Scikit-learn", "Machine Learning"],
                    "Cairo",
                    "Intern",
                    "Bachelor degree",
                ),
            ]
            for t, c, d, s, l, e, ed in samples:
                db.add(
                    Job(
                        title=t,
                        company=c,
                        description=d,
                        required_skills_json=json.dumps(s),
                        location=l,
                        experience_level=e,
                        education_required=ed,
                    )
                )
            db.commit()
    finally:
        db.close()


seed_jobs()

app = FastAPI(
    title=settings.app_name, version="1.0.0", description="AI Resume Analyzer REST API"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(resumes.router)
app.include_router(jobs.router)
app.include_router(matching.router)
app.include_router(career.router)


@app.get("/api/health", tags=["System"])
def health():
    return {"status": "ok", "service": settings.app_name}


frontend = ROOT_DIR / "frontend"
app.mount("/", StaticFiles(directory=str(frontend), html=True), name="frontend")
