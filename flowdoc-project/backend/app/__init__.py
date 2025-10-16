from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from redis import Redis
import boto3

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()

def create_app(config=None):
    app = Flask(__name__)
    
    # Load configuration
    if config:
        app.config.from_object(config)
    else:
        app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    
    # Initialize Redis
    app.redis = Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        password=app.config['REDIS_PASSWORD']
    )
    
    # Initialize AWS clients
    app.s3 = boto3.client('s3')
    app.textract = boto3.client('textract')
    
    # Register blueprints
    from .api.auth import auth_bp
    from .api.documents import documents_bp
    from .api.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(documents_bp, url_prefix='/api/documents')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    return app