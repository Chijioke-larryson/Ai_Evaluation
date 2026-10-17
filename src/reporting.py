"""CSV and Markdown reports built from saved records."""

from __future__ import annotations

from datetime import date
from typing import Any

from .scoring import calculate_overall_score


def experiments_dataframe(experiments: list[dict[str, Any]]):
    """Return a Pandas frame when the UI dependency is installed."""
    import pandas as pd

    return pd.DataFrame(experiments)


def experiments_csv(experiments: list[dict[str, Any]]) -> bytes:
    try:
        return experiments_dataframe(experiments).to_csv(index=False).encode("utf-8")
    except ModuleNotFoundError:
        import csv
        import io

        output = io.StringIO()
        fieldnames = list(experiments[0].keys()) if experiments else []
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
            writer.writerows(experiments)
        return output.getvalue().encode("utf-8")


def individual_markdown(experiment: dict[str, Any], test_cases: list[dict[str, Any]]) -> str:
    overall = calculate_overall_score(experiment.get("pass_rate"), {"correctness": experiment.get("reviewer_correctness_score"), "readability": experiment.get("reviewer_readability_score"), "maintainability": experiment.get("reviewer_maintainability_score"), "usefulness": experiment.get("reviewer_usefulness_score"), "documentation": experiment.get("reviewer_documentation_score")})
    lines = [f"# Evaluation: {experiment.get('title', 'Untitled')}", "", f"Generated: {date.today().isoformat()}", f"Tool: {experiment.get('tool_name', '')} ({experiment.get('tool_provider', '')})", f"Status: {experiment.get('status', '')}", f"Evaluation source: {experiment.get('evaluation_source') or 'Not recorded'}", "", "## Methodology", "Objective results come from the recorded test cases. Reviewer scores are subjective 1–5 judgements and are not merged unless all required dimensions are present.", "", "## Results", f"- Pass rate: {experiment.get('pass_rate') if experiment.get('pass_rate') is not None else 'Not run'}", f"- Tests passed: {experiment.get('tests_passed', 0)}", f"- Tests failed: {experiment.get('tests_failed', 0)}", f"- Execution time (ms): {experiment.get('execution_time_ms') if experiment.get('execution_time_ms') is not None else 'Not measured'}", f"- Internal overall score: {overall if overall is not None else 'Not calculated'}", "", "## Test cases", "| Test | Expected | Actual | Status | Error |", "|---|---|---|---|---|"]
    lines.extend(f"| {case['test_name']} | {case['expected_output']} | {case['actual_output']} | {case['status']} | {case['error_message']} |" for case in test_cases)
    lines += ["", "## Notes", experiment.get("notes") or "No notes recorded.", "", "## Limitations", experiment.get("limitations") or "No limitations recorded.", "", "## Caveat", "This is a record of one saved evaluation and is not a universal benchmark."]
    return "\n".join(lines)


def comparison_markdown(experiments: list[dict[str, Any]]) -> str:
    lines = ["# Tool comparison report", "", f"Generated: {date.today().isoformat()}", "", "## Methodology", "Only saved records supplied to this report are included. Compare task type, language, test count, and status before interpreting differences.", "", "## Results", "| Tool | Provider | Task | Tests passed | Tests failed | Pass rate | Time (ms) |", "|---|---|---|---:|---:|---:|---:|"]
    for experiment in experiments:
        lines.append(f"| {experiment.get('tool_name', '')} | {experiment.get('tool_provider', '')} | {experiment.get('category', '')} | {experiment.get('tests_passed', 0)} | {experiment.get('tests_failed', 0)} | {experiment.get('pass_rate', 'Not run')} | {experiment.get('execution_time_ms', 'Not measured')} |")
    lines += ["", "## Limitations", "Results may represent different prompts, tasks, test counts, or review conditions. This report does not create a fair benchmark where those contexts are not equivalent.", "", "## Recommendation", "Use the observed results as decision support and repeat equivalent tasks before making a tool-selection decision."]
    return "\n".join(lines)


def research_summary_markdown(notes: list[dict[str, Any]], experiments: list[dict[str, Any]]) -> str:
    lines = ["# Research summary", "", f"Generated: {date.today().isoformat()}", "", "## Observed findings", ""]
    if notes:
        for note in notes:
            lines += [f"### {note['title']}", f"- Tool: {note.get('tool_name') or 'Unlinked'}", f"- Source type: {note.get('source_type', '')}", f"- Observation: {note.get('observation', '')}", f"- Strengths: {note.get('strengths', '')}", f"- Limitations: {note.get('limitations', '')}", ""]
    else:
        lines.append("No research notes have been saved.")
    lines += ["## Recommendations", "Prioritise follow-up experiments where evidence is incomplete, keep claims tied to their source type, and require human review for business workflows.", "", "## Sample size and caveats", f"This summary contains {len(notes)} research note(s) and {len(experiments)} experiment record(s). It is not evidence of a population-level benchmark."]
    return "\n".join(lines)

