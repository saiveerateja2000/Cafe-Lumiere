# Fluent Bit: Collection, Parsing, and Delivery

## Role in the Stack
Fluent Bit is the edge collector. It runs close to workloads, reads container logs, enriches data, and forwards logs to Loki with resilience controls.

## Kubernetes Deployment Model
- Run as a DaemonSet (one pod per node).
- Mount `/var/log/containers`, `/var/log/pods`, and runtime-specific log paths.
- Use Kubernetes filter plugin to enrich with namespace/pod/container labels.

## Core Pipeline Stages

### Input
- Tail plugin for container logs.
- Configure multiline parsing for stack traces and Java/Python errors.
- Persist read offsets using storage DB to survive pod restarts.

### Filter
- Kubernetes metadata enrichment.
- Parser filters for JSON logs.
- Record modifier for stable service/environment labels.
- Optional grep/drop filters for noisy health checks.

### Output
- Loki output with sane label strategy.
- Retry with exponential backoff.
- TLS enabled for transport security.

## Critical Production Settings
- `Mem_Buf_Limit`: prevent OOM during downstream outages.
- Filesystem buffering enabled for backpressure tolerance.
- `Skip_Long_Lines`: avoid parser lockups.
- `Refresh_Interval` tuned to balance discovery speed vs overhead.

## Example Config Skeleton
```ini
[SERVICE]
    Flush         1
    Daemon        Off
    Log_Level     info
    Parsers_File  parsers.conf
    storage.path  /var/log/flb-storage
    storage.sync  normal

[INPUT]
    Name              tail
    Path              /var/log/containers/*.log
    Parser            cri
    Tag               kube.*
    Mem_Buf_Limit     50MB
    Skip_Long_Lines   On
    DB                /var/log/flb-storage/tail.db
    storage.type      filesystem

[FILTER]
    Name                kubernetes
    Match               kube.*
    Merge_Log           On
    Keep_Log            Off
    K8S-Logging.Parser  On

[OUTPUT]
    Name          loki
    Match         kube.*
    Host          loki-gateway.observability.svc
    Port          3100
    Labels        job=fluentbit,cluster=prod
    Line_Format   json
    Auto_Kubernetes_Labels Off
```

## Duplicate Log Prevention
- Ensure only one collector per node/path pair.
- Do not run Fluent Bit and Promtail on same container log files unless intentionally split.
- Keep stable tail database path and hostPath persistence.
- Avoid duplicated outputs in config merges.

## Validation Checklist
- New pod logs appear in Loki within expected delay.
- Metadata fields (`namespace`, `pod`, `container`) are present.
- No rapid re-read of old files after Fluent Bit restart.
- Buffer usage remains below threshold during peak traffic.
