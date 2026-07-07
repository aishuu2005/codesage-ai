from flask import Flask

# Create the Flask application
app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return {
        "message": "Welcome to CodeSage AI 🚀",
        "status": "Backend is running successfully!"
    }

# Run the application
if __name__ == "__main__":
    app.run(debug=True)