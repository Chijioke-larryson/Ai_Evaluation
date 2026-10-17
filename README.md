# AI Evaluation Lab

AI Evaluation Lab is a Streamlit dashboard for evaluating AI-assisted coding workflows with repeatable tests, human review, and context-aware comparisons.

It addresses a practical problem: an AI-generated answer can look convincing without being correct, maintainable, or useful in a real workflow. The lab records the prompt and response as evidence, runs a small set of trusted reference evaluations, separates measured results from reviewer judgement, and turns the saved work into comparison and research reports.

## Live demo

**[Open the live Streamlit demo](https://aievaluation-dzmxsznejh2jrdst4henz6.streamlit.app/Tool_Comparison)** · [View the GitHub repository](https://github.com/Chijioke-larryson/Ai_Evaluation)

The demo opens on the Tool Comparison page. Records shown in the application should be interpreted according to the methodology and limitations documented below; illustrative demo records are labelled in the UI.

## Features

- **Experiment records:** Create, search, filter, edit, and delete evaluation records containing the task context, tool/provider, prompt, generated response, expected behaviour, notes, limitations, and status.
- **Trusted test workflow:** Run eight predefined Python tasks covering arithmetic, factorials, prime detection, word frequency, duplicate detection, basic email validation, record summaries, and invalid-input handling.
- **Objective evidence:** Store individual test cases, expected and actual outputs, pass/fail status, errors, pass rate, and local execution time.
- **Reviewer assessment:** Record 1–5 ratings for correctness, readability, maintainability, usefulness, and documentation. The internal score is shown only when the required evidence and reviewer dimensions are present.
- **Tool comparison:** Filter completed records by tool, category, language, and date; view pass-rate and execution-time charts; and see warnings when records use different testing contexts.
- **Research notes:** Capture observations, strengths, limitations, capabilities, pricing notes, privacy/security observations, source type, source URL, and potential business applications.
- **Business opportunity register:** Document AI-assisted workflow hypotheses, target users, expected benefits, risks, implementation effort, priority, validation status, and required human review.
- **Reports and exports:** Download experiment data as CSV and generate Markdown reports for individual evaluations, tool comparisons, and research summaries.
- **Demo data controls:** Load clearly labelled illustrative records for exploration and remove only those demo records from the sidebar.
- **Optional provider drafting:** When configured, an OpenAI-compatible chat-completions endpoint can draft a response for an experiment. The response is shown for review before it is saved.
- **Security boundary:** Pasted AI-generated code is stored as evidence but is not executed with `exec()`, `eval()`, or an unrestricted subprocess. The built-in evaluator executes only trusted reference functions shipped with the application.

## Evaluation and comparison workflow

1. Create an experiment in **Experiments** and record the exact prompt, generated answer, expected behaviour, task category, programming language, and tool/provider.
2. In **Code Testing**, select the experiment and one of the predefined tasks. The application runs the trusted reference implementation against fixed normal, boundary, and invalid-input cases.
3. Review the saved test cases. The application records pass rate, failures, errors, and local execution time. These are objective results from the trusted adapter—not proof that pasted AI code was executed.
4. Add reviewer ratings and notes when appropriate. The internal project score uses 60% test pass rate plus 10% each for readability, maintainability, usefulness, and documentation. Correctness is required for a complete review but is not double-counted in that formula.
5. Use **Tool Comparison** for descriptive comparisons. Match task type, language, prompt conditions, test count, and review context before drawing conclusions; the page warns when the selected records are not comparable.
6. Add supporting observations in **Research Notes**, record adoption hypotheses in **Business Use Cases**, and export evidence from **Reports**.

## Technology stack

- Python 3.11+
- Streamlit `1.66.0`
- SQLite through Python’s standard library
- Pandas `2.3.3`
- Plotly `6.9.0`
- Pytest `9.1.1`
- Python standard library HTTP client for the optional OpenAI-compatible provider adapter

The exact package versions are pinned in [requirements.txt](requirements.txt). No external database, ORM, code execution sandbox, or OpenAI SDK is required by the current application.

## Project structure

```text
app.py                         Streamlit entry point and navigation
pages/0_Overview.py            Dashboard overview
pages/1_Experiments.py         Experiment records and optional provider drafting
pages/2_Code_Testing.py        Trusted test execution and reviewer scoring
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
src/scoring.py                 Pass-rate and internal score calculations
src/ui.py                      Shared theme, navigation, and layout components
src/validators.py              Form validation helpers
tests/                         Persistence, evaluation, scoring, reporting, and validation tests
```

## Screenshots

No screenshot files are currently tracked in this repository, so this README does not link to an invented image path.

To add genuine screenshots later:

1. Create a `docs/screenshots/` directory.
2. Save real captures there, for example an overview dashboard capture as `docs/screenshots/overview.png` and a comparison capture as `docs/screenshots/tool-comparison.png`.
3. Reference only files that have actually been added and committed:

```markdown
![AI Evaluation Lab overview](docs/screenshots/overview.png)
![Tool Comparison page](docs/screenshots/tool-comparison.png)
```

## Local installation and setup

Run the commands from the repository root. Python 3.11 or newer is recommended.

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

The app initializes the SQLite schema on startup and creates `data/evaluations.db` when it first writes data. The database and local secrets are excluded by [.gitignore](.gitignore).

## Environment variables

The repository includes [.env.example](.env.example). The application reads these values from the process environment with `os.getenv`; it does not automatically load a `.env` file. For local development, you can copy the template and export it in your shell:

```bash
cp .env.example .env
set -a
source .env
set +a
streamlit run app.py
```

Never replace the placeholders with real credentials in a committed file.

| Variable | Required? | Purpose | Default |
| --- | --- | --- | --- |
| `AI_EVAL_DB_PATH` | No | Overrides the SQLite database location. | `data/evaluations.db` |
| `OPENAI_API_KEY` | Optional | Enables requests to the configured OpenAI-compatible endpoint when used with `OPENAI_MODEL`. | Not set |
| `OPENAI_BASE_URL` | Optional | Full chat-completions endpoint URL. | `https://api.openai.com/v1/chat/completions` |
| `OPENAI_MODEL` | Optional | Model name sent to the configured provider. | Not set |

The core application and trusted evaluation workflow do not require an API key. Provider errors, authentication failures, timeouts, and rate limits are surfaced to the user rather than converted into fabricated results. The API key is not written to SQLite.

## Testing

Install the project dependencies, activate the virtual environment, and run:

```bash
python -m pytest -q
```

The test suite covers:

- SQLite initialization, foreign keys, relationships, CRUD operations, and cascading test-case deletion.
- The eight predefined tasks, their test cases, and unknown-task handling.
- Pass-rate and internal-score calculations.
- Input validation, URL validation, and reviewer-score validation.
- CSV/Markdown reporting.
- Demo-data loading, labelling, and removal.

## Streamlit Community Cloud deployment

The repository is structured for Streamlit Community Cloud: `app.py` is in the root, and the pinned `requirements.txt` is also in the root.

1. Push the repository to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/) and choose **Create app**.
3. Select `Chijioke-larryson/Ai_Evaluation`, branch `main`, and entrypoint `app.py`.
4. Select a supported Python version in **Advanced settings**. Use the same Python version locally where possible.
5. Deploy the app. Community Cloud installs the packages listed in `requirements.txt`.
6. If the optional provider is needed, add the root-level variables from the table above in the app’s Secrets settings. The provider reads them with `os.getenv`, so keep the keys at the root of the secrets configuration:

   ```toml
   OPENAI_API_KEY = "your_api_key_here"
   OPENAI_BASE_URL = "https://api.openai.com/v1/chat/completions"
   OPENAI_MODEL = "your_model_name_here"
   AI_EVAL_DB_PATH = "data/evaluations.db"
   ```

   Replace only the placeholders in the private Cloud settings. Do not commit API keys or a local `.env` file.

