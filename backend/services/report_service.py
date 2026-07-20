"""
report_service.py

Handles generation of professional PDF reports summarizing CodeSage AI
code analysis results (Pylint, Bandit, Radon) using ReportLab.
"""

import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    HRFlowable,
)

# Directory where generated reports are stored.
# This resolves to backend/reports/ regardless of the current working directory.
REPORTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports"
)


class ReportGenerationError(Exception):
    """Raised when PDF report generation fails."""
    pass


def _build_styles():
    """Build and return a dict of paragraph styles used in the report."""
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CodeSageTitle",
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1A237E"),
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CodeSageSubtitle",
            fontName="Helvetica",
            fontSize=13,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#424242"),
            spaceAfter=20,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.white,
            backColor=colors.HexColor("#1A237E"),
            spaceBefore=14,
            spaceAfter=10,
            leftIndent=6,
            borderPadding=(6, 6, 6, 6),
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubHeading",
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#1A237E"),
            spaceBefore=8,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyLabel",
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#212121"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyValue",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#212121"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="MonoBlock",
            fontName="Courier",
            fontSize=8,
            leading=10.5,
            textColor=colors.HexColor("#212121"),
            backColor=colors.HexColor("#F5F5F5"),
            borderColor=colors.HexColor("#E0E0E0"),
            borderWidth=0.5,
            borderPadding=(8, 8, 8, 8),
            alignment=TA_LEFT,
        )
    )

    return styles


def _escape(text):
    """Escape text for safe use inside ReportLab Paragraph/XML markup."""
    if text is None:
        return "N/A"
    text = str(text)
    text = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return text


def _mono_paragraph(text, style):
    """
    Convert raw tool output (e.g. Pylint/Bandit/Radon text) into one or more
    Paragraph flowables, preserving line breaks and escaping special chars.
    """
    if text is None or str(text).strip() == "":
        text = "No output produced."

    escaped = _escape(text)
    # Preserve line breaks inside the monospace block.
    escaped = escaped.replace("\n", "<br/>")
    return Paragraph(escaped, style)


def _summary_table(summary, styles):
    """Build a two-column key/value table for the analysis summary."""
    summary = summary or {}

    rows_data = [
        ("Quality Score", summary.get("quality_score")),
        ("Security Issues", summary.get("security_issues")),
        ("Complexity", summary.get("complexity")),
        ("Functions Analysed", summary.get("functions_analyzed")),
        ("Average Complexity", summary.get("average_complexity")),
    ]

    table_rows = []
    for label, value in rows_data:
        table_rows.append(
            [
                Paragraph(_escape(label), styles["BodyLabel"]),
                Paragraph(_escape(value), styles["BodyValue"]),
            ]
        )

    table = Table(table_rows, colWidths=[5.5 * cm, 10.5 * cm])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#E0E0E0")),
                ("LEFTPADDING", (0, 0), (0, -1), 4),
            ]
        )
    )
    return table


def _file_info_table(filename, generated_at, styles):
    """Build a two-column key/value table for file metadata."""
    rows_data = [
        ("File Name", filename),
        ("Generated Date & Time", generated_at),
    ]

    table_rows = []
    for label, value in rows_data:
        table_rows.append(
            [
                Paragraph(_escape(label), styles["BodyLabel"]),
                Paragraph(_escape(value), styles["BodyValue"]),
            ]
        )

    table = Table(table_rows, colWidths=[5.5 * cm, 10.5 * cm])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#E0E0E0")),
                ("LEFTPADDING", (0, 0), (0, -1), 4),
            ]
        )
    )
    return table


def generate_pdf_report(filename, analysis):
    """
    Generate a professional PDF report for the given analyzed file.

    Args:
        filename (str): Name of the originally uploaded file (e.g. "hello.py").
        analysis (dict): Analysis payload containing "summary", "pylint",
                          "bandit" and "radon" keys.

    Returns:
        str: Relative path to the generated PDF (e.g. "reports/hello_report.pdf").

    Raises:
        ReportGenerationError: If report generation fails for any reason.
    """
    if not filename or not isinstance(filename, str):
        raise ReportGenerationError("A valid 'filename' is required to generate a report.")

    if not isinstance(analysis, dict):
        raise ReportGenerationError("'analysis' must be a dictionary containing analysis results.")

    try:
        os.makedirs(REPORTS_DIR, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(filename))[0]
        report_filename = f"{base_name}_report.pdf"
        absolute_report_path = os.path.join(REPORTS_DIR, report_filename)

        summary = analysis.get("summary", {})
        pylint_output = analysis.get("pylint", "")
        bandit_output = analysis.get("bandit", "")
        radon_output = analysis.get("radon", "")

        styles = _build_styles()

        doc = SimpleDocTemplate(
            absolute_report_path,
            pagesize=A4,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
            leftMargin=2 * cm,
            rightMargin=2 * cm,
            title=f"CodeSage AI Report - {filename}",
        )

        elements = []

        # ---------- Header ----------
        elements.append(Paragraph("CodeSage AI", styles["CodeSageTitle"]))
        elements.append(Paragraph("AI Code Review Report", styles["CodeSageSubtitle"]))
        elements.append(
            HRFlowable(
                width="100%",
                thickness=1,
                color=colors.HexColor("#1A237E"),
                spaceAfter=16,
            )
        )

        # ---------- File Information ----------
        elements.append(Paragraph("File Information", styles["SectionHeading"]))
        generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elements.append(_file_info_table(filename, generated_at, styles))
        elements.append(Spacer(1, 12))

        # ---------- Summary ----------
        elements.append(Paragraph("Summary", styles["SectionHeading"]))
        elements.append(_summary_table(summary, styles))
        elements.append(Spacer(1, 12))

        # ---------- Pylint Section ----------
        elements.append(PageBreak())
        elements.append(Paragraph("Pylint Analysis", styles["SectionHeading"]))
        elements.append(_mono_paragraph(pylint_output, styles["MonoBlock"]))
        elements.append(Spacer(1, 12))

        # ---------- Bandit Section ----------
        elements.append(PageBreak())
        elements.append(Paragraph("Bandit Security Analysis", styles["SectionHeading"]))
        elements.append(_mono_paragraph(bandit_output, styles["MonoBlock"]))
        elements.append(Spacer(1, 12))

        # ---------- Radon Section ----------
        elements.append(PageBreak())
        elements.append(Paragraph("Radon Complexity Analysis", styles["SectionHeading"]))
        elements.append(_mono_paragraph(radon_output, styles["MonoBlock"]))

        doc.build(elements)

        # Return a path relative to the backend/ directory, as required by the API contract.
        relative_report_path = os.path.join("reports", report_filename)
        return relative_report_path

    except ReportGenerationError:
        raise
    except Exception as exc:
        raise ReportGenerationError(f"Failed to generate PDF report: {exc}") from exc