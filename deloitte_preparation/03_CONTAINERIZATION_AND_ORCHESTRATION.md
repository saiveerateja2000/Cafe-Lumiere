# AWS DevOps Interview Prep: Containerization & Orchestration

## 1. What is Docker and why is it important in DevOps?

**Answer:** Docker is containerization technology that packages applications with dependencies in isolated environments:
- **Consistency** - Dev, test, production environments identical
- **Portability** - Runs anywhere (laptop, server, cloud)
- **Efficiency** - Lightweight compared to VMs
- **Scalability** - Easy to spin up multiple containers
- **Isolation** - Containers don't interfere with each other

**DevOps value:** Enables Infrastructure as Code, reproducible builds, faster deployments

## 2. Explain Dockerfile components and best practices

**Answer:**
```dockerfile
FROM ubuntu:20.04                    # Base image
WORKDIR /app                         # Working directory
COPY . /app                          # Copy files
RUN apt-get update && \              # Install dependencies
    apt-get install -y python3
ENV APP_ENV=production               # Environment variable
EXPOSE 8000                          # Exposed port
CMD ["python3", "app.py"]            # Default command
```

**Best practices:**
- Use specific base image tags (not 'latest')
- Minimize layer count (combine RUN commands)
- Use .dockerignore to exclude unnecessary files
- Run as non-root user for security
- Keep images small (use Alpine as base)
- Multi-stage builds for smaller final images

## 3. What is ECS (Elastic Container Service)?

**Answer:** AWS's container orchestration service:
- **Managed service** - AWS handles orchestration infrastructure
- **Launch types:**
  - EC2: You manage EC2 instances
  - Fargate: Serverless, AWS manages infrastructure
- **Task Definition** - Docker image, memory, CPU, environment variables
- **Service** - Maintains running tasks, handles load balancing, scaling
- **Cluster** - Group of resources where tasks run

**vs Kubernetes:** Simpler, AWS-native, less operational overhead

## 4. Explain ECS service deployment strategies

**Answer:**
**Rolling:**
- Replace one task at a time
- Maintains service availability
- Slower deployment
- Default strategy

**Blue/Green:**
- New version (green) deployed alongside old (blue)
- Traffic switched atomically
- Quick rollback available
- Higher resource usage temporarily

**Canary:**
- Route small traffic % to new version
- Monitor metrics
- Gradually increase traffic
- Minimize blast radius of bugs

## 5. What is EKS (Elastic Kubernetes Service)?

**Answer:** 
- AWS-managed Kubernetes service
- Handles master node management
- You manage worker nodes (EC2 or Fargate)
- Fully compatible with standard Kubernetes
- Integrates with IAM, VPC, CloudWatch, etc.

**vs ECS:**
- EKS: Complex workloads, Kubernetes ecosystem, multi-cloud strategy
- ECS: Simpler AWS-native deployments, less operational overhead

## 6. Explain container networking in ECS

**Answer:**
**Bridge mode:**
- Container port mapped to host port
- Dynamic port allocation
- Multiple containers per host

**Host mode:**
- Container uses host's network
- High performance
- Port conflicts possible

**awsvpc mode (recommended):**
- Container gets independent ENI (Elastic Network Interface)
- Every container has own IP
- Better security and network isolation
- Required for Fargate

## 7. How do you implement container logging in ECS?

**Answer:**
**CloudWatch Logs** (easiest):
```json
{
  "logDriver": "awslogs",
  "options": {
    "awslogs-group": "/ecs/my-service",
    "awslogs-region": "us-east-1",
    "awslogs-stream-prefix": "ecs"
  }
}
```

**Other options:**
- Splunk
- Datadog
- New Relic
- S3
- AWS FireLens for log router (Fluent Bit, Logstash)

**CloudWatch Insights:** Query logs like SQL

## 8. Explain task definition and its key components

**Answer:**
```json
{
  "family": "my-app",
  "containerDefinitions": [
    {
      "name": "app",
      "image": "my-app:latest",
      "cpu": 256,
      "memory": 512,
      "portMappings": [{"containerPort": 8000}],
      "environment": [{"name": "ENV", "value": "prod"}],
      "logConfiguration": {...}
    }
  ],
  "taskRoleArn": "arn:aws:iam::account:role/task-role",
  "executionRoleArn": "arn:aws:iam::account:role/execution-role"
}
```

