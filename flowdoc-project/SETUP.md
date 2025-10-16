# Flowdoc Application Setup Guide

## Overview
Flowdoc is a document management system with OCR capabilities, workflow automation, and cloud integration.

## System Requirements

### Infrastructure Components
```yaml
# Required Services
database: PostgreSQL 14+
cache: Redis 5+
message_queue: AWS SQS/SNS
object_storage: AWS S3
ocr_service: AWS Textract
workflow_engine: N8N
```

### Cloud Resources (AWS)
```yaml
services:
  - S3:
      buckets:
        - documents
        - signatures
  - Textract
  - Lambda
  - RDS PostgreSQL
  - ElastiCache Redis
  - SQS/SNS
```

### Environment Variables
```bash
# Core Settings
FLASK_ENV=production
FLASK_APP=main.py
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/flowdoc
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Redis Cache
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# AWS Configuration
AWS_REGION=us-west-2
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET=flowdoc-documents
SIGNATURE_BUCKET=flowdoc-signatures

# Security
JWT_SECRET_KEY=your-secret-key
JWT_ACCESS_TOKEN_EXPIRES=86400  # 24 hours

# OCR Settings
ENABLE_OCR=true
OCR_LAMBDA_NAME=flowdoc-ocr-processor
TEXTRACT_ROLE_ARN=arn:aws:iam::account:role/TextractRole
SNS_TOPIC_ARN=arn:aws:sns:region:account:TextractCompletionTopic

# Workflow
N8N_WEBHOOK_URL=http://localhost:5678/webhook/flowdoc
ENABLE_N8N=true
N8N_API_KEY=your-n8n-api-key

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@flowdoc.com
```

## Installation Steps

1. **Clone Repository**
```bash
git clone https://github.com/yourorg/flowdoc.git
cd flowdoc
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Database Setup**
```bash
flask db upgrade
flask seed-db  # If available
```

5. **Start Services Locally**
```bash
# Start Redis
docker run -d -p 6379:6379 redis

# Start PostgreSQL
docker run -d -p 5432:5432 \
  -e POSTGRES_USER=flowdoc \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=flowdoc \
  postgres:14

# Start N8N
docker run -d -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=password \
  n8nio/n8n
```

## Running the Application

### Development
```bash
flask run --debug
```

### Production (with Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:8000 "main:create_app()"
```

## Docker Deployment
```bash
# Build Image
docker build -t flowdoc:latest .

# Run Container
docker run -d \
  --name flowdoc \
  -p 8000:8000 \
  --env-file .env \
  flowdoc:latest
```

## Kubernetes Deployment
```bash
# Apply ConfigMaps and Secrets first
kubectl apply -f k8s/config/

# Deploy application components
kubectl apply -f k8s/deployments/
```

## Monitoring

### Prometheus Metrics
Key metrics to monitor:
- Document processing time
- OCR success rate
- API endpoint latency
- Cache hit ratio
- Queue lengths

### Health Checks
Endpoints:
- `/health` - Basic health check
- `/health/live` - Liveness probe
- `/health/ready` - Readiness probe

## Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints
- Document all functions and classes
- Include docstring examples

### Testing
```bash
# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

### Common Development Tasks

1. **Adding New API Endpoint**
```python
@app.route('/api/v1/resource', methods=['POST'])
@jwt_required
def create_resource():
    data = request.get_json()
    # Validate input
    # Process request
    # Return response
```

2. **Creating New Service**
```python
class NewService:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.setup_connections()
    
    def setup_connections(self):
        # Initialize connections
        pass
    
    def process_something(self, data: Dict) -> Result:
        # Business logic here
        pass
```

3. **Adding Database Model**
```python
class NewModel(db.Model):
    __tablename__ = 'table_name'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Add other fields
```

## Troubleshooting

### Common Issues

1. **Document Processing Failures**
- Check AWS Textract quotas
- Verify Lambda function logs
- Ensure proper IAM permissions

2. **Performance Issues**
- Monitor Redis cache usage
- Check database query performance
- Review API endpoint metrics

3. **Workflow Problems**
- Verify N8N webhook configurations
- Check workflow execution logs
- Validate event payload format

## Support and Resources

- Documentation: `/docs`
- API Reference: `/docs/api`
- Architecture Diagrams: `/docs/architecture`
- Workflow Templates: `/docs/workflows`