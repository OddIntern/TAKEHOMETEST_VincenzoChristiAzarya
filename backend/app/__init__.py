from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
import os

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Simple Config (We will move this to config.py later)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://app_user:secure_password@localhost:5432/taskdb')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret')

    # Init extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    CORS(app) # Allow frontend communication

    # Register Blueprints
    from app.routes import auth, tasks
    app.register_blueprint(auth.bp)
    app.register_blueprint(tasks.bp)

    return app