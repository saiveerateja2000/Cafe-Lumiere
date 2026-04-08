# Loki: Log Storage, Query, and Retention

## Loki Architecture (Production)
- Distributor: receives log streams.
- Ingester: buffers and flushes chunks.
- Querier/query-frontend: executes LogQL with caching.
- Compactor: enforces retention and index/chunk lifecycle.
- Object storage backend (S3/GCS/Azure Blob) for durable scaling.

## Label Strategy (Most Important Design Choice)

### Good Labels
- Low-cardinality, stable values: `cluster`, `namespace`, `service`, `environment`.

### Avoid as Labels
- Request IDs, user IDs, session IDs, IP addresses (high-cardinality).
- Put these in log body and filter with LogQL parsers.

## Retention Model
- Use retention by tenant and stream selectors.
- Define shorter retention for debug logs, longer for audit/security logs.
- Validate legal/compliance requirements before deleting logs.

## Example Query Patterns
```logql
{cluster="prod", namespace="payments", level="error"}

{service="order-service"} |= "timeout" | json | duration_ms > 500

sum by (service) (count_over_time({cluster="prod"} |= "ERROR" [5m]))
```

## Ingestion and Query Limits
- Set per-tenant ingestion rate and burst limits.
- Cap max streams per tenant to prevent runaway cardinality.
- Configure query timeout, max query parallelism, and split intervals.

## Common Failure Modes
- Out-of-order entries from misaligned timestamps.
- High cardinality causing memory pressure and slow queries.
- Excessive regex use in LogQL causing expensive scans.

## Operational Practices
- Enable query-frontend caching.
- Run canary log producers to detect ingestion stalls.
- Track ingest rate, rejected samples, and query p95 latency.
