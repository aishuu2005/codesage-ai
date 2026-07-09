import os

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from config import Config
from services.analyzer import run_pylint

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"py", "zip"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@upload_bp.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return jsonify({
            "error": "No file uploaded."
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

    filepath = os.path.join(
        Config.UPLOAD_FOLDER,
        filename
    )

    file.save(filepath)

    analysis_result = ""

    if filename.endswith(".py"):
        analysis_result = run_pylint(filepath)

    return jsonify({
        "message": "File uploaded successfully.",
        "filename": filename,
        "pylint_report": analysis_result
    }), 200