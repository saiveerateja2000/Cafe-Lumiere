# Alerting, Escalation, and Email Delivery

## Alert Design Principles
- Alert on user impact and SLO violations first.
- Keep alert messages actionable: what, impact, owner, runbook.
- Use severity levels and explicit escalation paths.

## Grafana Unified Alerting Components
- Rules: expressions evaluated at intervals.
- Contact points: email, webhook, PagerDuty/ops tools.
- Notification policies: routing by labels (`team`, `severity`, `env`).
- Mute timings: maintenance windows.

## Email Configuration Essentials
- SMTP endpoint with TLS.
- Dedicated sender identity (e.g., observability@company).
- Distribution lists per team and escalation tier.
- Test email alerts in every environment.

## Routing Example
- `severity=critical, env=prod` → on-call + email + incident channel.
- `severity=warning, env=prod` → team email + work queue.
- `env=stage` → non-paging channel only.

## Alert Noise Reduction
- Use `for` durations and grouping.
- Add inhibit rules (suppress downstream alerts during root outage).
- Create dedup keys in notification templates.

## Escalation Model
- L1: primary on-call (5 min acknowledgment).
- L2: secondary on-call (15 min).
- L3: engineering manager/platform lead.
- Post-incident review required for missed/late alerts.

## Minimum Alert Set for Go-Live
- Service error-rate and latency SLO burn alerts.
- Pod crashloop and unavailable replicas.
- Loki/Prometheus/Tempo ingestion failures.
- Alert queue backlog and notification failures.
