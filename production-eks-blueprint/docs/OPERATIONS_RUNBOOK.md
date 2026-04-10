# Production Operations Guide

## Best Practices

- Use separate AWS accounts or strict IAM boundaries for dev/staging/prod.
- Enforce least privilege with IRSA for each workload.
- Keep image tags immutable and signed.
- Use PodDisruptionBudgets and anti-affinity for HA.
- Enable encryption at rest (EBS, Secrets Manager, RDS if adopted) and in transit (TLS).
- Apply WAF managed rules plus custom rate-limit rules.

## Scaling Strategy

- HPA scales services by CPU and custom app metrics.
- Karpenter provisions right-sized nodes for pending pods.
- Tune requests/limits to avoid overcommit and throttling.
- Use load tests to calibrate max replicas and target utilization.

## Troubleshooting Strategy

- Check ALB target health and Ingress events first.
- Validate pod readiness/liveness failures and restart loops.
- Trace latency using request ID across ingress, service logs, and DB metrics.
- Confirm Secrets sync and IAM permissions for IRSA roles.

## Monitoring and Alerting Flow

- Prometheus scrapes application and cluster metrics.
- Alert rules fire to Alertmanager (PagerDuty/Slack/email).
- Grafana dashboards show service SLOs, saturation, errors, and latency.
- On-call follows runbook-based remediation with rollback triggers.

## Disaster Recovery and Backup

- PostgreSQL logical backups + volume snapshots with retention.
- Cross-region backup copy for critical datasets.
- Store IaC and manifests in Git for rapid environment recreation.
- Define RPO/RTO per environment (e.g., prod RPO 15m, RTO 1h).
- Run quarterly restore drills and game days.
