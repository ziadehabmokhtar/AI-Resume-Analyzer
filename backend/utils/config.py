from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "AI Resume Analyzer"
    jwt_secret_key: str = "change-me-change-me-change-me-32"
    jwt_expire_minutes: int = 120
    database_url: str = f"sqlite:///{ROOT_DIR / 'resume_analyzer.db'}"
    ai_api_key: str = ""
    ai_base_url: str = "https://api.openai.com/v1"
    ai_model: str = "gpt-4o-mini"
    ai_timeout_seconds: int = 45
    max_upload_mb: int = 5
    model_config = SettingsConfigDict(env_file=str(ROOT_DIR / ".env"), extra="ignore")


settings = Settings()
UPLOAD_DIR = ROOT_DIR / "uploads"
KB_DIR = ROOT_DIR / "data" / "knowledge_base"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
