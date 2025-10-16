#!/bin/bash

# Flowdoc AWS Deployment Script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Load environment variables from .env file
if [ -f .env ]; then
    echo -e "${GREEN}Loading environment variables from .env file...${NC}"
    set -a
    source .env
    set +a
else
    echo -e "${YELLOW}No .env file found. You will need to set environment variables manually.${NC}"
fi

# Check AWS CLI installation
check_aws_cli() {
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}AWS CLI is not installed. Installing...${NC}"
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
        unzip awscliv2.zip
        sudo ./aws/install
        rm -rf aws awscliv2.zip
    fi
}

# Configure AWS credentials
configure_aws() {
    echo -e "${YELLOW}Configuring AWS credentials...${NC}"
    
    # Check if credentials already exist
    if [ -f ~/.aws/credentials ]; then
        echo -e "${YELLOW}AWS credentials file already exists. Do you want to reconfigure? (y/n)${NC}"
        read -r response
        if [ "$response" != "y" ]; then
            return
        fi
    fi
    
    # Get AWS credentials
    echo -e "${GREEN}Please enter your AWS credentials:${NC}"
    read -p "AWS Access Key ID: " aws_access_key
    read -p "AWS Secret Access Key: " aws_secret_key
    read -p "AWS Region [us-west-2]: " aws_region
    aws_region=${aws_region:-us-west-2}
    
    # Configure AWS CLI
    mkdir -p ~/.aws
    cat > ~/.aws/credentials << EOF
[default]
aws_access_key_id = ${aws_access_key}
aws_secret_access_key = ${aws_secret_key}
EOF

    cat > ~/.aws/config << EOF
[default]
region = ${aws_region}
output = json
EOF

    echo -e "${GREEN}AWS credentials configured successfully!${NC}"
}

# Validate AWS connection
validate_aws() {
    echo -e "${YELLOW}Validating AWS connection...${NC}"
    if aws sts get-caller-identity &> /dev/null; then
        echo -e "${GREEN}AWS connection successful!${NC}"
        return 0
    else
        echo -e "${RED}AWS connection failed. Please check your credentials.${NC}"
        return 1
    fi
}

# Configure ECR repository
setup_ecr() {
    echo -e "${YELLOW}Setting up ECR repository...${NC}"
    
    # Get AWS account ID
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    
    # Create ECR repository if it doesn't exist
    if ! aws ecr describe-repositories --repository-names flowdoc &> /dev/null; then
        aws ecr create-repository \
            --repository-name flowdoc \
            --image-scanning-configuration scanOnPush=true
    fi
    
    # Login to ECR
    aws ecr get-login-password --region ${aws_region} | \
    docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${aws_region}.amazonaws.com
    
    echo -e "${GREEN}ECR repository setup complete!${NC}"
}

# Deploy to AWS
deploy() {
    echo -e "${YELLOW}Starting deployment...${NC}"
    
    # Build Docker image
    docker build -t flowdoc:latest .
    
    # Tag and push to ECR
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    ECR_REPO="${AWS_ACCOUNT_ID}.dkr.ecr.${aws_region}.amazonaws.com/flowdoc"
    
    docker tag flowdoc:latest ${ECR_REPO}:latest
    docker push ${ECR_REPO}:latest
    
    # Update ECS service (if using ECS)
    if [ -n "${ECS_CLUSTER}" ] && [ -n "${ECS_SERVICE}" ]; then
        aws ecs update-service \
            --cluster ${ECS_CLUSTER} \
            --service ${ECS_SERVICE} \
            --force-new-deployment
    fi
    
    # Or update EKS deployment (if using EKS)
    if [ -n "${EKS_CLUSTER}" ]; then
        aws eks update-kubeconfig --name ${EKS_CLUSTER}
        kubectl apply -f infrastructure/kubernetes/config/
        kubectl apply -f infrastructure/kubernetes/deployments/
    fi
    
    echo -e "${GREEN}Deployment complete!${NC}"
}

# Main script
main() {
    echo -e "${GREEN}Flowdoc AWS Deployment${NC}"
    
    # Check and install AWS CLI
    check_aws_cli
    
    # Configure AWS if needed
    configure_aws
    
    # Validate AWS connection
    validate_aws || exit 1
    
    # Setup ECR
    setup_ecr
    
    # Deploy
    deploy
}

# Run main function
main