**Key points:**
- Can have multiple containers (sidecar pattern)
- Task role for application permissions
- Execution role for pulling images and logging

## 9. What is ECR (Elastic Container Registry)?

**Answer:** AWS's private Docker registry:
- **Security** - Images stored securely, integrated with IAM
- **Lifecycle policies** - Auto-delete old images
- **Scanning** - ECR image scanning for vulnerabilities
- **Push/Pull** - Via Docker CLI with temporary credentials
- **Integration** - Native with ECS, EKS, CodePipeline

**Advantages over Docker Hub:**
- Private by default
- Better security
- No rate limiting
- Integrated with AWS services

## 10. How would you implement container health checks?

**Answer:**
```json
{
  "healthCheck": {
    "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
    "interval": 30,
    "timeout": 5,
    "retries": 3,
    "startPeriod": 60
  }
}
```

**Key parameters:**
- **interval** - Check frequency (seconds)
- **timeout** - Wait time for response
- **retries** - Failures before marking unhealthy
- **startPeriod** - Startup grace period

**ECS behavior:** Unhealthy tasks replaced automatically

## 11. Explain sidecar pattern in containers

**Answer:** Additional container running alongside main container:

**Example (Logging sidecar):**
```
Main Container (app) → logs to file
Sidecar Container (log router) → reads file → sends to CloudWatch
```

**Other sidecars:**
- X-Ray daemon for tracing
- CloudWatch agent for custom metrics
- Secret manager for rotating secrets
- Reverse proxy for traffic management

**Task definition:** Multiple container definitions in same task

## 12. How do you handle secrets in container deployments?

**Answer:**
**NOT in environment variables (visible in task definition):**
```
❌ ENV API_KEY=secret123  # Visible in console and logs
```

**Better approaches:**
1. **AWS Secrets Manager:**
   ```json
   {
     "secrets": [
       {
         "name": "DB_PASSWORD",
         "valueFrom": "arn:aws:secretsmanager:region:account:secret:db-password"
       }
     ]
   }
   ```

2. **Parameter Store:**
   ```json
   {
     "secrets": [
       {
         "name": "API_KEY",
         "valueFrom": "arn:aws:ssm:region:account:parameter/api-key"
       }
     ]
   }
   ```

3. **IAM Role:** Let container assume role for AWS service access

## 13. What is the difference between task and service in ECS?

**Answer:**
| Aspect | Task | Service |
|--------|------|---------|
| **Definition** | Single instance of task definition | Manages multiple task instances |
| **Lifecycle** | Runs once, stops when done | Continuous, restarts if stopped |
| **Use case** | One-time jobs, batch processing | Long-running applications |
| **Load Balancing** | Not integrated | Auto integrated with ELB/ALB/NLB |
| **Scaling** | Manual | Auto Scaling support |

**Example:** Task for cron job, Service for web server

## 14. How would you troubleshoot a failing container in ECS?

**Answer:**
1. **Check task status** - Pending, running, stopped reason
2. **Review CloudWatch Logs** - Container stdout/stderr
3. **Verify task definition** - CPU/memory allocated, image exists
4. **Check security groups** - Network access allowed
5. **Verify IAM permissions** - Execution role can pull image and write logs
6. **Container exit codes** - Non-zero means failure
7. **Use ECS Exec** - Execute shell in running task
   ```bash
   aws ecs execute-command --cluster my-cluster --task task-id \
     --container container-name --interactive --command "/bin/sh"
   ```
8. **Check resource constraints** - Out of memory, CPU throttling

## 15. Explain container optimization for DevOps

**Answer:**
- **Image size** - Use Alpine, multi-stage builds (~100MB vs 1GB)
- **Layer caching** - Minimize layers that change frequently
- **Startup time** - Pre-warm connections, optimize initialization
- **Resource requests/limits** - Prevent noisy neighbor problem
- **Read-only root filesystem** - Security hardening
- **Minimal privileges** - Non-root user, specific IAM permissions
- **Health checks** - Detect and replace failing containers quickly

**Result:** Faster deployments, cheaper infrastructure, better security
