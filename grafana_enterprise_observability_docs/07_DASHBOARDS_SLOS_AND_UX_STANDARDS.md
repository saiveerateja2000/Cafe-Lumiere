# Dashboards, SLOs, and UX Standards

## Dashboard Taxonomy
- Executive: service health and SLO state.
- Service owner: latency, error rate, throughput, saturation.
- Platform: cluster, node, and telemetry pipeline health.
- Incident: short time-range triage with logs/metrics/traces links.

## Golden Dashboard Template
1. Service Overview (traffic, error, latency, saturation).
2. Dependency Health (DB/cache/external APIs).
3. Resource Usage (CPU/memory/restarts).
4. Logs Panel (Loki query pre-filtered by service).
5. Trace Panel (Tempo search for top failing spans).

## SLO Dashboard Elements
- SLO target and current compliance.
- Error budget remaining.
- Burn rate (fast/slow windows).
- Active SLO alerts and owning team.

## Design Standards
- Standard variables: `cluster`, `namespace`, `service`, `environment`.
- Consistent units and legend formats.
- No ambiguous colors; use consistent severity mapping.
- Add panel descriptions and runbook links.

## Anti-Patterns to Avoid
- Overloaded dashboards with too many panels.
- Missing time-window context for percentiles.
- Mixed environments on same dashboard without explicit filter.

## Release Process
- Dashboard changes via Git PR.
- Peer review for query efficiency and alert impact.
- Validate in staging with realistic load.
