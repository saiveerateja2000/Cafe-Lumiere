# AWS DevOps Interview Prep: Networking & Database

## 1. What is VPC and its key components?

**Answer:** Virtual Private Cloud - Isolated network environment:

**Components:**
- **Subnets** - CIDR blocks (segments of VPC)
- **Route tables** - Define traffic routing
- **Internet Gateway** - Connect to internet
- **NAT Gateway** - Allow private resources to reach internet
- **VPC Peering** - Connect VPCs
- **VPC Flow Logs** - Monitor traffic

**VPC example:**
```
VPC (CIDR: 10.0.0.0/16)
├── Public Subnet (10.0.1.0/24)
│   ├── ALB
│   └── NAT Gateway
├── Private Subnet (10.0.2.0/24)
│   └── Application servers
└── Database Subnet (10.0.3.0/24)
    └── RDS
```

**Routing:**
```
Traffic from internet → Internet Gateway → Route Table (0.0.0.0/0 → IGW) → Public subnet
Traffic from private subnet to internet → NAT Gateway → Internet Gateway → Internet
Private to database → Direct route through VPC
```

## 2. Explain Route 53 and its use in DevOps

**Answer:** AWS's DNS service:

**Routing policies:**
- **Simple** - Single resource
- **Weighted** - Distribute traffic by percentage
- **Latency** - Route to lowest latency region
- **Failover** - Active-passive failover
- **Geolocation** - Route by geographic location
- **Geoproximity** - Route based on geographic proximity + bias
- **Multi-value** - Return multiple values

**Health checks:**
```bash
aws route53 create-health-check \
  --health-check-config "Type=HTTP,ResourcePath=/health,FullyQualifiedDomainName=api.example.com,Port=80"
```

**Example (weighted routing):**
```
example.com
├── 70% → v1.example.com (stable version)
└── 30% → v2.example.com (canary version)
```

**DevOps use cases:**
- Blue/green deployments
- Gradual traffic shifting
- Geographic load balancing
- Multi-region failover
- A/B testing

## 3. What is CloudFront and how does it improve performance?

**Answer:** Global content delivery network (CDN):

**How it works:**
```
User request → CloudFront edge location (nearest) → 
If cached: Return from cache (low latency)
If not: Fetch from origin → Cache → Return to user
```

**Origins:**
- S3 buckets
- Application Load Balancer
- API Gateway
- Custom HTTP servers

**Benefits:**
- Reduced latency (users get content from nearest edge)
- Reduced origin load (caching)
- DDoS protection
- HTTPS encryption
- Cost reduction (transfer between edge and origin cheaper)

**Caching:**
```
Cache-Control: max-age=3600  # Cache for 1 hour
Vary: Accept-Encoding         # Cache based on compression
```

**Invalidation:**
```bash
aws cloudfront create-invalidation \
  --distribution-id E27XX0EXAMPLE \
  --paths "/index.html" "/assets/*"
```

## 4. Explain VPC peering and transit gateway

**Answer:**
**VPC Peering:**
- Direct connection between two VPCs
- Private IP communication
- Low latency, no internet gateway needed
- Limits: Transitive peering not allowed, CIDR overlap issues

**Example:**
```
VPC A (10.0.0.0/16) ← Peering → VPC B (172.31.0.0/16)
Bidirectional routing required in both route tables
```

**Transit Gateway:**
- Hub-and-spoke network topology
- Simplifies connections between VPCs, on-premises, and branch offices
- Single attachment point
- Simpler management, transitive peering works

**Example:**
```
On-premises ←→ Transit Gateway ←→ VPC A
                            ↑
                            VPC B
                            ↓
                           VPC C
```

**When to use:**
- Few VPCs (< 10): VPC Peering
- Many VPCs, complex topology: Transit Gateway

## 5. What is RDS and its deployment options?

**Answer:** Managed relational database service:

**Database engines:**
- MySQL
- PostgreSQL
- MariaDB
- Oracle
- SQL Server
- Aurora (AWS-proprietary)

**Deployment options:**
- **Single-AZ** - Cost-effective, no high availability
- **Multi-AZ** - Standby replica, automatic failover, higher cost but HA

**Aurora:**
- Faster than traditional RDS
- 5x faster than MySQL, 3x faster than PostgreSQL
- Automatic failover within region
- Read replicas across regions
- More expensive but better performance

