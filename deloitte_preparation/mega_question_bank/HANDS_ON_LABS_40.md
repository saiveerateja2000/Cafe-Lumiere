# Hands-On Practical Labs (40)

Each lab includes:
- Scenario
- Objective
- Expected approach
- Validation checklist

---

## AWS Labs (20)

### Lab 1 — Fix Over-Permissive IAM Policy
**Scenario:** CI role has `*:*` permissions.
**Objective:** Refactor to least privilege.
**Expected approach:** Identify used actions via logs, scope resources, add conditions, remove wildcards.
**Validation checklist:** Pipeline still works; denied non-required actions; policy review documented.

### Lab 2 — Broken Cross-Account Role Assumption
**Scenario:** AssumeRole fails after trust update.
**Objective:** Restore secure role assumption.
**Expected approach:** Verify principal ARN, external ID, session duration, condition constraints.
**Validation checklist:** AssumeRole succeeds from allowed account only; CloudTrail confirms attempts.

### Lab 3 — Private Subnet to S3 Without NAT
**Scenario:** App in private subnet cannot access S3 after NAT removal.
**Objective:** Restore private connectivity.
**Expected approach:** Add S3 gateway endpoint, update route table and endpoint policy.
**Validation checklist:** S3 access succeeds; no internet egress required.

### Lab 4 — ALB Health Check Failures
**Scenario:** New release causes targets unhealthy.
**Objective:** Recover service quickly.
**Expected approach:** Validate health path/port/timeout, app readiness state, security groups.
**Validation checklist:** Healthy host count restored; 5xx drops to baseline.

### Lab 5 — EC2 Hardening Baseline
**Scenario:** Legacy EC2 fleet has SSH open globally.
**Objective:** Harden access posture.
**Expected approach:** Move to SSM Session Manager, close SSH ingress, enforce IMDSv2.
**Validation checklist:** Admin access works via SSM; SSH exposure removed.

### Lab 6 — Auto Scaling Thrashing
**Scenario:** Group scales in/out repeatedly.
**Objective:** Stabilize scaling behavior.
**Expected approach:** Tune warm-up/cooldown, target metric, min/max capacity boundaries.
**Validation checklist:** Fewer oscillations; stable p95 latency under load.

### Lab 7 — S3 Public Exposure Guardrails
**Scenario:** Repeated accidental public bucket changes.
**Objective:** Prevent recurrence.
**Expected approach:** Enforce block-public-access, SCP guardrails, config rule alerts.
**Validation checklist:** Public policy change blocked/detected automatically.

### Lab 8 — RDS Performance Tuning
**Scenario:** Slow checkout queries impact API.
**Objective:** Reduce DB latency.
**Expected approach:** Analyze `EXPLAIN`, add/adjust indexes, optimize query predicates.
**Validation checklist:** Query latency improves; no regression on write throughput.

### Lab 9 — RDS Failover Drill
**Scenario:** Team never tested Multi-AZ failover.
**Objective:** Execute controlled failover.
**Expected approach:** Trigger failover in maintenance window, monitor app reconnect behavior.
**Validation checklist:** Recovery within target RTO; runbook updated.

### Lab 10 — DocumentDB Index Repair
**Scenario:** Collection scans dominate CPU.
**Objective:** Improve query efficiency.
**Expected approach:** Review query patterns, add selective compound indexes, tune projections.
**Validation checklist:** Scanned docs reduced significantly; p95 read latency improved.

### Lab 11 — CloudWatch Alarm Rationalization
**Scenario:** 200 alarms, high false-positive rate.
**Objective:** Improve signal quality.
**Expected approach:** Map alarms to SLO symptoms, tune thresholds/evaluation periods, composite alarms.
**Validation checklist:** Alert count reduced, actionable alerts ratio improved.

### Lab 12 — CloudTrail Coverage Audit
**Scenario:** Some regions lack trail data.
**Objective:** Ensure complete audit visibility.
**Expected approach:** Configure org multi-region trail, central S3 archive, log validation.
**Validation checklist:** Events present from all accounts/regions.

### Lab 13 — Security Group Drift Control
**Scenario:** Manual SG edits bypass IaC.
**Objective:** Re-establish controlled changes.
**Expected approach:** Lock down edit permissions, detect drift, enforce CI/CD path.
**Validation checklist:** Manual edits blocked/alerted; IaC remains source of truth.

