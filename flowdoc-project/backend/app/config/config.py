class Config:
    # Flask
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your-secret-key'  # Change in production

    # Database
    SQLALCHEMY_DATABASE_URI = 'postgresql://flowdoc:password@localhost/flowdoc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_PASSWORD = None

    # AWS
    AWS_REGION = 'us-west-2'
    S3_BUCKET = 'flowdoc-documents'
    
    # JWT
    JWT_SECRET_KEY = 'your-jwt-secret'  # Change in production
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour

    # Document Processing
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'tiff'}