**Backup:**
```
Automated backups: 7 days (configurable 1-35 days)
Manual snapshots: Keep indefinitely
Point-in-time recovery: Within retention window
```

## 6. Explain RDS read replicas and Multi-AZ

**Answer:**
**Read Replicas:**
```
Primary DB (write)
├── Read Replica 1 (same AZ or different region)
├── Read Replica 2 (same AZ or different region)
└── Read Replica 3 (same AZ or different region)
```

- Asynchronous replication (slight lag acceptable)
- Can be promoted to independent database
- Reduces read load on primary
- Good for reporting, analytics
- RPO (Recovery Point Objective): Acceptable data loss

**Multi-AZ:**
```
Primary DB (write) ← Synchronous replication → Standby (no read traffic)
If primary fails → Automatic failover to standby
```

- Synchronous replication (no data loss)
- Only for failover, not performance
- RTO (Recovery Time Objective): Seconds
- Higher cost than read replicas

**Use cases:**
- Read replicas: Scale read traffic, improve performance
- Multi-AZ: High availability, disaster recovery

## 7. What is DynamoDB and when to use it?

**Answer:** Fully managed NoSQL database:

**Key differences from RDS:**
- Schemaless (flexible structure)
- Horizontal scalability (automatic)
- Single-digit millisecond latency
- Pay per request or provisioned capacity
- No SQL queries (only key-value/range queries)

**DynamoDB components:**
- **Table** - Collection of items
- **Partition key** - Unique identifier
- **Sort key** - Optional secondary ordering
- **GSI** (Global Secondary Index) - Query on different attributes
- **TTL** - Auto-expire items

**Example:**
```json
{
  "OrderId": "12345",           // Partition key
  "Timestamp": "2024-01-01",    // Sort key
  "CustomerId": "cust-123",
  "Status": "delivered",
  "Items": [...]
}
```

**Use cases:**
- Real-time analytics
- IoT data
- Mobile apps
- Gaming leaderboards
- Session storage
- Caching layer

**vs RDS:**
- DynamoDB: Unstructured data, high throughput, no complex queries
- RDS: Structured data, complex queries, transactions

## 8. Explain database backup and disaster recovery

**Answer:**
**RDS backups:**
```
Daily snapshot → Stored in S3
+ Transaction logs → Point-in-time recovery
Retention: 1-35 days
```

**Multi-region replication:**
```
Primary region → Cross-region read replica → Can promote if disaster
RTO: Minutes, RPO: Seconds
```

**Disaster recovery strategies (RPO/RTO):**
| Strategy | RPO | RTO | Cost |
|----------|-----|-----|------|
| **Backup & Restore** | Hours | Hours | Low |
| **Pilot light** | Minutes | 10s minutes | Low-Medium |
| **Warm standby** | Seconds | 1-2 minutes | Medium |
| **Hot/Hot active-active** | None | None | High |

**Implementation:**
```
Production (Primary) → Continuous replication → 
Standby (Warm standby in different region)

On disaster:
1. Update DNS/Route 53 to point to standby
2. Promote standby to primary
3. Restore applications pointing to new primary
```

## 9. How do you implement high availability for databases?

**Answer:**
1. **Multi-AZ deployment:**
   ```
   Reduces AZ failure impact
   Minimal latency between primary and standby
   ```

2. **Read replicas for reads:**
   ```
   Distribute read traffic
   Separate reporting from transactional load
   ```

3. **Connection pooling:**
   ```
   Reuse connections instead of creating new ones
   Reduce connection overhead
   ```

4. **Caching (Redis/ElastiCache):**
   ```
   Cache frequently accessed data
   Reduce database load
   Low latency for hot data
   ```

5. **Database clustering:**
   ```
   Aurora: Automatic failover within region
   Multi-node: More resilient
   ```

## 10. What is ElastiCache and when to use it?

**Answer:** Fully managed in-memory cache:

**Engines:**
- **Redis** - Complex data structures, pub/sub, transactions
- **Memcached** - Simple key-value, distributed caching

**Use cases:**
- Session storage
- Real-time leaderboards
- Rate limiting
- Caching database queries
- Pub/sub messaging

**Architecture:**
```
Application → ElastiCache (Redis/Memcached) → Database
Cache miss → Fetch from DB → Update cache → Return to application
```

