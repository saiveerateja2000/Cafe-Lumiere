# Operations Runbooks

## Runbook: Logs Not Appearing in Grafana
1. Validate Fluent Bit pod health and restart count.
2. Check Fluent Bit output errors/retries.
3. Verify Loki ingestion rate and rejected stream metrics.
4. Run basic LogQL query for wide selector.
5. Confirm dashboard variables are not over-filtering.

## Runbook: Sudden Log Duplication Spike
1. Check for duplicate collectors or duplicated output sections.
2. Verify Fluent Bit tail DB persistence status.
3. Inspect recent config changes and rollout history.
4. Run duplicate detection query by pod and trace/message key.
5. Roll back bad config and monitor normalization.

## Runbook: Alert Storm
1. Identify top firing rules by count and source.
2. Apply temporary mute only with incident ticket.
3. Check upstream dependency outage causing cascade alerts.
4. Add/adjust inhibit rules and `for` durations.
5. Perform postmortem to tune thresholds and routing.

## Runbook: Email Notifications Not Delivered
1. Test SMTP connectivity from Grafana pod.
2. Validate credentials, TLS mode, sender policy.
3. Check Grafana notification logs and queue state.
4. Verify recipient list and organization spam policies.
5. Trigger test alert and confirm delivery latency.

## Runbook: Loki Query Latency High
1. Check query frontend/querier CPU and memory.
2. Inspect expensive regex queries and wide time ranges.
3. Review cache hit ratio.
4. Scale query path or optimize query patterns.
5. Add recording-style log metrics for expensive recurring queries.

## Runbook Governance
- Every alert must map to a runbook section.
- Runbooks must include owner and last-reviewed date.
- Review after each high-severity incident.
