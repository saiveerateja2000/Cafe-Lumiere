# Mock Interview Pack (25 Rounds)

Each round includes:
- Primary scenario prompt
- Follow-up cross-questions (AWS + K8s/Docker + Python + SQL)
- What a strong answer should cover

---

## Round 1 — IAM Access Outage
**Prompt:** A deployment pipeline suddenly gets `AccessDenied` while pushing to S3 and updating EKS manifests.
**Follow-ups:**
1. How do you isolate if failure is trust policy vs permission policy?
2. What CloudTrail events do you check first?
3. How do you prevent recurrence in CI/CD?
**Strong answer should cover:** policy simulator, recent IAM diff, role assumption chain, least privilege refactor, policy-as-code checks, break-glass role.

## Round 2 — VPC Connectivity Failure
**Prompt:** App pods in private subnet cannot reach RDS after a route table update.
**Follow-ups:**
1. SG vs NACL vs route-table check order?
2. How do VPC Flow Logs help?
3. What rollback plan do you execute?
**Strong answer should cover:** hop-by-hop path validation, CIDR overlap checks, immediate rollback, route guardrails and automated tests.

## Round 3 — ALB 5xx Spike
**Prompt:** ALB target 5xx spikes right after a release.
**Follow-ups:**
1. Difference between ALB 502 and 503 in triage?
2. Which metrics + logs correlate fastest?
3. Canary strategy to recover safely?
**Strong answer should cover:** target health check verification, app logs correlation, weighted traffic rollback, postmortem with release gates.

## Round 4 — EKS Pod CrashLoop
**Prompt:** Critical service in EKS enters `CrashLoopBackOff` after config change.
**Follow-ups:**
1. First 3 kubectl commands?
2. Probe tuning strategy?
3. How do you protect from same config error later?
**Strong answer should cover:** events/logs/env checks, startup/readiness probe fixes, config validation in CI, staged rollout.

## Round 5 — EC2 Cost Explosion
**Prompt:** Monthly compute cost rises 35% with no traffic increase.
**Follow-ups:**
1. Which reports identify waste fastest?
2. Rightsizing path with low risk?
3. Savings Plans selection method?
**Strong answer should cover:** Cost Explorer + utilization trend, instance family fit analysis, phased rightsizing, commitment based on baseline load.

## Round 6 — S3 Data Exposure Incident
**Prompt:** Sensitive bucket accidentally became public for 20 minutes.
**Follow-ups:**
1. Immediate containment sequence?
2. How to estimate blast radius?
3. Long-term controls?
**Strong answer should cover:** block-public-access enforcement, access log review, object access audit, SCP/config rule guardrails.

## Round 7 — RDS Slow Query Crisis
**Prompt:** Checkout API latency rises; root cause appears DB related.
**Follow-ups:**
1. What in `EXPLAIN` is red flag?
2. Index vs query rewrite decision?
3. How to validate fix safely?
**Strong answer should cover:** rows scanned and join strategy, targeted indexing, canary release + before/after p95.

## Round 8 — DocumentDB Connection Saturation
**Prompt:** API nodes hit connection limits on DocumentDB.
**Follow-ups:**
1. App-level pooling fixes?
2. Query/index hygiene checks?
3. Read scaling approach?
**Strong answer should cover:** connection pool bounds, long query detection, index plan review, reader endpoint usage.

## Round 9 — CloudWatch Alert Noise
**Prompt:** Team ignores alerts due to excessive false positives.
**Follow-ups:**
1. Alarm redesign principles?
2. Composite alarms where useful?
3. SLO-based alert example?
**Strong answer should cover:** symptom-focused alerting, actionable thresholds, dedupe/escalation, error-budget tie-in.

## Round 10 — CloudTrail Governance Gap
**Prompt:** Audit finds some accounts missing trail coverage.
**Follow-ups:**
1. Organization trail remediation?
2. Log integrity controls?
3. Who should access audit logs?
**Strong answer should cover:** org-level multi-region trail, log file validation, immutable archive bucket, strict read role separation.

## Round 11 — Security Group Misconfiguration
**Prompt:** Engineer opened admin port to `0.0.0.0/0` in production.
**Follow-ups:**
1. Immediate risk mitigation?
2. How to detect similar rules continuously?
3. How to enforce change approvals?
**Strong answer should cover:** revoke rule + investigate access, config/compliance alerts, IaC-only SG changes and approval workflow.

## Round 12 — EBS Throughput Bottleneck
**Prompt:** API nodes show high disk queue length, response time degrades.
**Follow-ups:**
1. Which CloudWatch disk metrics matter?
2. gp3 tuning vs io2 move?
3. Recovery without downtime?
**Strong answer should cover:** queue length + throughput + burst balance, volume performance tuning, rolling instance replacement.

