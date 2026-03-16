# Contributing Guide

## Working Rules

1. Load the mandatory skill bundle from `./skills.zip` in the repository root.
2. Keep all changes and documentation in English.
3. Use feature branches and open pull requests for review.
4. Run linting and tests before submitting changes.

## Local Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
```

## Run the Baseline Project

```bash
pdf-interpreter train --config configs/base.yaml
```

## Validation

```bash
ruff check .
pytest
```

## Pull Request Expectations

- Explain the business reason for the change.
- Note any PDF processing, extraction, or modeling assumptions.
- Mention whether sample outputs or metrics changed.
- Confirm that tests and linting passed locally.
