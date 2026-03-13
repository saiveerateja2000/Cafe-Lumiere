# AWS DevOps Interview Prep: Interview Tips & Scenario-Based Questions

## Interview Strategy

### 1. How to approach AWS DevOps interview questions

**Structure your answer (STAR method):**
- **Situation** - Context/problem
- **Task** - What needed to be done
- **Action** - What you did
- **Result** - Outcome and lessons learned

**Example answer:**
```
Q: Tell me about a time you deployed code to production.

A: Situation - We had a microservices app crashing in specific scenarios
Task - Need to deploy fix without downtime while monitoring carefully
Action - I implemented blue/green deployment using CodeDeploy with canary (5% traffic initially)
        - Pre-deployment: Validated with 1M synthetic requests in staging
        - Deployment: Automated CI/CD pipeline, 5min canary, then 95% traffic shift over 15 minutes
        - Monitoring: Set up alarms for error rate, latency, CPU
Result - Deployment successful with zero downtime, fix verified in prod
        - Learned: Importance of pre-deployment load testing
        - Implemented: Automated canary metrics validation for future deployments
```

### 2. Red flags in interview answers

**Avoid:**
- "I'll just restart the server" (ignores root cause)
- "No monitoring needed" (reliability issue)
- "No backups required" (disaster recovery failure)
- "Store password in code" (security red flag)
- "Single point of failure is OK" (HA failure)
- "Manual deployments work fine" (scaling issue)

### 3. Questions to ask interviewer

- "What's your deployment frequency?" (How serious about DevOps)
- "What monitoring/alerting do you have?" (Maturity level)
- "What's your incident response process?" (Reliability focus)
- "Tell me about your biggest production incident" (Learning culture)
- "How do you handle deployments?" (DevOps maturity)

---

## Scenario-Based Interview Questions

### Scenario 1: High CPU Alert at 3 AM

**Situation:** You're on-call, CloudWatch alarm: API server CPU > 90%

**What would you do?**

**Good answer:**
```
1. Check CloudWatch dashboard - see request rate also spiked
2. Review recent deployments - new code deployed 2 hours ago
3. Check X-Ray - identify slow database queries introduced by new code
4. Options:
   a) Rollback deployment (fastest, safest)
   b) Scale up auto-scaling group (quick, but masks problem)
   c) Optimize slow query (better long-term, risky in middle of night)
5. Decision: Rollback deployment immediately
6. Verify: CPU returns to normal, error rate drops
7. Post-incident: 
   - Debug slow query in staging
   - Add database query performance tests to CI/CD
   - Adjust alarms to catch before customer impact
```

**Red flags and how to avoid them:**
- ❌ "Kill the instance and restart it" → Better: Understand root cause first
- ❌ "Just add more instances" → Better: Fix the root cause, then scale if needed
- ❌ "No monitoring in place" → Always have alerting on key metrics
- ❌ "Can't rollback easily" → Always maintain quick rollback capability

---

### Scenario 2: Database Disk Space Running Out

**Situation:** Database storage 95% full, need plan to fix within 2 hours

**What would you do?**

**Good answer:**
```
1. Immediate (next 30 minutes):
   - Enable CloudWatch alarms if not already
   - Identify largest tables/indexes
   - Clean up old logs/temp data (can recover 10-20%)
   - Set up Auto Scaling for EBS volume (if using RDS)

2. Medium-term (within 2 hours):
   - Upgrade database storage capacity
   - Update auto-scaling threshold to trigger at 80% instead of 95%

3. Long-term:
   - Implement data retention policies
   - Archive old data to S3/Glacier
   - Optimize indexes (remove unused)
   - Monitor growth rate and plan capacity

4. Prevention:
   - Set monitoring alarms at 70% (warn), 85% (critical)
   - Regular storage capacity reviews
   - Unused EC2 snapshots cleanup automation
```

**What NOT to say:**
- ❌ "Delete oldest data" (data loss)
- ❌ "Ignore it for now" (will cause outage)
- ❌ "No monitoring in place" (should detect earlier)

---

### Scenario 3: Deployment Pipeline Failing

**Situation:** CodePipeline failing during build stage, code merged 5 minutes ago

**What would you do?**

**Good answer:**
```
1. Immediate investigation:
   - Check CodeBuild logs → Identify specific error
   - Common: Missing dependency, test failed, security scan issue

2. Determine severity:
   - Is main branch broken? (blocks all deployments)
   - Can we fix quickly? (< 5 minutes)
   - Should we revert? (> 15 minutes to fix)

3. Quick fix:
   - If missing dependency: Add to requirements.txt
   - If test failed: Review test failure, fix code
   - If security scan: Review flagged vulnerability
   - Push fix: New commit → Pipeline reruns

4. If can't fix quickly (> 15 minutes):
   - Revert the commit
   - Document issue in PR
   - Fix and test locally before pushing again

5. Prevention:
   - Run CI checks locally before push (pre-commit hooks)
   - Have separate test branch first (pull request testing)
   - Set up notifications (Slack, email) for pipeline failures
```

