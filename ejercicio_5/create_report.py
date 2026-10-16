"""Generate the Exercise 5 report PDF."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output" / "pdf" / "entrega_ejercicio_5.pdf"
EVIDENCE_IMAGE = ROOT / "evidence" / "mlflow_run_databricks.png"

GITHUB_URL = "https://github.com/JoaquinCampos22155/MLFlow_/tree/ejercicio_5"
DATABRICKS_NOTEBOOK_URL = (
    "https://dbc-72f37f9d-4aae.cloud.databricks.com/editor/notebooks/"
    "4362101708384986?o=7474651907383552#command/6540561542913743"
)

SOURCES = [
    (
        "MLflow en Databricks",
        "https://docs.databricks.com/aws/en/mlflow/",
    ),
    (
        "Tracking y experimentos",
        "https://docs.databricks.com/aws/en/mlflow/tracking",
    ),
    (
        "Databricks Feature Store",
        "https://docs.databricks.com/aws/en/machine-learning/feature-store",
    ),
    (
        "Model Registry en Unity Catalog",
        "https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/",
    ),
    (
        "Monitoreo de Model Serving",
        "https://docs.databricks.com/aws/en/machine-learning/model-serving/monitor-diagnose-endpoints",
    ),
    (
        "Fases CRISP-DM (IBM)",
        "https://www.ibm.com/docs/en/SS3RA7_18.5.0/pdf/ModelerCRISPDM.pdf",
    ),
    (
        "API de MLflow para scikit-learn",
        "https://mlflow.org/docs/latest/api_reference/python_api/mlflow.sklearn.html",
    ),
]

NAVY = colors.HexColor("#17365D")
TEAL = colors.HexColor("#087E8B")
PALE_BLUE = colors.HexColor("#EEF4F8")
PALE_TEAL = colors.HexColor("#E8F4F3")
TEXT = colors.HexColor("#263238")
MUTED = colors.HexColor("#52636B")
GRID = colors.HexColor("#D4DFE5")


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=26,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=7,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Subtitle",
            parent=styles["BodyText"],
            fontSize=10,
            leading=14,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=14,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=NAVY,
            spaceBefore=9,
            spaceAfter=6,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubsectionTitle",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=TEAL,
            spaceBefore=5,
            spaceAfter=4,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportBody",
            parent=styles["BodyText"],
            fontSize=9.2,
            leading=13,
            textColor=TEXT,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallBody",
            parent=styles["BodyText"],
            fontSize=8,
            leading=10.5,
            textColor=TEXT,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableHeaderText",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.2,
            leading=10,
            textColor=colors.white,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableCellText",
            parent=styles["BodyText"],
            fontSize=8,
            leading=10.2,
            textColor=TEXT,
            spaceAfter=0,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableCellSmall",
            parent=styles["BodyText"],
            fontSize=7.7,
            leading=9.6,
            textColor=TEXT,
            spaceAfter=0,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Callout",
            parent=styles["BodyText"],
            fontSize=9,
            leading=12,
            textColor=NAVY,
            backColor=PALE_TEAL,
            borderColor=TEAL,
            borderWidth=0.6,
            borderPadding=8,
            spaceBefore=5,
            spaceAfter=8,
        )
    )
    return styles


def paragraph(text, style):
    return Paragraph(text, style)


def make_table(rows, widths, header=True, small=False):
    table = Table(rows, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.45, GRID),
    ]
    if header:
        commands.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ]
        )
    start = 1 if header else 0
    for row in range(start, len(rows)):
        if (row - start) % 2 == 1:
            commands.append(("BACKGROUND", (0, row), (-1, row), PALE_BLUE))
    table.setStyle(TableStyle(commands))
    return table


def on_page(canvas, doc):
    canvas.saveState()
    width, height = letter
    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(0.6)
    canvas.line(doc.leftMargin, 0.48 * inch, width - doc.rightMargin, 0.48 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 0.31 * inch, "Ejercicio 5 | MLflow en Databricks")
    canvas.drawRightString(width - doc.rightMargin, 0.31 * inch, f"Página {doc.page}")
    canvas.restoreState()


def linked_text(label, url, styles):
    return paragraph(f'<link href="{url}" color="#087E8B">{label}</link>', styles["SmallBody"])


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        rightMargin=0.62 * inch,
        leftMargin=0.62 * inch,
        topMargin=0.58 * inch,
        bottomMargin=0.68 * inch,
        title="Ejercicio 5 - MLflow en Databricks",
        author="",
        subject="Investigacion y pipeline scikit-learn con MLflow",
    )
    body_width = doc.width
    story = []

    # Page 1: research and practical uses.
    story.extend(
        [
            Spacer(1, 0.08 * inch),
            paragraph("MLflow en Databricks", styles["ReportTitle"]),
            paragraph(
                "Ejercicio 5 | Pipeline de scikit-learn con seguimiento reproducible",
                styles["Subtitle"],
            ),
            paragraph("Objetivo", styles["SectionTitle"]),
            paragraph(
                "MLflow conecta el desarrollo de modelos con su seguimiento y operación. "
                "En Databricks, los runs se registran en un tracking server administrado por el workspace. "
                "Este ejercicio adapta un clasificador de Wine con un pipeline de scikit-learn y usa "
                "Experiments y MLflow Models.",
                styles["ReportBody"],
            ),
            paragraph("Usos en proyectos de Machine Learning", styles["SectionTitle"]),
        ]
    )
    use_rows = [
        [paragraph("Necesidad", styles["TableHeaderText"]), paragraph("Aporte de MLflow y Databricks", styles["TableHeaderText"])],
        [
            paragraph("Trazabilidad y comparación", styles["TableCellText"]),
            paragraph("Experiments agrupa runs y registra parámetros, métricas, etiquetas, código y artefactos para comparar alternativas.", styles["TableCellText"]),
        ],
        [
            paragraph("Reproducibilidad", styles["TableCellText"]),
            paragraph("MLflow Models empaqueta el modelo, la firma de entrada/salida y ejemplos para reutilizarlo con el mismo preprocesamiento.", styles["TableCellText"]),
        ],
        [
            paragraph("Features compartidas", styles["TableCellText"]),
            paragraph("Databricks Feature Store permite descubrir y gobernar features, mantener linaje y reutilizar cálculos entre entrenamiento e inferencia. Requiere Unity Catalog en la experiencia actual.", styles["TableCellText"]),
        ],
        [
            paragraph("Versionado y despliegue", styles["TableCellText"]),
            paragraph("Model Registry en Unity Catalog centraliza permisos, versiones y linaje; Model Serving publica modelos como endpoints.", styles["TableCellText"]),
        ],
        [
            paragraph("Operación", styles["TableCellText"]),
            paragraph("Las herramientas de serving ayudan a observar salud, latencia y solicitudes/respuestas para depurar y monitorear modelos desplegados.", styles["TableCellText"]),
        ],
    ]
    story.append(make_table(use_rows, [1.55 * inch, body_width - 1.55 * inch]))
    story.extend(
        [
            paragraph("Funcionalidades usadas en esta entrega", styles["SectionTitle"]),
            paragraph(
                "<b>Experiments:</b> cada ejecución registra hiperparámetros, accuracy, F1 ponderado y etiquetas. "
                "<b>MLflow Models:</b> se guarda el pipeline completo (StandardScaler y RandomForestClassifier) "
                "con una firma y un ejemplo de entrada. Variar los hiperparámetros y volver a ejecutar crea "
                "runs que se pueden comparar.",
                styles["ReportBody"],
            ),
            paragraph(
                "Alcance de la demo: registra un MLflow Model asociado al run; no crea una versión en Model Registry "
                "ni una tabla de Feature Store. Esas funciones se describen como capacidades de la plataforma, "
                "pero no se activan porque necesitan catálogo, recursos y permisos del workspace.",
                styles["Callout"],
            ),
            PageBreak(),
        ]
    )

    # Page 2: CRISP-DM mapping and concrete pipeline.
    story.extend(
        [
            paragraph("Relación con CRISP-DM", styles["ReportTitle"]),
            paragraph(
                "CRISP-DM tiene seis fases. MLflow apoya varias con trazabilidad, modelos y servicios de Databricks, "
                "pero no reemplaza la comprensión del negocio ni el criterio del equipo.",
                styles["ReportBody"],
            ),
        ]
    )
    crisp_rows = [
        [
            paragraph("Fase", styles["TableHeaderText"]),
            paragraph("Cómo puede apoyar MLflow/Databricks", styles["TableHeaderText"]),
            paragraph("En este ejercicio", styles["TableHeaderText"]),
        ],
        [
            paragraph("Comprensión del negocio", styles["TableCellSmall"]),
            paragraph("Puede guardar objetivos, etiquetas y resultados como metadatos; no define por sí solo el problema ni los criterios de negocio.", styles["TableCellSmall"]),
            paragraph("No cubierta por el código.", styles["TableCellSmall"]),
        ],
        [
            paragraph("Comprensión de datos", styles["TableCellSmall"]),
            paragraph("Puede registrar datasets, código y artefactos para conservar contexto; el análisis exploratorio sigue siendo tarea del equipo.", styles["TableCellSmall"]),
            paragraph("Usa Wine incluido en scikit-learn; no hace EDA.", styles["TableCellSmall"]),
        ],
        [
            paragraph("Preparación de datos", styles["TableCellSmall"]),
            paragraph("Pipelines mantienen el preprocesamiento junto al modelo. Feature Store ayuda a compartir features y reducir diferencias entre entrenamiento e inferencia.", styles["TableCellSmall"]),
            paragraph("StandardScaler está dentro del pipeline; no usa Feature Store.", styles["TableCellSmall"]),
        ],
        [
            paragraph("Modelado", styles["TableCellSmall"]),
            paragraph("Experiments registra parámetros y runs; MLflow Models empaqueta modelos de scikit-learn y otros frameworks.", styles["TableCellSmall"]),
            paragraph("Cubierta: Random Forest y modelo registrado en el run.", styles["TableCellSmall"]),
        ],
        [
            paragraph("Evaluación", styles["TableCellSmall"]),
            paragraph("Métricas de cada run permiten comparar resultados y elegir una alternativa con evidencia.", styles["TableCellSmall"]),
            paragraph("Cubierta: accuracy y F1 ponderado. La comparación mejora al ejecutar varias configuraciones.", styles["TableCellSmall"]),
        ],
        [
            paragraph("Despliegue", styles["TableCellSmall"]),
            paragraph("Model Registry gestiona versiones y permisos; Model Serving publica endpoints. Databricks ofrece herramientas de monitoreo para endpoints.", styles["TableCellSmall"]),
            paragraph("No desplegado: el modelo solo se registra en el run.", styles["TableCellSmall"]),
        ],
    ]
    story.append(make_table(crisp_rows, [1.35 * inch, 3.05 * inch, body_width - 4.4 * inch]))
    story.extend(
        [
            paragraph("Pipeline implementado", styles["SectionTitle"]),
            paragraph(
                "Dataset Wine integrado en scikit-learn; partición 75/25 con estratificación y semilla 42; "
                "StandardScaler seguido de RandomForestClassifier (150 árboles, profundidad máxima 5); "
                "métricas accuracy y F1 ponderado. El mismo flujo existe en notebook y en archivo Python.",
                styles["ReportBody"],
            ),
            paragraph(
                "El notebook usa el experimento asociado a Databricks. El archivo Python usa tracking administrado "
                "cuando se ejecuta en Databricks Runtime; en una computadora local mantiene SQLite.",
                styles["Callout"],
            ),
            PageBreak(),
        ]
    )

    # Page 3: upload steps and deliverable links.
    story.extend(
        [
            paragraph("Ejecución y entregables", styles["ReportTitle"]),
            paragraph("Pasos para ejecutar en Databricks", styles["SectionTitle"]),
            paragraph(
                "1. Importa el archivo IPYNB en una carpeta de tu workspace (Workspace > Import).<br/>"
                "2. Adjunta el notebook a un Databricks Runtime ML compatible con MLflow 3 o superior.<br/>"
                "3. Ejecuta Run all. El dataset viene incluido y no requiere almacenamiento, tokens ni archivos externos.<br/>"
                "4. Revisa los runs y el modelo desde Experiments.",
                styles["ReportBody"],
            ),
            paragraph("Enlaces", styles["SectionTitle"]),
            linked_text("Repositorio GitHub - rama ejercicio_5", GITHUB_URL, styles),
            Spacer(1, 3),
            linked_text("Notebook ejecutado en el workspace de Databricks", DATABRICKS_NOTEBOOK_URL, styles),
            Spacer(1, 8),
            paragraph(
                "El notebook se ejecutó en Databricks y registró un run de MLflow. La captura de evidencia de la página siguiente muestra el run y las métricas.",
                styles["ReportBody"],
            ),
            paragraph("Referencias", styles["SectionTitle"]),
        ]
    )
    for label, url in SOURCES:
        story.append(linked_text(label, url, styles))

    story.extend(
        [
            PageBreak(),
            paragraph("Evidencia de ejecución en Databricks", styles["ReportTitle"]),
            paragraph(
                "La ejecución registró un run en Experiments con accuracy de 1.0 y F1 ponderado de 1.0. La tabla también muestra los parámetros del Random Forest.",
                styles["ReportBody"],
            ),
        ]
    )
    evidence = Image(
        str(EVIDENCE_IMAGE),
        width=body_width,
        height=body_width * (347 / 1365),
    )
    evidence.hAlign = "CENTER"
    story.append(evidence)

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)


if __name__ == "__main__":
    main()
