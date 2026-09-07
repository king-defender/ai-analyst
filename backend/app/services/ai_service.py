import logging
from typing import Optional

from openai import AsyncOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)


class AiService:
    """Thin client for any OpenAI-compatible /v1/chat/completions endpoint.

    Defaults to a local Ollama instance (settings.AI_BASE_URL) so structured extraction
    works with zero cloud credentials - the same pattern used elsewhere in this codebase's
    sibling projects. Point AI_BASE_URL/AI_MODEL at Vertex AI's OpenAI-compatible endpoint
    or plain OpenAI later; no code change needed, only configuration.
    """

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            base_url=settings.AI_BASE_URL,
            api_key=settings.OPENAI_API_KEY or "ollama",
        )
        self._model = settings.AI_MODEL

    async def complete(self, prompt: str, system_prompt: Optional[str] = None) -> Optional[str]:
        """Returns the raw completion text, or None if the AI backend is unreachable or
        returns something unusable. Callers must treat None as "no real result" and degrade
        honestly - never substitute fabricated content when this returns None."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                timeout=30.0,
            )
            text = response.choices[0].message.content
            if not text or not text.strip():
                logger.warning("AI backend returned an empty completion")
                return None
            return text.strip()
        except Exception as exc:  # noqa: BLE001 - any failure here means "degrade", not crash
            logger.warning(
                "AI backend unreachable at %s: %s", settings.AI_BASE_URL, exc
            )
            return None
