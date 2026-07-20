"""
routes/report.py

Exposes the /report endpoint which generates a PDF analysis report
for a previously analyzed file.
"""

print("✅ report.py imported")

from flask import Blueprint, request, jsonify

from services.report_service import (
    generate_pdf_report,
    ReportGenerationError,
)

report_bp = Blueprint("report", __name__)


@report_bp.route("/report", methods=["POST"])
def create_report():
    """
    POST /report

    Request body:
    {
        "filename": "hello.py",
        "analysis": { ... }
    }

    Response:
    {
        "message": "PDF generated successfully",
        "report_path": "reports/hello_report.pdf"
    }
    """

    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "Request body must be valid JSON."
            }), 400

        filename = data.get("filename")
        analysis = data.get("analysis")

        if not filename:
            return jsonify({
                "error": "'filename' is required."
            }), 400

        if not analysis or not isinstance(analysis, dict):
            return jsonify({
                "error": "'analysis' is required and must be an object."
            }), 400

        report_path = generate_pdf_report(filename, analysis)

        return jsonify({
            "message": "PDF generated successfully",
            "report_path": report_path
        }), 200

    except ReportGenerationError as e:
        return jsonify({
            "error": str(e)
        }), 500

    except Exception as e:
        return jsonify({
            "error": f"Unexpected error while generating report: {e}"
        }), 500