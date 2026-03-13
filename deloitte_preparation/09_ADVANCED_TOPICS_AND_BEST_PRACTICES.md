# AWS DevOps Interview Prep: Advanced Topics & Best Practices

## 1. What is high availability vs disaster recovery?

**Answer:**
**High Availability (HA):**
- Minimize downtime (99.99% uptime = 4.38 minutes/year)
- Multiple instances across AZs
- Load balancing distributes traffic
- Automatic failover
- Fast RTO (seconds to minutes)

**Disaster Recovery (DR):**
- Recover from major failures (region failure, data corruption)
- Backup in different region
- Recovery process takes longer
- Slower RTO (hours to days)
- Lower RPO than HA

**Example:**
```
HA (Multi-AZ):
Region 1
├── AZ 1: ALB + EC2 instances
├── AZ 2: EC2 instances
└── AZ 3: EC2 instances
RTO: Minutes, RPO: Seconds

DR (Multi-region):
Region 1 (Primary) → Continuous backup → Region 2 (Standby)
RTO: Hours, RPO: Minutes
```

## 2. Explain chaos engineering and resilience testing

**Answer:**
Intentionally introduce failures to test system resilience:

**Common tests:**
- Kill random EC2 instances (Netflix Chaos Monkey)
- Disable availability zones
- Saturate network links
- Introduce latency on services
- Crash services

**Implementation:**
```bash
# Chaos toolkit
python -m pytest test_resilience.py --resilience

# AWS Fault Injection Service
aws fis create-experiment-template \
  --description "Kill EC2 instances" \
  --targets Instances={"Filters":[{"Name":"tag:Environment","Values":["test"]}]}
```

**Benefits:**
- Find single points of failure
- Verify failover mechanisms work
- Build confidence in production
- Document RTO/RPO
- Train incident response

## 3. What is the Well-Architected Framework?

**Answer:** AWS best practices across 6 pillars:

**1. Operational Excellence:**
- Infrastructure as Code
- Monitoring and logging
- Regular reviews and improvements
- Automation and rapid recovery

**2. Security:**
- Least privilege access (IAM)
- Data encryption (in transit and at rest)
- Auditability (CloudTrail)
- Defense in depth (multiple layers)

**3. Reliability:**
- Multi-AZ deployment
- Regular backups
- Capacity planning
- Resilient architecture

**4. Performance Efficiency:**
- Right-sized resources
- Caching (CloudFront, ElastiCache)
- Multi-region deployment
- Monitoring and optimization

**5. Cost Optimization:**
- Reserved Instances for predictable workloads
- Right-sizing instances
- Automated resource cleanup
- Reserved capacity planning

**6. Sustainability:**
- Optimized resource utilization
- Efficient code
- Data center energy efficiency

## 4. Explain GitOps and its benefits

**Answer:**
Git as single source of truth for infrastructure and applications:

**Workflow:**
```
Developer push to Git → 
Automated CI/CD → 
Deploy to staging → 
PR approval → 
Deploy to prod
All changes tracked in Git
```

**Tools:**
- ArgoCD (Kubernetes GitOps)
- Flux (Kubernetes GitOps)
- CloudFormation StackSets (AWS-native)
- Terraform Cloud

**Benefits:**
- Audit trail (every change tracked)
- Rollback capability (revert commit)
- Code review process
- Self-documenting (code is documentation)
- Disaster recovery (rebuild from Git)

## 5. What is production readiness review?

**Answer:**
Checklist before deploying to production:

**Infrastructure:**
- [ ] Multi-AZ deployment
- [ ] Load balancing configured
- [ ] Auto Scaling policies
- [ ] Database backups enabled
- [ ] KMS encryption configured
- [ ] VPC security groups reviewed
- [ ] VPC Flow Logs enabled

**Application:**
- [ ] Unit tests > 80% coverage
- [ ] Integration tests passing
- [ ] Load testing completed
- [ ] Logging configured
- [ ] Error handling implemented
- [ ] Graceful shutdown implemented

**Operations:**
- [ ] Monitoring/alerting configured
- [ ] Runbooks written
- [ ] Incident response plan
- [ ] Disaster recovery tested
- [ ] Deployment plan documented
- [ ] Rollback plan tested

**Security:**
- [ ] Security groups reviewed
- [ ] IAM roles least privilege
- [ ] Secrets in secrets manager
- [ ] SSL/TLS enabled
- [ ] Data encryption enabled
- [ ] Security scanning passed

## 6. Explain canary deployments in production

**Answer:**
Gradually roll out new version to small percentage of users:

**Process:**
```
1. Deploy new version alongside current
2. Route 5% traffic to new version
3. Monitor metrics (error rate, latency)
4. If good, gradually increase (5% → 10% → 50% → 100%)
5. If bad, rollback immediately
6. Complete rollout or instant rollback
```

