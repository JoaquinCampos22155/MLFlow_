# Ejercicio 5 - Pipeline de scikit-learn con MLflow

Este directorio es independiente del Taller 3. Demuestra dos funcionalidades de MLflow:

- **Experiments:** registro reproducible de parametros y metricas en un experimento propio.
- **Models:** registro del `Pipeline` completo (escalado y `RandomForestClassifier`) como un modelo MLflow.

## Contenido

- `notebooks/ejercicio_5_mlflow.ipynb`: version para Jupyter y para importar a Databricks.
- `src/pipeline_mlflow.py`: version ejecutable desde Python.
- `output/pdf/entrega_ejercicio_5.pdf`: informe de entrega.

## Ejecucion local

Desde la raiz del repositorio:

```powershell
.\.venv\Scripts\Activate.ps1
python ejercicio_5\src\pipeline_mlflow.py
mlflow ui --backend-store-uri sqlite:///ejercicio_5/mlflow_ejercicio_5.db
```

Abra `http://127.0.0.1:5000` y seleccione el experimento `ejercicio-5-sklearn-mlflow`.

## Enlaces de entrega

- Repositorio y rama: https://github.com/JoaquinCampos22155/MLFlow_/tree/ejercicio_5
- Notebook de Databricks: **pendiente de importar el notebook a tu workspace y copiar su URL.**

### Publicar el notebook en Databricks

1. En Databricks, entre a **Workspace > Import**.
2. Seleccione `ejercicio_5/notebooks/ejercicio_5_mlflow.ipynb`.
3. Abra el notebook importado, ejecútelo y copie la URL del navegador.
4. Reemplace el marcador de Databricks en el PDF antes de entregarlo.
