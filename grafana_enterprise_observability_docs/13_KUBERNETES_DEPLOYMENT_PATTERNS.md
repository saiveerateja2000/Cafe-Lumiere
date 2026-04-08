# Kubernetes Deployment Patterns

## Namespace and Segmentation
- Use dedicated `observability` namespace.
- Separate `prod-observability` from non-prod when risk profile requires.
- Apply resource quotas and limit ranges.

## Helm/IaC Recommendations
- Version pin chart and image tags.
- Store values files per environment.
- Keep secrets externalized.

## Fluent Bit Pattern
- DaemonSet with hostPath mounts for log paths and tail DB.
- Tolerations for system nodes if platform logs are needed.
- Priority class to reduce collector eviction risk.

## Backend Pattern
- Loki/Tempo with object storage and persistent metadata components.
- Prometheus with persistent volumes and anti-affinity.
- Grafana with external DB and replica-safe deployment config.

## Scheduling and Reliability
- Pod anti-affinity for replicas.
- PodDisruptionBudgets for critical components.
- Topology spread constraints across zones.

## Security Controls
- Run as non-root where supported.
- Restrictive service accounts and RBAC rules.
- Network policies for data source paths.

## Release Pattern
- Deploy to staging first.
- Run smoke tests: ingestion, query, alert test, email send.
- Promote with immutable artifact versions.
