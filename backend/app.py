import os

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

    # ------------------------------------------------------------------
    # WHY use_reloader IS DISABLED BY DEFAULT
    # ------------------------------------------------------------------
    # Werkzeug's debug auto-reloader watches files for changes so it can
    # restart the app on edits. When the "watchdog" package is installed
    # (it is, in this project's environment), Werkzeug switches from its
    # basic "stat" reloader (which only polls imported .py modules) to a
    # filesystem-event based reloader that watches the ENTIRE project
    # directory tree - including data directories like Config.UPLOAD_FOLDER.
    #
    # /upload saves the uploaded .py file inside that watched tree and then
    # runs Pylint + Bandit + Radon, which takes a noticeable amount of
    # wall-clock time. The reloader's filesystem watcher notices the new
    # file almost immediately and restarts the whole server process WHILE
    # the request is still being handled. The in-flight request's socket
    # is torn down mid-response, which is exactly what produces:
    #
    #     curl: (56) Recv failure: Connection was reset
    #
    # ...while the server (the new, restarted process) appears to still be
    # running normally right afterwards, and routes like OPTIONS /upload
    # still resolve, because it's a fresh instance of the same app.
    #
    # This is why the bug only appeared after the analyzer was made to do
    # real work (multiple subprocess calls): the earlier lightweight
    # version finished before the reloader's watcher fired.
    #
    # Fix: keep debug=True (so you still get the interactive debugger and
    # verbose tracebacks) but turn the reloader OFF by default. You can
    # opt back in with FLASK_USE_RELOADER=true, but only do so once
    # UPLOAD_FOLDER/REPORT_FOLDER are moved outside the watched project
    # tree (e.g. a system temp directory or a path outside the repo) -
    # otherwise this bug will resurface.
    # ------------------------------------------------------------------
    use_reloader = os.environ.get("FLASK_USE_RELOADER", "false").lower() == "true"

    app.run(debug=True, use_reloader=use_reloader, host="0.0.0.0", port=5000)