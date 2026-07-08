import os

class Config:
    SECRET_KEY = "codesage-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///codesage.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "uploads"
    REPORT_FOLDER = "reports"

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024