# scripts/deploy_k8s.zsh

#!/bin/zsh

# Exit immediately if a command exits with a non-zero status
set -e

echo "=== Deploying to Kubernetes ==="

NAMESPACE="thoughtful-ai"

# Apply Namespace
echo "Creating namespace '${NAMESPACE}'..."
kubectl apply -f kubernetes/namespace.yaml

# Apply Secret
echo "Creating OpenAI API Key secret..."
kubectl apply -f kubernetes/secret.yaml

# Apply Deployment and Service
echo "Deploying application..."
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml

# Apply Ingress (if exists)
if [ -f "kubernetes/ingress.yaml" ]; then
    echo "Setting up Ingress..."
    kubectl apply -f kubernetes/ingress.yaml
fi

# Verify Deployment
echo "Verifying deployment..."
kubectl rollout status deployment/ai-support-agent-deployment -n ${NAMESPACE}

echo "=== Deployment to Kubernetes Completed ==="
