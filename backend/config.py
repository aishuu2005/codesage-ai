import os


class Config:
    """
    Central application configuration.

    NOTE: UPLOAD_FOLDER and REPORT_FOLDER are resolved to ABSOLUTE paths
    anchored to this file's directory (the project root), instead of
    plain relative strings. A relative path like "uploads" depends on
    the current working directory the process happens to be started
    from (python app.py vs. flask run vs. gunicorn from a different
    cwd) and can silently point at the wrong location. Anchoring it to
    BASE_DIR makes the app's file locations deterministic regardless of
    how/where it's launched.
    """

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = "codesage-secret-key"

    JWT_SECRET_KEY = "codesage-jwt-secret"

    SQLALCHEMY_DATABASE_URI = "sqlite:///codesage.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024