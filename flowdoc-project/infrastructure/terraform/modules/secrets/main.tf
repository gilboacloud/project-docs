# AWS Secrets Manager Terraform Configuration

resource "aws_secretsmanager_secret" "flowdoc_secrets" {
  name = "flowdoc/credentials"
  description = "Flowdoc application secrets"
  
  tags = {
    Environment = var.environment
    Application = "flowdoc"
  }
}

resource "aws_secretsmanager_secret_version" "flowdoc_secrets" {
  secret_id = aws_secretsmanager_secret.flowdoc_secrets.id
  
  # DO NOT PUT ACTUAL SECRETS HERE - this is a template
  secret_string = jsonencode({
    DB_PASSWORD         = "your-db-password"
    REDIS_PASSWORD      = "your-redis-password"
    JWT_SECRET_KEY      = "your-jwt-secret"
    AWS_ACCESS_KEY_ID   = "your-aws-access-key"
    AWS_SECRET_ACCESS_KEY = "your-aws-secret-key"
  })
}