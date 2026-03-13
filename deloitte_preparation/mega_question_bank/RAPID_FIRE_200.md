# Rapid-Fire Interview Revision (200 Q&A)

Format: one-liner questions with concise 20–30 second answers.

## AWS (120)

1. **Q:** IAM role vs IAM user?
   **A:** Users are identities for people/services; roles are assumable identities for temporary credentials and safer cross-account/service access.

2. **Q:** Why prefer roles over long-lived access keys?
   **A:** Roles issue short-lived credentials, reduce key leakage risk, and simplify rotation.

3. **Q:** Explicit deny vs allow in IAM?
   **A:** Explicit deny always wins, even if another policy allows.

4. **Q:** Trust policy vs permission policy?
   **A:** Trust policy defines who can assume the role; permission policy defines what actions the role can perform.

5. **Q:** Least privilege in one line?
   **A:** Grant only required actions on required resources for required time.

6. **Q:** Condition keys in IAM used for?
   **A:** Narrow access with context like IP, MFA present, tags, or source VPC endpoint.

7. **Q:** What is VPC?
   **A:** Logically isolated virtual network where you define CIDR, subnets, route tables, and gateways.

8. **Q:** Public subnet vs private subnet?
   **A:** Public subnet routes to Internet Gateway; private subnet does not.

9. **Q:** NAT Gateway purpose?
   **A:** Lets private subnet instances reach internet outbound without allowing inbound internet access.

10. **Q:** Security Group vs NACL?
    **A:** SG is stateful and instance-level; NACL is stateless and subnet-level.

11. **Q:** Why multi-AZ design?
    **A:** Survives single AZ failure with minimal downtime.

12. **Q:** Route table role?
    **A:** Controls destination CIDR to next hop mapping per subnet.

13. **Q:** VPC endpoint benefit?
    **A:** Private AWS service access without internet/NAT traversal.

14. **Q:** Interface endpoint vs gateway endpoint?
    **A:** Interface endpoint uses ENIs/PrivateLink; gateway endpoint supports S3/DynamoDB via route tables.

15. **Q:** ALB vs NLB?
    **A:** ALB is Layer 7 with host/path routing; NLB is Layer 4 for high throughput/low latency.

16. **Q:** Target group health checks do what?
    **A:** Route traffic only to healthy targets.

17. **Q:** Sticky sessions on ALB trade-off?
    **A:** Better session affinity but can reduce even load distribution.

18. **Q:** Blue/green on ALB how?
    **A:** Shift traffic between target groups gradually using weights.

19. **Q:** EC2 user data use case?
    **A:** Bootstraps instance configuration at launch.

20. **Q:** Spot instances best for?
    **A:** Fault-tolerant, interruptible workloads needing cost savings.

21. **Q:** Savings Plans vs Reserved Instances?
    **A:** Savings Plans are more flexible; RIs can be more rigid but predictable.

22. **Q:** IMDSv2 why important?
    **A:** Reduces SSRF credential theft risk with session-oriented metadata access.

23. **Q:** AMI purpose?
    **A:** Reusable machine image for consistent EC2 launches.

24. **Q:** Auto Scaling target tracking?
    **A:** Automatically adjusts capacity to maintain a metric target like CPU 50%.

25. **Q:** Step scaling when useful?
    **A:** When scaling response should vary by breach magnitude.

26. **Q:** Cooldown/warm-up effect?
    **A:** Prevents scaling thrash during transient metric spikes.

27. **Q:** S3 standard durability claim?
    **A:** Designed for 11 9s durability via multi-AZ redundancy.

28. **Q:** S3 versioning helps with?
    **A:** Recovery from accidental overwrite/delete.

29. **Q:** S3 lifecycle policy purpose?
    **A:** Automatic tiering/expiration to reduce storage cost.

30. **Q:** S3 block public access should be?
    **A:** Enabled by default unless explicitly required and controlled.

31. **Q:** SSE-S3 vs SSE-KMS?
    **A:** SSE-KMS gives key control/audit granularity; SSE-S3 is simpler managed encryption.

32. **Q:** Pre-signed URL use case?
    **A:** Temporary secure object access without exposing bucket publicly.

33. **Q:** RDS Multi-AZ vs Read Replica?
    **A:** Multi-AZ for HA failover; read replica for read scaling.

34. **Q:** When enable Performance Insights?
    **A:** For query-level performance diagnostics and bottleneck detection.

35. **Q:** DocumentDB core fit?
    **A:** Managed document database for JSON-like workloads needing scale and availability.

