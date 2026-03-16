# Architecture

## Overview

This repository follows a simple enterprise data science delivery pattern:

1. Read PDF document metadata from a structured CSV source.
2. Apply configuration-driven feature selection.
3. Train a scikit-learn classification pipeline.
4. Persist model artifacts, metrics, and scored outputs.
5. Validate changes through tests and GitHub CI.

## Main Components

- `configs/base.yaml`: declares data source, feature sets, random seed, and output paths.
- `src/enterprise_ds/config.py`: loads and validates project configuration.
- `src/enterprise_ds/data.py`: reads the dataset and enforces column presence.
- `src/enterprise_ds/modeling.py`: builds the preprocessing and classification pipeline.
- `src/enterprise_ds/train.py`: executes training, evaluation, and artifact persistence.
- `tests/`: covers configuration loading and training behavior.

## Design Principles

- Keep code reproducible and configuration-driven.
- Keep outputs auditable for business review.
- Keep the starter project simple enough to adapt quickly.
- Keep the structure ready for future orchestration, registry, or deployment layers.

## Extension Paths

- Replace CSV ingestion with PDF processing pipelines, OCR services, or warehouse extraction.
- Add model monitoring and drift checks.
- Introduce experiment tracking.
- Expand from batch training to scheduled document scoring.
