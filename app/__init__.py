from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

# Initialize environment variables from .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configure the app using values from .env file
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Import the routes after initializing the app
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
