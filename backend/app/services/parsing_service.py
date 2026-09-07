import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, Optional

from app.models.startup import StartupData
from app.services.ai_service import AiService
from app.services.prompts import STARTUP_DATA_EXTRACTION_PROMPT

logger = logging.getLogger(__name__)


class ParsingService:
    """Parses startup data from extracted pitch-deck text using a real AI call.

    No fabricated fallback: if the AI backend is unreachable or returns something that
    doesn't validate against StartupData, this returns None. AnalysisService already
    treats that as a failure and marks the job FAILED with a clear message - a job that
    fails honestly beats one that "succeeds" with invented team members and financials.
    """

    def __init__(self, ai_service: Optional[AiService] = None) -> None:
        self._ai = ai_service or AiService()

    async def parse_startup_data(self, extracted_text: str) -> Optional[StartupData]:
        if not extracted_text or len(extracted_text.strip()) < 50:
            return None

        prompt = STARTUP_DATA_EXTRACTION_PROMPT.format(pitch_deck_text=extracted_text[:12000])
        raw = await self._ai.complete(
            prompt,
            system_prompt="You are an expert startup analyst. Return ONLY valid JSON, no prose.",
        )
        if raw is None:
            logger.warning("Parsing failed: AI backend returned no result")
            return None

        parsed = self._extract_json(raw)
        if parsed is None:
            logger.warning("Parsing failed: AI response did not contain valid JSON")
            return None

        shaped = self._shape_for_model(parsed)

        try:
            return StartupData(**shaped)
        except Exception as exc:  # noqa: BLE001 - a bad/incomplete AI response, not a bug
            logger.warning("Parsing failed: AI response did not match the expected shape: %s", exc)
            return None

    @staticmethod
    def _extract_json(text: str) -> Optional[Dict[str, Any]]:
        """Models frequently wrap JSON in ```json fences or add a stray sentence either
        side despite being told not to - pull out the first {...} block rather than
        assuming the whole response is bare JSON."""
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return None
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
        return data if isinstance(data, dict) else None

    @staticmethod
    def _shape_for_model(data: Dict[str, Any]) -> Dict[str, Any]:
        """Maps the flat extraction shape the prompt asks for onto StartupData's nested
        shape. Anything the model didn't return is left absent - the model's own Optional
        fields and defaults handle the rest, no invented values here."""
        competitors = [
            {"name": c, "description": ""} if isinstance(c, str) else c
            for c in data.get("competitors", []) or []
        ]

        return {
            "id": f"startup_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "company_name": data.get("company_name") or "Unknown Company",
            "founded_year": data.get("founded_year") or datetime.now().year,
            "industry": data.get("industry") or "Unknown",
            "stage": data.get("stage") or "Unknown",
            "description": data.get("description") or "",
            "team": data.get("team", []) or [],
            "metrics": {
                "revenue_arr": data.get("revenue_arr"),
                "monthly_growth_rate": data.get("monthly_growth_rate"),
                "customer_count": data.get("customer_count"),
                "burn_rate": data.get("burn_rate"),
            },
            "financial_data": {
                "total_funding_raised": data.get("total_funding_raised"),
                "burn_rate": data.get("burn_rate"),
            },
            "market_data": {
                "total_addressable_market": data.get("total_addressable_market"),
                "market_growth_rate": data.get("market_growth_rate"),
                "competitors": competitors,
            },
            "product_info": {
                "product_name": data.get("product_name"),
                "product_type": data.get("product_type"),
                "key_features": data.get("key_features", []) or [],
            },
            "traction": {},
            "funding_history": [],
        }
