# Flowdoc Configuration Reference

This document lists all configuration values that need to be set across different parts of the application.

## Project Structure
All paths are relative to the project root directory.

## AWS Deployment Configuration

File: `scripts/aws_deploy.sh`

### Required AWS Credentials
```bash
# AWS CLI Configuration (prompted during deployment)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=your-preferred-region  # defaults to us-west-2
```

### Container Orchestration Settings

#### For ECS Deployment
```bash
# Environment variables needed before running aws_deploy.sh
export ECS_CLUSTER=flowdoc-ecs-cluster
export ECS_SERVICE=flowdoc-ecs-service
```

#### For EKS Deployment
```bash
# Environment variable needed before running aws_deploy.sh
export EKS_CLUSTER=flowdoc-eks-cluster
```

## Kubernetes Configuration

File: `infrastructure/kubernetes/config/k8s-flask-deployment.yaml`

```yaml
# Required environment variables in deployment configuration
- POSTGRES_USER=flowdoc-db-user
- POSTGRES_PASSWORD=your-postgres-password  # Sensitive - set via secrets
- POSTGRES_DB=flowdoc-db
- POSTGRES_HOST=flowdoc-db-host
```

## Database Configuration

File: `config/config.py`

```python
# Database connection settings
DB_USER=flowdoc-db-user
DB_PASSWORD=your-db-password  # Sensitive - set via secrets
DB_HOST=flowdoc-db-host
DB_NAME=flowdoc-db
```

## N8N Configuration

File: `infrastructure/docker/docker-compose.yml`

```yaml
# N8N environment variables
N8N_BASIC_AUTH_USER=flowdoc-n8n-user
N8N_BASIC_AUTH_PASSWORD=your-n8n-password  # Sensitive - set via secrets
N8N_PORT=5678  # defaults to 5678
```

## Redis Configuration

File: `config/config.py`

```python
# Redis connection settings
REDIS_HOST=flowdoc-redis
REDIS_PORT=6379  # defaults to 6379
REDIS_PASSWORD=your-redis-password  # Sensitive - set via secrets
```

## JWT Configuration

File: `config/config.py`

```python
# JWT settings
JWT_SECRET_KEY=your-jwt-secret  # Sensitive - set via secrets
JWT_ACCESS_TOKEN_EXPIRES=15  # in minutes, defaults to 15
```

## OCR Service Configuration (AWS Lambda)

File: `services/ocr_service.py`

```python
# AWS Lambda configuration
LAMBDA_FUNCTION_NAME=flowdoc-ocr-lambda
S3_BUCKET_NAME=flowdoc-documents
```

## Document Sharing Settings

File: `config/config.py`

```python
# Document sharing configuration
SHARE_LINK_EXPIRY=24  # in hours, defaults to 24
MAX_UPLOAD_SIZE=10  # in MB, defaults to 10
```

## Monitoring Configuration

File: `infrastructure/prometheus/prometheus-config.yaml`

```yaml
# Prometheus settings
scrape_interval: 15s  # defaults to 15s
evaluation_interval: 15s  # defaults to 15s
```

## Important Notes

1. Never commit sensitive values directly to the repository
2. Use environment variables or secure vaults for production deployments
3. Keep a backup of your configuration values in a secure location
4. Consider using a secret management service for production environments

## Best Practices

1. Create a `.env.example` file with dummy values for local development
2. Document any changes to configuration requirements
3. Use different configurations for development, staging, and production
4. Regularly rotate sensitive credentials
5. Monitor and audit access to sensitive configuration values