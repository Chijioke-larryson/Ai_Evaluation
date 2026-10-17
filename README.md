# AI Tool Evaluation Lab

AI Tool Evaluation Lab is a small, honest, locally runnable research dashboard for recording AI-assisted coding experiments, running safe predefined Python evaluations, comparing results, and turning saved observations into reports.

It is designed as a portfolio project for an AI Adoption Intern application. The core application does not require an API key and does not execute arbitrary code pasted into the browser.

## Problem statement

AI coding tools can produce useful code quickly, but their output still needs repeatable testing, human review, and context-aware comparison. This project makes those activities visible in one place without presenting illustrative or incomplete data as a benchmark.

## Features

- SQLite persistence with foreign-key enforcement and automatic initialization.
- Experiment CRUD with Draft, Ready for testing, Tested, and Reviewed statuses.
- Eight predefined Python tasks with trusted reference implementations, edge cases, expected exceptions, timings, and test results.
- Objective metrics (test pass rate, failures, execution time) separated from reviewer-assessed 1–5 scores.
- Tool comparison charts and CSV/Markdown exports using saved records.
- Searchable research notes and a business opportunity register.
- Explicit, reproducible demo data that can be removed without touching real records.
- Optional OpenAI-compatible HTTP provider integration using environment variables only.
- Pytest coverage for persistence, validation, evaluation, scoring, exports, and demo data.

## Architecture

`app.py` is the overview page. Streamlit pages in `pages/` contain presentation and user interactions. Business logic lives in `src/`:

- `database.py`: connection handling, schema initialization, CRUD, and demo-data cleanup.
- `evaluation_engine.py`: safe, predefined tasks and trusted reference adapters.
- `scoring.py`: pass-rate and transparent overall-score calculations.
- `reporting.py`: CSV and Markdown report generation.
- `sample_data.py`: clearly marked illustrative records.
- `validators.py`: reusable input validation.
- `provider.py`: optional, configurable OpenAI-compatible request adapter.

## Technology stack

Python 3.11+, Streamlit, SQLite, Pandas, Plotly, and Pytest. The project also runs on newer compatible Python versions.

## Installation

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

Run the tests:

```bash
pytest -q
```

The application creates `data/evaluations.db` on first start. Set `AI_EVAL_DB_PATH` to use another database path, especially for a local experiment or deployment.

## Using the application

1. Open **Experiments** and record the exact prompt, generated answer, expected behaviour, and notes. A configured optional provider can draft a response, but no response is fabricated when it is unavailable.
2. Select a predefined task and click **Run trusted reference evaluation**. This executes only code shipped with the application and records real test results as a reference baseline.
3. Review the result, enter subjective scores only when appropriate, and mark the experiment as Reviewed.
4. Use **Tool Comparison** only for records with comparable tasks and test counts.
5. Add evidence-backed observations in **Research Notes** and hypotheses in **Business Use Cases**.
6. Export reports from **Reports**. Demo records are labelled and can be removed from the sidebar.

## Database design

The database contains `tools`, `experiments`, `test_cases`, `research_notes`, and `business_use_cases`. Foreign keys and indexes are enabled. Demo records have an internal `is_demo` marker so removal is scoped to the loader's records.

## Evaluation methodology

Read [docs/evaluation_methodology.md](docs/evaluation_methodology.md). In short, pass rate and timing are measured facts from the trusted adapter. Correctness, readability, maintainability, usefulness, and documentation are reviewer judgements. The internal overall score is 60% objective pass rate plus 10% for each of four reviewer dimensions; it is not a universal benchmark.

## Optional API setup

Copy `.env.example` to `.env` and load the variables in your shell or Streamlit deployment secrets. The app reads `OPENAI_API_KEY`, `OPENAI_BASE_URL` (defaulting to the OpenAI-compatible endpoint), and `OPENAI_MODEL`. The API key is never written to SQLite. Rate limits, authentication errors, timeouts, and provider errors are shown as errors rather than converted into fake data. See [docs/evaluation_methodology.md](docs/evaluation_methodology.md) for the evaluation boundary.

## Security limitations

The app deliberately does not use `exec`, `eval`, or unrestricted subprocess calls on pasted AI output. The current evaluator runs trusted reference implementations only. This means it measures the evaluation workflow and reference baseline; it does not claim that pasted source code has been executed. A future code-runner would need a separate, restricted process with resource limits, filesystem restrictions, no network, and a timeout.

## Known limitations and future improvements

The optional provider adapter currently targets OpenAI-compatible chat-completions APIs. It does not include a secure arbitrary-code sandbox, automatic source-code parsing, or a universal benchmark suite. Future work could add isolated runners, richer task packs, provider-specific adapters, and export templates.

## Screenshots

No screenshots are included because this repository does not claim a deployment or a captured interface. Run the application locally to create screenshots from your own environment.

## Author and contact

Project author: not specified in the source brief. Add your name and preferred contact details before publishing this portfolio project.

