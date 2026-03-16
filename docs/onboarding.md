# Onboarding

## Prerequisites

- Python 3.11 or newer
- Git
- A local environment capable of loading the required skill bundle

## Mandatory Skill Loading Step

Before doing anything else, load the required skill bundle from:

`./skills.zip`

This is a mandatory project requirement for contributors and AI agents.

The `skills.zip` bundle should be committed at the root of the repository so it is available from the `main` branch in GitHub.

## Local Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
```

## Run the Baseline Pipeline

```bash
pdf-interpreter train --config configs/base.yaml
```

Expected outputs:

- `models/pdf_interpreter_model.joblib`
- `reports/pdf_interpreter_metrics.json`
- `reports/pdf_interpreter_predictions.csv`

## Validation Commands

```bash
ruff check .
pytest
```

## Publishing to GitHub

1. Initialize the repository if needed.
2. Commit the generated project files.
3. Create a remote GitHub repository.
4. Push the `main` branch.
5. Enable GitHub Actions for CI.
