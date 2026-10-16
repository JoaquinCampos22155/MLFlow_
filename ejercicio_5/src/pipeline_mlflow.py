# Databricks notebook source
"""scikit-learn pipeline tracked with MLflow Experiments and Models.

Run locally from the repository root with:
    python ejercicio_5/src/pipeline_mlflow.py

To use the script in Databricks, import this .py file as a notebook or run it
as a Python task on Databricks Runtime ML. Databricks-managed tracking is used
automatically. Set MLFLOW_EXPERIMENT_NAME to a writable workspace experiment
path when you want to select a specific experiment.
"""

from __future__ import annotations

import os
from pathlib import Path

import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

EXPERIMENT_NAME = "ejercicio-5-sklearn-mlflow"
LOCAL_DATABASE_NAME = "mlflow_ejercicio_5.db"


def configure_tracking() -> str:
    """Use Databricks-managed tracking on DBR and SQLite for local runs."""
    if os.environ.get("DATABRICKS_RUNTIME_VERSION"):
        experiment_name = os.environ.get("MLFLOW_EXPERIMENT_NAME")
        if experiment_name:
            mlflow.set_experiment(experiment_name)
            return f"Databricks workspace experiment: {experiment_name}"

        # Databricks manages the tracking URI and uses the active/default
        # experiment. This also works when the .py file is imported as a notebook.
        return "Databricks-managed MLflow tracking"

    if "__file__" in globals():
        database = Path(__file__).resolve().parents[1] / LOCAL_DATABASE_NAME
    else:
        database = Path.cwd() / LOCAL_DATABASE_NAME
    mlflow.set_tracking_uri(f"sqlite:///{database.as_posix()}")
    mlflow.set_experiment(EXPERIMENT_NAME)
    return f"MLflow local (SQLite): {database}"


def load_data():
    """Load the built-in Wine classification dataset and split it."""
    wine = load_wine(as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(
        wine.data,
        wine.target,
        test_size=0.25,
        random_state=42,
        stratify=wine.target,
    )
    return X_train, X_test, y_train, y_test


def main() -> None:
    if int(mlflow.__version__.split(".")[0]) < 3:
        raise RuntimeError(
            "This exercise requires MLflow 3 or newer. Use a compatible "
            "Databricks Runtime ML or install the versions in requirements.txt."
        )

    tracking_target = configure_tracking()
    X_train, X_test, y_train, y_test = load_data()

    params = {"n_estimators": 150, "max_depth": 5, "random_state": 42}
    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("classifier", RandomForestClassifier(**params)),
        ]
    )

    with mlflow.start_run(run_name="random-forest-wine-pipeline"):
        mlflow.log_params({f"rf_{name}": value for name, value in params.items()})
        mlflow.log_param("test_size", 0.25)
        pipeline.fit(X_train, y_train)

        predictions = pipeline.predict(X_test)
        metrics = {
            "accuracy": accuracy_score(y_test, predictions),
            "f1_weighted": f1_score(y_test, predictions, average="weighted"),
        }
        mlflow.log_metrics(metrics)
        mlflow.set_tags(
            {"exercise": "5", "framework": "scikit-learn", "dataset": "wine"}
        )

        signature = infer_signature(X_train, pipeline.predict(X_train))
        model_info = mlflow.sklearn.log_model(
            sk_model=pipeline,
            name="wine_random_forest_pipeline",
            signature=signature,
            input_example=X_train.head(5),
        )

    print("Tracking:", tracking_target)
    print("Métricas:", {name: round(value, 4) for name, value in metrics.items()})
    print("MLflow Model guardado en:", model_info.model_uri)
    if not os.environ.get("DATABRICKS_RUNTIME_VERSION"):
        print(
            "UI local: mlflow ui --backend-store-uri "
            f"sqlite:///{(Path(__file__).resolve().parents[1] / LOCAL_DATABASE_NAME).as_posix()}"
        )


if __name__ == "__main__":
    main()
