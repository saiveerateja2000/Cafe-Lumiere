# Capacity Planning and Sizing

## What to Measure First
- Log ingestion rate (MB/s and lines/s).
- Active log streams and label cardinality.
- Prometheus active series and sample ingestion rate.
- Tempo spans/s and average span size.

## Baseline Formula Examples
- Daily logs: `ingest_mb_per_sec * 86400 / 1024` (GB/day).
- Storage estimate: `daily_volume * retention_days * compression_factor_adjustment`.
- Prometheus samples/day: `targets * metrics_per_target * (86400/scrape_interval_seconds)`.

## Practical Sizing Process
1. Measure current telemetry for 7-14 days.
2. Add peak multiplier (2x to 3x) for incident bursts.
3. Add growth factor for 6-12 months.
4. Add resilience headroom (20-30%).

## Cost Drivers
- Loki cardinality and retention windows.
- Prometheus high-frequency scrape jobs.
- Tempo sampling rate and retained trace volume.
- Grafana query concurrency and reporting workloads.

## Optimization Techniques
- Drop low-value logs at edge (Fluent Bit filters).
- Convert expensive PromQL into recording rules.
- Use selective tracing sampling.
- Enforce label governance policy.

## Capacity Alerts
- Ingestion rejected samples/logs.
- Queue backlogs and buffer saturation.
- Query p95 latency and timeout rates.
- Storage growth vs retention budget.
