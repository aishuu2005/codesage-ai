from flask import Flask
from config import Config
from routes.home import home_bp

# Create Flask application
app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Register Blueprint
app.register_blueprint(home_bp)

if __name__ == "__main__":
    app.run(debug=True)