36. **Q:** CloudWatch metric vs log?
    **A:** Metric is numeric time series; log is event text stream.

37. **Q:** CloudWatch alarm best practice?
    **A:** Alert on symptoms tied to SLO impact, not noisy raw metrics only.

38. **Q:** CloudTrail core value?
    **A:** API audit trail for governance, incident investigation, compliance.

39. **Q:** Organization trail advantage?
    **A:** Centralized mandatory logging across all accounts.

40. **Q:** EBS gp3 vs io2?
    **A:** gp3 general purpose configurable; io2 for high durability/critical IOPS workloads.

41. **Q:** EBS snapshot use case?
    **A:** Incremental backups and disaster recovery.

42. **Q:** Route 53 failover routing?
    **A:** Routes to primary/secondary based on health checks.

43. **Q:** TTL effect in DNS failover?
    **A:** Lower TTL speeds failover but increases resolver query volume.

44. **Q:** WAF with ALB why?
    **A:** Filters web attacks (SQLi, XSS, bad bots) before app layer.

45. **Q:** Shield Standard provides?
    **A:** Baseline DDoS protection for AWS resources.

46. **Q:** KMS CMK rotation why?
    **A:** Limits long-term key exposure and supports crypto hygiene.

47. **Q:** Secrets Manager vs Parameter Store?
    **A:** Secrets Manager adds rotation workflows and secret-focused features.

48. **Q:** Shared responsibility model one line?
    **A:** AWS secures cloud infrastructure; customer secures workloads/data/config.

49. **Q:** What is blast radius in AWS design?
    **A:** Scope of impact from a failure/misconfiguration.

50. **Q:** Why use separate AWS accounts by environment?
    **A:** Better isolation, governance boundaries, and billing clarity.

51. **Q:** Why centralized logging account?
    **A:** Tamper-resistant audit archive and unified investigation.

52. **Q:** Why tag resources?
    **A:** Ownership, cost allocation, automation targeting, governance.

53. **Q:** SCP in AWS Organizations purpose?
    **A:** Guardrails that set permission boundaries at account/org level.

54. **Q:** GuardDuty value?
    **A:** Managed threat detection using logs and anomaly models.

55. **Q:** Config rules value?
    **A:** Continuous compliance checks against desired state.

56. **Q:** Patch Manager use case?
    **A:** Automated patch orchestration for managed instances.

57. **Q:** SSM Session Manager advantage?
    **A:** Secure shell access without opening inbound SSH ports.

58. **Q:** Why prefer private subnets for app tiers?
    **A:** Reduces direct exposure and enforces controlled ingress paths.

59. **Q:** Bastion host still needed always?
    **A:** Not always; SSM often replaces bastions securely.

60. **Q:** What causes asymmetric routing issues?
    **A:** Return path mismatch across route/NACL/firewall boundaries.

61. **Q:** Why flow logs matter?
    **A:** Network visibility for rejects, anomaly detection, troubleshooting.

62. **Q:** ALB 502 common cause?
    **A:** Backend target closed connection or invalid response.

63. **Q:** ALB 503 common cause?
    **A:** No healthy targets available.

64. **Q:** EC2 status checks two types?
    **A:** System status check and instance status check.

65. **Q:** Why immutable infra?
    **A:** Reduces config drift; replace instances instead of in-place patching.

66. **Q:** Golden AMI pipeline value?
    **A:** Pre-hardened, pre-tested images speed secure deployments.

67. **Q:** Capacity reservation use case?
    **A:** Guarantees EC2 capacity for critical workloads.

68. **Q:** Spot interruption mitigation?
    **A:** Diversify instance pools, checkpoint state, graceful draining.

69. **Q:** S3 event notifications used for?
    **A:** Trigger workflows on object create/delete via Lambda/SQS/SNS.

70. **Q:** CRR in S3 stands for?
    **A:** Cross-Region Replication for DR/compliance latency needs.

71. **Q:** Why encrypt data in transit?
    **A:** Prevents eavesdropping and tampering.

72. **Q:** Why enforce TLS policy on ALB?
    **A:** Blocks weak ciphers/protocols and improves compliance posture.

73. **Q:** CloudWatch composite alarm benefit?
    **A:** Reduces alert noise by combining multiple alarm conditions.

74. **Q:** Metric math in CloudWatch useful for?
    **A:** Derived KPIs without changing application instrumentation.

75. **Q:** CloudTrail log file validation gives?
    **A:** Integrity verification to detect tampering.

