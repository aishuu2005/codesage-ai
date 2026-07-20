import os

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from config import Config
from services.analyzer import analyze_file

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"py", "zip"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@upload_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():

    try:

        if "file" not in request.files:
            return jsonify({
                "error": "No file part in the request."
            }), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({
                "error": "No file selected."
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                "error": "Only .py and .zip files are allowed."
            }), 400

        filename = secure_filename(file.filename)

        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)

        file.save(filepath)

        analysis_result = None

        if filename.endswith(".py"):
            # analyze_file() is guaranteed not to raise (each analysis
            # step catches and reports its own errors), but we keep this
            # try/except as defense in depth: a bug here must never take
            # down an otherwise-successful upload.
            try:
                analysis_result = analyze_file(filepath)
            except Exception:
                current_app.logger.exception(
                    "analyze_file() raised unexpectedly for %s", filepath
                )
                analysis_result = {
                    "summary": {
                        "quality_score": "N/A",
                        "security_issues": "N/A",
                        "complexity": "N/A",
                    },
                    "pylint": "ERROR: Analysis failed unexpectedly.",
                    "bandit": "ERROR: Analysis failed unexpectedly.",
                    "radon": "ERROR: Analysis failed unexpectedly.",
                }

        return jsonify({
            "message": "File uploaded successfully.",
            "filename": filename,
            "analysis": analysis_result
        }), 200

    except Exception as e:
        current_app.logger.exception("Unexpected error handling /upload")

        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 500