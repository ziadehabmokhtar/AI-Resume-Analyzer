import json
import httpx
from backend.utils.config import settings


class AIClient:
    """Small OpenAI-compatible client. Falls back to local deterministic logic when no key is configured."""

    def __init__(self):
        self.enabled = bool(settings.ai_api_key)

    async def generate_json(
        self, system_prompt: str, user_prompt: str, fallback: dict
    ) -> dict:
        if not self.enabled:
            return fallback
        url = settings.ai_base_url.rstrip("/") + "/chat/completions"
        payload = {
            "model": settings.ai_model,
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        headers = {
            "Authorization": f"Bearer {settings.ai_api_key}",
            "Content-Type": "application/json",
        }
        try:
            async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
                return json.loads(content)
        except Exception:
            return fallback

    async def generate_text(
        self, system_prompt: str, user_prompt: str, fallback: str
    ) -> str:
        if not self.enabled:
            return fallback
        url = settings.ai_base_url.rstrip("/") + "/chat/completions"
        payload = {
            "model": settings.ai_model,
            "temperature": 0.3,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        headers = {
            "Authorization": f"Bearer {settings.ai_api_key}",
            "Content-Type": "application/json",
        }
        try:
            async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
        except Exception:
            return fallback
