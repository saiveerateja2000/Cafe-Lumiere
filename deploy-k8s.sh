#!/usr/bin/env bash
set -euo pipefail
NAMESPACE=cafe-lumiere

# Optional: build and push images (uncomment & set REGISTRY)
# REGISTRY=your.registry.io/your-org
# docker build -t $REGISTRY/cafe-lumiere/order-service:latest cafe/order-service
# docker push $REGISTRY/cafe-lumiere/order-service:latest
# docker build -t $REGISTRY/cafe-lumiere/kitchen-service:latest cafe/kitchen-service
# docker push $REGISTRY/cafe-lumiere/kitchen-service:latest
# docker build -t $REGISTRY/cafe-lumiere/frontend:latest cafe/frontend
# docker push $REGISTRY/cafe-lumiere/frontend:latest

# Create namespace
kubectl create ns $NAMESPACE || true

# Install Postgres Helm chart (service will be cafe-lumiere-postgresql)
helm upgrade --install cafe-lumiere-postgresql cafe/helm/postgresql -n $NAMESPACE

# Apply app manifests (ConfigMap, Secrets, Deployments, Services)
kubectl apply -f cafe/k8s/deployments.yaml -n $NAMESPACE

# Wait for Postgres StatefulSet to be ready
kubectl -n $NAMESPACE rollout status statefulset/cafe-lumiere-postgresql --timeout=180s

# Wait for app deployments to roll out
kubectl -n $NAMESPACE rollout status deployment/order-service --timeout=120s
kubectl -n $NAMESPACE rollout status deployment/kitchen-service --timeout=120s
kubectl -n $NAMESPACE rollout status deployment/frontend --timeout=120s

# Quick checks
kubectl -n $NAMESPACE get pods -o wide
kubectl -n $NAMESPACE get svc

# Verify order-service health (from control plane)
ORDER_POD=$(kubectl -n $NAMESPACE get pod -l app=order-service -o jsonpath='{.items[0].metadata.name}')
kubectl -n $NAMESPACE exec -it $ORDER_POD -- curl -sS http://localhost:5001/health || kubectl -n $NAMESPACE logs $ORDER_POD

# Verify kitchen -> order connectivity (from a kitchen pod)
KITCHEN_POD=$(kubectl -n $NAMESPACE get pod -l app=kitchen-service -o jsonpath='{.items[0].metadata.name}')
kubectl -n $NAMESPACE exec -it $KITCHEN_POD -- curl -sS http://order-service:5001/health || kubectl -n $NAMESPACE logs $KITCHEN_POD

echo "Deployment finished. Frontend service is exposed as a ClusterIP; port-forward if you need local access:"
echo "kubectl -n $NAMESPACE port-forward svc/frontend 8080:80"
