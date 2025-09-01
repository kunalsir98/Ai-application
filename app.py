import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure CORS
CORS(app)

# Configure database (SQLite by default)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///ai_platform.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
from extensions import db
db.init_app(app)

# Import and register routes
from routes import register_routes
register_routes(app)

# Initialize database and create default user
with app.app_context():
    from models import User, create_default_user  # Import models BEFORE db.create_all()
    
    db.create_all()  # Creates tables if they don't exist
    create_default_user()  # Creates default user if none exists

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
