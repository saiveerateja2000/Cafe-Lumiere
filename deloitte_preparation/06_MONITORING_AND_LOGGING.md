# AWS DevOps Interview Prep: Monitoring & Logging

## 1. What is CloudWatch and its key components?

**Answer:** AWS's monitoring and logging service:

**Metrics:**
- Performance data from AWS resources
- CPU utilization, network throughput, disk I/O
- Custom metrics from application/agent
- 1-minute to 5-minute granularity (detailed monitoring)

**Logs:**
- Application logs, system logs, 3rd party service logs
- Log Groups (logical grouping), Log Streams (sequence of events)
- Log retention policies (never expire to 1 day to 10 years)

**Alarms:**
- Monitor metrics and trigger actions
- SNS notifications, Auto Scaling actions, EC2 actions
- States: OK, ALARM, INSUFFICIENT_DATA

**Events (EventBridge):**
- React to system events
- Trigger Lambda, SNS, CodePipeline, etc.

## 2. How do you setup CloudWatch alarms for production?

**Answer:**
**CPU Alarm:**
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name high-cpu \
  --alarm-description "Alert when CPU > 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --alarm-actions arn:aws:sns:us-east-1:account:topic
```

**Key parameters:**
- **Statistic** - Average, Sum, Minimum, Maximum, SampleCount
- **Period** - Evaluation window (60-3600 seconds)
- **EvaluationPeriods** - How many periods to breach alarm
- **Threshold** - Trigger value

**Best practices:**
- Set meaningful alarm names
- Use SNS for notifications
- Create alarms for:
  - CPU > 80%
  - Memory > 85%
  - Disk space < 10%
  - Network errors
  - Application errors
  - Database connections

## 3. What is CloudWatch Agent and how to configure it?

**Answer:** Agent for collecting metrics beyond standard CloudWatch:

**Installation:**
```bash
wget https://s3.amazonaws.com/amazoncloudwatch-agent/linux/amd64/latest/amazon-cloudwatch-agent.rpm
rpm -U ./amazon-cloudwatch-agent.rpm
```

**Configuration (agent-config.json):**
```json
{
  "metrics": {
    "namespace": "MyApp",
    "metrics_collected": {
      "mem": {
        "measurement": [
          {
            "name": "mem_used_percent",
            "rename": "MemoryUtilization",
            "unit": "Percent"
          }
        ],
        "metrics_collection_interval": 60
      },
      "disk": {
        "measurement": [{"name": "used_percent"}],
        "metrics_collection_interval": 60,
        "resources": ["/"]
      }
    }
  },
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/application.log",
            "log_group_name": "/aws/ec2/application",
            "log_stream_name": "{instance_id}"
          }
        ]
      }
    }
  }
}
```

**Metrics collected:**
- Memory utilization
- Disk space usage
- Disk I/O
- Network interfaces
- CPU detailed metrics
- Processes

## 4. Explain CloudWatch Insights and how to use it

**Answer:** Powerful query language for logs (like SQL):

**Queries:**
```
# Find errors in logs
fields @timestamp, @message | filter @message like /ERROR/ | stats count() by @message

# Response time analysis
fields @duration | stats avg(@duration), max(@duration), pct(@duration, 95)

# Count requests by status code
fields @status | stats count() by @status
```

**Common use cases:**
- Troubleshooting application errors
- Performance analysis
- Security investigation
- Usage patterns

**Benefits:**
- No need to export to separate tools
- Fast querying of large log volumes
- Visualization of results

## 5. What is X-Ray and how does it work?

**Answer:** Distributed tracing service for microservices:

**Components:**
- **X-Ray Daemon** - Collects trace data (runs on EC2/Lambda)
- **SDKs** - Instrument application code
- **Console** - Visualize service map and traces

**Service map visualizes:**
- Service dependencies
- Latency between services
- Error rates
- Throttling

**Example (Python Flask):**
```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

app = Flask(__name__)
XRayMiddleware(app, xray_recorder)

