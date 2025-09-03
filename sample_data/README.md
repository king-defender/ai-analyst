# Sample Pitch Deck Data

This directory contains sample pitch decks and expected outputs for testing and development.

## Structure

```
sample_data/
├── pitch_decks/          # Sample PDF pitch decks
│   ├── saas_startup.pdf
│   ├── fintech_series_a.pdf
│   └── healthcare_seed.pdf
├── extracted/            # Expected extracted data (JSON)
│   ├── saas_startup.json
│   ├── fintech_series_a.json
│   └── healthcare_seed.json
├── benchmarks/           # Sample benchmark data
│   ├── saas_benchmarks.csv
│   ├── fintech_benchmarks.csv
│   └── healthcare_benchmarks.csv
└── outputs/              # Sample generated memos
    ├── saas_startup_memo.pdf
    ├── fintech_series_a_memo.pdf
    └── healthcare_seed_memo.pdf
```

## Data Sources

The sample data is sourced from:
- Publicly available pitch deck templates
- Anonymized real startup data (with permission)
- Industry reports and benchmarks
- Generated synthetic data for testing

## Usage

### For Development
```python
# Load sample extracted data
import json
with open('sample_data/extracted/saas_startup.json') as f:
    sample_data = json.load(f)
```

### For Testing
```python
# Use in unit tests
def test_risk_assessment():
    from sample_data.extracted import saas_startup
    risks = assess_risks(saas_startup.data)
    assert len(risks) > 0
```

### For Demos
- Use `saas_startup.pdf` for SaaS demo
- Use `fintech_series_a.pdf` for fintech demo
- Use `healthcare_seed.pdf` for healthcare demo

## Data Privacy

All sample data has been:
- Anonymized and sanitized
- Cleared for public use
- Reviewed for sensitive information
- Generated synthetically where needed

## Contributing Sample Data

To add new sample data:
1. Ensure data is properly anonymized
2. Follow the naming convention: `{industry}_{stage}.{ext}`
3. Include all formats: PDF, JSON, and expected output
4. Update this README with the new samples
5. Add appropriate tests using the new data