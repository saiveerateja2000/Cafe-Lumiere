from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Topic:
    domain: str
    name: str
    compare_to: str
    primary_goal: str
    key_metrics: str
    common_issue: str
    first_triage: str
    security_focus: str
    cost_focus: str
    practical_action: str


THEORY_TEMPLATES = [
    ("What problem does {name} solve in a production cloud architecture?", "purpose"),
    ("How is {name} different from {compare_to}, and when would you choose each?", "comparison"),
    ("What are the most important limits, quotas, or scaling boundaries for {name}?", "limits"),
    ("What reliability patterns should be applied when designing with {name}?", "reliability"),
    ("What are common anti-patterns teams make when adopting {name}?", "antipatterns"),
    ("How do you secure {name} following least-privilege and defense-in-depth?", "security"),
]

PRACTICAL_TEMPLATES = [
    ("How would you configure {name} for a workload focused on {primary_goal}?", "configuration"),
    ("Which operational metrics and alerts would you set for {name}?", "metrics"),
    ("What day-2 runbook tasks are essential to keep {name} healthy?", "runbook"),
    ("How would you reduce cost for {name} without hurting reliability?", "cost"),
    ("What deployment strategy lowers risk when changing {name} settings in production?", "deployment"),
    ("How do you test failover and recovery behavior for {name}?", "dr-test"),
    ("Which logs or traces do you inspect first while debugging {name}?", "debug"),
]

SCENARIO_TEMPLATES = [
    ("Your team reports an outage related to {name}. What do you do in the first 15 minutes?", "incident"),
    ("Latency suddenly increases after a change in {name}. How do you isolate root cause?", "latency"),
    ("A security review flags risk in {name}. What immediate and long-term fixes do you implement?", "security-risk"),
    ("Traffic doubles overnight and {name} becomes a bottleneck. What is your scaling approach?", "scale"),
    ("A rollback is needed after changing {name}. How do you roll back safely with minimal impact?", "rollback"),
    ("An auditor asks for evidence of governance around {name}. What artifacts do you provide?", "audit"),
    ("A junior engineer misconfigures {name} in production. How do you recover and prevent recurrence?", "misconfig"),
]


def make_answer(topic: Topic, style: str, focus: str) -> str:
    if style == "Theory":
        if focus == "purpose":
            return f"Use {topic.name} to achieve {topic.primary_goal}. In real systems it is part of a broader reliability model, not a standalone fix."
        if focus == "comparison":
            return f"Choose {topic.name} when you need stronger support for {topic.primary_goal}; use {topic.compare_to} when the requirement is simpler or lower-level. The decision should be based on latency, operability, and team expertise."
        if focus == "limits":
            return f"Track service quotas and soft limits early, then alarm on {topic.key_metrics}. Capacity planning should include burst behavior and regional failure assumptions."
        if focus == "reliability":
            return f"Apply multi-AZ design, graceful degradation, and tested rollback paths around {topic.name}. Reliability is proven only after game days and failure injection exercises."
        if focus == "antipatterns":
            return f"A frequent anti-pattern is {topic.common_issue}. Prevent it with standards, policy-as-code checks, and peer review before production rollout."
        if focus == "security":
            return f"Secure {topic.name} through {topic.security_focus}. Add continuous detection so drift is caught before it becomes an incident."

    if style == "Practical":
        if focus == "configuration":
            return f"Start from a production baseline aligned to {topic.primary_goal}, then apply {topic.practical_action}. Validate the setup in staging under load before go-live."
        if focus == "metrics":
            return f"Use golden signals plus domain KPIs: {topic.key_metrics}. Alert on sustained deviation and map every alarm to a documented runbook action."
        if focus == "runbook":
            return f"Your day-2 runbook should cover health verification, safe config rollout, backup checks, and periodic access review. Explicitly include steps to detect {topic.common_issue}."
        if focus == "cost":
            return f"Optimize spend with {topic.cost_focus}, but gate changes with SLO checks so cost savings do not degrade availability or performance."
        if focus == "deployment":
            return f"Use progressive delivery (canary/blue-green), define rollback triggers, and keep previous known-good configuration ready for immediate restore."
        if focus == "dr-test":
            return f"Run controlled DR tests that simulate AZ failure, dependency timeout, and partial data loss. Measure recovery against explicit RTO/RPO targets."
        if focus == "debug":
            return f"Start with recent changes, then correlate logs, metrics, and traces. Prioritize evidence around {topic.first_triage} to reduce mean-time-to-resolution."

    if focus == "incident":
        return f"First stabilize: {topic.first_triage}. Freeze risky deploys, communicate incident status, and restore service before deep root-cause analysis."
    if focus == "latency":
        return f"Compare baseline vs current latency, inspect saturation indicators ({topic.key_metrics}), and isolate whether the bottleneck is compute, network, storage, or config drift."
    if focus == "security-risk":
        return f"Apply immediate containment (block exposure, rotate credentials, enforce least privilege), then implement long-term controls using {topic.security_focus}."
    if focus == "scale":
        return f"Scale horizontally where possible, pre-warm dependent layers, and tune queue/backpressure behavior. Validate headroom with production-like load tests."
    if focus == "rollback":
        return f"Rollback using immutable artifacts and known-good config snapshots. Confirm data compatibility first to avoid rollback-induced corruption."
    if focus == "audit":
        return f"Provide policy definitions, change history, monitoring dashboards, and incident postmortems. Evidence must show both preventive controls and response effectiveness."
    return f"Recover safely, document the sequence of failure, and add guardrails (tests, policy checks, approval gates) so {topic.common_issue} cannot reoccur unnoticed."


