import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # --- DATABASE CONFIGURATION ---
    # CONSTRAINT: Must use PostgreSQL.
    # FORMAT: postgresql://username:password@localhost:5432/db_name
    
    # Check for environment variable first, fallback to local default
    # You can change 'postgres:password' to match your local DB credentials.
    default_pg_uri = 'postgresql://postgres:1234@localhost:5432/taskdb'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', default_pg_uri)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev_secret_key'

    # Init extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    CORS(app) 

    # Register Blueprints
    from app.routes import auth, tasks
    app.register_blueprint(auth.bp)
    app.register_blueprint(tasks.bp)

    return app