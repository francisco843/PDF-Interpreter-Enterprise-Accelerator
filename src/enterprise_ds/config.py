from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class DataConfig:
    source_path: Path
    target_column: str
    test_size: float


@dataclass(frozen=True)
class ModelConfig:
    numeric_features: list[str]
    categorical_features: list[str]
    random_state: int


@dataclass(frozen=True)
class OutputConfig:
    model_path: Path
    metrics_path: Path
    predictions_path: Path


@dataclass(frozen=True)
class AppConfig:
    project_name: str
    data: DataConfig
    model: ModelConfig
    output: OutputConfig


def _resolve_path(raw_path: str | Path) -> Path:
    path = Path(raw_path)
    return path if path.is_absolute() else PROJECT_ROOT / path


def _require_keys(payload: dict[str, Any], keys: list[str], context: str) -> None:
    missing_keys = [key for key in keys if key not in payload]
    if missing_keys:
        raise KeyError(f"Missing keys in {context}: {', '.join(missing_keys)}")


def load_config(config_path: str | Path) -> AppConfig:
    resolved_path = _resolve_path(config_path)
    payload = yaml.safe_load(resolved_path.read_text(encoding="utf-8"))

    if not isinstance(payload, dict):
        raise ValueError("Configuration file must contain a top-level mapping.")

    _require_keys(payload, ["project_name", "data", "model", "output"], "root")

    data_payload = payload["data"]
    model_payload = payload["model"]
    output_payload = payload["output"]

    if not all(
        isinstance(section, dict) for section in [data_payload, model_payload, output_payload]
    ):
        raise ValueError("Configuration sections 'data', 'model', and 'output' must be mappings.")

    _require_keys(data_payload, ["source_path", "target_column", "test_size"], "data")
    _require_keys(
        model_payload,
        ["numeric_features", "categorical_features", "random_state"],
        "model",
    )
    _require_keys(output_payload, ["model_path", "metrics_path", "predictions_path"], "output")

    return AppConfig(
        project_name=str(payload["project_name"]),
        data=DataConfig(
            source_path=_resolve_path(data_payload["source_path"]),
            target_column=str(data_payload["target_column"]),
            test_size=float(data_payload["test_size"]),
        ),
        model=ModelConfig(
            numeric_features=[str(column) for column in model_payload["numeric_features"]],
            categorical_features=[str(column) for column in model_payload["categorical_features"]],
            random_state=int(model_payload["random_state"]),
        ),
        output=OutputConfig(
            model_path=_resolve_path(output_payload["model_path"]),
            metrics_path=_resolve_path(output_payload["metrics_path"]),
            predictions_path=_resolve_path(output_payload["predictions_path"]),
        ),
    )