def build_topic_questions(topic: Topic, count: int) -> List[tuple[str, str, str, str, str]]:
    # Mix: 35% theory, 35% practical, 30% scenario
    theory_count = round(count * 0.35)
    practical_count = round(count * 0.35)
    scenario_count = count - theory_count - practical_count

    rows: List[tuple[str, str, str, str, str]] = []

    for i in range(theory_count):
        q_template, focus = THEORY_TEMPLATES[i % len(THEORY_TEMPLATES)]
        q = q_template.format(
            name=topic.name,
            compare_to=topic.compare_to,
            primary_goal=topic.primary_goal,
            key_metrics=topic.key_metrics,
            common_issue=topic.common_issue,
            security_focus=topic.security_focus,
        )
        rows.append((topic.domain, topic.name, "Theory", q, focus))

    for i in range(practical_count):
        q_template, focus = PRACTICAL_TEMPLATES[i % len(PRACTICAL_TEMPLATES)]
        q = q_template.format(
            name=topic.name,
            compare_to=topic.compare_to,
            primary_goal=topic.primary_goal,
            key_metrics=topic.key_metrics,
            common_issue=topic.common_issue,
            security_focus=topic.security_focus,
        )
        rows.append((topic.domain, topic.name, "Practical", q, focus))

    for i in range(scenario_count):
        q_template, focus = SCENARIO_TEMPLATES[i % len(SCENARIO_TEMPLATES)]
        q = q_template.format(
            name=topic.name,
            compare_to=topic.compare_to,
            primary_goal=topic.primary_goal,
            key_metrics=topic.key_metrics,
            common_issue=topic.common_issue,
            security_focus=topic.security_focus,
        )
        rows.append((topic.domain, topic.name, "Scenario", q, focus))

    return rows


