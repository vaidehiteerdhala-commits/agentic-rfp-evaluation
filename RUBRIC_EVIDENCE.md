# Rubric-to-Evidence Matrix

## Agentic workflow and tool use (20)
`services/orchestrator.py` explicitly coordinates criteria, PDF extraction, LLM evaluation, validation, deterministic scoring, ranking, persistence and presentation. The run JSON includes an audit trail.

## PDF extraction and prompting (15)
`services/pdf_service.py` performs reliable page-labelled extraction and rejects empty or scanned/image-only files. `services/llm_service.py` uses dynamic SQLite criteria, JSON-only output and evidence-grounding instructions.

## Validation and scoring (20)
`services/validation_service.py` checks weight configuration and normalizes missing, duplicate, unknown, invalid, non-numeric and out-of-range results. Database maximum scores are authoritative.

## Peer ranking and tie-breaks (20)
`services/scoring_service.py` calculates weighted absolute scores, criterion benchmarks, gaps, relative percentages and PPI, then applies all mandatory tie-break rules. Unit tests cover every formula and tie-break level.

## SQLite and persistence (10)
SQLite stores criteria, run state, complete supplier JSON, queryable criterion results and warnings. The UI provides a recent-runs view.

## Streamlit UI (10)
The UI includes criteria, multi-supplier upload, validation messages, workflow progress, leaderboard, scorecard drill-down, benchmark leaders, evidence, warnings, formulas, recent runs and JSON download.

## Documentation and testing (5)
The package includes setup instructions, synthetic PDFs, deterministic exports, edge cases, a rubric matrix and automated tests for PDFs, database, validation, formulas, zero benchmarks and tie-breaks.
