"""
Unit tests for ParsingService - specifically that it no longer fabricates data.
"""
import json
import pytest
from unittest.mock import AsyncMock

from app.services.parsing_service import ParsingService


def make_service(ai_response):
    ai = AsyncMock()
    ai.complete = AsyncMock(return_value=ai_response)
    return ParsingService(ai_service=ai), ai


class TestParsingService:
    @pytest.mark.asyncio
    async def test_returns_none_when_text_too_short(self):
        service, _ = make_service(None)
        result = await service.parse_startup_data("too short")
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_when_ai_backend_unreachable(self):
        """The core regression test: an unreachable AI backend must come back as
        None, never as a StartupData full of invented team members and financials."""
        service, ai = make_service(None)
        result = await service.parse_startup_data("A" * 100)
        assert result is None
        ai.complete.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_returns_none_on_unparseable_response(self):
        service, _ = make_service("I couldn't extract anything useful, sorry.")
        result = await service.parse_startup_data("A" * 100)
        assert result is None

    @pytest.mark.asyncio
    async def test_parses_a_genuine_ai_response_into_startup_data(self):
        ai_json = {
            "company_name": "Quantum Widgets Inc",
            "founded_year": 2021,
            "industry": "FinTech",
            "stage": "Seed",
            "description": "A widget-as-a-service platform.",
            "team": [{"name": "Alex Rivera", "role": "CEO"}],
            "revenue_arr": 500000,
            "customer_count": 42,
            "total_addressable_market": 1000000000,
            "competitors": ["WidgetCo"],
            "product_name": "QuantumFlow",
            "product_type": "SaaS",
            "key_features": ["Real-time sync"],
        }
        # Real models often wrap JSON in a fenced code block despite instructions - the
        # extractor must handle that, not just a bare JSON string.
        wrapped = f"```json\n{json.dumps(ai_json)}\n```"
        service, _ = make_service(wrapped)

        result = await service.parse_startup_data("A" * 100)

        assert result is not None
        assert result.company_name == "Quantum Widgets Inc"
        assert result.team[0].name == "Alex Rivera"
        assert result.metrics.revenue_arr == 500000
        assert result.market_data.competitors[0].name == "WidgetCo"
        # None of the old hardcoded fabricated content should ever appear.
        assert "Sarah Chen" not in [m.name for m in result.team]
        assert "WorkflowMax" not in [c.name for c in result.market_data.competitors]

    @pytest.mark.asyncio
    async def test_missing_optional_fields_dont_crash_validation(self):
        """A minimal, genuine but sparse AI response should still validate - required
        fields the model actually asks for are present, everything else is honestly
        absent rather than backfilled with invented numbers."""
        ai_json = {
            "company_name": "Sparse Co",
            "founded_year": 2023,
            "industry": "SaaS",
            "stage": "Pre-Seed",
            "description": "Not much else known.",
        }
        service, _ = make_service(json.dumps(ai_json))

        result = await service.parse_startup_data("A" * 100)

        assert result is not None
        assert result.company_name == "Sparse Co"
        assert result.metrics.revenue_arr is None
        assert result.market_data.total_addressable_market is None
        assert result.team == []