AWS_TOPICS = [
    Topic("AWS", "IAM", "resource-based policies", "least-privilege access control", "AccessDenied count, auth failures, role assumption rate", "overly broad wildcard permissions", "identify impacted principals and evaluate policy simulator before policy change", "MFA, scoped roles, condition keys, short-lived credentials", "remove unused roles and right-size policy scope", "permission boundaries, role separation, and periodic access reviews"),
    Topic("AWS", "VPC", "Transit Gateway", "network isolation and controlled connectivity", "flow-log rejects, route-table drift, NAT egress volume", "overlapping CIDR and asymmetric routing", "check route tables, NACLs, and SG paths hop-by-hop", "segmented subnets, NACL strategy, and private endpoints", "VPC endpoints and NAT optimization", "multi-AZ subnet design and explicit routing standards"),
    Topic("AWS", "ALB", "NLB", "Layer-7 intelligent traffic routing", "target 5xx, target response time, healthy host count", "health checks pointing to unstable endpoints", "verify health check path, target health, and recent deploy changes", "WAF integration, TLS policies, and strict listener rules", "optimize idle timeout and right-size target groups", "blue/green with weighted routing and canary rules"),
    Topic("AWS", "EKS", "self-managed Kubernetes", "managed Kubernetes control plane operations", "pod restarts, node pressure, API server latency", "missing resource limits and weak autoscaling configuration", "inspect failing workloads, events, and node conditions", "IRSA, network policies, secrets encryption, least-privileged service accounts", "cluster autoscaler tuning and spot/on-demand mix", "versioned manifests, HPA/VPA strategy, and PDB enforcement"),
    Topic("AWS", "EC2", "AWS Lambda", "compute flexibility for long-running workloads", "CPU steal, memory pressure, status check failures", "instance type mismatch and missing patching process", "check system logs, status checks, and recent AMI changes", "IMDSv2, SSM Session Manager, minimal open ports", "rightsizing and savings plans", "golden AMI pipeline and immutable replacement"),
    Topic("AWS", "S3", "EFS", "durable object storage", "4xx/5xx rates, replication lag, request latency", "public bucket exposure and missing lifecycle policies", "validate bucket policy, block-public-access, and access logs", "SSE-KMS, bucket policy conditions, object lock where needed", "lifecycle tiering and intelligent-tiering", "versioning, replication, and bucket policy-as-code"),
    Topic("AWS", "Networking", "service mesh", "reliable east-west and north-south connectivity", "packet loss, DNS latency, connection resets", "DNS misconfiguration and MTU mismatch", "trace DNS, route path, and TCP handshake failures", "segmentation, TLS in transit, and egress controls", "optimize data transfer paths and endpoint usage", "standardized DNS, CIDR planning, and connectivity tests"),
    Topic("AWS", "RDS", "Aurora", "managed relational persistence", "CPU, free storage, replica lag, deadlocks", "long-running transactions and missing indexes", "check slow query logs and replication health", "encryption at rest, TLS, IAM auth where applicable", "reserved instances and storage optimization", "parameter group control and automated backups/failover drills"),
    Topic("AWS", "DocumentDB", "MongoDB self-hosted", "document data model at scale", "connections, read/write latency, replication lag", "schema bloat and unbounded document growth", "review query plans and connection pool saturation", "VPC isolation, TLS, secrets rotation", "instance class sizing and retention policy tuning", "index governance and workload-specific read scaling"),
    Topic("AWS", "CloudWatch", "open-source Prometheus stack", "centralized metrics, logs, and alarms", "alarm noise ratio, ingestion lag, dashboard freshness", "high-cardinality logs without retention strategy", "validate alarm thresholds and noisy dimensions", "log encryption, access controls, and auditability", "retention tuning and log class optimization", "SLO-based alerting and dashboard ownership"),
    Topic("AWS", "CloudTrail", "AWS Config", "API activity audit and governance traceability", "trail coverage, delivery failures, suspicious API calls", "single-region trails and disabled log validation", "confirm org trail status and S3 delivery integrity", "immutable log storage and least-privilege read access", "lifecycle policy for old audit data", "org-wide multi-region trail with centralized archive"),
    Topic("AWS", "Security Groups", "NACLs", "stateful instance-level traffic filtering", "rejected connections, unexpected open ports", "allow-all ingress and stale rules", "trace source-destination-port path and evaluate SG refs", "least-open ports and SG referencing patterns", "clean stale rules and consolidate SG sets", "policy-driven SG templates and review cadence"),
    Topic("AWS", "EBS", "instance store", "durable block storage for EC2", "volume queue length, burst balance, IO latency", "wrong volume type for IO profile", "inspect CloudWatch IO metrics and instance throughput limits", "encryption and snapshot controls", "gp3 tuning and snapshot lifecycle", "throughput/IOPS baselines and restore playbooks"),
    Topic("AWS", "Route 53", "third-party DNS", "highly available DNS and health-based routing", "DNS query latency, health check status, failover events", "long TTLs slowing failover", "verify health checks, resolver behavior, and record policy", "DNSSEC, restricted change controls", "right-size health checks and TTL strategy", "policy-based routing with tested failover"),
    Topic("AWS", "Auto Scaling", "manual scaling", "elastic capacity for variable traffic", "scaling activity success rate, cooldown conflicts", "aggressive thresholds causing thrash", "inspect scaling history and metric behavior", "safe rollout with capacity headroom and alarms", "predictive scaling and spot diversification", "target tracking with warm-up and guardrails"),
]

