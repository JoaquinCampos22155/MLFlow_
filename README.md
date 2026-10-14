# Taller 3 - MLflow y scikit-learn

Repositorio de la solucion para el Taller 3 de Machine Learning Engineering. Incluye un experimento reproducible con datos sinteticos, un `Pipeline` de scikit-learn y seguimiento local con MLflow.

## 1. Tres paginas de la documentacion de MLflow

1. [MLflow Tracking Quickstart](https://mlflow.org/docs/latest/ml/getting-started/quickstart/). Es una introduccion concreta al ciclo completo: registrar parametros y metricas, guardar un modelo y recuperarlo para inferencia. Es especialmente util para pasar de scripts aislados a experimentos trazables.
2. [MLflow Tracking](https://mlflow.org/docs/latest/tracking/). Esta pagina explica el concepto de *run* y la separacion entre parametros, metricas y artefactos. La elegi porque aclara que MLflow no es solo una interfaz grafica: es un registro reproducible de cada ejecucion.
3. [Integracion de MLflow con scikit-learn](https://mlflow.org/docs/latest/ml/traditional-ml/sklearn). Describe `mlflow.sklearn.autolog()`, el registro de modelos y su uso con busqueda de hiperparametros. La elegi por ser la integracion mas cercana a un flujo tradicional de aprendizaje supervisado.


## Ejecucion

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/train_pipeline.py
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

Para abrir el notebook desde Jupyter local, instale adicionalmente `pip install -r requirements-notebook.txt`.

Abra `http://127.0.0.1:5000` y entre al experimento `taller-3-mlflow-pipeline`. Tome una captura de la tabla de ejecuciones y otra de la pagina del run, donde aparecen parametros, metricas y artefactos. El archivo local `mlflow.db` guarda los metadatos del experimento; los artefactos se almacenan localmente por MLflow. Las evidencias generadas durante la entrega se guardan en `evidence/`.

Tambien puede ejecutar el notebook [notebooks/taller_3_mlflow.ipynb](notebooks/taller_3_mlflow.ipynb) celda por celda.

## 4. Conclusiones

MLflow aporta orden y comparabilidad cuando un proyecto empieza a tener varios experimentos. En un proyecto personal serviria para elegir un modelo sin depender de notas manuales; en un equipo, para conservar los parametros, metricas, artefactos y modelo exacto que produjo un resultado. El uso conjunto con `Pipeline` es importante: conserva el preprocesamiento junto al estimador y reduce el riesgo de que inferencia y entrenamiento usen transformaciones distintas. Para produccion, el siguiente paso razonable seria centralizar el tracking en un servidor compartido y definir criterios de promocion de modelos basados en metricas.
