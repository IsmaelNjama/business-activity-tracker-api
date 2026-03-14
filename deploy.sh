#!/bin/bash
set -e

# Configuration
AWS_REGION="us-east-1"
FUNCTION_NAME="business-activity-tracker"
ECR_REPO_NAME="business-activity-tracker"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
VPC_STACK_NAME="business-activity-tracker-vpc"
STACK_NAME="business-activity-tracker-stack"
SECRET_ARN="${SECRET_ARN:?SECRET_ARN environment variable is required}"

echo "Building and deploying Lambda function..."

# Build Docker image
docker build -f Dockerfile.lambda -t $FUNCTION_NAME .

# Create ECR repository if it doesn't exist
aws ecr describe-repositories --repository-names $ECR_REPO_NAME --region $AWS_REGION 2>/dev/null || \
aws ecr create-repository --repository-name $ECR_REPO_NAME --region $AWS_REGION

# Get ECR login token
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Tag and push image
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
IMAGE_TAG="$TIMESTAMP"
docker tag $FUNCTION_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:$IMAGE_TAG
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:$IMAGE_TAG
IMAGE_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:$IMAGE_TAG"

# Deploy VPC stack first
if aws cloudformation describe-stacks --stack-name $VPC_STACK_NAME --region $AWS_REGION 2>/dev/null; then
    echo "Updating VPC stack..."
    aws cloudformation update-stack \
        --stack-name $VPC_STACK_NAME \
        --template-body file://infra/vpc.yml \
        --region $AWS_REGION || echo "VPC stack already up to date"
else
    echo "Creating VPC stack..."
    aws cloudformation create-stack \
        --stack-name $VPC_STACK_NAME \
        --template-body file://infra/vpc.yml \
        --region $AWS_REGION
fi
echo "Waiting for VPC stack..."
aws cloudformation wait stack-create-complete --stack-name $VPC_STACK_NAME --region $AWS_REGION 2>/dev/null || \
aws cloudformation wait stack-update-complete --stack-name $VPC_STACK_NAME --region $AWS_REGION 2>/dev/null || true

# Deploy main stack
if aws cloudformation describe-stacks --stack-name $STACK_NAME --region $AWS_REGION 2>/dev/null; then
    echo "Updating CloudFormation stack..."
    aws cloudformation update-stack \
        --stack-name $STACK_NAME \
        --template-body file://infra/cloudformation.yml \
        --parameters \
            ParameterKey=ImageUri,ParameterValue=$IMAGE_URI \
            ParameterKey=SecretArn,ParameterValue=$SECRET_ARN \
        --capabilities CAPABILITY_NAMED_IAM \
        --region $AWS_REGION
else
    echo "Creating CloudFormation stack..."
    aws cloudformation create-stack \
        --stack-name $STACK_NAME \
        --template-body file://infra/cloudformation.yml \
        --parameters \
            ParameterKey=ImageUri,ParameterValue=$IMAGE_URI \
            ParameterKey=SecretArn,ParameterValue=$SECRET_ARN \
        --capabilities CAPABILITY_NAMED_IAM \
        --region $AWS_REGION
fi
echo "Waiting for main stack..."
aws cloudformation wait stack-create-complete --stack-name $STACK_NAME --region $AWS_REGION 2>/dev/null || \
aws cloudformation wait stack-update-complete --stack-name $STACK_NAME --region $AWS_REGION 2>/dev/null || true

echo "Deployment complete!"
