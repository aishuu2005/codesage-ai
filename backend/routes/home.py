from flask import Blueprint
from datetime import datetime

# Create Blueprint
home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    return {
        "message": "Welcome to CodeSage AI",
        "status": "Backend is running successfully!"
    }


@home_bp.route("/health")
def health():
    return {
        "status": "Healthy",
        "application": "CodeSage AI",
        "version": "1.0.0",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }