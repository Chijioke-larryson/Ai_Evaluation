"""Methodology page."""

import streamlit as st

st.set_page_config(page_title="Methodology | AI Evaluation Lab", layout="wide")
st.title("Methodology")
st.markdown("""
### What is measured

The app records test pass rate, failures, errors, and local execution time from the trusted predefined evaluator. Unexecuted test cases are not counted as passing.

### What is reviewed

Correctness, readability, maintainability, usefulness, and documentation quality are 1–5 reviewer judgements. They are subjective and should be accompanied by notes.

### Internal overall score

When a real evaluation has run and all required reviewer dimensions are present, the app uses 60% objective pass rate and 10% each for readability, maintainability, usefulness, and documentation. This is an internal project metric, not a universal AI benchmark.

### Security boundary

Pasted AI-generated code is never executed in the Streamlit process. The current workflow runs only trusted reference implementations shipped in `src/evaluation_engine.py`. A future arbitrary-code runner would need process isolation, limits, timeout, filesystem restrictions, and no network access.

### Fair comparison

Tools should be compared on equivalent prompts, tasks, languages, test counts, and review conditions. Speed alone is not a quality ranking. Demo records are illustrative and must not be presented as real findings.
""")

