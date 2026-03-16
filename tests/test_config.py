from enterprise_ds.config import PROJECT_ROOT, load_config


def test_load_config_returns_expected_paths() -> None:
    config = load_config(PROJECT_ROOT / "configs/base.yaml")

    assert config.project_name == "PDF Interpreter Enterprise Intelligence"
    assert config.data.source_path == PROJECT_ROOT / "data/external/pdf_document_sample.csv"
    assert config.output.model_path == PROJECT_ROOT / "models/pdf_interpreter_model.joblib"
    assert "document_type" in config.model.categorical_features
