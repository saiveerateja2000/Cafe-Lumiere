# Tempo: Tracing, Sampling, and Correlation

## Why Tempo
Tempo provides cost-efficient distributed tracing with object storage and tight Grafana integration for logs-metrics-traces correlation.

## Ingestion Architecture
- Instrument applications with OpenTelemetry SDK.
- Export OTLP traces to Tempo (direct or through OpenTelemetry Collector).
- Store trace blocks in object storage.

## Sampling Strategy
- Head-based sampling for baseline cost control.
- Tail-based sampling (via OTel Collector) for error/high-latency bias.
- Keep near-100% sampling during controlled incident windows if possible.

## Instrumentation Requirements
- Propagate trace context across service calls.
- Include `service.name`, `deployment.environment`, `version` resource attrs.
- Capture key spans: inbound request, DB calls, external API calls.

## Correlation in Grafana
- Add trace ID in structured logs.
- Configure derived fields in Loki to link trace IDs to Tempo.
- Expose exemplars from Prometheus histograms to traces.

## Query and Retention Considerations
- Tune search limits and span attribute indexing scope.
- Keep short high-resolution retention and longer reduced-fidelity retention if needed.
- Track ingest errors, block flush delays, and query latency.

## Common Pitfalls
- Missing context propagation results in broken traces.
- Overly high span attribute cardinality inflates storage and search costs.
- No consistent service naming breaks topology view.
