"""Genera el informe PDF del Ejercicio 5."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output" / "pdf" / "entrega_ejercicio_5.pdf"
GITHUB_URL = "https://github.com/JoaquinCampos22155/MLFlow_/tree/ejercicio_5"


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
        p("Funcionalidades utilizadas", styles["Section"]),
        p("<b>Experiments:</b> cada ejecucion queda registrada con los hiperparametros, las metricas y etiquetas del ejercicio. <b>Models:</b> se registra el Pipeline completo, que contiene el escalado y el clasificador, para poder reproducir inferencias con el mismo preprocesamiento.", styles["Body"]),
        p("Enlaces", styles["Section"]),
        p(f"<b>Repositorio GitHub (rama ejercicio_5):</b> <link href=\"{GITHUB_URL}\" color=\"blue\">{GITHUB_URL}</link>", styles["Body"]),
        p("<b>Notebook en Databricks:</b> Pendiente de importar el notebook al workspace personal de Databricks. Tras importarlo, se debe pegar aqui la URL que genera el workspace antes de entregar el PDF.", styles["Body"]),
        p("Conclusion", styles["Section"]),
        p("La integracion permite comparar ejecuciones sin depender de anotaciones manuales y preservar el pipeline completo como modelo. En proyectos reales esto facilita reproducibilidad, auditoria y despliegue, porque el preprocesamiento queda asociado al clasificador entrenado.", styles["Body"]),
    ]
    SimpleDocTemplate(str(OUTPUT), pagesize=letter, rightMargin=0.65 * inch, leftMargin=0.65 * inch, topMargin=0.6 * inch, bottomMargin=0.6 * inch).build(story)


if __name__ == "__main__":
    main()
