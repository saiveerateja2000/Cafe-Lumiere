# AWS DevOps Interview Prep: Load Balancing & Auto Scaling

## 1. What are the types of AWS Load Balancers?

**Answer:**
| Type | Layer | Use Case | Protocol |
|------|-------|----------|----------|
| **ELB (Classic)** | Layer 4/7 | Legacy apps, basic load balancing | HTTP/HTTPS, TCP |
| **ALB** | Layer 7 (Application) | Modern apps, path/hostname routing | HTTP/HTTPS |
| **NLB** | Layer 4 (Transport) | Extreme performance, gaming, IoT | TCP/UDP, millions of req/sec |
| **GWLB** | Layer 3 | Virtual appliances, security inspection | IP protocol |

## 2. Explain ALB path-based and hostname-based routing

**Answer:**
**Path-based routing:**
```
example.com/api/* → API service
example.com/static/* → Static content
example.com/admin/* → Admin service
```

**Hostname-based routing:**
```
api.example.com → API service
admin.example.com → Admin service
www.example.com → Web service
```

**Advantage:** Deploy multiple services on single ALB, reduce costs, simpler updates

## 3. How does connection draining (deregistration delay) work?

**Answer:**
- When instance is deregistered/unhealthy, ALB stops sending new requests
- Existing connections allowed to complete (default 300 seconds)
- Graceful shutdown of application
- If timeout exceeded, connections forcibly closed

**Configuration:**
```
Deregistration delay: 30-300 seconds (shorter = faster updates, longer = safer)
Connection timeout: 60 seconds (TCP idle timeout)
```

## 4. Describe Auto Scaling lifecycle hooks

**Answer:** Allows custom actions during scaling events:

**Termination Hook Example:**
```
Scaling signal received → Termination hook triggered → 
Custom code executes (app cleanup, log collection) → 
Instance terminates after hook timeout
```

**Use cases:**
- Drain connections gracefully
- Backup data from instance
- Deregister from service discovery
- Publish metrics before termination

## 5. What is the difference between target tracking and step scaling?

**Answer:**
**Target Tracking:**
- Maintains metric at target value (e.g., CPU 70%)
- AWS manages scaling automatically
- Simpler to configure
- Better for stable, predictable workloads

**Step Scaling:**
- Defined steps: if CPU > 80% → add 2 instances, if CPU > 90% → add 4 instances
- More granular control
- Requires manual policy management
- Better for rapid scaling needs

## 6. How would you handle deployment during Auto Scaling?

**Answer:**
1. **Update Launch Template** with new AMI/configuration
2. **Instance Refresh** - Gradually replace instances (respects min healthy percentage)
3. **Canary Deployment** - Replace 10% first, monitor, then continue
4. **Rolling Update** - Replace instances gradually to maintain availability

**Best practice:**
```
1. Test new AMI thoroughly
2. Update launch template
3. Create instance refresh with 90% min healthy percentage
4. Monitor CloudWatch metrics during refresh
5. Rollback if issues detected
```

## 7. Explain predictive scaling

**Answer:**
- Uses ML to forecast demand based on historical patterns
- Proactively scales before demand spike
- Combines with target tracking for optimal performance
- Good for predictable workloads (business hours, seasonal patterns)

**Example:** E-commerce site scales before holiday shopping season starts

## 8. What is lifecycle state transition and how do you handle failures?

**Answer:**
**States:**
- Pending → Running → InService
- Standby (manual pause without termination)
- Terminating → Terminated

**Failure handling:**
- Unhealthy instances detected via health checks
- Instance marked for termination
- Replaced with new instance
- If replacement fails, Auto Scaling retries

**CloudWatch alarms** should notify of scaling failures

## 9. How do you monitor Load Balancer performance?

**Answer:**
- **Request Count** - Track traffic volume
- **Target Response Time** - Application latency
- **HTTP 4xx/5xx Errors** - Request failures
- **Target Health** - Detect unhealthy instances
- **Active Connection Count** - Connection load
- **Processed Bytes** - Data throughput

**Alarms:** Alert on high error rate, response time > threshold

## 10. Explain cross-zone load balancing

**Answer:**
- Distributes traffic evenly across all AZs
- Without it: traffic distributed evenly across targets in each AZ (uneven per target)
- With it: traffic distributed evenly across ALL targets
- Slightly increases latency (inter-AZ traffic)

**Recommendation:** Enable for high availability, cost is minimal

## 11. What are sticky sessions and when to use them?

**Answer:**
- Sends requests from same client to same target
- **Duration-based** - Cookie expires after duration
- **Application-based** - Application-generated cookie

**Use cases:**
- Shopping cart state retention
- User session data not in external cache
- WebSocket connections

**Drawback:**
- Reduces load distribution
- If target fails, session lost
- Better solution: Use externalized session store (Redis, DynamoDB)

## 12. How would you troubleshoot high latency on ALB?

**Answer:**
1. **Check target health** - Verify all targets are healthy
2. **Monitor target response time** - Identify slow backend services
3. **Check target capacity** - Too few targets for traffic
4. **Verify security groups** - Confirm traffic allowed
5. **Check VPC routing** - Ensure proper routing between LB and targets
6. **Monitor ALB metrics** - Active connections, processed bytes
7. **Review target logs** - Application-level issues
8. **Consider connection draining** - May be causing delays
9. **Check cross-zone status** - Network bottlenecks
10. **Profile application** - Use X-Ray for service bottlenecks

## 13. Explain target groups and their importance

**Answer:**
- Logical set of targets (EC2, Lambda, on-premises servers)
- Defined by protocol and port
- Health checks monitor target health
- Can have multiple target groups per ALB

**Key configurations:**
- Health check path, port, interval, timeout
- Healthy/unhealthy thresholds
- Stickiness settings
- Protocol version (HTTP/1.1, HTTP/2, gRPC)

## 14. What is connection multiplexing on ALB?

**Answer:**
- HTTP/2 and gRPC support allows multiplexing
- Multiple requests over single connection
- Reduces connection overhead
- Improves throughput and reduces latency

**Configuration:** Set target protocol to HTTP2 or gRPC in target group settings
