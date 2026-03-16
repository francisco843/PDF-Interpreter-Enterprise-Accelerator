from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

from .config import PROJECT_ROOT, load_config
from .data import (
    ensure_parent_directory,
    load_dataset,
    save_json,
    save_predictions,
    validate_columns,
)
from .modeling import build_training_pipeline


def _relative_to_project(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def _build_metrics(
    y_true: pd.Series,
    y_pred: pd.Series,
    y_probabilities: pd.Series | None,
    feature_columns: list[str],
    model_path: Path,
    metrics_path: Path,
    predictions_path: Path,
) -> dict[str, Any]:
    metrics: dict[str, Any] = {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
        "feature_columns": feature_columns,
        "model_path": _relative_to_project(model_path),
        "metrics_path": _relative_to_project(metrics_path),
        "predictions_path": _relative_to_project(predictions_path),
        "records_scored": int(len(y_true)),
    }

    if y_probabilities is not None and y_true.nunique() > 1:
        metrics["roc_auc"] = round(float(roc_auc_score(y_true, y_probabilities)), 4)

    return metrics


def train_model(config_path: str | Path) -> dict[str, Any]:
    config = load_config(config_path)
    frame = load_dataset(config.data.source_path)

    feature_columns = config.model.numeric_features + config.model.categorical_features
    validate_columns(frame, feature_columns + [config.data.target_column])

    features = frame[feature_columns]
    target = frame[config.data.target_column]

    stratify = target if target.nunique() > 1 and target.value_counts().min() >= 2 else None

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=config.data.test_size,
        random_state=config.model.random_state,
        stratify=stratify,
    )

    pipeline = build_training_pipeline(
        numeric_features=config.model.numeric_features,
        categorical_features=config.model.categorical_features,
        random_state=config.model.random_state,
    )
    pipeline.fit(x_train, y_train)

    predicted_labels = pd.Series(pipeline.predict(x_test), index=y_test.index)
    predicted_probabilities = None

    if hasattr(pipeline, "predict_proba"):
        predicted_probabilities = pd.Series(
            pipeline.predict_proba(x_test)[:, 1], index=y_test.index
        )

    ensure_parent_directory(config.output.model_path)
    joblib.dump(pipeline, config.output.model_path)

    metrics = _build_metrics(
        y_true=y_test,
        y_pred=predicted_labels,
        y_probabilities=predicted_probabilities,
        feature_columns=feature_columns,
        model_path=config.output.model_path,
        metrics_path=config.output.metrics_path,
        predictions_path=config.output.predictions_path,
    )
    save_json(metrics, config.output.metrics_path)

    predictions = x_test.copy()
    predictions[config.data.target_column] = y_test
    predictions["predicted_label"] = predicted_labels
    if predicted_probabilities is not None:
        predictions["predicted_probability"] = predicted_probabilities.round(4)
    save_predictions(predictions.reset_index(drop=True), config.output.predictions_path)

    return metrics
