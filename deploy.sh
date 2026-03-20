#!/usr/bin/env bash
set -euo pipefail

REGION="us-east-1"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_URL="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/showstats"

echo "==> Authenticating Docker to ECR..."
aws ecr get-login-password --region "${REGION}" | \
  docker login --username AWS --password-stdin "${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"

echo "==> Building Docker image..."
docker build --platform linux/amd64 -t showstats .

echo "==> Tagging and pushing to ECR..."
docker tag showstats:latest "${ECR_URL}:latest"
docker push "${ECR_URL}:latest"

echo "==> Forcing ECS redeployment..."
aws ecs update-service \
  --cluster showstats \
  --service showstats-app \
  --force-new-deployment \
  --region "${REGION}" \
  --output text --query 'service.serviceName'

echo "==> Done. New deployment in progress."
echo "    Monitor: https://console.aws.amazon.com/ecs/home?region=${REGION}#/clusters/showstats/services"