K8S_TOPICS = [
    Topic("Kubernetes", "Pods", "VM-based deployments", "workload runtime encapsulation", "restart count, OOM kills, pending duration", "missing requests/limits", "describe pod events and node resource pressure", "securityContext, image policy, least privilege", "bin-packing with requests and autoscaling", "liveness/readiness/startup probes and budget controls"),
    Topic("Kubernetes", "Deployments", "StatefulSets", "declarative stateless rollout management", "rollout status, unavailable replicas, surge pressure", "misconfigured rolling update strategy", "check rollout history and failing replica set", "image provenance and admission controls", "optimize surge/unavailable and image pull policy", "progressive delivery with canary and rollback hooks"),
    Topic("Kubernetes", "StatefulSets", "Deployments", "stable identity for stateful workloads", "PVC binding delays, ordered pod startup issues", "improper storage class assumptions", "inspect PVC events and storage backend health", "encryption and restricted storage access", "volume reclaim policy and capacity planning", "pod management policy and backup validation"),
    Topic("Kubernetes", "Services", "Ingress", "stable service discovery and virtual IP routing", "service latency, endpoint availability", "selector mismatch and empty endpoints", "verify endpoint objects and kube-proxy behavior", "network policy enforcement", "optimize internal traffic paths", "clear service ownership and port conventions"),
    Topic("Kubernetes", "Ingress", "Service mesh gateway", "HTTP routing and TLS termination", "4xx/5xx at ingress, cert expiration", "incorrect host/path rules", "check ingress controller logs and backend health", "TLS policy and WAF/security headers", "consolidate rules and reduce duplicate paths", "versioned ingress manifests and staged rollout"),
    Topic("Kubernetes", "ConfigMaps and Secrets", "hardcoded app config", "externalized configuration management", "config reload errors, secret access failures", "stale config and secret sprawl", "verify mounts/env injection and app reload behavior", "secret encryption and RBAC minimization", "remove unused config and rotate secrets", "immutable config patterns and rollout triggers"),
    Topic("Kubernetes", "RBAC", "coarse cluster-admin access", "fine-grained authorization", "forbidden API errors, policy violation count", "overuse of cluster-admin", "audit denied calls and role bindings", "least privilege roles and namespace boundaries", "periodic access cleanup", "role templates and review automation"),
    Topic("Kubernetes", "Network Policies", "open east-west traffic", "pod-level traffic segmentation", "unexpected connection drops, policy denies", "default allow assumptions", "test allowlist path from source to destination", "default deny and explicit allow", "minimize policy sprawl", "policy testing in CI before production"),
]

DOCKER_TOPICS = [
    Topic("Docker", "Images", "VM templates", "portable app packaging", "image size, CVE count, pull latency", "bloated multi-purpose images", "inspect layers and base image pedigree", "minimal base images and image signing", "multi-stage builds", "repeatable Dockerfile standards"),
    Topic("Docker", "Containers", "processes on host", "isolated runtime execution", "restart loops, memory limits, exit codes", "running multiple concerns in one container", "inspect logs, health checks, and exit reasons", "drop capabilities and non-root users", "resource limits and right-sized runtime", "one-process principle and health probes"),
    Topic("Docker", "Networking", "host-only networking", "service connectivity between containers", "dns resolution failures, port collisions", "implicit network assumptions", "inspect bridge/overlay config and DNS", "network segmentation and restricted publishes", "remove unused published ports", "explicit network contracts and naming"),
    Topic("Docker", "Volumes", "ephemeral container filesystem", "persistent state and data sharing", "io latency, orphan volume growth", "assuming container fs is durable", "check mount targets and filesystem permissions", "encryption and access restrictions", "volume lifecycle cleanup", "backup/restore practice and retention rules"),
    Topic("Docker", "Registry and Supply Chain", "manual artifact sharing", "trusted image distribution", "failed pulls, signature verification failures", "tag drift and mutable release tags", "validate digest pinning and registry availability", "signed images and scanning gates", "retention policies and cache efficiency", "digest-based deployment with policy checks"),
]

PYTHON_TOPICS = [
    Topic("Python", "Data Structures", "naive list-only approach", "efficient in-memory data handling", "runtime complexity, memory usage", "using O(n^2) patterns unknowingly", "profile hotspot functions and input size", "input validation and safe parsing", "choose optimal structures", "clear complexity-aware implementations"),
    Topic("Python", "Functions and OOP", "script-only coding", "modular and maintainable design", "cyclomatic complexity, test pass rate", "god classes and side effects", "isolate behavior and add tests", "encapsulation and type hints", "refactor duplicated logic", "small focused classes/functions"),
    Topic("Python", "Concurrency", "single-threaded blocking", "parallelism and responsive IO", "queue depth, timeout rate", "blocking network calls without timeouts", "capture stack traces and event loop lag", "safe shared state and timeouts", "async where IO-bound", "bounded worker pools and retries"),
    Topic("Python", "Error Handling", "silent failures", "resilient and observable execution", "exception rate, retry success", "blanket except without context", "log tracebacks with correlation ids", "sanitize sensitive logs", "handle only expected exceptions", "typed exceptions and fallback logic"),
    Topic("Python", "Testing and Packaging", "manual validation", "confidence in releases", "unit test coverage, flaky tests", "no dependency pinning", "reproduce failures in CI", "supply-chain pinning and scanning", "cache dependencies and isolate envs", "pytest strategy and reproducible builds"),
]

