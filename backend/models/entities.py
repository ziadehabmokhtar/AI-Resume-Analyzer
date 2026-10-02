from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.session import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    resumes = relationship(
        "Resume", back_populates="user", cascade="all, delete-orphan"
    )


class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False)
    raw_text = Column(Text, default="")
    full_name = Column(String(255), default="")
    email = Column(String(255), default="")
    phone = Column(String(100), default="")
    education_json = Column(Text, default="[]")
    experience_json = Column(Text, default="[]")
    technical_skills_json = Column(Text, default="[]")
    soft_skills_json = Column(Text, default="[]")
    summary = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    user = relationship("User", back_populates="resumes")


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    required_skills_json = Column(Text, default="[]")
    location = Column(String(255), default="")
    experience_level = Column(String(100), default="Entry Level")
    education_required = Column(String(255), default="")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class MatchResult(Base):
    __tablename__ = "match_results"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    score = Column(Float, nullable=False)
    matching_skills_json = Column(Text, default="[]")
    missing_skills_json = Column(Text, default="[]")
    explanation = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