The current live deployment is available at the [Tool Comparison page](https://aievaluation-dzmxsznejh2jrdst4henz6.streamlit.app/Tool_Comparison). After a new commit is pushed, Community Cloud can rebuild the app from the repository.

## Known limitations

- **SQLite persistence is local:** The app stores records in a local SQLite file. There is no hosted database, authentication, backup process, or multi-user synchronization. This is suitable for local exploration and small demonstrations, but data written to a hosted app should be treated as disposable because a rebuild, restart, or runtime replacement can remove the local file. The database files are also ignored by Git and are not versioned.
- **No arbitrary-code execution:** The application does not execute pasted AI-generated Python. It evaluates trusted reference implementations only, so it demonstrates an evaluation workflow rather than a secure end-to-end model-code benchmark.
- **Small starter task pack:** The eight tasks are intentionally small and are not representative of every software engineering workload.
- **Timing is environment-dependent:** Execution time is measured locally and can vary with the machine or cloud runtime.
- **Reviewer scores are subjective:** Human ratings can be biased and should be read with notes and the objective test evidence.
- **Comparisons require context:** The UI warns about differences in task and test context, but it cannot make incomparable evaluations statistically equivalent.
- **Provider scope:** The optional adapter targets OpenAI-compatible chat-completions APIs and uses the standard library HTTP client. It does not provide provider-specific features, automatic source-code parsing, or a secure sandbox.
- **Basic email rule:** The email task checks a simple documented pattern; it is not full RFC email validation.
- **Business benefits are hypotheses:** Entries in the business opportunity register are not measured productivity or financial outcomes until validated in a real workflow.

## What I learned building this project

This project helped me practice turning an ambiguous AI-tool question into a traceable evaluation workflow. The main lessons were:

- Separate objective evidence—test results, failures, and timing—from subjective review scores.
- Design test cases around normal behaviour, boundaries, invalid inputs, and expected exceptions.
- Make security boundaries explicit: storing generated code is different from executing it.
- Treat tool comparisons as context-dependent evidence rather than universal rankings.
- Use SQLite and a small modular Python structure to build a useful local prototype quickly, while recognizing when hosted persistence and authentication would be needed for a production system.
- Document uncertainty, limitations, and business assumptions so that recommendations remain useful without overstating the evidence.

## Further documentation

- [Evaluation methodology](docs/evaluation_methodology.md)
- [Sample research report](docs/sample_research_report.md)
- [GitHub repository](https://github.com/Chijioke-larryson/Ai_Evaluation)
- [Live demo](https://aievaluation-dzmxsznejh2jrdst4henz6.streamlit.app/Tool_Comparison)
