import re
from backend.services.ai_client import AIClient


class JobMatchingAgent:
    name = "Job Matching Agent"
    SKILLS_WEIGHT = 0.60
    EXPERIENCE_WEIGHT = 0.25
    EDUCATION_WEIGHT = 0.15

    def __init__(self):
        self.ai = AIClient()

    @staticmethod
    def norm(s):
        return re.sub(r"[^a-z0-9+#.]", " ", s.lower()).strip()

    def calculate(self, resume: dict, job: dict) -> dict:
        resume_skills = {
            self.norm(x)
            for x in resume.get("technical_skills", []) + resume.get("soft_skills", [])
        }
        required = {self.norm(x) for x in job.get("required_skills", [])}
        matching = sorted([x for x in required if x in resume_skills])
        missing = sorted(required - resume_skills)
        skills_score = len(matching) / len(required) if required else 1.0
        exp_text = " ".join(str(x) for x in resume.get("experience", []))
        level = job.get("experience_level", "").lower()
        if "entry" in level or "junior" in level:
            exp_score = 1.0 if exp_text else 0.5
        elif any(
            k in exp_text.lower()
            for k in ["experience", "developer", "engineer", "analyst", "intern"]
        ):
            exp_score = 0.8
        else:
            exp_score = 0.3
        edu_required = job.get("education_required", "").lower()
        edu_text = " ".join(str(x) for x in resume.get("education", []))
        edu_score = (
            1.0
            if not edu_required
            else (
                1.0
                if any(
                    word in edu_text.lower()
                    for word in edu_required.split()
                    if len(word) > 3
                )
                else 0.5
            )
        )
        score = round(
            (
                skills_score * self.SKILLS_WEIGHT
                + exp_score * self.EXPERIENCE_WEIGHT
                + edu_score * self.EDUCATION_WEIGHT
            )
            * 100,
            2,
        )
        explanation = f"Skills contributed {round(skills_score*60,1)} points, experience {round(exp_score*25,1)} points, and education {round(edu_score*15,1)} points."
        return {
            "score": score,
            "matching_skills": matching,
            "missing_skills": missing,
            "experience_score": round(exp_score * 100, 2),
            "education_score": round(edu_score * 100, 2),
            "explanation": explanation,
        }

    async def match(self, resume: dict, job: dict) -> dict:
        result = self.calculate(resume, job)
        prompt = "Provide a concise explanation of the supplied deterministic match result. Do not change the score, matching skills, or missing skills."
        ai_text = await self.ai.generate_text(
            prompt,
            str({"resume": resume, "job": job, "result": result}),
            result["explanation"],
        )
        result["explanation"] = ai_text
        return result
