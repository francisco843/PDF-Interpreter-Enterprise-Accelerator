from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def load_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    return pd.read_csv(path)


def validate_columns(frame: pd.DataFrame, required_columns: list[str]) -> None:
    missing_columns = [column for column in required_columns if column not in frame.columns]
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing_columns)}")


def ensure_parent_directory(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def save_json(payload: dict[str, Any], path: Path) -> None:
    ensure_parent_directory(path)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def save_predictions(frame: pd.DataFrame, path: Path) -> None:
    ensure_parent_directory(path)
    frame.to_csv(path, index=False)
