# Ejercicio 5 - scikit-learn con MLflow y Databricks

La entrega entrena un clasificador multiclase con el dataset Wine incluido en scikit-learn. El pipeline agrupa el escalado y el `RandomForestClassifier`, y registra cada ejecución con MLflow.

## Funcionalidades de MLflow usadas

- **Experiments y Tracking:** registra hiperparámetros, métricas y etiquetas por ejecución para comparar intentos y mantener trazabilidad.
- **MLflow Models:** guarda el pipeline completo con ejemplo de entrada y firma de modelo, para cargarlo y predecir con el mismo preprocesamiento.

El ejemplo no registra el modelo en Unity Catalog Model Registry ni usa Feature Store. Esas funcionalidades se describen en el informe, pero requieren recursos y permisos del workspace.

## Ejecutar el notebook en Databricks

1. Descarga `notebooks/ejercicio_5_mlflow.ipynb` desde GitHub y luego impórtalo en una carpeta de tu workspace (Workspace > Import).
2. Adjunta el notebook a un **Databricks Runtime ML** compatible con MLflow 3 o superior.
3. Selecciona **Run all**. El dataset ya viene incluido en scikit-learn; no necesita archivos externos, tokens ni conexión a almacenamiento.
4. Revisa los parámetros, métricas y el modelo en **Experiments**. Databricks usa el tracking administrado y el experimento asociado al notebook.

El notebook ya se ejecutó en Databricks. [Abre el notebook en el workspace](https://dbc-72f37f9d-4aae.cloud.databricks.com/editor/notebooks/4362101708384986?o=7474651907383552#command/6540561542913743) para revisar el run y el modelo registrados.

## Ejecutar el archivo Python en Databricks

`src/pipeline_mlflow.py` incluye el encabezado de notebook source de Databricks. Puedes importarlo como notebook o usarlo como tarea Python. En Databricks el script usa el tracking administrado; si quieres seleccionar un experimento de workspace, configura `MLFLOW_EXPERIMENT_NAME` con una ruta donde tengas permiso de escritura, por ejemplo `/Users/tu-correo@dominio.com/ejercicio-5-sklearn-mlflow`.

## Ejecutar localmente

Desde la raíz del repositorio, instala las dependencias del proyecto y ejecuta:

```bash
python -m pip install -r requirements.txt
python ejercicio_5/src/pipeline_mlflow.py
mlflow ui --backend-store-uri sqlite:///ejercicio_5/mlflow_ejercicio_5.db
```

Abre `http://127.0.0.1:5000` y selecciona `ejercicio-5-sklearn-mlflow`. Fuera de Databricks, el script usa SQLite local; dentro de Databricks cambia al tracking administrado.

## Entregables

- [Notebook Jupyter listo para importar](https://github.com/JoaquinCampos22155/MLFlow_/blob/ejercicio_5/ejercicio_5/notebooks/ejercicio_5_mlflow.ipynb)
- [Codigo del pipeline en Python](https://github.com/JoaquinCampos22155/MLFlow_/blob/ejercicio_5/ejercicio_5/src/pipeline_mlflow.py)
- [Repositorio GitHub, rama ejercicio_5](https://github.com/JoaquinCampos22155/MLFlow_/tree/ejercicio_5)
- [Notebook ejecutado en Databricks](https://dbc-72f37f9d-4aae.cloud.databricks.com/editor/notebooks/4362101708384986?o=7474651907383552#command/6540561542913743)
- [Captura de evidencia del run](evidence/mlflow_run_databricks.png)
- `output/pdf/entrega_ejercicio_5.pdf`: informe de investigacion, enlace al workspace y captura de evidencia del run.
