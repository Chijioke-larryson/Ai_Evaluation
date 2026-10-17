"""Safe evaluation adapters for predefined Python tasks.

Only trusted reference functions in this module are executed. Pasted AI output
is stored as evidence for a manual review and is never passed to exec/eval.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Any, Callable

from .validators import validate_email


@dataclass(frozen=True)
class EvaluationCase:
    name: str
    input_data: Any
    expected: Any = None
    expected_exception: type[BaseException] | None = None


@dataclass(frozen=True)
class EvaluationTask:
    key: str
    title: str
    description: str
    criteria: str
    reference: Callable[..., Any]
    cases: tuple[EvaluationCase, ...]


def total_price(amount: float, tax_rate: float) -> float:
    if amount < 0 or tax_rate < 0:
        raise ValueError("Amount and tax rate must be non-negative")
    return round(amount * (1 + tax_rate), 2)


def factorial(number: int) -> int:
    if not isinstance(number, int) or isinstance(number, bool) or number < 0:
        raise ValueError("number must be a non-negative integer")
    result = 1
    for value in range(2, number + 1):
        result *= value
    return result


def is_prime(number: int) -> bool:
    if not isinstance(number, int) or isinstance(number, bool) or number < 2:
        return False
    return all(number % divisor for divisor in range(2, int(number**0.5) + 1))


def word_frequency(text: str) -> dict[str, int]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return {word: text.lower().split().count(word) for word in sorted(set(text.lower().split()))}


def duplicate_values(values: list[Any]) -> list[Any]:
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    seen: set[Any] = set()
    duplicates: list[Any] = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    return duplicates


def summary_report(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(records, list) or any(not isinstance(record, dict) for record in records):
        raise TypeError("records must be a list of dictionaries")
    amounts = [float(record["amount"]) for record in records]
    return {"record_count": len(records), "total_amount": round(sum(amounts), 2), "average_amount": round(sum(amounts) / len(amounts), 2) if amounts else 0}


def _case(name: str, value: Any, expected: Any = None, error: type[BaseException] | None = None) -> EvaluationCase:
    return EvaluationCase(name, value, expected, error)


TASKS: dict[str, EvaluationTask] = {
    "total_price": EvaluationTask("total_price", "Calculate total price after tax", "Return amount × (1 + tax rate), rounded to two decimals.", "Correct arithmetic, rounding, and rejection of negative inputs.", total_price, (_case("No tax", (100, 0), 100.0), _case("Standard tax", (100, 0.075), 107.5), _case("Negative amount", (-1, 0.1), error=ValueError))),
    "factorial": EvaluationTask("factorial", "Calculate a factorial", "Return n! for a non-negative integer.", "Correct base case, multiplication, and invalid-input handling.", factorial, (_case("Zero", 0, 1), _case("Small integer", 5, 120), _case("Negative integer", -1, error=ValueError))),
    "prime": EvaluationTask("prime", "Determine whether a number is prime", "Return whether an integer is prime.", "Correctly classify boundaries, primes, and composites.", is_prime, (_case("Below boundary", 1, False), _case("Prime", 13, True), _case("Composite", 100, False))),
    "word_frequency": EvaluationTask("word_frequency", "Return word frequencies", "Count case-insensitive whitespace-separated words.", "Correct counting, normalization, and empty-string handling.", word_frequency, (_case("Repeated words", "Red blue red", {"blue": 1, "red": 2}), _case("Empty text", "", {}), _case("Wrong input", 12, error=TypeError))),
    "duplicates": EvaluationTask("duplicates", "Find duplicate values", "Return each repeated list value once, preserving first duplicate order.", "Correct repeated-value detection and list validation.", duplicate_values, (_case("Repeated integers", [1, 2, 1, 3, 2], [1, 2]), _case("No duplicates", [1, 2, 3], []), _case("Wrong input", "abc", error=TypeError))),
    "email": EvaluationTask("email", "Validate a basic email address", "Use the documented rule: one non-space @ and a non-space dot-containing domain.", "Apply the same basic rule consistently; this is not full RFC validation.", validate_email, (_case("Valid address", "person@example.com", True), _case("Missing at sign", "person.example.com", False), _case("Empty address", "", False))),
    "summary": EvaluationTask("summary", "Convert records into a summary report", "Return count, total amount, and average amount for records with numeric amount fields.", "Correct aggregation, rounding, empty lists, and invalid record handling.", summary_report, (_case("Two records", [{"amount": 10}, {"amount": 20.5}], {"record_count": 2, "total_amount": 30.5, "average_amount": 15.25}), _case("Empty records", [], {"record_count": 0, "total_amount": 0, "average_amount": 0}), _case("Wrong record shape", [{"name": "x"}], error=KeyError))),
    "invalid_input": EvaluationTask("invalid_input", "Handle invalid input and expected exceptions", "Validate that the adapter raises a documented exception for invalid factorial input.", "Raise ValueError instead of silently returning a misleading result.", factorial, (_case("Negative integer", -1, error=ValueError), _case("Boolean is not an integer", True, error=ValueError), _case("String input", "4", error=ValueError))),
}


def task_options() -> list[EvaluationTask]:
    return list(TASKS.values())


def run_task(task_key: str) -> dict[str, Any]:
    """Run only the trusted reference adapter and return serializable results."""
    if task_key not in TASKS:
        raise KeyError(f"Unknown task: {task_key}")
    task = TASKS[task_key]
    results: list[dict[str, Any]] = []
    for case in task.cases:
        started = perf_counter()
        status = "Failed"
        actual: Any = None
        error_message = ""
        try:
            if isinstance(case.input_data, tuple):
                actual = task.reference(*case.input_data)
            else:
                actual = task.reference(case.input_data)
            if case.expected_exception:
                error_message = f"Expected {case.expected_exception.__name__}, but no exception was raised."
                status = "Failed"
            else:
                status = "Passed" if actual == case.expected else "Failed"
        except Exception as exc:  # Reference adapters intentionally report test errors.
            actual = None
            if case.expected_exception and isinstance(exc, case.expected_exception):
                status = "Passed"
            else:
                status = "Error"
            error_message = f"{type(exc).__name__}: {exc}"
        results.append({"test_name": case.name, "input_data": repr(case.input_data), "expected_output": repr(case.expected) if not case.expected_exception else f"raises {case.expected_exception.__name__}", "actual_output": repr(actual), "status": status, "error_message": error_message, "execution_time_ms": round((perf_counter() - started) * 1000, 3)})
    passed = sum(result["status"] == "Passed" for result in results)
    total = len(results)
    return {"task_key": task_key, "task_title": task.title, "results": results, "tests_passed": passed, "tests_failed": total - passed, "total_tests": total, "pass_rate": round(passed / total * 100, 2) if total else None, "execution_time_ms": round(sum(result["execution_time_ms"] for result in results), 3), "evaluation_source": "Trusted reference implementation"}

