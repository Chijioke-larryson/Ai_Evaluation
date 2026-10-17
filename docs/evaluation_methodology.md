# Evaluation methodology

## Repeatability

An experiment should preserve the exact prompt, generated answer, task category, programming language, tool/provider, status, and notes. The predefined evaluator uses fixed inputs and trusted reference implementations, records every attempted test case, and measures elapsed execution time locally.

The current application intentionally does not execute pasted AI-generated source. This is a security boundary: the generated answer is evidence for manual review, while the built-in reference evaluation demonstrates the test workflow. No result should be described as a model result unless that model output was genuinely evaluated using an approved runner.

## Test design

The eight starter tasks cover arithmetic, validation, collections, aggregation, and expected exceptions. Each has multiple normal cases and at least one boundary or invalid-input case. Expected results are stored alongside actual results. An unexecuted case is never counted as passed.

## Objective and subjective metrics

Objective metrics are test pass rate, test failures, error count, and execution time. Reviewer scores from 1 to 5 cover correctness, readability, maintainability, usefulness, and documentation quality. Reviewer scores are subjective and should include notes.

The internal overall score is calculated only after a real evaluation has been run and all reviewer dimensions are present:

`60% × test pass rate + 10% × readability + 10% × maintainability + 10% × usefulness + 10% × documentation`

Each 1–5 reviewer score is converted to a percentage first. The score is an internal project metric, not a universally accepted AI benchmark.

## Fair comparisons

Compare tools only when task type, programming language, prompt conditions, test count, and review context are meaningfully similar. A faster result is not automatically better. The comparison page warns when saved records have different contexts.

## Limitations

Timing depends on the local machine. The starter tasks are small and are not representative of all software work. Reviewer ratings can be biased. Sample data is illustrative and must not be presented as measured benchmark evidence. Business benefits are hypotheses until measured in a real workflow.

