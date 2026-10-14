"""Entrena y registra un Pipeline de scikit-learn con MLflow.

Ejecutar desde la raiz del repositorio:
    python src/train_pipeline.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = ROOT / "mlflow.db"


def make_data(seed: int = 42):
    """Genera datos sinteticos estratificados e introduce faltantes controlados.

    Frente a una generacion ingenua, explicita separacion entre clases, ruido,
    pesos y semilla. Los faltantes prueban tambien el preprocesamiento del Pipeline.
    """
    X, y = make_classification(
        n_samples=1_200,
        n_features=12,
        n_informative=8,
        n_redundant=2,
        n_classes=2,
        weights=[0.55, 0.45],
        class_sep=1.2,
        flip_y=0.03,
        random_state=seed,
    )
    columns = [f"feature_{i}" for i in range(X.shape[1])]
    features = pd.DataFrame(X, columns=columns)
    # Faltantes reproducibles: el imputador evita que el entrenamiento falle.
    features.loc[features.sample(frac=0.02, random_state=seed).index, "feature_0"] = float("nan")
    return train_test_split(features, y, test_size=0.25, stratify=y, random_state=seed)


def main() -> None:
    # MLflow 3 desaconseja el backend de archivos. SQLite mantiene el tracking
    # local, pero permite usar las caracteristicas actuales de MLflow.
    mlflow.set_tracking_uri(f"sqlite:///{DATABASE_PATH.as_posix()}")
    mlflow.set_experiment("taller-3-mlflow-pipeline")
    X_train, X_test, y_train, y_test = make_data()

    params = {"C": 1.0, "max_iter": 1_000, "solver": "lbfgs", "random_state": 42}
    pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(**params)),
        ]
    )

    with mlflow.start_run(run_name="logistic-regression-pipeline"):
        mlflow.log_params({f"classifier_{key}": value for key, value in params.items()})
        mlflow.log_params({"test_size": 0.25, "n_samples": 1_200, "pipeline": "imputer-scaler-logreg"})
        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)
        metrics = {
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(y_test, predictions),
            "recall": recall_score(y_test, predictions),
            "f1": f1_score(y_test, predictions),
        }
        mlflow.log_metrics(metrics)

        figure, axis = plt.subplots(figsize=(5, 4))
        ConfusionMatrixDisplay.from_predictions(y_test, predictions, ax=axis, colorbar=False)
        axis.set_title("Matriz de confusion - conjunto de prueba")
        figure.tight_layout()
        chart_path = ROOT / "confusion_matrix.png"
        figure.savefig(chart_path, dpi=150)
        plt.close(figure)
        mlflow.log_artifact(str(chart_path), artifact_path="figures")
        chart_path.unlink(missing_ok=True)

        model_info = mlflow.sklearn.log_model(
            sk_model=pipeline,
            name="pipeline_logistic_regression",
            input_example=X_train.head(3),
            serialization_format="cloudpickle",
        )
        mlflow.set_tags({"course": "Machine Learning Engineering", "exercise": "Taller 3"})
        print("Metricas registradas:", {key: round(value, 4) for key, value in metrics.items()})
        print("URI del modelo:", model_info.model_uri)
        print("Para abrir la interfaz: mlflow ui --backend-store-uri sqlite:///mlflow.db")


if __name__ == "__main__":
    main()