@app.route('/api/order')
@xray_recorder.capture('create_order')
def create_order():
    # Application code
```

**Insights provided:**
- Request flow through services
- Bottlenecks and latency
- Errors and exceptions
- Database query performance
- External API calls

## 6. How do you implement centralized logging?

**Answer:**
**CloudWatch Logs aggregation:**
```
EC2 → CloudWatch Logs Agent → CloudWatch Logs
ECS → CloudWatch Logs driver → CloudWatch Logs
Lambda → Automatic logging → CloudWatch Logs
ALB → Access logs → S3 → CloudWatch Logs Insights
```

**Multi-account logging (using Kinesis):**
```
App logs → Kinesis Firehose → S3 + CloudWatch Logs
Allows cross-account log analysis
```

**Log retention:**
```
CloudWatch → Set retention policy (30/60/90 days)
Old logs automatically deleted
Alternatively export to S3 for long-term archival
```

**Log aggregation tools:**
- CloudWatch Logs (AWS-native)
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Splunk (enterprise logging)
- Datadog (cloud monitoring)

## 7. Explain CloudWatch composite alarms

**Answer:**
Combine multiple alarms into single alarm:

```bash
aws cloudwatch put-composite-alarm \
  --alarm-name "Application-Health" \
  --alarm-rule "(ALARM(cpu-alarm) OR ALARM(memory-alarm)) AND OK(disk-alarm)" \
  --actions-enabled \
  --alarm-actions arn:aws:sns:us-east-1:account:topic
```

**Use cases:**
- Dashboard health overall
- Reduce alert fatigue
- Complex alerting logic
- Weighted alerting (2 out of 3 must fail)

## 8. What is CloudWatch EventBridge?

**Answer:** Event-driven architecture service:

**Features:**
- **Event sources** - AWS services, SaaS, custom apps
- **Rules** - Route events to targets
- **Targets** - Lambda, SNS, SQS, CodePipeline, etc.

**Example (Auto-scaling on CPU spike):**
```json
{
  "Name": "scale-on-cpu",
  "EventPattern": {
    "source": ["aws.cloudwatch"],
    "detail-type": ["CloudWatch Alarm State Change"],
    "detail": {
      "state": {
        "value": ["ALARM"]
      }
    }
  },
  "Targets": [{
    "Arn": "arn:aws:autoscaling:region:account:...",
    "RoleArn": "arn:aws:iam::account:role/service-role"
  }]
}
```

**Advantages over SNS:**
- Content-based filtering
- Multiple targets
- Built-in transformations
- Event replay

## 9. How would you troubleshoot high latency in application?

**Answer:**
1. **CloudWatch metrics:**
   ```
   ALB Target Response Time → Application is slow
   ALB Active Connection Count → Too many connections
   ```

2. **X-Ray service map:**
   - Identify slowest service
   - Check database queries
   - Check external API calls

3. **CloudWatch Insights on application logs:**
   ```
   fields @duration | stats avg(@duration) by @operation
   ```

4. **Database performance:**
   - Query performance insights
   - Slow query logs
   - Connection pooling issues

5. **Infrastructure metrics:**
   - CPU utilization
   - Memory pressure
   - Disk I/O
   - Network latency

6. **Application profiling:**
   - APM tools (New Relic, Datadog)
   - Custom instrumentation

## 10. Explain synthetic monitoring and canary deployments

**Answer:**
**CloudWatch Synthetics:**
- Periodically test endpoints
- Detect issues before customers
- Measure user experience
- Create canary scripts in Node.js or Python

**Canary script (Node.js):**
```javascript
const synthetics = require('Synthetics');

const apiCanary = async function () {
  const get_options = {
    hostname: 'api.example.com',
    port: 443,
    path: '/api/health',
    method: 'GET'
  };

  const response = await synthetics.executeHttpStep(
    'CheckAPI',
    get_options,
    undefined,
    { includeRequestHeaders: true, includeResponseHeaders: true }
  );

  if (response.statusCode !== 200) {
    throw 'API returned ' + response.statusCode;
  }
};

