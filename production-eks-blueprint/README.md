# Cafe Lumiere - Production EKS Blueprint

This folder is a standalone production-grade blueprint for deploying a microservices application on AWS EKS.

## Architecture Diagram

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full Mermaid architecture diagram and supporting notes.

## Folder Structure

```text
production-eks-blueprint/
├── frontend/
│   └── nginx/
├── backend/
│   ├── user-service/
│   ├── order-service/
│   └── health-service/
├── database/
├── kubernetes/
│   ├── base/
│   ├── environments/
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   └── addons/
│       ├── ingress/
│       ├── monitoring/
│       ├── secrets/
│       └── karpenter/
├── helm/
│   └── cafe-lumiere/
├── terraform/
│   ├── modules/
│   └── environments/
├── cicd/
│   ├── github-actions/
│   ├── argocd/
│   └── jenkins/
├── monitoring/
│   ├── prometheus/
│   ├── grafana/
│   └── alerts/
├── secrets/
│   ├── external-secrets/
│   └── k8s-sealed-secrets/
└── docs/
```

See docs under `docs/` for request flow, lifecycle, scaling, and DR strategy.
