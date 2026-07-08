from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from models import db
from models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    # Validate input
    if not data:
        return jsonify({
            "error": "Request body cannot be empty."
        }), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Check required fields
    if not username or not email or not password:
        return jsonify({
            "error": "Username, email and password are required."
        }), 400

    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "error": "Email already registered."
        }), 409

    # Hash password
    hashed_password = generate_password_hash(password)

    # Create user
    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    # Save to database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully!",
        "username": username,
        "email": email
    }), 201