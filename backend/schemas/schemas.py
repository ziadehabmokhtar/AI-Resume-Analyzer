from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ResumeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    original_filename: str
    file_type: str
    full_name: str
    email: str
    phone: str
    education: list
    experience: list
    technical_skills: list
    soft_skills: list
    summary: str


class JobCreate(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    company: str = Field(min_length=2, max_length=255)
    description: str = Field(min_length=10)
    required_skills: List[str] = []
    location: str = ""
    experience_level: str = "Entry Level"
    education_required: str = ""


class JobOut(JobCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class MatchOut(BaseModel):
    job_id: int
    score: float
    matching_skills: list
    missing_skills: list
    experience_score: float
    education_score: float
    explanation: str


class CareerQuestion(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    resume_id: Optional[int] = None
