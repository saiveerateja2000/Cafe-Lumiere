# Architecture and Data Flow

## Reference Architecture

### Signal Types
- Logs: emitted to stdout/stderr by app containers, collected via Fluent Bit.
- Metrics: scraped by Prometheus from application and infrastructure endpoints.
- Traces: emitted by instrumented applications via OpenTelemetry to Tempo.

### End-to-End Flow
1. App pods emit logs, metrics, traces.
2. Fluent Bit daemonset tails node log files and enriches with Kubernetes metadata.
3. Fluent Bit forwards logs to Loki using tenant-aware labels.
4. Prometheus scrapes pod/service/node exporters and stores TSDB blocks.
5. OpenTelemetry SDK/collector sends traces to Tempo.
6. Grafana queries Loki/Prometheus/Tempo and renders dashboards.
7. Grafana Unified Alerting evaluates rules and routes notifications (email/webhook/on-call).

## Data Path Boundaries

### Control Plane
- Helm/Kustomize/Terraform provisioning.
- Secret and config management.
- SSO, RBAC, folder/data source permissions.

### Data Plane
- Collectors and telemetry transport.
- Backend ingestion and storage engines.
- Query path and alert evaluation.

## Environment Separation
- Separate namespaces and storage per environment.
- Use distinct Loki tenants and Prometheus external labels.
- Keep alert channels environment-specific to avoid paging from non-prod.

## Reliability Principles
- At-least-once shipping for logs with idempotent query patterns.
- Backpressure-aware buffering in Fluent Bit.
- HA configuration for Loki/Prometheus/Tempo/Grafana in production.
- Retention and compaction tuned per signal criticality.

## Golden Signals and Ownership
- Latency, traffic, errors, saturation per service.
- Assign dashboard and alert ownership per team.
- Define SLOs and escalation policy before production rollout.

## Minimal Production Topology
- Fluent Bit as DaemonSet on all worker nodes.
- Loki distributed mode with object storage for chunks/index.
- Prometheus with HA pair and alertmanager-compatible route model via Grafana alerting.
- Tempo with object storage backend.
- Grafana Enterprise with external database and persistent provisioning.
