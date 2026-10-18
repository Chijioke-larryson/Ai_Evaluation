# AI Evaluation Lab

AI Evaluation Lab is a Streamlit portfolio application for evaluating AI-assisted coding workflows with repeatable tests, human review, and evidence-aware tool comparisons.

It solves a common adoption and QA problem: an AI-generated answer can sound convincing without being correct, maintainable, or useful in context. The lab preserves the prompt and response, runs trusted reference evaluations, separates measured results from reviewer judgement, and turns the saved evidence into comparison and research reports.

## Try the live demo

**[Open AI Evaluation Lab](https://aievaluation-dzmxsznejh2jrdst4henz6.streamlit.app/Tool_Comparison)** · [View the source on GitHub](https://github.com/Chijioke-larryson/Ai_Evaluation)

The demo opens on **Tool Comparison**. Use the sidebar to explore the other pages and load clearly labelled illustrative records if the deployment has no saved data.

## Why this project matters

This project demonstrates a practical evaluation workflow for AI adoption, QA, and DevOps-oriented review:

- preserve the original evidence;
- test consistent, documented behaviours;
- distinguish automated results from human assessment;
- compare tools only when their context is understood; and
- document limitations before making an adoption recommendation.

## Features

- **Structured experiment records:** Create, search, filter, edit, and delete records containing the task context, AI tool, prompt, response, expected behaviour, notes, limitations, and status.
- **Trusted reference testing:** Run eight predefined Python tasks covering total-price calculation, factorials, prime detection, word frequency, duplicate detection, basic email validation, record summaries, and invalid-input handling.
- **Objective evidence:** Save individual test cases with expected output, actual output, pass/fail status, errors, pass rate, and local execution time.
- **Human review:** Record 1–5 ratings for correctness, readability, maintainability, usefulness, and documentation.
- **Transparent internal score:** Show the score only when a test run and all reviewer dimensions are present. The formula uses 60% test pass rate plus 10% each for readability, maintainability, usefulness, and documentation; correctness is required but is not double-counted.
- **Tool comparison:** Filter completed records by tool, category, language, and date; view pass-rate and execution-time charts; and receive a warning when selected records use different test contexts.
- **Research notebook:** Capture observations, strengths, limitations, capabilities, pricing notes, privacy/security observations, source type, source URL, and potential business applications.
- **Business opportunity register:** Record AI-assisted workflow hypotheses, target users, expected benefits, risks, implementation effort, priority, validation status, and required human review.
- **Reports and exports:** Download experiment data as CSV and generate Markdown reports for individual evaluations, comparisons, and research summaries.
- **Illustrative demo data:** Load labelled sample records for exploration and remove only records marked as demo data.
- **Optional provider drafting:** When configured, call an OpenAI-compatible chat-completions endpoint to draft a response for an experiment before saving it.
- **Security boundary:** Store pasted AI-generated code as evidence, but do not execute it with `exec()`, `eval()`, or an unrestricted subprocess. The built-in evaluator runs only trusted reference functions shipped with the application.
- **Portfolio-ready interface:** Use the responsive Streamlit layout, sidebar navigation, metric cards, filters, tables, charts, status badges, and shared footer to make the evidence easy to scan.

## Evaluation and comparison workflow

1. Create an experiment in **Experiments** and record the problem, exact prompt, generated response, expected behaviour, task category, language, and tool/provider.
2. In **Code Testing**, select the experiment and one predefined task. The application runs the trusted reference implementation against fixed normal, boundary, and invalid-input cases.
3. Review the saved test cases. The application records pass rate, failures, errors, and local execution time. These results describe the trusted adapter; the pasted AI response is not executed by the application.
4. Add reviewer ratings and notes when appropriate. The internal score is calculated only after a completed test run and all five reviewer dimensions are present.
5. Use **Tool Comparison** for descriptive comparisons. Match task type, language, prompt conditions, test count, and review context before treating differences as meaningful; the page warns when the selected records are not comparable.
6. Add supporting observations in **Research Notes**, record adoption hypotheses in **Business Use Cases**, and export the evidence from **Reports**.

## Technology stack

- Python 3.11+
- Streamlit `1.66.0`
- SQLite through Python's standard library
- Pandas `2.3.3`
- Plotly `6.9.0`
- Pytest `9.1.1`
- Python standard-library HTTP client for the optional OpenAI-compatible provider adapter

The exact versions are pinned in [requirements.txt](requirements.txt). The current application does not require an ORM, external database, code-execution sandbox, or OpenAI SDK.

## Screenshots

The repository includes a genuine capture of the **Code Testing** workflow:

![AI Evaluation Lab Code Testing page](screenshots/Screenshot%202026-10-17%20at%2020.52.54.png)

To add more captures, save real images under `screenshots/` and reference the committed files with relative Markdown paths. For example:

```markdown
![Overview dashboard](screenshots/overview.png)
![Tool Comparison page](screenshots/tool-comparison.png)
```

Do not add placeholder paths or screenshots that do not represent the running application.

## Project structure

```text
app.py                         Streamlit entry point and navigation
pages/0_Overview.py            Dashboard overview and metrics
pages/1_Experiments.py         Experiment records and optional provider drafting
pages/2_Code_Testing.py        Trusted task execution and reviewer scoring
pages/3_Tool_Comparison.py     Evidence-aware charts and comparison table
pages/4_Research_Notes.py      Research findings and source notes
pages/5_Business_Use_Cases.py  Business opportunity hypotheses
pages/6_Reports.py             CSV and Markdown exports
pages/7_Methodology.py         Evaluation method and limitations
src/database.py                SQLite connection, schema, CRUD, and demo cleanup
src/evaluation_engine.py       Predefined tasks and trusted reference functions
src/provider.py                Optional OpenAI-compatible HTTP adapter
src/reporting.py               CSV and Markdown report generation
src/sample_data.py             Clearly labelled illustrative records
src/scoring.py                 Pass-rate and internal-score calculations
src/ui.py                      Shared theme, navigation, and layout components
src/validators.py              Form validation helpers
tests/                         Persistence, evaluation, scoring, reporting, and validation tests
docs/                          Methodology and sample report documentation
screenshots/                   Genuine application captures
```

## Local installation and setup

Run these commands from the repository root. Python 3.11 or newer is recommended.

### macOS/Linux

```bash
git clone https://github.com/Chijioke-larryson/Ai_Evaluation.git
cd Ai_Evaluation

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

### Windows PowerShell

```powershell
git clone https://github.com/Chijioke-larryson/Ai_Evaluation.git
Set-Location Ai_Evaluation

py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

The application initializes the SQLite schema at startup. By default it creates `data/evaluations.db`; the `data/*.db` and `data/*.sqlite` patterns are excluded by [.gitignore](.gitignore).

## Environment configuration

The application reads process environment variables with `os.getenv`. It does not automatically load a `.env` file, and no secret values belong in this repository. The core application and trusted evaluation workflow work without an API key.

| Variable | Required? | Purpose | Default |
| --- | --- | --- | --- |
| `AI_EVAL_DB_PATH` | No | Override the SQLite database location. | `data/evaluations.db` |
| `OPENAI_API_KEY` | Optional | Enables the optional provider adapter when used with `OPENAI_MODEL`. | Not set |
| `OPENAI_BASE_URL` | Optional | Full OpenAI-compatible chat-completions endpoint URL. | `https://api.openai.com/v1/chat/completions` |
| `OPENAI_MODEL` | Optional | Model name sent to the configured provider. | Not set |

For local development, set only the values you need in your shell:

```bash
export AI_EVAL_DB_PATH="$PWD/data/evaluations.db"
export OPENAI_BASE_URL="https://api.openai.com/v1/chat/completions"
export OPENAI_MODEL="your_model_name_here"
export OPENAI_API_KEY="your_api_key_here"
streamlit run app.py
```

The API key is used for the provider request and is not written to SQLite. Provider errors, authentication failures, timeouts, and rate limits are surfaced to the user.

## Testing

Install the dependencies and activate the virtual environment, then run:

```bash
python -m pytest -q
```

The test suite covers:

- SQLite initialization, foreign keys, relationships, CRUD operations, and cascading test-case deletion;
- all eight predefined tasks, their test cases, and unknown-task handling;
- pass-rate and internal-score calculations;
- input, URL, email, and reviewer-score validation;
- CSV and Markdown report generation; and
- demo-data loading, labelling, and removal.

## Streamlit Community Cloud deployment

The repository is ready for Streamlit Community Cloud because `app.py` and the pinned `requirements.txt` are at the repository root.

1. Push the repository, including the `screenshots/` asset, to GitHub.
2. In [Streamlit Community Cloud](https://share.streamlit.io/), choose **Create app**.
3. Select `Chijioke-larryson/Ai_Evaluation`, the deployment branch, and `app.py` as the main file.
4. Choose a supported Python version in **Advanced settings**. Use the same version locally where possible.
5. Deploy. Community Cloud installs the packages from `requirements.txt`.
6. The core app requires no secrets. If the optional provider is needed, add root-level `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and `OPENAI_MODEL` values in the app's private Secrets settings. Never commit real credentials.

The current public deployment is available at the [Tool Comparison page](https://aievaluation-dzmxsznejh2jrdst4henz6.streamlit.app/Tool_Comparison).

## Known limitations

- **SQLite is local, not hosted:** Records are stored in a local SQLite file. The application has no hosted database, authentication, backup process, or multi-user synchronization. The database file is ignored by Git, so it is not versioned.
- **Hosted data is not durable:** On Streamlit Community Cloud, the local runtime filesystem should not be treated as permanent storage. A rebuild, restart, or runtime replacement can remove records written to the local database. Treat hosted records as disposable unless an external persistence layer is added.
- **No arbitrary-code execution:** The application does not execute pasted AI-generated Python. It evaluates trusted reference implementations, so this is an evaluation-workflow prototype rather than an end-to-end model-code benchmark.
- **Small task pack:** The eight predefined tasks are intentionally small and do not represent every software-engineering workload.
- **Timing is environment-dependent:** Execution time is measured in the local runtime and can vary by machine or cloud environment.
- **Reviewer scores are subjective:** Human ratings can be biased and should be interpreted alongside notes and objective test evidence.
- **Comparisons require context:** The UI warns about different task and test contexts, but it cannot make incomparable evaluations statistically equivalent.
- **Optional provider scope:** The provider adapter targets OpenAI-compatible chat-completions APIs through the standard library HTTP client. It does not add provider-specific features, source-code parsing, or a secure execution sandbox.
- **Basic email rule:** The email task checks a simple documented pattern; it is not full RFC email validation.
- **Business benefits are hypotheses:** Business opportunity entries are not measured productivity or financial outcomes until validated in a real workflow.

## What I learned building this project

Building this lab helped me turn an ambiguous AI-tool question into a traceable evaluation workflow. I learned to:

- separate objective test evidence from subjective reviewer judgement;
- design cases around normal behaviour, boundaries, invalid inputs, and expected exceptions;
- make security boundaries explicit when storing generated code;
- treat tool comparisons as context-dependent evidence rather than universal rankings;
- use a small modular Python structure and SQLite to build a useful local prototype quickly; and
- document uncertainty, limitations, and business assumptions without overstating the evidence.

## Further documentation

- [Evaluation methodology](docs/evaluation_methodology.md)
- [Sample research report](docs/sample_research_report.md)
- [GitHub repository](https://github.com/Chijioke-larryson/Ai_Evaluation)
- [Live demo](https://aievaluation-dzmxsznejh2jrdst4henz6.streamlit.app/Tool_Comparison)

---

**Built by [Chijioke Larryson](https://github.com/Chijioke-larryson)** · AI Adoption, QA, and DevOps portfolio project · [Connect with the developer on GitHub](https://github.com/Chijioke-larryson)
