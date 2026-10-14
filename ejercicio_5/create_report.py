"""Genera el informe PDF del Ejercicio 5."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output" / "pdf" / "entrega_ejercicio_5.pdf"
GITHUB_URL = "https://github.com/JoaquinCampos22155/MLFlow_/tree/ejercicio_5"
NOTEBOOK_PATH = "ejercicio_5/notebooks/ejercicio_5_mlflow.ipynb"


def p(text, style):
    return Paragraph(text, style)


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER, textColor=colors.HexColor("#17365D")))
    styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], textColor=colors.HexColor("#17365D"), spaceBefore=12))
    styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], leading=15, spaceAfter=7))
    story = [
        p("Ejercicio 5 - Pipeline de scikit-learn con MLflow", styles["TitleCenter"]),
        Spacer(1, 0.18 * inch),
        p("<b>Objetivo.</b> Adaptar un pipeline de scikit-learn para aprovechar las funcionalidades de <b>MLflow Experiments</b> y <b>MLflow Models</b>, tanto desde un notebook de Jupyter como desde un archivo Python.", styles["Body"]),
        p("Funcionalidades utilizadas", styles["Section"]),
        p("<b>Experiments:</b> cada ejecucion queda registrada con los hiperparametros, las metricas y etiquetas del ejercicio. <b>Models:</b> se registra el Pipeline completo, que contiene el escalado y el clasificador, para poder reproducir inferencias con el mismo preprocesamiento.", styles["Body"]),
        p("Implementacion", styles["Section"]),
        p("Se utiliza el conjunto Wine de scikit-learn. El flujo divide los datos estratificadamente, aplica <i>StandardScaler</i> y entrena un <i>RandomForestClassifier</i> con 150 arboles y profundidad maxima 5. MLflow registra accuracy, F1 ponderado, hiperparametros y el modelo versionado.", styles["Body"]),
        Table([
            ["Elemento", "Ubicacion"],
            ["Notebook Jupyter", NOTEBOOK_PATH],
            ["Archivo Python", "ejercicio_5/src/pipeline_mlflow.py"],
            ["Experimento MLflow", "ejercicio-5-sklearn-mlflow"],
            ["Metricas verificadas", "accuracy = 1.0000; f1_weighted = 1.0000"],
        ], colWidths=[1.65 * inch, 4.85 * inch], style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B7C9D6")),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F3F7FA")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ])),
        p("Enlaces solicitados", styles["Section"]),
        p(f"<b>Repositorio GitHub (rama ejercicio_5):</b> <link href=\"{GITHUB_URL}\" color=\"blue\">{GITHUB_URL}</link>", styles["Body"]),
        p("<b>Notebook en Databricks:</b> Pendiente de importar el notebook al workspace personal de Databricks. Tras importarlo, se debe pegar aqui la URL que genera el workspace antes de entregar el PDF.", styles["Body"]),
        p("Ejecucion", styles["Section"]),
        p("En la raiz del repositorio: <font name=\"Courier\">python ejercicio_5/src/pipeline_mlflow.py</font>. Para la interfaz: <font name=\"Courier\">mlflow ui --backend-store-uri sqlite:///ejercicio_5/mlflow_ejercicio_5.db</font>.", styles["Body"]),
        p("Conclusion", styles["Section"]),
        p("La integracion permite comparar ejecuciones sin depender de anotaciones manuales y preservar el pipeline completo como modelo. En proyectos reales esto facilita reproducibilidad, auditoria y despliegue, porque el preprocesamiento queda asociado al clasificador entrenado.", styles["Body"]),
    ]
    SimpleDocTemplate(str(OUTPUT), pagesize=letter, rightMargin=0.65 * inch, leftMargin=0.65 * inch, topMargin=0.6 * inch, bottomMargin=0.6 * inch).build(story)


if __name__ == "__main__":
    main()
