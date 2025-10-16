from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import redis
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object('src.core.config.Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    
    # Initialize Redis
    app.redis = redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        db=int(os.getenv('REDIS_DB', 0)),
        decode_responses=True
    )
    
    # Register blueprints
    from src.api.routes.auth import auth_bp
    from src.api.routes.documents import documents_bp
    from src.api.routes.workflows import workflows_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(documents_bp, url_prefix='/api/v1/documents')
    app.register_blueprint(workflows_bp, url_prefix='/api/v1/workflows')
    
    # Register error handlers
    from src.api.errors import register_error_handlers
    register_error_handlers(app)
    
    return app