**Metrics to monitor:**
- Error rate (5xx errors)
- Response latency
- Custom application metrics
- User complaints

**AWS implementation:**
```
CodeDeploy with Canary traffic shift:
- Linear: Increase traffic in equal steps every 10 mins
- Exponential: Double traffic each step
- All at once: Immediate full deployment (risky)
```

**Example (SAM):**
```yaml
Globals:
  Function:
    Timeout: 30

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.handler
      Runtime: python3.9
      AutoPublishAlias: live
      DeploymentPreference:
        Type: Canary
        Percent: 10
        Interval: 5
```

## 7. What is blue/green deployment?

**Answer:**
Maintain two identical environments, switch between them:

**Setup:**
```
Blue (v1.0) - Production traffic
Green (v2.0) - No traffic yet

Testing phase:
- Deploy and test v2.0 in green
- Run smoke tests
- Verify functionality

If OK:
- Update load balancer/Route 53
- Traffic switches from blue to green
- Green is now production

If not OK:
- Simply revert switch
- Blue remains unchanged
```

**Advantages:**
- Zero downtime
- Quick rollback
- Easy A/B testing
- Full environment test before switch

**Disadvantages:**
- Double resource costs during switch
- Database schema changes more complex
- State synchronization

**AWS implementation:**
```
ALB with two target groups:
- Blue target group (v1.0 instances)
- Green target group (v2.0 instances)

Switch by updating ALB listener rule
```

## 8. How do you approach performance optimization?

**Answer:**
**Measurement (know current state):**
- Baseline metrics
- CloudWatch dashboards
- X-Ray tracing
- Load testing

**Identify bottleneck:**
```
1. Is it CPU? → Upgrade instance type or add instances
2. Is it memory? → Increase instance memory or cache more
3. Is it disk I/O? → Add EBS optimization, use SSD
4. Is it network? → Enhanced networking, placement groups
5. Is it database? → Read replicas, caching, indexing
6. Is it application? → Profile code, optimize queries
```

**Implement optimization:**
```
Application layer:
- Code optimization
- Database query optimization
- Caching (Redis/ElastiCache)

Infrastructure layer:
- Right-size instances
- Load balancing
- Auto Scaling
- CDN (CloudFront)

Database layer:
- Indexes
- Query optimization
- Read replicas
- Connection pooling
```

**Measure improvement:**
- Compare before/after metrics
- Validate cost/benefit
- Document changes

## 9. What is immutable infrastructure?

**Answer:**
Servers never updated, always replaced with new versions:

**Traditional (mutable):**
```
Server 1.0 running
SSH into server
Apply patches
Install new software
Update config
Result: Server 1.1 (uncertain what changed)
```

**Immutable:**
```
Create new image (AMI) with v1.1 config
Deploy instance from new AMI
Verify health checks pass
Update load balancer to new instance
Terminate old instance
```

**Benefits:**
- Predictable, consistent servers
- Quick rollback (old AMI still available)
- No configuration drift
- Simpler troubleshooting
- Easier testing

**Implementation:**
```
Packer → Build immutable image (AMI)
↓
CloudFormation/Terraform → Deploy instance from image
↓
Auto Scaling → Replace unhealthy instances
↓
Blue/Green deployments → Switch versions atomically
```

## 10. How do you implement observability (3 pillars)

**Answer:**
**Metrics (quantitative):**
- CPU, memory, disk, network
- Request count, latency, error rate
- Custom application metrics
- CloudWatch

**Logs (events):**
- Application logs
- System logs
- Audit logs
- CloudWatch Logs, ELK Stack

**Traces (requests):**
- Request flow through services
- Service dependencies
- Latency per component
- X-Ray

**Complete observability:**
```json
{
  "trace_id": "abc-123",
  "timestamp": "2024-01-01T10:00:00Z",
  "service": "order-service",
  "duration_ms": 150,
  "status": "success",
  "metrics": {
    "cpu": 45,
    "memory": 2048,
    "database_calls": 3,
    "external_api_calls": 1
  }
}
```

## 11. What is rate limiting and throttling?

**Answer:**
**Rate limiting (client perspective):**
- Limit API calls (e.g., 100 requests/minute)
- Prevent abuse, DoS protection
- CloudFront, API Gateway

**Throttling (server perspective):**
- Server actively rejects requests exceeding limit
- HTTP 429 Too Many Requests
- Back off and retry

**Implementation:**
```python
# Token bucket algorithm
from time import time

class RateLimiter:
    def __init__(self, rate, capacity):
        self.rate = rate           # tokens per second
        self.capacity = capacity   # max tokens
        self.tokens = capacity
        self.last_update = time()
    
    def allow_request(self):
        now = time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now
        
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

**AWS implementation:**
```
API Gateway → Usage plans and API keys → Rate limit: 1000 req/sec
```

## 12. Explain fault isolation and circuit breaker pattern

**Answer:**
**Fault isolation:**
- Prevent cascade failures
- If service A fails, don't let it take down service B

**Pattern:**
```
Service A → Service B (timeout: 2 seconds)
If Service B doesn't respond in 2 seconds:
  - Return cached response OR
  - Return error response rapidly OR
  - Degrade functionality gracefully
