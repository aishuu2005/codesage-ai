from flask import Flask
from flask_jwt_extended import JWTManager

from config import Config

from models import db
from models.user import User

from routes.home import home_bp
from routes.auth import auth_bp
from routes.upload import upload_bp

# Create Flask application
app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(upload_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)