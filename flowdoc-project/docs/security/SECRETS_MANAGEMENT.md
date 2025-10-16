# Secrets Management in Flowdoc

## Overview
This document describes how secrets are managed in different environments of the Flowdoc application.

## Development Environment

### Local Development
- Use `.env` file (not committed to git)
- Copy `.env.example` and fill in your local values
- Location: Project root directory

### Development Cluster
- Use Kubernetes Secrets
- Location: `infrastructure/kubernetes/secrets/`
- Apply using: `kubectl apply -f secrets.yaml`

## Staging/Production Environments

### AWS Secrets Manager
- Production secrets are stored in AWS Secrets Manager
- Managed via Terraform in `infrastructure/terraform/modules/secrets/`
- Accessed using IAM roles and policies

### Secret Rotation
- Database passwords: Every 90 days
- JWT secrets: Every 30 days
- AWS credentials: Use IAM roles when possible

## Creating Secrets

### For Kubernetes (Development)
```bash
# Generate base64 encoded secrets
echo -n "your-secret" | base64

# Create the secrets file
cp infrastructure/kubernetes/secrets/secrets.yaml.template infrastructure/kubernetes/secrets/secrets.yaml

# Edit the secrets file with your base64 encoded values
vim infrastructure/kubernetes/secrets/secrets.yaml

# Apply the secrets
kubectl apply -f infrastructure/kubernetes/secrets/secrets.yaml
```

### For AWS Secrets Manager (Production)
1. Use AWS Console or AWS CLI to create secrets
2. Use Terraform to manage secret infrastructure
3. Access secrets using AWS SDK in application

## Accessing Secrets

### In Kubernetes
```yaml
# In deployment yaml
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: flowdoc-db-secrets
        key: DB_PASSWORD
```

### In Application Code
```python
# Using AWS Secrets Manager
import boto3

def get_secret(secret_name):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-west-2'
    )
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except Exception as e:
        logging.error(f"Error retrieving secret: {e}")
        raise
```

## Security Best Practices

1. Never commit secrets to git
2. Use different secrets for each environment
3. Rotate secrets regularly
4. Use least privilege access
5. Audit secret access
6. Use encryption at rest
7. Enable secret rotation where possible

## Secret Types and Locations

1. Database Credentials
   - Location: AWS Secrets Manager or K8s Secrets
   - Used in: Backend application

2. Redis Credentials
   - Location: AWS Secrets Manager or K8s Secrets
   - Used in: Cache service

3. JWT Secrets
   - Location: AWS Secrets Manager or K8s Secrets
   - Used in: Authentication service

4. AWS Credentials
   - Location: IAM Roles for Production
   - AWS Secrets Manager or K8s Secrets for Development

5. API Keys
   - Location: AWS Secrets Manager or K8s Secrets
   - Used in: External service integrations