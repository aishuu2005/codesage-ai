from flask import Flask
from config import Config

from models import db
from models.user import User

from routes.home import home_bp
from routes.auth import auth_bp

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)