### Lab 14 — EBS Performance Mismatch
**Scenario:** Workload IO spikes but volumes are under-provisioned.
**Objective:** Match storage to workload profile.
**Expected approach:** Tune gp3 IOPS/throughput or migrate to io2 where justified.
**Validation checklist:** Queue length and latency normalize.

### Lab 15 — Route 53 Failover Validation
**Scenario:** Failover policy exists but untested.
**Objective:** Prove DNS failover works.
**Expected approach:** Simulate primary outage, monitor health-check transition and client behavior.
**Validation checklist:** Traffic shifts to secondary within expected TTL window.

### Lab 16 — Cost Optimization Sprint
**Scenario:** Monthly bill exceeds forecast by 20%.
**Objective:** Cut cost safely.
**Expected approach:** Rightsize compute, S3 lifecycle, eliminate idle resources, commitment plan review.
**Validation checklist:** Spend reduced without SLO violations.

### Lab 17 — WAF Rule Tuning
**Scenario:** WAF blocks valid requests after rule update.
**Objective:** Reduce false positives.
**Expected approach:** Analyze sampled requests, adjust rule precedence/exceptions, staged rollout.
**Validation checklist:** Legit traffic restored; malicious traffic still blocked.

### Lab 18 — KMS Key Access Issue
**Scenario:** App fails decrypt after role change.
**Objective:** Restore encrypted data access securely.
**Expected approach:** Validate key policy + IAM policy + grants alignment.
**Validation checklist:** Decrypt succeeds only for approved principals.

### Lab 19 — Backup Restore Proof
**Scenario:** Backups exist but restore unverified.
**Objective:** Validate recoverability.
**Expected approach:** Restore to isolated env, run integrity checks and app smoke tests.
**Validation checklist:** Data integrity confirmed; restore time measured.

### Lab 20 — Multi-Account Logging Pipeline
**Scenario:** Security needs central logs from all accounts.
**Objective:** Build centralized log archive.
**Expected approach:** Organization trail + cross-account write policy + retention controls.
**Validation checklist:** Logs visible centrally; access tightly scoped.

## Kubernetes Labs (8)

### Lab 21 — CrashLoopBackOff Triage
**Scenario:** Critical pod restarts continuously.
**Objective:** Restore healthy deployment.
**Expected approach:** Check events/logs/probes/env secrets/config mismatch.
**Validation checklist:** Pod stable; probe success sustained.

### Lab 22 — Pending Pods Due to Capacity
**Scenario:** New release pods remain pending.
**Objective:** Resolve scheduling bottleneck.
**Expected approach:** Inspect requests/limits, node capacity, taints/tolerations, autoscaler state.
**Validation checklist:** Pods scheduled; no cluster-wide starvation.

### Lab 23 — Readiness Probe Misconfiguration
**Scenario:** Traffic routed before app startup complete.
**Objective:** Prevent premature routing.
**Expected approach:** Tune readiness/startup probes and initial delays.
**Validation checklist:** No cold-start 5xx during rollout.

### Lab 24 — NetworkPolicy Lockdown
**Scenario:** Namespace should deny all east-west except explicit dependencies.
**Objective:** Implement least-privilege network model.
**Expected approach:** Default deny + allowlist specific namespace/pod/port.
**Validation checklist:** Allowed paths work; all other paths blocked.

### Lab 25 — RBAC Hardening
**Scenario:** Team currently uses cluster-admin broadly.
**Objective:** Replace with scoped roles.
**Expected approach:** Namespace roles, role bindings, service account separation.
**Validation checklist:** Required operations succeed; unauthorized actions denied.

### Lab 26 — Safe Deployment Rollback
**Scenario:** New version increases error rate.
**Objective:** Roll back quickly with minimal user impact.
**Expected approach:** Pause rollout, rollback revision, verify prior replica health.
**Validation checklist:** Error rate returns baseline; incident notes updated.

### Lab 27 — Node Upgrade Without Downtime
**Scenario:** Cluster node upgrade planned.
**Objective:** Perform zero/near-zero downtime maintenance.
**Expected approach:** Cordon/drain in batches, respect PDB, monitor SLOs.
**Validation checklist:** Availability maintained throughout maintenance.

