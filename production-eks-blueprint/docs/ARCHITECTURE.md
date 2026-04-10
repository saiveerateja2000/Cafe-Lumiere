# Cafe Lumiere Production EKS Architecture

This blueprint deploys Cafe Lumiere as a production-ready microservices platform on AWS EKS. The diagram below shows the request path, platform layers, delivery pipeline, and supporting services.

```mermaid
flowchart LR
  %% External users
  subgraph U[Clients]
    browser[Browser / Mobile Client]
  end

  %% Edge and networking
  subgraph E[Edge and Networking]
    route53[Route 53 DNS]
    waf[AWS WAF]
    alb[Application Load Balancer]
    cognito[Amazon Cognito OIDC]
    acm[ACM TLS Certificate]
  end

  %% Kubernetes platform
  subgraph K[EKS Platform]
    direction TB
    subgraph NS[Application Namespace]
      frontend[frontend-service\nReact + Nginx]
      user[user-service\nFastAPI / Flask]
      orders[order-service\nFastAPI / Flask]
      health[health-service\nIngress health endpoint]
    end

    subgraph ADDONS[Cluster Add-ons]
      ingress[AWS Load Balancer Controller]
      externalSecrets[External Secrets Operator]
      prometheus[Prometheus]
      grafana[Grafana]
      alertmanager[Alertmanager]
      karpenter[Karpenter]
      hpa[Horizontal Pod Autoscaler]
    end

    subgraph DATA[Data and Secrets]
      postgres[(PostgreSQL StatefulSet)]
      pvc[(PersistentVolumeClaim)]
      k8sSecrets[Kubernetes Secrets]
      secretsManager[AWS Secrets Manager]
      configMap[ConfigMaps]
    end
  end

  %% Delivery and provisioning
  subgraph D[Delivery and Provisioning]
    github[GitHub Repository]
    cicd[CI: tests, lint, scan, build]
    ecr[Amazon ECR]
    gitops[Argo CD GitOps Sync]
    terraform[Terraform Modules and Environments]
    awsInfra[AWS Infrastructure\nVPC, EKS, IAM, ALB, ECR, S3, DynamoDB]
  end

  %% Traffic flow
  browser --> route53 --> waf --> alb
  alb --> frontend
  alb --> user
  alb --> orders
  alb --> health
  alb -. authentication .-> cognito
  alb -. TLS .-> acm
  ingress --- alb

  %% Service dependencies
  frontend --> user
  frontend --> orders
  user --> postgres
  orders --> postgres
  health --> postgres
  user --> configMap
  orders --> configMap
  user --> k8sSecrets
  orders --> k8sSecrets
  externalSecrets --> secretsManager --> k8sSecrets
  postgres --> pvc

  %% Observability and scaling
  prometheus --> grafana
  prometheus --> alertmanager
  prometheus -. scrapes .-> frontend
  prometheus -. scrapes .-> user
  prometheus -. scrapes .-> orders
  prometheus -. scrapes .-> health
  hpa --> frontend
  hpa --> user
  hpa --> orders
  hpa --> health
  karpenter --> K

  %% Delivery flow
  github --> cicd --> ecr --> gitops --> frontend
  gitops --> user
  gitops --> orders
  gitops --> health
  terraform --> awsInfra --> K
  terraform --> ecr
  terraform --> gitops
  terraform --> secretsManager

  %% Styling
  classDef edge fill:#e8f0fe,stroke:#1a73e8,color:#0b1f44;
  classDef platform fill:#e6f4ea,stroke:#1e8e3e,color:#102814;
  classDef data fill:#fef7e0,stroke:#f29900,color:#4a3200;
  classDef delivery fill:#f3e8ff,stroke:#9333ea,color:#2d114f;
  classDef client fill:#fff3e0,stroke:#ef6c00,color:#4a2500;

  class browser client;
  class route53,waf,alb,cognito,acm edge;
  class frontend,user,orders,health,ingress,externalSecrets,prometheus,grafana,alertmanager,karpenter,hpa platform;
  class postgres,pvc,k8sSecrets,secretsManager,configMap data;
  class github,cicd,ecr,gitops,terraform,awsInfra delivery;
```

## What This Blueprint Includes

- Public entry through Route 53, AWS WAF, and an ALB with ACM-backed TLS.
- Cognito-based authentication at the load balancer layer.
- EKS application workloads for the frontend, user API, order API, and health endpoint.
- PostgreSQL persistence through a StatefulSet and PVC-backed storage.
- Kubernetes secrets synced from AWS Secrets Manager by External Secrets Operator.
- Prometheus, Grafana, and Alertmanager for metrics, dashboards, and alerting.
- HPA for pod scaling and Karpenter for node provisioning.
- Terraform for AWS foundation and Argo CD for GitOps-based deployment promotion.

## Related Docs

- [Request flow](REQUEST_FLOW.md)
- [Deployment lifecycle](DEPLOYMENT_LIFECYCLE.md)
- [Operations runbook](OPERATIONS_RUNBOOK.md)
