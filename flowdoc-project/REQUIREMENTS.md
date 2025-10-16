# Flowdoc Requirements

## Python Dependencies
```
# Core Framework
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.5
Flask-JWT-Extended==4.5.3
Flask-Cors==4.0.0
gunicorn==21.2.0

# Database
psycopg2-binary==2.9.7
SQLAlchemy==2.0.21
alembic==1.12.0

# AWS
boto3==1.29.7
aws-xray-sdk==2.12.0

# Cache & Queue
redis==5.0.1
celery==5.3.4

# Utils
python-dotenv==1.0.0
pydantic==2.4.2
requests==2.31.0
PyJWT==2.8.0
python-jose==3.3.0
marshmallow==3.20.1

# Testing
pytest==7.4.2
pytest-cov==4.1.0
pytest-mock==3.11.1
factory-boy==3.3.0

# Development
black==23.9.1
flake8==6.1.0
mypy==1.5.1
isort==5.12.0
pre-commit==3.4.0
```

## System Dependencies
```
# Runtime
python>=3.11
postgresql>=14
redis>=5.0
docker>=20.10
kubernetes>=1.25

# Development
git
make
docker-compose
kubectl
```

## AWS Services
- S3
- Textract
- Lambda
- SQS/SNS
- RDS PostgreSQL
- ElastiCache Redis

## Third-Party Services
- N8N Workflow Engine
- SMTP Server (for notifications)

## Development Tools
- VS Code or PyCharm
- AWS CLI
- kubectl
- Docker Desktop
- PostgreSQL Client
- Redis CLI