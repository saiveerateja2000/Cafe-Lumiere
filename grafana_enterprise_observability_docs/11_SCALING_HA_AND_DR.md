# Scaling, High Availability, and Disaster Recovery

## HA Targets
- No single point of failure in ingestion, storage, query, or alerting path.
- Survive single-node and single-zone failures without major telemetry loss.

## Component-Level HA
- Fluent Bit: DaemonSet auto-reschedules; local buffering for transient failures.
- Loki: distributed mode with replicated ingesters and object storage.
- Prometheus: HA pair with identical scrape configs.
- Tempo: replicated ingestion path and object storage backend.
- Grafana: multiple replicas behind load balancer with shared DB/session strategy.

## Scaling Levers
- Horizontal scaling for query and ingestion components.
- Partition by tenant/environment.
- Caching layers for hot queries.
- Apply rate limits to protect control plane.

## DR Strategy
- Define RPO/RTO per signal and per environment.
- Cross-region backup for config, metadata DB, and object storage.
- Regular restore drills and validation dashboards.

## Backup Scope
- Grafana metadata database.
- Provisioning files and IaC repository.
- Loki/Tempo object storage lifecycle policies.
- Alert routing configuration exports.

## Failure Scenarios to Drill
- Loki object storage outage.
- Prometheus disk full / WAL corruption.
- Grafana DB failure.
- SMTP provider outage affecting alerts.

## Success Criteria
- Alerting path recovers within RTO.
- No silent telemetry loss beyond agreed error budget.
- Runbooks produce consistent, audited recovery actions.
