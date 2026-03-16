from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from .train import train_model

app = typer.Typer(add_completion=False, no_args_is_help=True)

ConfigOption = Annotated[
    Path,
    typer.Option(
        ...,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Path to the YAML configuration file.",
    ),
]


@app.callback()
def app_callback() -> None:
    """Enterprise Data Science CLI."""


@app.command()
def train(config: ConfigOption) -> None:
    metrics = train_model(config)
    typer.echo(
        "Training complete. "
        f"Accuracy={metrics['accuracy']}, F1={metrics['f1']}, "
        f"Metrics={metrics['metrics_path']}"
    )


def main() -> None:
    app()