## Round 13 — Route 53 Failover Not Triggering
**Prompt:** Primary endpoint down but traffic not failing over quickly.
**Follow-ups:**
1. TTL influence explanation?
2. Health check misconfig pitfalls?
3. How to test failover quarterly?
**Strong answer should cover:** DNS caching behavior, endpoint health validation, game-day failover script and evidence.

## Round 14 — Kubernetes Noisy Neighbor
**Prompt:** One namespace starves node resources and impacts others.
**Follow-ups:**
1. Which controls stop this?
2. requests/limits tuning approach?
3. HPA interaction pitfalls?
**Strong answer should cover:** quotas + limit ranges, right-sized resource specs, autoscaling with saturation signals.

## Round 15 — Docker Supply Chain Risk
**Prompt:** Security team reports critical CVEs in base images.
**Follow-ups:**
1. Build pipeline hardening steps?
2. Image provenance controls?
3. Runtime policy enforcement?
**Strong answer should cover:** minimal patched base images, scanning gates, signed images, digest pinning + admission policy.

## Round 16 — Python API Timeout Storm
**Prompt:** Service times out under moderate load despite healthy infra.
**Follow-ups:**
1. CPU-bound vs I/O-bound diagnosis?
2. async/thread/process choice?
3. Retry + timeout strategy?
**Strong answer should cover:** profiling evidence, proper concurrency model, bounded retries with jitter + circuit breaker.

## Round 17 — Python Memory Leak Investigation
**Prompt:** Worker memory grows steadily until OOM kills.
**Follow-ups:**
1. Tooling to identify leak patterns?
2. Common leak causes in Python apps?
3. Fix validation criteria?
**Strong answer should cover:** heap snapshots/profilers, reference retention patterns, steady-state memory verification under soak test.

## Round 18 — SQL Deadlock in Checkout
**Prompt:** Random deadlocks occur during high-traffic order placement.
**Follow-ups:**
1. Deadlock graph interpretation?
2. App transaction redesign?
3. Retry policy boundaries?
**Strong answer should cover:** lock order consistency, shorter transactions, idempotent retries with limits.

## Round 19 — SQL Reporting Query Too Slow
**Prompt:** Monthly reporting query takes 40 minutes and blocks other workloads.
**Follow-ups:**
1. OLTP vs OLAP separation options?
2. Partitioning/materialized view strategy?
3. Scheduling without production impact?
**Strong answer should cover:** workload isolation, index/partition planning, off-peak execution and resource governance.

## Round 20 — EKS Node Drain Incident
**Prompt:** During node upgrade, too many pods terminate simultaneously.
**Follow-ups:**
1. Which Kubernetes objects prevent this?
2. Safe rolling node upgrade process?
3. Monitoring during drain?
**Strong answer should cover:** PodDisruptionBudgets, cordon/drain batching, real-time SLO monitoring and rollback gates.

## Round 21 — Multi-Region DR Design
**Prompt:** You need active-passive DR for critical customer APIs.
**Follow-ups:**
1. Define RTO/RPO targets and trade-offs.
2. Data replication choices for S3 and RDS.
3. DNS and failback strategy.
**Strong answer should cover:** explicit RTO/RPO, tested replication, Route53 failover, runbook automation and rehearse.

## Round 22 — Incident Communication Failure
**Prompt:** Technical fix happened fast, but stakeholders were unhappy with updates.
**Follow-ups:**
1. What should incident commander do differently?
2. Status update cadence/template?
3. What belongs in postmortem?
**Strong answer should cover:** clear ownership, regular factual updates, timeline + impact + corrective actions.

## Round 23 — IaC Drift Production Issue
**Prompt:** Terraform state says healthy; runtime config differs and caused outage.
**Follow-ups:**
1. Drift detection process?
2. Emergency fix vs IaC source-of-truth?
3. How to block manual drift?
**Strong answer should cover:** drift scans, controlled break-glass then IaC reconciliation, IAM restrictions against console-only edits.

## Round 24 — Cross-Account Data Pipeline
**Prompt:** Need secure S3 data sharing between producer and analytics account.
**Follow-ups:**
1. Role assumption and bucket policy model?
2. Encryption key sharing model?
3. Audit and revocation plan?
**Strong answer should cover:** least-privilege role trust, KMS permissions scoping, CloudTrail evidence and rapid revocation mechanism.

## Round 25 — End-to-End Production Readiness
**Prompt:** Before launching new service, what go-live checklist do you enforce?
**Follow-ups:**
1. Reliability checks?
2. Security checks?
3. Operability checks?
**Strong answer should cover:** SLO/error budget, load/failover tests, IAM/network hardening, dashboards/alerts/runbooks/on-call readiness.

---

## How to Practice
- Time-box each round: 4 minutes answer + 3 minutes follow-ups.
- Use STAR for scenario framing.
- End each answer with measurable impact and one lesson learned.
