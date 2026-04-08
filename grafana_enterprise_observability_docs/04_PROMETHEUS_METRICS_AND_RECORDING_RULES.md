# Prometheus: Metrics, Recording Rules, and Alert Quality

## Core Principles
- Metrics must be dimensional but controlled.
- Scrape intervals and retention should match use case and cost.
- Alerting should be symptom-focused and actionable.

## Scrape Strategy
- Kubernetes service discovery for pods/services/nodes.
- Separate jobs for app, infra, and platform exporters.
- Use relabeling to drop volatile labels and reduce cardinality.

## Naming and Label Conventions
- Metric names: `<domain>_<resource>_<unit>` (e.g., `http_request_duration_seconds`).
- Required labels: `service`, `namespace`, `cluster`, `environment`.
- Avoid unbounded labels (user, path raw, query params).

## Recording Rules
Use recording rules to precompute expensive expressions and standardize SLO metrics.

```yaml
groups:
- name: app-slo
  interval: 30s
  rules:
  - record: service:http_request_error_rate:5m
    expr: |
      sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
      /
      sum(rate(http_requests_total[5m])) by (service)

  - record: service:http_request_p95_seconds:5m
    expr: |
      histogram_quantile(0.95,
        sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
      )
```

## Alert Rule Quality
- Use `for` durations to avoid flapping.
- Add severity levels (`warning`, `critical`).
- Include runbook URL and owner label.
- Prefer multi-window burn-rate alerts for SLOs.

## Remote Write and Long-Term Storage
- Keep local TSDB for short-to-medium retention.
- Use remote write backend for long-term analysis.
- Monitor WAL size, remote write queue, and sample drop metrics.

## Prometheus HA Pattern
- Run two identical Prometheus instances scraping same targets.
- External labels identify replica.
- De-duplicate in query layer if required.
