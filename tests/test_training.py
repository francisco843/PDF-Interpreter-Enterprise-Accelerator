from pathlib import Path

import pandas as pd

from enterprise_ds.config import PROJECT_ROOT
from enterprise_ds.train import train_model


def test_train_model_writes_artifacts(tmp_path: Path) -> None:
    model_path = tmp_path / "model.joblib"
    metrics_path = tmp_path / "metrics.json"
    predictions_path = tmp_path / "predictions.csv"
    dataset_path = PROJECT_ROOT / "data/external/pdf_document_sample.csv"
    config_path = tmp_path / "config.yaml"

    config_path.write_text(
        "\n".join(
            [
                "project_name: Test Project",
                "data:",
                f"  source_path: {dataset_path}",
                "  target_column: human_review_required",
                "  test_size: 0.25",
                "model:",
                "  numeric_features:",
                "    - page_count",
                "    - extracted_characters",
                "    - image_count",
                "    - table_count",
                "    - ocr_confidence",
                "  categorical_features:",
                "    - document_type",
                "    - source_channel",
                "    - language",
                "    - contains_signature",
                "  random_state: 42",
                "output:",
                f"  model_path: {model_path}",
                f"  metrics_path: {metrics_path}",
                f"  predictions_path: {predictions_path}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    metrics = train_model(config_path)

    assert model_path.exists()
    assert metrics_path.exists()
    assert predictions_path.exists()
    assert 0.0 <= metrics["accuracy"] <= 1.0

    predictions = pd.read_csv(predictions_path)
    assert "predicted_label" in predictions.columns