**Cache strategies:**
- **Lazy loading** - Load on miss, complexity on first access
- **Write-through** - Update cache when database updates, double writes
- **Refresh-ahead** - Proactively refresh cache before expiration

## 11. How would you optimize database performance?

**Answer:**
1. **Index design:**
   ```sql
   CREATE INDEX idx_customer ON orders(customer_id);
   Create indexes on frequently queried columns
   Monitor unused indexes (performance overhead)
   ```

2. **Query optimization:**
   ```sql
   SELECT id, name FROM customers WHERE status = 'active';
   NOT: SELECT * FROM customers WHERE status = 'active';
   ```

3. **Connection pooling:**
   ```
   Reuse connections: 10-20 connections for 100s of requests
   Reduce connection establishment overhead
   ```

4. **Read replicas:**
   ```
   Separate read traffic from writes
   Reporting queries don't impact transactional database
   ```

5. **Caching:**
   ```
   Cache frequently accessed data
   Reduce database load
   Faster response times
   ```

6. **Database tuning:**
   - Buffer pool size (MySQL)
   - Shared buffers (PostgreSQL)
   - Cost-based optimizer parameters
   - Connection pool size

## 12. Explain database migration strategies

**Answer:**
**AWS DMS (Database Migration Service):**
- Migrate from on-premises or other cloud to AWS
- Minimal downtime
- Schema conversion available for different database engines

**Migration approaches:**

**Homogeneous (MySQL → MySQL):**
```
Custom replication → Golden gate → AWS DMS
Simpler, field mapping already known
```

**Heterogeneous (Oracle → PostgreSQL):**
```
Schema conversion tool → Map Oracle objects to PostgreSQL
More complex, requires transformation
```

**Phases:**
```
1. Full load - Initial data transfer
2. CDC (Change Data Capture) - Capture ongoing changes
3. Validation - Verify data consistency
4. Cutover - Switch to new database
5. Rollback - Plan B if issues detected
```

## 13. What is eventual consistency and how does it affect DevOps?

**Answer:**
- DynamoDB is eventually consistent
- Data replicated across partitions, takes few milliseconds
- Strong consistency option available (higher cost, latency)

**Example:**
```
Write operation → Acknowledge to user (written to partition)
→ Replicate to other partitions (takes milliseconds)
→ If read immediately from different partition, might get old data

For strong consistency: Read from primary partition only
```

**DevOps implications:**
- Session data fine with eventual consistency
- Financial transactions need strong consistency
- Design for consistency requirements
- Test with realistic data volumes

## 14. How do you monitor database health in production?

**Answer:**
**CloudWatch metrics (RDS):**
- CPU utilization
- Database connections
- Read/write throughput (IOPS)
- Network receive/transmit
- Storage space

**Enhanced monitoring:**
```
OS-level metrics visible
Specific process CPU/memory usage
Helps identify slow queries from application
```

**Performance Insights:**
- Visual view of database load
- Identify bottlenecks
- SQL statement performance
- Per-user analysis

**Slow query logs (MySQL):**
```sql
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2; -- 2+ second queries
```

**Alarms:**
- High CPU utilization (> 80%)
- Low free storage (<10%)
- High connection count (approaching limit)
- High read/write latency

## 15. What are database best practices for zero-downtime deployments?

**Answer:**
1. **Schema changes:**
   ```sql
   -- Add column with default
   ALTER TABLE orders ADD COLUMN new_field VARCHAR(100) DEFAULT '';
   -- Update existing rows gradually
   -- Remove default when done
   ```

2. **Read replicas for testing:**
   ```
   Promote read replica
   Test migrations on replica
   If OK, promote to primary
   If not, revert quickly
   ```

3. **Blue/green database pattern:**
   ```
   Same schema on both databases
   Initially replicate from blue to green
   Test green thoroughly
   Switch connection strings (Route 53)
   ```

4. **Backward compatibility:**
   ```
   Old code must work with new schema
   New code must work with old schema during transition
   Remove old code only after all instances updated
   ```

5. **Rollback plan:**
   ```
   Keep database backup from before migration
   Keep old application version running (blue)
   Can quickly fall back if green has issues
   ```

6. **Testing:**
   ```
   Test migrations with prod-like data volume
   Load test schema changes
   Monitor performance before/after
   Have incident response plan
   ```