**Red flags:**
- ❌ "Force push to bypass checks" (skips tests intentionally)
- ❌ "Disable security scanning" (introduces vulnerabilities)
- ❌ "No tests in pipeline" (can't catch issues)

---

### Scenario 4: Service Dependency Failure in Microservices

**Situation:** Order service depends on Inventory service, Inventory service down, orders failing

**What would you do?**

**Good answer:**
```
1. Immediate response:
   - Service A (Order): Implement circuit breaker
     * Stop calling Inventory Service immediately
     * Return cached inventory data or "limited availability" message
     * Don't wait for timeout (fail fast)
   
   - Service B (Inventory): Start recovery
     * Alert team to incident
     * Check logs for root cause
     * Determine if restart/redeploy needed

2. Customer impact mitigation:
   - Show user: "Inventory check temporarily unavailable"
   - Allow order placement without inventory verification (risk accepted)
   - Send alerts to operations team

3. Recovery:
   - If restart fixes: Restart container
   - If bad deploy: Rollback to previous version
   - If bug: Deploy hotfix

4. Re-enable traffic:
   - Start with 5% traffic (canary)
   - Monitor error rate
   - Gradually increase to 100%

5. Long-term improvements:
   - Add retry logic with exponential backoff
   - Implement timeout (fail fast, don't hang)
   - Cache inventory data (survive short outages)
   - Health checks for circuit breaker (know when to retry)
   - Better monitoring/alerting
```

**Good patterns:**
- Circuit Breaker ✓ (fail fast)
- Timeout ✓ (don't wait forever)
- Fallback/Degradation ✓ (serve partial functionality)
- Retry ✓ (recover from transient failures)
- Bulkhead ✓ (isolate failures)

---

### Scenario 5: Performance Degradation in Production

**Situation:** API response time increased from avg 100ms to avg 500ms, no recent deployments

**What would you do?**

**Good answer:**
```
1. Check infrastructure first:
   - CloudWatch CPU/Memory utilization
   - Network throughput
   - Disk I/O
   - Instance type sufficient? (unusual traffic spike?)

2. Check database:
   - Slow queries in performance insights
   - Connection pool exhausted?
   - Disk space issue?
   - Sudden load increase?

3. Check application:
   - X-Ray traces → identify slow services
   - Are database connections pooled? (new connection per request)
   - Any new features/logging?

4. Check network:
   - Latency between services
   - Security group rules blocking traffic
   - VPC routing issues

5. Identify culprit:
   - If database slow: Optimize queries, add indexes, add read replicas
   - If application slow: Profile code, optimize algorithms
   - If network slow: Move to same AZ, enable placement groups
   - If infra slow: Scale up, upgrade instance type

6. Quick mitigation:
   - Enable caching (ElastiCache)
   - Add more instances (Auto Scaling)
   - Route traffic away from problematic instance

7. Root cause fix:
   - Once identified, implement proper fix
   - Test in staging with similar load
   - Monitor closely during rollout

8. Prevention:
   - Load testing before deployments
   - Continuous performance monitoring
   - Alerting on latency thresholds
```

**Tools to mention:**
- CloudWatch Dashboards
- X-Ray for tracing
- RDS Performance Insights
- Application APM (New Relic, Datadog)

---

### Scenario 6: Security Breach Discovery

**Situation:** Security team discovers exposed AWS credentials in GitHub public repository

**Immediate actions within first hour:**

**Good answer:**
```
1. Pre-fire (0-5 minutes):
   - REMOVE credentials immediately
   - If in source code: Cannot just delete from Git (still in history)
   - Use git filter-branch or BFG to rewrite history
   - Force push to main (risky but necessary)

2. Containment (5-15 minutes):
   - Assume compromised: Rotate all exposed credentials
   - If AWS access keys: Deactivate immediately via IAM console
   - If database password: Change password, review other accounts
   - If API key: Revoke and issue new key

3. Detection (15-30 minutes):
   - Check CloudTrail for unauthorized AWS API calls
   - Check database logs for suspicious queries
   - Review S3 access logs for unusual downloads
   - Review application logs for anomalies

4. Audit (30 minutes - ongoing):
   - What data accessed? What damage done?
   - When was it accessed?
   - What permissions did exposed credentials have?

5. Notification (after investigation):
   - Notify affected customers if data accessed
   - Notify management/legal
   - Public security disclosure if significantly impacted

6. Prevention:
   - Pre-commit hook to scan for secrets (detect-secrets, TruffleHog)
   - GitHub secret scanning enabled
   - Secrets in AWS Secrets Manager, not code
   - IAM rule: Use roles, not long-term keys
   - Credentials have limited permissions (least privilege)
   - Regular access reviews
```

**Red flags to avoid:**
- ❌ "Just delete the file" (still in Git history)
- ❌ "No monitoring, didn't detect" (need CloudTrail alarms)
- ❌ "It's just one key, not important" (Assume compromise)
- ❌ "Don't tell customers" (Legal/regulatory requirement)

---

### Scenario 7: Multi-Region Failover

**Situation:** Primary region AWS services are down, need to fail over to secondary region, target 15 minutes RTO

**What would you do?**

**Good answer:**
```
Pre-incident planning (should already be done):
- Hot standby in secondary region (all services running)
- Continuous data replication (database, cache)
- Route 53 health checks configured
- DNS switchover automation ready
- Regular failover drills

During incident:
1. Detect failure (0-1 minute):
   - Route 53 health check fails
   - Multiple services down
   - Automated alert triggers

2. Initiate failover (1-3 minutes):
   - Route 53 updates DNS to point to secondary region
   - Traffic automatically routes to secondary region
   - (If automated, happens within seconds)

3. Verify secondary region (3-5 minutes):
   - Check that traffic flowing to secondary
   - Services responding normally
   - Database replication caught up
   - User traffic metrics normal

4. Communicate (5-10 minutes):
   - Status page update
   - Notify customers of failover
   - Internal team notification

5. Recovery (10-15 minutes):
   - Investigate primary region issue
   - Once fixed, plan failback
   - OR gracefully fail back when ready

6. Failback (when ready):
   - Verify primary region healthy
   - Sync any diverged data from secondary to primary
   - Switch DNS back to primary
   - Decommission secondary if temporary

Prevention/Testing:
- Monthly failover drills in staging
- Automated failover testing
- Regular DR plan reviews
- Data consistency testing
```

**Key considerations:**
- DNS TTL (how long until DNS change propagates)
- Data consistency between regions
- Application state (sessions, cache)
- Cost (keeping secondary running is expensive)

---

## Common Tricky Questions

### "How would you handle a rollback that has database schema changes?"

**Answer:**
```
Problem: Can't easily roll back database schema
Solution 1: Backward compatibility
- New application code works with old schema
- Add new column with default value
- New code reads new column, old code ignores it
- Schema migration happens gradually
- Old code can still run

Solution 2: Separate schema from code
- Maintain database schema version separate from app version
- Schema changes queued until app supports it
- Can rollback app without rolling back schema

Solution 3: Blue/green with database
- Keep two identical databases (blue/green)
- Replicate from old to new during switch
- If green fails, can instantly revert to blue
- More complex, higher cost

Solution 4: Backup and restore
- Take backup before schema change
- If rollback needed, restore from backup
- Lose data since backup (minutes to hours)
```

### "How do you decide between ECS and Kubernetes?"

**Answer:**
```
Use ECS if:
- AWS-only environment
- Don't need multi-cloud
- Simpler to manage
- Team doesn't know Kubernetes
- Tight AWS integration needed (Lambda, RDS)
- Fewer services to manage

Use Kubernetes if:
- Multi-cloud strategy (avoid vendor lock-in)
- On-premises infrastructure
- Larger, complex deployments
- Team experienced with K8s
- Need advanced orchestration
- Community/ecosystem important
```

### "How do you handle database connection limits?"

**Answer:**
```
1. Understand the problem:
   - Each application connection to database
   - Database has max connections (usually 100-1000)
   - If all exhausted → new connections rejected

2. Solutions:
   a) Connection pooling
      - Reuse connections
      - 10 connections for 100s requests
      - PgBouncer (PostgreSQL), ProxySQL (MySQL)
   
   b) Read replicas
      - Distribute read traffic
      - Primary: Writes only
      - Replicas: Reads only
   
   c) Caching
      - Cache query results
      - Reduce database hits
      - Redis/Memcached
   
   d) Increase database limit
      - Scale up database
      - But usually shouldn't rely on this

3. Monitoring:
   - Alert on connection count > 80% of limit
   - Alert on failed connections
   - Connection pool metrics
```

---

## Practice Tips

1. **Practice with real scenarios** - Tell stories from your experience
2. **Know your numbers** - AWS limits, pricing, performance baselines
3. **Ask clarifying questions** - Don't assume, understand requirements
4. **Think out loud** - Interviewer wants to see your problem-solving
5. **Mention monitoring** - Every answer should include observability
6. **Focus on learning** - "What I learned from this..."
7. **Discuss trade-offs** - No perfect solution, discuss pros/cons
8. **Prepare for follow-ups** - "Why did you choose that approach?"

---

## Key Phrases to Use

- "Automate everything"
- "Infrastructure as Code"
- "Failing fast"
- "Graceful degradation"
- "Observability is critical"
- "Zero downtime deployment"
- "Blue/green deployment"
- "Monitoring and alerting"
- "Root cause analysis"
- "Disaster recovery testing"
- "Security first mindset"
- "Cost optimization"
- "Immutable infrastructure"
- "API-first approach"