76. **Q:** Why centralized KMS strategy matters?
    **A:** Consistent key governance, policy review, and audit traceability.

77. **Q:** EBS delete-on-termination caution?
    **A:** Prevent accidental data loss on instance termination.

78. **Q:** EC2 instance profile is?
    **A:** IAM role attached to an instance for API permissions.

79. **Q:** Why avoid 0.0.0.0/0 in SG for admin ports?
    **A:** Excessive exposure increases attack surface.

80. **Q:** Transit Gateway use case?
    **A:** Scalable hub-and-spoke inter-VPC and hybrid connectivity.

81. **Q:** VPC peering limitation to note?
    **A:** No transitive routing.

82. **Q:** Why route53 health checks externally sometimes?
    **A:** Validate user-facing endpoint behavior from outside VPC.

83. **Q:** What is RTO?
    **A:** Maximum acceptable time to restore service after disruption.

84. **Q:** What is RPO?
    **A:** Maximum acceptable data loss measured in time.

85. **Q:** Multi-region strategy challenge?
    **A:** Data consistency, failover orchestration, and cost complexity.

86. **Q:** Why chaos testing in cloud?
    **A:** Validates resilience assumptions under controlled failure.

87. **Q:** Cost Explorer good for?
    **A:** Analyze spend trends, anomalies, and optimization targets.

88. **Q:** Budgets alerts help with?
    **A:** Early detection of spend overrun risk.

89. **Q:** Trusted Advisor value?
    **A:** Best-practice recommendations across cost, security, reliability.

90. **Q:** Why rightsize EC2?
    **A:** Align capacity with real usage to reduce waste.

91. **Q:** Storage class analysis in S3 used for?
    **A:** Choosing optimal tier based on access pattern.

92. **Q:** Why backup restore drills?
    **A:** Backups are unproven until restore is tested.

93. **Q:** DB parameter group change risk?
    **A:** Wrong settings can degrade performance or break compatibility.

94. **Q:** Why canary deployment?
    **A:** Limits blast radius while validating production behavior.

95. **Q:** Why feature flags?
    **A:** Decouple code deploy from feature release and rollback quickly.

96. **Q:** What is idempotency in cloud APIs?
    **A:** Repeated requests produce same final state safely.

97. **Q:** Why retry with backoff?
    **A:** Handles transient failures without thundering herd.

98. **Q:** Why dead-letter queue?
    **A:** Isolates repeatedly failing messages for analysis/reprocessing.

99. **Q:** Why correlation IDs?
    **A:** Trace a request across distributed components.

100. **Q:** SLO vs SLA?
     **A:** SLO is internal reliability target; SLA is external contractual commitment.

101. **Q:** Mean time to detect (MTTD) improvement driver?
     **A:** Better telemetry quality and actionable alerting.

102. **Q:** Mean time to recover (MTTR) reduction driver?
     **A:** Clear runbooks, automation, and rehearsed incident response.

103. **Q:** Why post-incident review?
     **A:** Learn systemic fixes and prevent recurrence.

104. **Q:** What is defense in depth?
     **A:** Multiple independent security controls across layers.

105. **Q:** Why deny-by-default network model?
     **A:** Minimizes unintended access paths.

106. **Q:** Why private link style connectivity preferred?
     **A:** Keeps traffic on private network and lowers exposure.

107. **Q:** Why isolate production workloads?
     **A:** Limits blast radius and strengthens compliance posture.

108. **Q:** Why infrastructure as code?
     **A:** Versioned, repeatable, reviewable, automatable infrastructure changes.

109. **Q:** Drift detection means?
     **A:** Identifying runtime config deviation from declared IaC state.

110. **Q:** Why policy-as-code?
     **A:** Enforces security/compliance rules early in CI/CD.

111. **Q:** Why periodic key/access review?
     **A:** Remove stale privileges and reduce insider/exposure risk.

112. **Q:** Why service quotas monitoring?
     **A:** Prevent hidden scale ceiling incidents.

113. **Q:** Why synthetic monitoring?
     **A:** Detect user-visible failures before customer reports.

114. **Q:** Why workload segmentation by account/VPC?
     **A:** Security boundaries, fault isolation, and clearer ownership.

115. **Q:** Why avoid manual hotfixes directly in prod?
     **A:** Causes drift and weakens reproducibility.

116. **Q:** Why maintain runbooks in repo?
     **A:** Versioned operations knowledge and faster onboarding.

