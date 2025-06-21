# End-to-End Tests

This directory contains Playwright-based end-to-end tests for the Splatoon weapon generator.

## Prerequisites

1. Install dependencies: `pip install -r requirements.txt`
2. Install Playwright browsers: `python -m playwright install`
3. Start the application: `streamlit run app.py` (or your main app file)

## Running Tests

### Run all e2e tests
```bash
pytest tests/e2e/
```

### Run with visible browser (for debugging)
```bash
HEADLESS=false pytest tests/e2e/
```

### Run against different URL
```bash
BASE_URL=http://localhost:3000 pytest tests/e2e/
```

## Environment Variables

- `BASE_URL`: Application URL (default: http://localhost:8501)
- `HEADLESS`: Browser headless mode (default: true)

## Test Evidence

Screenshots are automatically saved to the `evidence/` directory during test execution.