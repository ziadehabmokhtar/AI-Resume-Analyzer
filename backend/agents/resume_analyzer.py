import re
from backend.services.ai_client import AIClient

TECH_SKILLS = [
    "python",
    "java",
    "c++",
    "javascript",
    "typescript",
    "sql",
    "sqlite",
    "mysql",
    "postgresql",
    "fastapi",
    "django",
    "flask",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "power bi",
    "tableau",
    "excel",
    "git",
    "docker",
    "aws",
    "azure",
    "html",
    "css",
    "rest api",
    "machine learning",
    "deep learning",
    "data analysis",
]
SOFT_SKILLS = [
    "communication",
    "teamwork",
    "leadership",
    "problem solving",
    "time management",
    "adaptability",
    "critical thinking",
    "collaboration",
]


class ResumeAnalyzerAgent:
    name = "Resume Analyzer Agent"

    def __init__(self):
        self.ai = AIClient()

    def local_analysis(self, text: str) -> dict:
        lower = text.lower()
        email = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
        phone = re.search(r"(?:\+?\d[\d\s().-]{7,}\d)", text)
        lines = [x.strip() for x in re.split(r"[\n.]", text) if x.strip()]
        full_name = ""
        if (
            lines
            and len(lines[0].split()) <= 5
            and not re.search(r"@|resume|cv|curriculum", lines[0], re.I)
        ):
            full_name = lines[0]
        technical = [s for s in TECH_SKILLS if s in lower]
        soft = [s for s in SOFT_SKILLS if s in lower]
        education = []
        for line in lines:
            if re.search(
                r"education|university|college|bachelor|master|degree|faculty",
                line,
                re.I,
            ):
                education.append(line[:300])
        experience = []
        for line in lines:
            if re.search(
                r"experience|intern|developer|engineer|analyst|manager|worked|employment",
                line,
                re.I,
            ):
                experience.append(line[:300])
        summary = f"Resume profile with {len(technical)} detected technical skills and {len(soft)} soft skills."
        return {
            "full_name": full_name,
            "email": email.group(0) if email else "",
            "phone": phone.group(0) if phone else "",
            "education": education[:10],
            "experience": experience[:10],
            "technical_skills": technical,
            "soft_skills": soft,
            "summary": summary,
        }

    async def analyze(self, text: str) -> dict:
        fallback = self.local_analysis(text)
        prompt = """Return ONLY valid JSON with keys full_name,email,phone,education,experience,technical_skills,soft_skills,summary. Lists must contain concise strings. Extract only evidence from the resume; do not invent facts."""
        result = await self.ai.generate_json(prompt, text[:12000], fallback)
        for key in ["education", "experience", "technical_skills", "soft_skills"]:
            if not isinstance(result.get(key), list):
                result[key] = fallback[key]
        return result