NOT: Wait 30 seconds and cascade failure
```

**Circuit breaker pattern:**
```
Closed: Normal operation, requests go through
↓ (errors exceed threshold)
Open: Fail immediately, requests rejected
↓ (after wait period)
Half-open: Send test request
  - If succeeds → Closed (recover)
  - If fails → Open (still broken)
```

**Implementation (Spring Cloud):**
```java
@CircuitBreaker(name = "userService", fallbackMethod = "fallback")
public UserData getUser(String id) {
    return userServiceClient.getUser(id);
}

public UserData fallback(String id) {
    return new UserData(id, "Unknown", "unknown@example.com");
}
```

## 13. What is cost optimization in DevOps?

**Answer:**
**Continuous cost management:**

```
1. Visibility: Track costs by service/team/environment
   - Cost Explorer
   - Tagging resources
   - Chargeback models

2. Right-sizing: Use only resources needed
   - Reserved Instances (3-year commitment, 72% discount)
   - Spot Instances (up to 90% discount, can be interrupted)
   - Savings Plans (flexible across families)

3. Automation:
   - Shutdown non-prod environments after hours
   - Delete unused resources (old snapshots, volumes)
   - Auto Scaling to handle variable load

4. Architecture:
   - Use serverless for variable workloads (Lambda)
   - Cache frequently accessed data
   - Use CDN to reduce data transfer costs
   - Choose cheaper regions if possible

5. Monitoring:
   - Budget alerts
   - Anomaly detection
   - Regular cost reviews
```

**Example savings:**
```
On-demand: $0.10 per hour
Reserved Instance: $0.03 per hour (70% savings)

Running 24/7 for year:
On-demand: $876/year
Reserved: $263/year
Savings: $613/year per instance
```

## 14. How do you handle secrets in production?

**Answer:**
**Never store in code/config:**
```
❌ password = "secret123" in GitHub
❌ API_KEY=abc123 in Docker image
❌ Private key in CloudFormation template
```

**Use AWS Secrets Manager:**
```python
import boto3
client = boto3.client('secretsmanager')

secret = client.get_secret_value(SecretId='prod/db-password')
password = secret['SecretString']
```

**Use Parameter Store (free):**
```python
ssm = boto3.client('ssm')
param = ssm.get_parameter(Name='/prod/api-key', WithDecryption=True)
api_key = param['Parameter']['Value']
```

**Environment variables with injection:**
```bash
# Not in code, injected at runtime
export DB_PASSWORD=$(aws secretsmanager get-secret-value --secret-id db-password --query SecretString --output text)
```

**Secrets in CI/CD:**
```
GitHub Actions:
- Store secrets in GitHub Secrets settings
- Use env: with secret reference
- Automatically masked in logs

CodePipeline:
- Store in Systems Manager Parameter Store
- Reference in buildspec.yml
- Audit via CloudTrail
```

## 15. What is SRE (Site Reliability Engineering) and DevOps relationship?

**Answer:**
**DevOps:**
- Culture of collaboration between dev and ops
- Automate everything
- Deploy frequently
- Focus: Delivery speed

**SRE:**
- Engineering approach to operations
- Measure reliability (SLOs, error budgets)
- Prevent toil (repetitive manual work)
- Focus: System reliability

**Key SRE concepts:**

**SLO (Service Level Objective):**
```
Example: 99.9% uptime = 43 minutes downtime/month
Example: p99 latency < 200ms
```

**Error budget:**
```
If SLO is 99.9% (0.1% errors allowed)
Over month: 0.1% × 43,200 minutes = 43 minutes of allowed downtime
Once reached: Freeze deployments to reduce risk
```

**Toil reduction:**
```
Instead of: Monthly manual OS patching
Implement: Fully automated patching system
```

**On-call rotation:**
```
Every engineer takes turns being on-call
- Paged for production issues
- Have runbooks for quick resolution
- Post-mortems document root causes
- Prevent burnout with alert tuning
```

**Runbooks (playbooks):**
```
Alert: High CPU on API servers
1. Check CloudWatch metrics
2. Check application logs for errors
3. Check recent deployments
4. If new deployment caused: Rollback or scale up
5. Contact team lead if cannot resolve in 5 minutes
```

**Reliability testing:**
- Chaos engineering
- Disaster recovery drills
- Load testing
- Incident simulations

**Relationship to DevOps:**
```
DevOps creates deployment infrastructure
SRE applies engineering to reliability

Together:
- Automated testing and deployment (DevOps)
- Measure and maintain reliability (SRE)
- Continuous improvement culture
- Focus on customer experience
```
