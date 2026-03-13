# AWS DevOps Interview Prep: EC2 & Compute

## 1. What is EC2 and what are its key benefits?

**Answer:** EC2 (Elastic Compute Cloud) is AWS's virtual computing service. Key benefits:
- **Elasticity** - Scale up/down based on demand
- **Cost-effective** - Pay-as-you-go pricing
- **Flexible** - Multiple instance types and sizes
- **Reliable** - SLAs and multi-AZ deployment
- **Security** - VPC integration, security groups, IAM roles
- **Performance** - Various instance families optimized for different workloads

## 2. Explain EC2 instance types and use cases

**Answer:**
- **General Purpose (M5, M6i)** - Balanced compute/memory/network, web servers, SMB databases
- **Compute Optimized (C5, C6i)** - High-performance processors, batch processing, ML inference
- **Memory Optimized (R5, X1)** - High RAM, in-memory databases, caching
- **Storage Optimized (I3, H1)** - High IOPS/throughput, NoSQL databases, data warehousing
- **Accelerated Computing (P3, G4)** - GPU/FPGA instances, ML training, graphics rendering

## 3. What are EC2 lifecycle states?

**Answer:**
- **Pending** - Instance launching
- **Running** - Instance is active and can accept traffic
- **Stopping** - Instance shutting down gracefully
- **Stopped** - Instance stopped (can be restarted, storage persists)
- **Shutting-down** - Instance terminating
- **Terminated** - Instance removed, storage deleted (no recovery possible)

## 4. Explain EC2 pricing models

**Answer:**
- **On-Demand** - Pay per hour, highest cost, best for unpredictable workloads
- **Reserved Instances (RI)** - Commit 1-3 years, up to 72% discount, predictable workloads
- **Spot Instances** - Up to 90% discount, but can be interrupted, for fault-tolerant apps
- **Dedicated Hosts** - Physical servers for licensing/compliance needs
- **Savings Plans** - Flexible commitment across instance families

## 5. What is an AMI (Amazon Machine Image)?

**Answer:** AMI is a pre-configured template containing:
- Operating system (Windows, Linux, macOS)
- Pre-installed software and applications
- Configuration settings
- Launch permissions
- Block device mapping

**Why important:** Enables quick instance launches, consistency, and sharing. Can be created from running instances as custom AMIs.

## 6. Explain Security Groups and Network ACLs

**Answer:**
| Feature | Security Groups | NACLs |
|---------|-----------------|-------|
| **Level** | Instance-level | Subnet-level |
| **Type** | Stateful | Stateless |
| **Default** | Deny all inbound | Allow all |
| **Rules** | Allow only | Allow/Deny |
| **Performance** | Better | Detailed control |

**Use:** Security Groups for app-level firewall, NACLs for subnet-wide traffic control

## 7. What is an Elastic IP and when would you use it?

**Answer:** Elastic IP is a static public IPv4 address that:
- Persists across stop/start cycles (unlike regular public IPs)
- Can be remapped to any instance in your account
- Charged when not associated

**Use cases:**
- Mail servers (consistent IP for DNS)
- APIs requiring static IP whitelisting
- Failover scenarios with quick IP remapping

## 8. How do you achieve high availability with EC2?

**Answer:**
- **Multi-AZ Deployment** - Distribute instances across availability zones
- **Load Balancing** - Use ELB/ALB/NLB to distribute traffic
- **Auto Scaling** - Automatically adjust capacity
- **Health Checks** - Remove unhealthy instances
- **RDS Multi-AZ** - Database failover
- **Route 53** - DNS failover with health checks

## 9. What is AWS Systems Manager and its use in DevOps?

**Answer:** Systems Manager helps manage EC2 instances and on-premises servers:
- **Session Manager** - Secure shell access without SSH/RDP
- **Parameter Store** - Centralized config management
- **Patch Manager** - Automated patching
- **Automation** - Workflow execution across instances
- **Inventory** - Track software/hardware across fleet

## 10. Explain EC2 user data and its role in automation

**Answer:** User data is a script that runs when instance launches (runs as root):
```bash
#!/bin/bash
yum update -y
yum install httpd -y
systemctl start httpd
```

**Key points:**
- Executes only on first boot
- Limited to 16 KB base64-encoded data
- Good for automation but not ideal for large deployments (use AMIs instead)
- Visible in metadata, so don't include sensitive data

## 11. What is Auto Scaling and its components?

**Answer:**
- **Launch Template/Configuration** - Specifies instance type, AMI, security groups
- **Auto Scaling Group** - Manages instance scaling based on policies
- **Scaling Policies** - Define when to scale (target tracking, step scaling, scheduled)
- **Health Checks** - Determines instance health (ELB or EC2)

**Best practice:** Use target tracking (e.g., CPU 70%) for simplicity

## 12. How would you implement instance monitoring in production?

**Answer:**
- **CloudWatch** - CPU, network, disk metrics
- **CloudWatch Agent** - Memory, disk utilization, custom metrics
- **X-Ray** - Application performance and service tracing
- **Third-party tools** - New Relic, Datadog, Prometheus
- **Alarms** - SNS notifications for threshold breaches
- **Logs** - Stream instance logs to CloudWatch Logs

**Key metrics:** CPU%, memory%, disk I/O, network throughput, application response time
