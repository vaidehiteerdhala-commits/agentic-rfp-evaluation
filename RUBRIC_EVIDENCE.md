# Rubric-to-Evidence Matrix

## 1. Agentic Workflow and Tool Use: 20 Marks

### Implementation

- `services/orchestrator.py`
- `services/pdf_service.py`
- `services/llm_service.py`
- `services/validation_service.py`
- `services/scoring_service.py`
- `utils/db.py`

### Evidence

The orchestrator coordinates PDF extraction, LLM evaluation, normalization,
deterministic scoring, peer benchmarking, tie-breaking, persistence, and
presentation.

The LLM evaluates supplier evidence only. Python controls all final
calculations and ranks.

The completed JSON includes an audit trail. Temporary provider failures use
limited retry with exponential backoff.

## 2. PDF Extraction and Prompting: 15 Marks

### Implementation

- Page-labelled text extraction
- Invalid and empty PDF checks
- Minimum extractable-text validation
- Dynamic criteria from SQLite
- JSON-only response requirement
- Proposal-only evidence requirement
- Conservative scoring for missing evidence

### Evidence

- `services/pdf_service.py`
- `services/llm_service.py`
- Four PDFs under `data/sample_rfps/`
- `tests/test_pdf.py`

## 3. Validation and Scoring: 20 Marks

### Implementation

The validator handles:

- Missing criteria
- Duplicate criteria
- Unknown criteria
- Non-numeric values
- Negative values
- Scores above the maximum
- Incorrect maximum scores
- Missing evidence
- Invalid criteria configuration

### Evidence

- `services/validation_service.py`
- `exports/validation_error_case.json`
- `tests/test_validation.py`
- `tests/test_formulas.py`

## 4. Peer Ranking and Tie-Breaks: 20 Marks

### Implementation

The deterministic scoring engine calculates:

- Absolute weighted score
- Criterion benchmark
- Criterion gap
- Relative performance percentage
- Weighted PPI
- Zero-benchmark handling
- Final ranks

Tie-break order:

1. Higher PPI
2. Earlier submission date
3. Higher experience rating
4. Supplier name ascending

### Evidence

- `services/scoring_service.py`
- `exports/actual_completed_run.json`
- `tests/test_formulas.py`
- `screenshots/06_calculation_verification.png`

## 5. SQLite and Persistence: 10 Marks

### Tables

- `evaluation_criteria`
- `rfp_runs`
- `supplier_results`
- `criterion_results`
- `run_warnings`

### Evidence

- `db/seed_db.py`
- `utils/db.py`
- Recent-runs Streamlit tab
- `screenshots/07_recent_runs.png`

## 6. Streamlit UI: 10 Marks

### Features

- Criteria table
- Multiple proposal uploads
- Supplier metadata
- Input validation
- Workflow progress
- Leaderboard
- Supplier drill-down
- Evidence and justification
- Benchmark indicators
- Warnings
- Formula explanation
- Recent runs
- JSON download

### Evidence

- `app.py`
- Public Streamlit application
- Files under `screenshots/`

## 7. Documentation and Testing: 5 Marks

### Evidence

- `README.md`
- `COLAB_STEPS.md`
- `RUBRIC_EVIDENCE.md`
- Four synthetic PDFs
- Deterministic sample JSON
- Validation-case JSON
- Actual completed-run JSON
- Eleven passing tests
- Google Colab verification
- Deployment screenshots

Rubric-to-Evidence Matrix
1. Agentic Workflow and Tool Use: 20 Marks
Implementation
services/orchestrator.py
services/pdf_service.py
services/llm_service.py
services/validation_service.py
services/scoring_service.py
utils/db.py
Evidence
The orchestrator coordinates PDF extraction, LLM evaluation, normalization, deterministic scoring, peer benchmarking, tie-breaking, persistence, and presentation.

The LLM evaluates supplier evidence only. Python controls all final calculations and ranks.

The completed JSON includes an audit trail. Temporary provider failures use limited retry with exponential backoff.

2. PDF Extraction and Prompting: 15 Marks
Implementation
Page-labelled text extraction
Invalid and empty PDF checks
Minimum extractable-text validation
Dynamic criteria from SQLite
JSON-only response requirement
Proposal-only evidence requirement
Conservative scoring for missing evidence
Evidence
services/pdf_service.py
services/llm_service.py
Four PDFs under data/sample_rfps/
tests/test_pdf.py
3. Validation and Scoring: 20 Marks
Implementation
The validator handles:

Missing criteria
Duplicate criteria
Unknown criteria
Non-numeric values
Negative values
Scores above the maximum
Incorrect maximum scores
Missing evidence
Invalid criteria configuration
Evidence
services/validation_service.py
exports/validation_error_case.json
tests/test_validation.py
tests/test_formulas.py
4. Peer Ranking and Tie-Breaks: 20 Marks
Implementation
The deterministic scoring engine calculates:

Absolute weighted score
Criterion benchmark
Criterion gap
Relative performance percentage
Weighted PPI
Zero-benchmark handling
Final ranks
Tie-break order:

Higher PPI
Earlier submission date
Higher experience rating
Supplier name ascending
Evidence
services/scoring_service.py
exports/actual_completed_run.json
tests/test_formulas.py
screenshots/06_calculation_verification.png
5. SQLite and Persistence: 10 Marks
Tables
evaluation_criteria
rfp_runs
supplier_results
criterion_results
run_warnings
Evidence
db/seed_db.py
utils/db.py
Recent-runs Streamlit tab
screenshots/07_recent_runs.png
6. Streamlit UI: 10 Marks
Features
Criteria table
Multiple proposal uploads
Supplier metadata
Input validation
Workflow progress
Leaderboard
Supplier drill-down
Evidence and justification
Benchmark indicators
Warnings
Formula explanation
Recent runs
JSON download
Evidence
app.py
Public Streamlit application
Files under screenshots/
7. Documentation and Testing: 5 Marks
Evidence
README.md
COLAB_STEPS.md
RUBRIC_EVIDENCE.md
Four synthetic PDFs
Deterministic sample JSON
Validation-case JSON
Actual completed-run JSON
Eleven passing tests
Google Colab verification
Deployment screenshots