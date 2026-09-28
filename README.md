# Agentic RFP Evaluation and Supplier Ranking

A Streamlit application that evaluates supplier PDFs with a JSON-capable LLM while keeping validation, arithmetic, peer benchmarking, tie-breaking and ranking deterministic in Python.

## Architecture

```text
Streamlit UI -> Orchestrator -> PDF Extraction Tool -> Gemini Evaluation Agent
             -> Validation Tool -> Scoring and Ranking Tools -> SQLite -> UI/JSON
```

The LLM judges proposal evidence only. Python determines all business calculations and final rank.

## Setup

1. Use Python 3.11 or 3.12.
2. Run `pip install -r requirements.txt`.
3. Run `python db/seed_db.py`.
4. Create `.streamlit/secrets.toml` locally with `GEMINI_API_KEY="your-key"`. Never commit this file.
5. Run `streamlit run app.py`.

## Formulas

- Absolute weighted score = sum((criterion score / maximum score) x criterion weight)
- Benchmark = highest valid score for the criterion
- Gap = supplier score - benchmark
- Relative performance = supplier score / benchmark x 100; when benchmark is zero, use 100%
- PPI = weighted average of relative-performance percentages
- Tie-breaks = PPI descending, submission date ascending, experience descending, supplier name ascending

## Validation rules

The validator handles invalid JSON structures, missing criteria, duplicates, unknown IDs, non-numeric values, missing evidence, score clipping and incorrect model maximum scores. All changes generate warnings.

## Testing

Run `python -m pytest -q`. Tests cover PDF extraction, database schema and seed data, normalization, absolute score, benchmarks, gaps, PPI, zero benchmark behavior and all tie-break stages.

## Deployment

Push the project contents to GitHub. In Streamlit Community Cloud select the repository, `main` branch and `app.py`. Add `GEMINI_API_KEY="..."` in Advanced settings under Secrets, then deploy.

## Synthetic data

The four proposals in `data/sample_rfps` are fictional and contain no confidential data.

## Demonstration

Run `python run_demo.py` to create a deterministic successful-run JSON and malformed-output validation JSON. For the final demonstration, run all four PDFs in the deployed app, download the actual JSON, show one missing-input error and explain the normalization warnings.

## Rubric evidence

See `RUBRIC_EVIDENCE.md` for a direct rubric-to-code mapping.

## Screenshots

Add final screenshots after deployment: criteria, supplier input, workflow progress, leaderboard, supplier drill-down, validation error and recent runs.
