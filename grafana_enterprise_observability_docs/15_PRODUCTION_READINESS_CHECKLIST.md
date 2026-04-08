# Production Readiness Checklist

## Architecture and Reliability
- [ ] End-to-end telemetry flow validated under load.
- [ ] No single-point failures in Grafana/Loki/Prometheus/Tempo path.
- [ ] Backpressure and retry behavior tested for downstream outage.

## Logs (Fluent Bit + Loki)
- [ ] One collector per node/path pair confirmed.
- [ ] Tail DB persistence survives collector restart.
- [ ] Multiline parser validated for app stack traces.
- [ ] Retention tiers documented and approved.
- [ ] Duplicate detection dashboard and alert in place.

## Metrics (Prometheus)
- [ ] Cardinality budget defined per team.
- [ ] Recording rules for key SLO expressions enabled.
- [ ] HA pair deployed and de-duplication behavior understood.

## Traces (Tempo)
- [ ] Context propagation validated across services.
- [ ] Sampling policy documented for normal and incident mode.
- [ ] Log-trace and metric-trace correlation links working.

## Grafana Enterprise
- [ ] SSO enabled and local admin constrained.
- [ ] Folder/team/data source permissions enforced.
- [ ] Dashboards managed as code with review workflow.

## Alerting and Notifications
- [ ] Severity-based routing policies active.
- [ ] Email contact points tested in each environment.
- [ ] Inhibit/mute rules validated for maintenance and major incidents.
- [ ] Every critical alert includes runbook and owner labels.

## Security and Compliance
- [ ] TLS enabled for all telemetry paths.
- [ ] Secrets stored in approved secret manager.
- [ ] PII handling and retention compliant with policy.
- [ ] Audit logs enabled and retained.

## DR and Operations
- [ ] Backup/restore tested for Grafana metadata.
- [ ] Restore drill completed for telemetry backend data paths.
- [ ] Capacity alerts configured for ingestion, storage, and query latency.
- [ ] On-call team trained on runbooks.

## Go-Live Gate
Only proceed when all mandatory items are complete, validated in staging, and signed off by platform + security + service owners.
