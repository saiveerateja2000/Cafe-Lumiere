# Log Duplication, Rotation, and Retention Controls

## Log Duplication: Root Causes
- Multiple collectors tailing same files.
- Fluent Bit position DB reset/loss.
- Container runtime log rewrite after node restart.
- Duplicate output blocks or mirror pipelines not deduplicated.

## Duplication Prevention
- One primary node collector per path.
- Persist Fluent Bit tail DB on hostPath.
- Use stable stream labels and ingestion path.
- Protect config from duplicate includes.

## Rotation Mechanics (Kubernetes)
- Container runtimes rotate logs by size/time.
- Collector must handle file rename/truncate safely.
- Tune scanner and rotate_wait settings to avoid missed lines.

## Rotation Best Practices
- Keep max file size small enough for rapid shipping.
- Keep enough rotated files to absorb downstream outages.
- Validate multiline parser behavior across rotation boundaries.

## Retention Strategy
- Tier 1 (hot, high-value logs): 7-30 days.
- Tier 2 (operational logs): 30-90 days.
- Tier 3 (audit/compliance): 180+ days as policy requires.
- Use tenant/stream-based retention overrides in Loki.

## Data Lifecycle Governance
- Classify logs by sensitivity and legal obligation.
- Enforce deletion windows and document exceptions.
- Audit retention policy changes.

## Verification Tests
- Forced log rotation during peak traffic.
- Collector restart test without replay storms.
- Duplicate detection query baseline.

## Duplicate Detection Query Examples
```logql
sum by (pod) (count_over_time({cluster="prod", service="order-service"} [1m]))

{cluster="prod", service="order-service"} | json | line_format "{{.trace_id}} {{.message}}"
```
