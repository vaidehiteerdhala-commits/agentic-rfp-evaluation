# Agentic RFP Evaluation and Supplier Ranking

An evidence-grounded Agentic AI application that evaluates multiple supplier
RFP proposals against dynamically configured criteria and produces an
explainable, deterministic supplier ranking.

The LLM evaluates supplier-document evidence only. Python independently
performs validation, normalization, weighted scoring, peer benchmarking,
tie-breaking, final ranking, and SQLite persistence.

## Live Application

[Open the deployed Streamlit application](PASTE_STREAM_URL_HERE

## Submitted By

Vydehi Theerdhala

## Project Objective

The objective of this project is to automate the first-stage evaluation of
supplier RFP proposals while preserving explainability, auditability, and
deterministic business calculations.

The system:

1. Loads active evaluation criteria from SQLite.
2. Accepts multiple supplier proposal PDFs and supplier metadata.
3. Extracts page-labelled text from each proposal.
4. Uses a JSON-capable Gemini model to evaluate proposal evidence.
5. Validates and normalizes the model response.
6. Calculates weighted scores, benchmarks, gaps, and relative performance.
7. Calculates the Peer Performance Index.
8. Applies deterministic tie-break rules.
9. Persists complete run results in SQLite.
10. Displays a leaderboard and detailed supplier scorecards.
11. Exports the completed run as JSON.

## Architecture

```text
Streamlit User Interface
          |
          v
Agentic Workflow Orchestrator
          |
          +--> SQLite Criteria Tool
          |
          +--> PDF Extraction Tool
          |
          +--> Gemini Evaluation Agent
          |
          +--> Validation and Normalization Tool
          |
          +--> Deterministic Scoring Tool
          |
          +--> Peer Benchmark and Ranking Tool
          |
          +--> SQLite Persistence Tool
          |
          v
Leaderboard, Drill-Down and JSON Export

Agentic RFP Evaluation and Supplier Ranking
An evidence-grounded Agentic AI application that evaluates multiple supplier RFP proposals against dynamically configured criteria and produces an explainable, deterministic supplier ranking.

The LLM evaluates supplier-document evidence only. Python independently performs validation, normalization, weighted scoring, peer benchmarking, tie-breaking, final ranking, and SQLite persistence.

Live Application
[Open the deployed Streamlit application](PASTE_STREAM_URL_HERE

Submitted By
Vydehi Theerdhala

Project Objective
The objective of this project is to automate the first-stage evaluation of supplier RFP proposals while preserving explainability, auditability, and deterministic business calculations.

The system:

Loads active evaluation criteria from SQLite.
Accepts multiple supplier proposal PDFs and supplier metadata.
Extracts page-labelled text from each proposal.
Uses a JSON-capable Gemini model to evaluate proposal evidence.
Validates and normalizes the model response.
Calculates weighted scores, benchmarks, gaps, and relative performance.
Calculates the Peer Performance Index.
Applies deterministic tie-break rules.
Persists complete run results in SQLite.
Displays a leaderboard and detailed supplier scorecards.
Exports the completed run as JSON.
Architecture
Streamlit User Interface
          |
          v
Agentic Workflow Orchestrator
          |
          +--> SQLite Criteria Tool
          |
          +--> PDF Extraction Tool
          |
          +--> Gemini Evaluation Agent
          |
          +--> Validation and Normalization Tool
          |
          +--> Deterministic Scoring Tool
          |
          +--> Peer Benchmark and Ranking Tool
          |
          +--> SQLite Persistence Tool
          |
          v
Leaderboard, Drill-Down and JSON Export
services/orchestrator.py

The orchestrator is implemented in:

Plain Text
services/orchestrator.py
 
Show more lines

It explicitly coordinates PDF extraction, LLM evaluation, validation, deterministic scoring, ranking, and persistence.

Separation of Responsibilities
LLM Responsibilities

The LLM is responsible for:

Interpreting supplier proposal content
Producing criterion-level scores
Providing supporting document evidence
Providing criterion-level justification
Identifying proposal risks
Producing an overall supplier summary
Deterministic Python Responsibilities

Python is responsible for:

Loading active criteria from SQLite
Checking that criterion weights total 100%
Rejecting duplicate supplier names
Validating LLM JSON structure
Adding missing criteria
Ignoring unknown criteria
Handling duplicate criteria
Normalizing incorrect maximum scores
Clipping out-of-range scores
Calculating weighted absolute scores
Calculating peer benchmarks
Calculating gaps and relative percentages
Calculating PPI
Applying tie-break rules
Assigning sequential ranks
Persisting results
Exporting JSON

The LLM never calculates or decides the official final rank.

Agentic Workflow

For every supplier, the orchestrator executes:

Plain Text
PDF_EXTRACTION
-> LLM_EVALUATION
-> VALIDATION
Show more lines

After all suppliers are evaluated, it executes:

Plain Text
DETERMINISTIC_SCORING
-> PEER_BENCHMARKING
-> PPI_CALCULATION
-> TIE_BREAKING
-> PERSISTENCE
-> PRESENTATION
Show more lines

The exported run JSON includes an audit trail for the major supplier-level workflow steps.

Folder Structure
Plain Text
agentic-rfp-evaluation/
├── app.py
├── requirements.txt
├── README.md
├── RUBRIC_EVIDENCE.md
├── COLAB_STEPS.md
├── run_demo.py
├── .gitignore
├── .streamlit/
│ └── config.toml
├── db/
│ ├── __init__.py
│ └── seed_db.py
├── models/
│ ├── __init__.py
│ └── schemas.py
├── services/
│ ├── __init__.py
│ ├── orchestrator.py
│ ├── pdf_service.py
│ ├── llm_service.py
│ ├── validation_service.py
│ └── scoring_service.py
├── utils/
│ ├── __init__.py
│ └── db.py
├── data/
│ └── sample_rfps/
│ ├── Apex_Systems.pdf
│ ├── BrightPath_Tech.pdf
│ ├── NexaWorks.pdf
│ └── Orbit_Digital.pdf
├── exports/
│ ├── sample_completed_run.json
│ ├── validation_error_case.json
│ └── actual_completed_run.json
├── screenshots/
└── tests/
├── test_database.py
├── test_formulas.py
├── test_pdf.py
└── test_validation.py
``
Show more lines
Technologies Used
Python
Streamlit
SQLite
PyMuPDF
Google GenAI SDK
Gemini
Pydantic
Pandas
Pytest
GitHub
Streamlit Community Cloud
Google Colab
Evaluation Criteria

The application seeds and loads the following criteria dynamically from SQLite:

Criterion	Weight	Maximum ScoreTechnical Capability	30%	10
Implementation Plan	20%	10
Commercial Value	20%	10
Security & Compliance	20%	10
Support & Experience	10%	10
Total	100%	

Criteria are not hardcoded into the scoring workflow. The application reads the active database configuration at runtime.

PDF Extraction and Prompting

The PDF extraction tool:

Confirms that the uploaded file is not empty
Opens and validates the PDF
Confirms that the PDF contains pages
Extracts text page by page
Adds page markers such as [PAGE 1]
Rejects PDFs with insufficient extractable text
Produces a clear message when OCR may be required

The evaluation prompt instructs the LLM to:

Use only the uploaded supplier proposal
Avoid external knowledge
Return one result for every active criterion
Return JSON only
Provide page-referenced evidence
Score conservatively when evidence is missing
Keep scores within the configured maximum
Validation and Normalization

The validation layer handles:

Invalid output structure
Missing criteria
Duplicate criterion IDs
Unknown criterion IDs
Non-numeric scores
Boolean score values
Negative scores
Scores above the configured maximum
Incorrect model-provided maximum scores
Missing evidence
Missing justification
Invalid active-weight configuration
Duplicate active database criteria

The database maximum score is authoritative.

Every correction or default is recorded as a validation warning.

Deterministic Scoring Formulas
Absolute Weighted Score

For each criterion:

Plain Text
Criterion contribution
= Validated score / Maximum score x Criterion weight
Show more lines

The total absolute score is:

Plain Text
Absolute weighted score
= Sum of all criterion contributions
Show more lines
Criterion Benchmark
Plain Text
Benchmark
= Highest validated supplier score for the criterion
Show more lines
Criterion Gap
Plain Text
Gap
= Supplier score - Benchmark
Show more lines

A benchmark leader has a gap of zero.

Relative Performance
Plain Text
Relative performance percentage
= Supplier score / Benchmark x 100
Show more lines

When the benchmark is zero:

Plain Text
Relative performance percentage = 100
Show more lines

This avoids division by zero and treats suppliers equally when every supplier has a zero score for the same criterion.

Peer Performance Index
Plain Text
Criterion PPI contribution
= Relative performance percentage x Criterion weight / 100
Show more lines
Plain Text
PPI
= Sum of all criterion PPI contributions
Show more lines
Deterministic Tie-Break Rules

Suppliers are sorted using this exact order:

Higher PPI
Earlier submission date
Higher historical experience rating
Supplier name in ascending alphabetical order

Sequential ranks are assigned only after sorting.

SQLite Database

The application creates and uses:

Plain Text
evaluation_criteria
rfp_runs
supplier_results
criterion_results
run_warnings
Show more lines
Stored run information
Run ID
Creation timestamp
Processing status
Error message for failed runs
Supplier metadata
Absolute score
PPI
Final rank
Complete supplier JSON
Criterion-level results
Benchmarks
Gaps
Relative percentages
Evidence
Justification
Validation warnings
Streamlit User Interface

The application provides:

Active-criteria display
Total-weight validation
Configurable supplier count
Supplier name input
Submission date input
Historical experience rating
Multiple PDF upload
Duplicate-name validation
Missing-input validation
Agentic workflow progress
Final leaderboard
Tie-break explanation
Supplier drill-down
Benchmark-leader indicator
Evidence and justification
Risks and summary
Validation warnings
Formula explanation
Recent persisted runs
Complete JSON download
Synthetic Supplier Proposals

The repository contains four fictional supplier proposals:

Apex Systems
BrightPath Tech
NexaWorks
Orbit Digital

All supplier names, implementation claims, costs, project references, and other proposal details are artificial and were created only for this demonstration.

No confidential company or supplier information is included.

Successful Demonstration Run

The successful live run evaluated four supplier proposals.

Plain Text
Run status: COMPLETED
Number of suppliers: 4
Gemini model: PASTE_SUCCESSFUL_MODEL_HERE
Show more lines

The actual exported result is available at:

Plain Text
exports/actual_completed_run.json
Show more lines

The JSON includes:

Four supplier evaluations
Validated criterion scores
Evidence and justification
Benchmarks
Gaps
Relative percentages
Absolute weighted scores
PPI
Tie-break order
Sequential final ranks
Validation warnings
Audit trail
Validation and Error Demonstration

The project demonstrates two types of validation.

User Input Validation

The Streamlit interface prevents evaluation when:

A supplier name is missing
A supplier PDF is missing
Duplicate supplier names are entered
The API key is unavailable
Malformed LLM Output Validation

The file:

Plain Text
exports/validation_error_case.json
Show more lines

contains deliberately malformed input demonstrating:

An out-of-range score
An incorrect maximum score
A duplicate criterion
An unknown criterion
Missing criteria

The validator:

Clips the score to its valid range
Replaces the incorrect maximum with the database maximum
Ignores duplicate and unknown criteria
Adds missing criteria with zero scores
Records all normalization warnings
Provider Failure Handling

Temporary provider failures such as HTTP 503 are handled through controlled retry logic with exponential backoff and jitter.

After maximum retry attempts, the run is marked as failed with an error message. A later run can be started independently after provider recovery.

Automated Testing

Run:

Shell
python -m pytest -q
Show more lines

Verified result:

Plain Text
11 passed
Show more lines

The test suite covers:

Four sample PDFs exist
Sample PDF text extraction
Invalid PDF rejection
Database creation
Database table schema
Five seeded criteria
Criteria weights total 100%
Missing criterion normalization
Score clipping
Maximum-score normalization
Duplicate criterion handling
Unknown criterion handling
Non-numeric score handling
Invalid weight configuration
Absolute weighted score
Benchmark calculation
Gap calculation
PPI calculation
Zero-benchmark handling
Submission-date tie-break
Experience-rating tie-break
Supplier-name tie-break
Independent Calculation Verification

The actual completed-run JSON was independently checked in Google Colab.

The verification confirms:

Completed run status
Four suppliers present
Sequential ranks
Absolute weighted-score calculations
Criterion benchmarks
Criterion gaps
Relative percentages
PPI values
Mandatory ranking order
Completed audit-trail events

Evidence is available in:

Plain Text
screenshots/06_calculation_verification.png
Show more lines
Assumptions
Active criterion weights must total 100%.
Every active criterion must have a positive maximum score.
Proposal PDFs must contain extractable text.
Scanned or image-only PDFs require OCR, which is outside the minimum scope.
The supplier name, submission date, and experience rating are entered by the evaluator.
LLM scores are advisory until validated.
Database maximum scores override model-provided maximum scores.
Python calculations are the final source of truth.
The four included supplier proposals are synthetic.
Limitations
LLM Variability

Criterion scores and wording may vary slightly between model runs. The validation, formulas, tie-breaks, and rank calculation remain deterministic for the validated input scores.

Provider Availability

The external LLM service may occasionally return temporary overload or quota errors. The application uses limited retries for transient failures.

OCR

The current version supports text-based PDFs. Image-only or scanned PDFs require an OCR extension.

Streamlit Local Storage

SQLite provides local persistence for the project demonstration. Streamlit Community Cloud uses an ephemeral local filesystem, so database contents can reset when the application is rebuilt, restarted, or moved.

A production implementation would use a managed persistent database.

Supplier-Level Resume

If all retry attempts fail for one supplier, the complete run is marked as failed. A future production enhancement would persist supplier checkpoints and resume only incomplete supplier evaluations.

Local Setup
Prerequisites
Python 3.11 or Python 3.12
A Gemini API key
Installation
Shell
pip install -r requirements.txt
Show more lines
Initialize SQLite
Shell
python db/seed_db.py
Show more lines
Configure the API key locally

Create:

Plain Text
.streamlit/secrets.toml
Show more lines

Add:

TOML
GEMINI_API_KEY = "your-private-key"
Show more lines

Never commit this file.

Start the application
Shell
streamlit run app.py
Show more lines
Google Colab Verification

Upload and extract the ZIP, then run:

Shell
pip install -r requirements.txt
python db/seed_db.py
python run_demo.py
python -m pytest -q
Show more lines

The complete Colab steps are available in:

Plain Text
COLAB_STEPS.md
Show more lines
Deployment

The project is deployed from GitHub using Streamlit Community Cloud.

Deployment configuration:

Plain Text
Repository: PASTE_GITHUB_REPOSITORY_NAME_HERE
Branch: main
Application file: app.py
Python version: 3.12
Show more lines

The Gemini API key is stored only in Streamlit Secrets.

Application Screenshots
Active Criteria Loaded from SQLite

screenshots/01_criteria.png

Supplier Inputs and Proposal Uploads

screenshots/02_supplier_input_part1.png

screenshots/02_supplier_input_part2.png

Agentic Workflow Progress

screenshots/03_agentic_workflow.png

Completed Supplier Leaderboard

screenshots/04_leaderboard.png

Supplier Scorecard Drill-Down

screenshots/05_supplier_scorecard_part1.png

screenshots/05_supplier_scorecard_part2.png

Independent Calculation Verification

screenshots/06_calculation_verification.png

Persisted Recent Runs

screenshots/07_recent_runs.png

Provider Failure and Recovery

screenshots/08_retry_failure_and_recovery.png

Evaluation Rubric Mapping
Agentic Workflow and Tool Use: 20 Marks

Evidence:

services/orchestrator.py
Explicit tool ordering
Separate LLM and deterministic responsibilities
Run-status management
Audit trail
Retry and failure handling
PDF Extraction and Prompting: 15 Marks

Evidence:

services/pdf_service.py
Page-labelled extraction
PDF validity checks
Dynamic SQLite criteria
Evidence-grounded JSON prompt
Conservative missing-evidence rule
Validation and Scoring: 20 Marks

Evidence:

services/validation_service.py
Missing, duplicate, unknown, and invalid criterion handling
Score clipping
Database maximum-score authority
Warning generation
Deterministic weighted-score calculation
Automated validation and formula tests
Peer Ranking and Tie-Breaks: 20 Marks

Evidence:

services/scoring_service.py
Criterion benchmarks
Criterion gaps
Relative performance
Zero-benchmark safety
Weighted PPI
Four-stage deterministic sorting
Sequential ranks
Independent calculation verification
SQLite and Persistence: 10 Marks

Evidence:

db/seed_db.py
utils/db.py
Five SQLite tables
Run status and errors
Complete supplier JSON
Criterion-level details
Warning persistence
Recent-runs display
Streamlit UI: 10 Marks

Evidence:

app.py
Active criteria
Multiple supplier inputs
Workflow status
Leaderboard
Drill-down
Evidence
Warnings
Formula explanation
Recent runs
JSON download
Documentation and Testing: 5 Marks

Evidence:

README.md
RUBRIC_EVIDENCE.md
COLAB_STEPS.md
Four synthetic proposals
Deterministic demonstration exports
Actual completed-run JSON
Eleven passing automated tests
Validation and edge-case examples
Screenshots and reproducibility instructions
Future Enhancements
OCR for scanned proposals
Managed persistent cloud database
Supplier-level checkpoint and resume
Configurable criteria-management screen
Authentication and role-based access
Evaluation history retrieval
Prompt and token observability
API usage monitoring
Human approval before final ranking
Migration to the Gemini Interactions API
SAP Ariba or SAP S/4HANA procurement integration
Security
No API key is committed to GitHub.
.streamlit/secrets.toml is excluded through .gitignore.
Supplier proposals are synthetic.
The public JSON export contains no credentials.
Users should revoke any API key accidentally exposed in source control.
License and Data Notice

This repository is an educational and portfolio demonstration.

All supplier proposals, names, prices, project references, and evaluation results are fictional.


---

# Part F: Replace the README placeholders

You must replace these placeholders:

```text
PASTE_STREAMLIT_URL_HERE
PASTE_GITHUB_URL_HERE
PASTE_SUCCESSFUL_MODEL_HERE
PASTE_GITHUB_REPOSITORY_NAME_HERE

Example replacement
Markdown
https://your-app.streamlit.app
Show more lines
Markdown
[Open the GitHub repository](https://github.com/your-user/agentic-rfp-evaluation)
Show more lines
Plain Text
Gemini model: gemini-3.8-flash
Show more lines
Plain Text
Repository: your-user/agentic-rfp-evaluation
Show more lines

Use the exact model that completed the live run.