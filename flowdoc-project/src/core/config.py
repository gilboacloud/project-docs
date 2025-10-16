import os
from datetime import timedelta

class Config:
    """Base configuration."""
    
    # Application
    APP_NAME = "flowdoc"
    VERSION = "2.0.0"
    
    # Flask
    SECRET_KEY = os.getenv('FLOWDOC_SECRET_KEY', 'your-secret-key-here')
    FLASK_ENV = os.getenv('FLOWDOC_ENV', 'production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('FLOWDOC_DATABASE_URL', 'postgresql://flowdoc:password@localhost/flowdoc')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('FLOWDOC_JWT_SECRET_KEY', 'your-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv('FLOWDOC_JWT_TOKEN_HOURS', 24)))
    
    # AWS
    AWS_REGION = os.getenv('FLOWDOC_AWS_REGION', 'us-west-2')
    S3_BUCKET = os.getenv('FLOWDOC_S3_BUCKET', 'flowdoc-documents')
    SIGNATURE_BUCKET = os.getenv('FLOWDOC_SIGNATURE_BUCKET', 'flowdoc-signatures')
    
    # Redis
    REDIS_HOST = os.getenv('FLOWDOC_REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('FLOWDOC_REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('FLOWDOC_REDIS_DB', 0))
    
    # OCR
    ENABLE_OCR = os.getenv('FLOWDOC_ENABLE_OCR', 'true').lower() == 'true'
    OCR_LAMBDA_NAME = os.getenv('FLOWDOC_OCR_LAMBDA_NAME', 'flowdoc-ocr-processor')
    
    # N8N
    ENABLE_N8N = os.getenv('FLOWDOC_ENABLE_N8N', 'true').lower() == 'true'
    N8N_WEBHOOK_URL = os.getenv('FLOWDOC_N8N_WEBHOOK_URL')
    N8N_API_KEY = os.getenv('FLOWDOC_N8N_API_KEY')
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Development configuration."""
    FLASK_ENV = 'development'
    DEBUG = True
    
class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/flowdoc_test'
    
class ProductionConfig(Config):
    """Production configuration."""
    # Add production-specific settings here
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}