import os

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from config import Config
from services.analyzer import analyze_file

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"py", "zip"}


def allowed_file(filename):
    """Check whether the uploaded file has an allowed extension."""

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@upload_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    """Upload a source-code file and run supported analyzers."""

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

    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    filepath = os.path.join(
        Config.UPLOAD_FOLDER,
        filename
    )

    file.save(filepath)

    analysis_result = None

    if filename.lower().endswith(".py"):
        analysis_result = analyze_file(filepath)

    return jsonify({
        "message": "File uploaded successfully.",
        "filename": filename,
        "analysis": analysis_result
    }), 200