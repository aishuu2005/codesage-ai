import os

class Config:
    SECRET_KEY = "codesage-secret-key"

    UPLOAD_FOLDER = "uploads"

    REPORT_FOLDER = "reports"

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB