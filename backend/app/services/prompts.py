"""
Prompt templates used by backend services.

Kept inside the backend package (not imported from ../ml/) on purpose: this backend's
Docker build context is ./backend only (see docker-compose.dev.yml), so ml/ is never
actually present in a deployed container - a module-level `from ml... import` here would
crash the real server at startup with ModuleNotFoundError. It only ever appeared to work
locally because pytest's sys.path handling happens to reach the repo root; `uvicorn
main:app` does not. If ml/'s prompt content changes, update the copy here too.
"""

STARTUP_DATA_EXTRACTION_PROMPT = """
You are an expert startup analyst. Extract structured information from this pitch deck text and return it as JSON.

IMPORTANT: Return ONLY valid JSON without any additional text or formatting.

Extract the following information:

REQUIRED FIELDS:
- company_name: string
- founded_year: integer (estimate if not provided)
- industry: string (SaaS, FinTech, HealthTech, etc.)
- stage: string (Pre-Seed, Seed, Series A, B, C, etc.)
- description: string (1-2 sentence company description)

TEAM INFORMATION:
- team: array of objects with name, role, bio, experience_years

FINANCIAL METRICS:
- revenue_arr: number (annual recurring revenue)
- monthly_growth_rate: number (as decimal, e.g., 0.25 for 25%)
- customer_count: integer
- burn_rate: number (monthly burn rate)
- total_funding_raised: number

MARKET DATA:
- total_addressable_market: number
- market_growth_rate: number (as decimal)
- competitors: array of competitor names

PRODUCT INFORMATION:
- product_name: string
- product_type: string
- key_features: array of strings

If a value is genuinely not stated or clearly implied in the text, return null for it.
Do not invent a plausible-sounding number or name to fill a gap - a null the analyst can
see and investigate is far more useful than a fabricated figure they can't tell apart from
a real one.

PITCH DECK TEXT:
{pitch_deck_text}

JSON OUTPUT:
"""