### Lab 28 — Secret Rotation in Kubernetes
**Scenario:** Credential rotation required urgently.
**Objective:** Rotate secrets safely.
**Expected approach:** Update secret source, rollout restart controlled, confirm app reconnect.
**Validation checklist:** New credentials active; old credentials invalidated.

## Docker Labs (5)

### Lab 29 — Shrink Oversized Image
**Scenario:** Service image is 1.8GB.
**Objective:** Reduce image size and attack surface.
**Expected approach:** Multi-stage build, slim base image, remove build artifacts.
**Validation checklist:** Image size reduced significantly; app functionality intact.

### Lab 30 — Container Runs as Root
**Scenario:** Security review flags root execution.
**Objective:** Run non-root securely.
**Expected approach:** Create app user, adjust file permissions, update runtime user.
**Validation checklist:** Container starts as non-root; permissions still valid.

### Lab 31 — Secret Leak in Build History
**Scenario:** Token accidentally embedded in Docker layer.
**Objective:** Remove exposed secret and rotate credentials.
**Expected approach:** Purge/rebuild image, rotate token, move secrets to runtime injection.
**Validation checklist:** No secret in layers/logs; new token operational.

### Lab 32 — Registry Tag Drift
**Scenario:** `latest` tag changed unexpectedly causing rollback confusion.
**Objective:** Enforce immutable artifact strategy.
**Expected approach:** Use digest pinning and immutable tags in deployment manifests.
**Validation checklist:** Deployments reference deterministic image digest.

### Lab 33 — Healthcheck-Driven Restarts
**Scenario:** Containers fail intermittently but orchestrator not reacting.
**Objective:** Add meaningful health checks.
**Expected approach:** Implement app health endpoint and Docker healthcheck command.
**Validation checklist:** Unhealthy containers detected/restarted predictably.

## Python Labs (4)

### Lab 34 — Optimize Slow Python Function
**Scenario:** Endpoint latency high due to inefficient in-memory processing.
**Objective:** Improve algorithmic efficiency.
**Expected approach:** Profile function, replace nested loops with dict/set or vectorized logic.
**Validation checklist:** Runtime drops measurably on representative dataset.

### Lab 35 — Async I/O Refactor
**Scenario:** Service handles many outbound API calls sequentially.
**Objective:** Improve throughput with concurrency.
**Expected approach:** Add async client, bounded concurrency, timeout + retry controls.
**Validation checklist:** Higher throughput, controlled error rates, no event-loop blocking.

### Lab 36 — Exception Hygiene
**Scenario:** Broad exceptions hide root causes.
**Objective:** Improve debuggability and resilience.
**Expected approach:** Catch specific exceptions, structured logs, preserve stack traces.
**Validation checklist:** Error logs actionable; no silent failures.

### Lab 37 — Add Unit Tests for Critical Logic
**Scenario:** Regressions slip into production.
**Objective:** Improve confidence before deploy.
**Expected approach:** Add pytest unit tests + fixtures + edge cases.
**Validation checklist:** Tests fail on known bug, pass on fix.

## SQL Labs (3)

### Lab 38 — Rewrite Non-Sargable Query
**Scenario:** Query uses function on indexed column causing scan.
**Objective:** Enable index usage.
**Expected approach:** Rewrite predicate to be sargable; verify plan change.
**Validation checklist:** Index seek observed; latency reduced.

### Lab 39 — Deadlock Reproduction and Fix
**Scenario:** Production deadlocks are hard to reproduce.
**Objective:** Recreate and eliminate deadlock pattern.
**Expected approach:** Simulate concurrent transactions, enforce consistent lock order.
**Validation checklist:** Deadlock frequency reduced/removed under load test.

### Lab 40 — Pagination at Scale
**Scenario:** Offset pagination becomes slow on large table.
**Objective:** Improve query performance.
**Expected approach:** Implement keyset pagination with proper index.
**Validation checklist:** Stable latency across deep pages.

---

## Practice Mode
- Pick 3 labs/day: 1 AWS, 1 platform (K8s/Docker), 1 coding/data (Python/SQL).
- Record: root cause, fix, validation, prevention.
- End every lab with: “What alert/runbook/policy would have prevented this earlier?”
