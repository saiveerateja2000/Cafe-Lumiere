# Grafana Enterprise Observability Playbook

This folder provides end-to-end production documentation for building and operating an observability stack using:
- Fluent Bit (logs collection and forwarding)
- Loki (log storage and query)
- Prometheus (metrics)
- Tempo (distributed tracing)
- Grafana Enterprise (visualization, RBAC, alerting, reporting)

The scope starts at Kubernetes application pods and ends at dashboards, alerts, and email notifications.

## Start Here

1. [00_AGENDA.md](00_AGENDA.md)
2. [01_ARCHITECTURE_AND_DATA_FLOW.md](01_ARCHITECTURE_AND_DATA_FLOW.md)
3. [15_PRODUCTION_READINESS_CHECKLIST.md](15_PRODUCTION_READINESS_CHECKLIST.md)

## Full Documentation Map

- [00_AGENDA.md](00_AGENDA.md)
- [01_ARCHITECTURE_AND_DATA_FLOW.md](01_ARCHITECTURE_AND_DATA_FLOW.md)
- [02_FLUENT_BIT_COLLECTION_AND_PARSING.md](02_FLUENT_BIT_COLLECTION_AND_PARSING.md)
- [03_LOKI_LOG_STORAGE_AND_QUERYING.md](03_LOKI_LOG_STORAGE_AND_QUERYING.md)
- [04_PROMETHEUS_METRICS_AND_RECORDING_RULES.md](04_PROMETHEUS_METRICS_AND_RECORDING_RULES.md)
- [05_TEMPO_TRACING_AND_CORRELATION.md](05_TEMPO_TRACING_AND_CORRELATION.md)
- [06_GRAFANA_ENTERPRISE_SETUP_AND_RBAC.md](06_GRAFANA_ENTERPRISE_SETUP_AND_RBAC.md)
- [07_DASHBOARDS_SLOS_AND_UX_STANDARDS.md](07_DASHBOARDS_SLOS_AND_UX_STANDARDS.md)
- [08_ALERTING_ESCALATION_AND_EMAIL.md](08_ALERTING_ESCALATION_AND_EMAIL.md)
- [09_LOG_DUPLICATION_ROTATION_RETENTION.md](09_LOG_DUPLICATION_ROTATION_RETENTION.md)
- [10_SECURITY_COMPLIANCE_AND_SECRETS.md](10_SECURITY_COMPLIANCE_AND_SECRETS.md)
- [11_SCALING_HA_AND_DR.md](11_SCALING_HA_AND_DR.md)
- [12_CAPACITY_PLANNING_AND_SIZING.md](12_CAPACITY_PLANNING_AND_SIZING.md)
- [13_KUBERNETES_DEPLOYMENT_PATTERNS.md](13_KUBERNETES_DEPLOYMENT_PATTERNS.md)
- [14_OPERATIONS_RUNBOOKS.md](14_OPERATIONS_RUNBOOKS.md)
- [15_PRODUCTION_READINESS_CHECKLIST.md](15_PRODUCTION_READINESS_CHECKLIST.md)

## Suggested Learning/Implementation Path

- Phase 1: Architecture and data modeling
- Phase 2: Install stack in non-prod and validate ingestion
- Phase 3: Build golden dashboards and SLO alerts
- Phase 4: Add HA, security hardening, and retention controls
- Phase 5: Production rollout with runbooks and DR drills