117. **Q:** What is shared-nothing architecture benefit?
     **A:** Better horizontal scaling and fault isolation.

118. **Q:** Why event-driven autoscaling?
     **A:** Better alignment to real demand than static schedules alone.

119. **Q:** Why monitor saturation, not only utilization?
     **A:** Saturation predicts pending failures before full outages.

120. **Q:** Why design for graceful degradation?
     **A:** Keeps core experience available during partial failures.

## Kubernetes (35)

121. **Q:** Pod vs Deployment?
     **A:** Pod is runtime unit; Deployment manages replica lifecycle and rolling updates.

122. **Q:** Deployment vs StatefulSet?
     **A:** Deployment for stateless workloads; StatefulSet for stable identity/storage stateful apps.

123. **Q:** Service ClusterIP purpose?
     **A:** Internal stable virtual IP for pod set.

124. **Q:** NodePort use case?
     **A:** Exposes service on node ports, usually for simple/dev scenarios.

125. **Q:** Ingress role?
     **A:** L7 routing + TLS termination into cluster services.

126. **Q:** Readiness probe vs liveness probe?
     **A:** Readiness controls traffic eligibility; liveness restarts unhealthy containers.

127. **Q:** Startup probe when useful?
     **A:** Slow-start apps to avoid premature liveness failures.

128. **Q:** requests vs limits?
     **A:** Requests influence scheduling; limits cap container resource usage.

129. **Q:** OOMKilled usually means?
     **A:** Container exceeded memory limit.

130. **Q:** HPA scales on what?
     **A:** Metrics like CPU/memory/custom metrics.

131. **Q:** PDB purpose?
     **A:** Controls voluntary disruption to maintain availability during maintenance.

132. **Q:** RBAC least privilege means?
     **A:** Grant minimal verbs/resources at namespace scope where possible.

133. **Q:** NetworkPolicy value?
     **A:** Micro-segmentation of pod traffic.

134. **Q:** ConfigMap vs Secret?
     **A:** ConfigMap for non-sensitive config; Secret for sensitive values.

135. **Q:** Why avoid latest tag?
     **A:** Non-deterministic deployments and rollback confusion.

136. **Q:** DaemonSet use case?
     **A:** One pod per node (logging agent, CNI component).

137. **Q:** CrashLoopBackOff first check?
     **A:** Container logs, events, probe failures, env/config errors.

138. **Q:** Pending pod first check?
     **A:** Scheduler events, resource shortage, taints/tolerations, PVC binding.

139. **Q:** Taints and tolerations purpose?
     **A:** Control which pods can schedule onto specific nodes.

140. **Q:** Affinity/anti-affinity why?
     **A:** Placement control for performance or fault isolation.

141. **Q:** Stateful workload backup concern?
     **A:** Volume snapshots + consistency guarantees during restore.

142. **Q:** Rolling update safe default?
     **A:** Small maxUnavailable, controlled surge, health probes validated.

143. **Q:** Canary in Kubernetes common approach?
     **A:** Split traffic by ingress/service mesh weights.

144. **Q:** Why image pull policy matters?
     **A:** Controls freshness vs startup speed/caching behavior.

145. **Q:** etcd critical because?
     **A:** It stores cluster state; corruption impacts control plane.

146. **Q:** kubelet role?
     **A:** Agent on node managing pod lifecycle from API instructions.

147. **Q:** Admission controller purpose?
     **A:** Enforce policy/mutation/validation at API request time.

148. **Q:** Pod security baseline intent?
     **A:** Restrict risky privileges and host-level access.

149. **Q:** Why IRSA on EKS?
     **A:** Pod-level IAM permissions without node-wide broad credentials.

150. **Q:** Why limit range and resource quota?
     **A:** Prevent noisy neighbors and namespace resource starvation.

151. **Q:** Service mesh core benefit?
     **A:** Traffic policy, mTLS, retries/timeouts, observability.

152. **Q:** Why graceful termination config?
     **A:** Drain traffic before pod shutdown to avoid dropped requests.

153. **Q:** Helm value override risk?
     **A:** Hidden config drift and unexpected runtime behavior.

154. **Q:** Why GitOps for k8s?
     **A:** Declarative, auditable, and controlled cluster changes.

155. **Q:** What causes 503 at ingress often?
     **A:** No ready backend endpoints or bad service mapping.

## Docker (20)

156. **Q:** Container vs VM one line?
     **A:** Containers share host kernel; VMs include full guest OS.

157. **Q:** Multi-stage build why?
     **A:** Smaller secure final images by separating build/runtime layers.