exports.handler = async function() {
  return await apiCanary();
};
```

**Metrics from canaries:**
- Success/failure rate
- Response latency
- Visual screenshots (headless browser)

**Use:** Detect availability issues, performance degradation before users affected

## 11. How do you implement dashboards for operations team?

**Answer:**
**CloudWatch Dashboard:**
```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/EC2", "CPUUtilization"],
          ["AWS/RDS", "DatabaseConnections"],
          ["AWS/ApplicationELB", "TargetResponseTime"]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "Infrastructure Health"
      }
    },
    {
      "type": "log",
      "properties": {
        "query": "fields @timestamp, @message | filter @message like /ERROR/ | stats count()",
        "region": "us-east-1",
        "title": "Error Count"
      }
    }
  ]
}
```

**Best practices:**
- High-level overview
- Key metrics only (avoid clutter)
- Color coding for health
- Real-time updates (60-second refresh)
- Team-specific dashboards

## 12. What is CloudWatch Logs Subscriptions?

**Answer:**
Stream logs to other services in real-time:

```bash
aws logs put-subscription-filter \
  --log-group-name "/aws/lambda/myfunction" \
  --filter-name "ErrorFilter" \
  --filter-pattern "[ERROR]" \
  --destination-arn "arn:aws:lambda:region:account:function:process-logs"
```

**Targets:**
- Lambda (process and transform logs)
- Kinesis (real-time streaming)
- Kinesis Firehose (load to S3, Redshift)
- CloudWatch Logs Insights

**Use cases:**
- Filter and forward specific logs
- Real-time log processing
- Centralize logs from multiple accounts
- Stream to 3rd party tools

## 13. Explain VPC Flow Logs

**Answer:**
Capture network traffic information:

```
eni-12345 123456789012 10.0.0.3 10.0.0.4 443 52341 6 64 1024 1612345678 1612345679 ACCEPT OK
srcip destip sourceport destport protocol packets bytes
```

**Setup:**
```bash
aws ec2 create-flow-logs \
  --resource-type NetworkInterface \
  --resource-ids eni-12345 \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name "/aws/vpc/flowlogs"
```

**Fields:**
- Source/destination IP
- Source/destination port
- Protocol
- Bytes, packets transferred
- Accept/Reject status

**Use cases:**
- Monitor traffic patterns
- Troubleshoot connectivity issues
- Security analysis
- Compliance auditing

## 14. How would you monitor database performance?

**Answer:**
**RDS Performance Insights:**
- Visual dashboard of database load
- Identify bottlenecks
- DB-specific metrics

**CloudWatch metrics:**
- CPU utilization
- Database connections
- Read/write IOPS
- Storage space
- Query latency

**Enhanced monitoring:**
- OS-level metrics
- Per-process CPU/memory
- Network throughput

**Slow query logs:**
```sql
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;
```

## 15. What are best practices for production monitoring?

**Answer:**
1. **Key metrics:**
   - Availability (uptime %)
   - Latency (p50, p95, p99)
   - Error rate (4xx, 5xx)
   - Throughput (requests/sec)
   - Resource utilization (CPU, memory, disk)

2. **Alert design:**
   - Alert on business metrics (not just infrastructure)
   - Avoid alert fatigue
   - Clear escalation paths
   - Runbooks for each alert

3. **Logging:**
   - Structured logging (JSON format)
   - Correlation IDs for tracing requests
   - Log important state changes
   - Don't log sensitive data

4. **Dashboards:**
   - One dashboard per team
   - Key metrics at glance
   - Update frequently for accuracy

5. **Testing:**
   - Synthetic monitoring for API endpoints
   - Load testing before peak times
   - Chaos engineering for resilience

6. **Cost:**
   - Monitor AWS costs
   - Alert on budget thresholds
   - Right-size resources
