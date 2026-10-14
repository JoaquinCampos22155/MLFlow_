"""Ejercicio 5: Pipeline de scikit-learn con MLflow Experiments y Models.

Ejecutar desde la raiz del repositorio:
    python ejercicio_5/src/pipeline_mlflow.py
"""

from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "mlflow_ejercicio_5.db"
EXPERIMENT_NAME = "ejercicio-5-sklearn-mlflow"


def load_data():
    """Carga Wine, una clasificacion multiclase incluida en scikit-learn."""
    wine = load_wine(as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(
        wine.data, wine.target, test_size=0.25, random_state=42, stratify=wine.target
    )
    return X_train, X_test, y_train, y_test


def main() -> None:
    # Experiments: backend SQLite local para comparar y conservar ejecuciones.
    mlflow.set_tracking_uri(f"sqlite:///{DATABASE.as_posix()}")
    mlflow.set_experiment(EXPERIMENT_NAME)
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

        # Models: registra el Pipeline completo (escalado + clasificador).
        model_info = mlflow.sklearn.log_model(
            sk_model=pipeline,
            name="wine_random_forest_pipeline",
            input_example=X_train.head(3),
            serialization_format="cloudpickle",
        )
        mlflow.set_tags({"exercise": "5", "framework": "scikit-learn"})
        print("Metricas:", {name: round(value, 4) for name, value in metrics.items()})
        print("Modelo registrado:", model_info.model_uri)
        print("UI: mlflow ui --backend-store-uri sqlite:///ejercicio_5/mlflow_ejercicio_5.db")


if __name__ == "__main__":
    main()