SQL_TOPICS = [
    Topic("SQL", "Query Optimization", "unindexed full scans", "fast and predictable queries", "query latency, rows scanned", "missing or wrong indexes", "run EXPLAIN and inspect execution plan", "least-privilege DB access", "archive cold data and optimize indexes", "sargable predicates and index-aware joins"),
    Topic("SQL", "Transactions and Isolation", "autocommit-only workflow", "data correctness under concurrency", "deadlocks, lock wait time", "long transactions blocking writers", "inspect lock graph and offending sessions", "role separation and audit logging", "short transactions and batch tuning", "idempotent writes and retry-safe logic"),
    Topic("SQL", "Schema Design and Analytics", "flat unnormalized schema", "maintainable OLTP and analytics", "table bloat, null ratio, query complexity", "over-normalization or uncontrolled denormalization", "review access patterns and storage growth", "column-level controls for sensitive fields", "partitioning and retention policies", "balanced normalization with targeted materialization"),
]


def build_bank() -> List[tuple[int, str, str, str, str, str]]:
    rows: List[tuple[int, str, str, str, str, str]] = []
    counter = 1

    for topic in AWS_TOPICS:
        for domain, name, kind, q, focus in build_topic_questions(topic, count=20):
            rows.append((counter, domain, name, kind, q, make_answer(topic, kind, focus)))
            counter += 1

    for topic in K8S_TOPICS:
        for domain, name, kind, q, focus in build_topic_questions(topic, count=15):
            rows.append((counter, domain, name, kind, q, make_answer(topic, kind, focus)))
            counter += 1

    for topic in DOCKER_TOPICS:
        for domain, name, kind, q, focus in build_topic_questions(topic, count=10):
            rows.append((counter, domain, name, kind, q, make_answer(topic, kind, focus)))
            counter += 1

    for topic in PYTHON_TOPICS:
        for domain, name, kind, q, focus in build_topic_questions(topic, count=10):
            rows.append((counter, domain, name, kind, q, make_answer(topic, kind, focus)))
            counter += 1

    for topic in SQL_TOPICS:
        for domain, name, kind, q, focus in build_topic_questions(topic, count=10):
            rows.append((counter, domain, name, kind, q, make_answer(topic, kind, focus)))
            counter += 1

    return rows


def render_markdown(rows: List[tuple[int, str, str, str, str, str]]) -> str:
    lines: List[str] = []
    lines.append("# Mega Interview Q&A Bank (550 Questions)")
    lines.append("")
    lines.append("This file contains a mixed set of theory, practical, and scenario-based questions with concise answers.")
    lines.append("")
    lines.append("## Domain Distribution")
    lines.append("- AWS: 300")
    lines.append("- Kubernetes: 120")
    lines.append("- Docker: 50")
    lines.append("- Python: 50")
    lines.append("- SQL: 30")
    lines.append("")

    current_domain = None
    for idx, domain, topic, kind, question, answer in rows:
        if domain != current_domain:
            current_domain = domain
            lines.append(f"## {domain}")
            lines.append("")
        lines.append(f"### Q{idx} [{kind}] ({topic})")
        lines.append(f"**Question:** {question}")
        lines.append(f"**Answer:** {answer}")
        lines.append("")

    return "\n".join(lines)


def render_index() -> str:
    return """# Mega Question Bank

Generated interview prep resources:

- `MEGA_INTERVIEW_QA_550.md` — 550 questions with answers across AWS, Kubernetes, Docker, Python, and SQL.
- `generate_qa_bank.py` — generator used to build the bank.

## Recommended Study Flow
1. Start with AWS sections (Q1–Q300).
2. Move to Kubernetes + Docker (Q301–Q470).
3. Finish with Python + SQL (Q471–Q550).
4. Practice 15 scenario questions daily and answer them aloud in STAR format.
"""


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    rows = build_bank()
    if len(rows) != 550:
        raise RuntimeError(f"Expected 550 questions, got {len(rows)}")

    md = render_markdown(rows)
    (out_dir / "MEGA_INTERVIEW_QA_550.md").write_text(md, encoding="utf-8")
    (out_dir / "README.md").write_text(render_index(), encoding="utf-8")


if __name__ == "__main__":
    main()