158. **Q:** Why minimal base image?
     **A:** Reduces attack surface and image size.

159. **Q:** Why run as non-root?
     **A:** Limits privilege escalation impact.

160. **Q:** COPY vs ADD quick rule?
     **A:** Prefer COPY unless ADD-specific features are required.

161. **Q:** Layer caching optimization?
     **A:** Put rarely changing instructions first, app code later.

162. **Q:** .dockerignore value?
     **A:** Avoid bloated context and accidental secret inclusion.

163. **Q:** Why pin image tags/digests?
     **A:** Deterministic reproducible deployments.

164. **Q:** Healthcheck role?
     **A:** Signals runtime health for orchestration restart/routing decisions.

165. **Q:** ENTRYPOINT vs CMD?
     **A:** ENTRYPOINT defines executable; CMD provides default args.

166. **Q:** Bind mount vs volume?
     **A:** Bind mount maps host path; volume is Docker-managed persistence.

167. **Q:** Why avoid many processes in one container?
     **A:** Harder lifecycle/observability/failure isolation.

168. **Q:** Container exits immediately common reason?
     **A:** Main process terminated.

169. **Q:** Why scan images?
     **A:** Detect known vulnerabilities before deployment.

170. **Q:** Registry immutability value?
     **A:** Prevents tag overwrite and artifact drift.

171. **Q:** Why sign images?
     **A:** Verifies provenance and integrity in supply chain.

172. **Q:** Docker bridge network default behavior?
     **A:** Isolated network with internal DNS for containers on same bridge.

173. **Q:** Port publishing risk?
     **A:** Exposes services externally; tighten scope and SG/firewall rules.

174. **Q:** Why build once, deploy many?
     **A:** Same artifact across environments increases consistency.

175. **Q:** Why avoid secrets in image layers?
     **A:** They persist in history and are hard to revoke.

## Python (15)

176. **Q:** List vs tuple?
     **A:** List mutable; tuple immutable and hashable if contents hashable.

177. **Q:** dict lookup complexity average?
     **A:** O(1) average-case hash lookup.

178. **Q:** set primary advantage?
     **A:** Fast membership checks and deduplication.

179. **Q:** shallow copy vs deep copy?
     **A:** Shallow copies references; deep recursively copies nested objects.

180. **Q:** generator benefit?
     **A:** Lazy iteration saves memory on large sequences.

181. **Q:** *args and **kwargs?
     **A:** Variable positional and keyword arguments.

182. **Q:** context manager purpose?
     **A:** Deterministic setup/cleanup with `with` statement.

183. **Q:** common async use case?
     **A:** High-concurrency I/O-bound operations.

184. **Q:** GIL impact summary?
     **A:** Limits true parallel CPU-bound threads; use multiprocessing for CPU-bound work.

185. **Q:** exception handling best practice?
     **A:** Catch specific exceptions, add context, avoid bare `except`.

186. **Q:** why type hints?
     **A:** Better readability, tooling support, earlier error detection.

187. **Q:** pytest fixture advantage?
     **A:** Reusable test setup/teardown with clear dependency injection.

188. **Q:** mocking use case?
     **A:** Isolate unit behavior from external dependencies.

189. **Q:** virtual environment purpose?
     **A:** Dependency isolation across projects.

190. **Q:** packaging reproducibility key?
     **A:** Pin dependency versions and lock file usage.

## SQL (10)

191. **Q:** INNER JOIN vs LEFT JOIN?
     **A:** INNER returns matching rows only; LEFT keeps all left rows plus matches.

192. **Q:** WHERE vs HAVING?
     **A:** WHERE filters before grouping; HAVING filters grouped results.

193. **Q:** index improves what?
     **A:** Read/query speed, at cost of write overhead/storage.

194. **Q:** composite index order matters why?
     **A:** Leftmost prefix determines index usability.

195. **Q:** normalization purpose?
     **A:** Reduce redundancy and improve consistency.

196. **Q:** transaction ACID stands for?
     **A:** Atomicity, Consistency, Isolation, Durability.

197. **Q:** deadlock handling approach?
     **A:** Keep transactions short, consistent lock order, retry aborted tx.

198. **Q:** EXPLAIN used for?
     **A:** Inspect query plan and bottlenecks.

199. **Q:** window function value?
     **A:** Analytics over row sets without collapsing via GROUP BY.

200. **Q:** SQL injection prevention?
     **A:** Parameterized queries/prepared statements, never string concatenation.
