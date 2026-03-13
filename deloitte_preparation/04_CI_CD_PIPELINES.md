# AWS DevOps Interview Prep: CI/CD Pipelines

## 1. What is a CI/CD pipeline and its importance in DevOps?

**Answer:** 
**CI (Continuous Integration):**
- Developers frequently merge code to main branch (daily)
- Automated builds and tests run on every commit
- Catches integration issues early

**CD (Continuous Delivery/Deployment):**
- Continuous Delivery: Deploy-ready code, manual approval for production
- Continuous Deployment: Automated deployment to production

**Benefits:**
- Faster release cycles
- Early bug detection
- Reduced manual testing
- Consistent deployments
- Faster time-to-market

## 2. Explain AWS CodePipeline architecture

**Answer:**
```
Source (CodeCommit/GitHub) 
  ↓
Build (CodeBuild)
  ↓
Deploy (CodeDeploy/CloudFormation)
  ↓
Production
```

**Key components:**
- **Stages** - Logical groupings of actions (Source, Build, Test, Deploy)
- **Actions** - Individual tasks within stage
- **Artifacts** - Output from one stage feeds into next
- **Execution** - Pipeline run triggered by source changes or manual trigger

**Integration:** Supports GitHub, GitLab, Bitbucket, CodeCommit, S3

## 3. What is CodeBuild and how do you configure it?

**Answer:** AWS's managed build service:
- **Supported languages** - Java, Python, Node.js, Ruby, Go, .NET, PHP, Docker
- **Build environment** - AWS-managed or custom
- **buildspec.yml** - Build instructions

**buildspec.yml example:**
```yaml
version: 0.2
phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
  build:
    commands:
      - echo Build started on `date`
      - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
  post_build:
    commands:
      - docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG
      - docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG
artifacts:
  files:
    - imagedefinitions.json
```

## 4. Explain CodeDeploy deployment strategies

**Answer:**
**EC2/On-premises:**
- **All at once** - Deploy to all instances simultaneously (downtime, fast)
- **Half at a time** - Deploy to 50% first, then rest (rolling)
- **One at a time** - Slowest, safest (maintains service availability)
- **Custom** - Define your own strategy

**Lambda:**
- **All at once** - Update all versions simultaneously
- **Linear** - Gradually shift traffic in equal steps
- **Canary** - Shift small percentage first, monitor, then shift rest
- **Gradual** - Linear with custom time intervals

**ECS/CloudFormation:**
- **All at once**
- **Linear**
- **Canary**

## 5. What is an appspec.yml file in CodeDeploy?

**Answer:** Deployment configuration file:
```yaml
version: 0.0
Resources:
  - TargetService:
      Type: AWS::CloudFormation::Stack
      Properties:
        TemplateUrl: https://s3-region.amazonaws.com/bucket/template.yml
        TimeoutInMinutes: 10
Hooks:
  - BeforeAllowTraffic: "CodeDeployHook_BeforeAllowTraffic"
    AfterAllowTraffic: "CodeDeployHook_AfterAllowTraffic"
```

**For EC2 (appspec.yml):**
```yaml
version: 0.0
os: linux
files:
  - source: /
    destination: /var/www/html
hooks:
  BeforeInstall:
    - location: scripts/install_dependencies.sh
      timeout: 300
  ApplicationStart:
    - location: scripts/start_server.sh
```

## 6. How would you implement blue/green deployment with CodeDeploy?

**Answer:**
1. **Blue environment** - Current production
2. **Green environment** - New version deployed
3. **Test** - Verify green environment works
4. **Switch traffic** - Update load balancer or Route 53 to green
5. **Rollback** - Revert to blue if issues detected

**Implementation:**
- CodeDeploy with Blue/Green option enabled
- Load Balancer target group switching
- Route 53 weighted routing for gradual traffic shift

**Advantages:**
- Zero downtime deployment
- Quick rollback
- Easy A/B testing

## 7. Explain artifact management in CodePipeline

**Answer:**
- Artifacts are output from one stage, input to next
- Stored in S3 bucket specified in pipeline
- Each stage can produce artifacts (build output, test reports)
- Automatic cleanup policies available

**Example:**
```
Source stage → codebuild-output.zip
Build stage → app.jar, test-reports.xml
Deploy stage → deployment-status.txt
```

**Best practices:**
- Set lifecycle policies (delete artifacts > 30 days old)
- Use separate buckets for different pipelines
- Enable versioning for audit trail

## 8. How do you handle secrets in CodeBuild/CodeDeploy?

**Answer:**
**Secrets Manager:**
```yaml
build:
  commands:
    - aws secretsmanager get-secret-value --secret-id my-secret --query SecretString --output text > secret.txt
```

**Parameter Store:**
```yaml
build:
  commands:
    - aws ssm get-parameter --name /api/key --with-decryption --query 'Parameter.Value' --output text
```

**Environment variables (encrypted):**
```
At CodeBuild level, encrypt variables with KMS
```

**NOT in environment variables:**
❌ API_KEY=secret123 (visible in console)

## 9. What is CodeCommit and its advantages?

**Answer:** AWS's managed Git service:
- **Built-in integrations** - CodePipeline, CodeBuild, CodeDeploy
- **High availability** - Multi-AZ, automatic failover
- **Security** - IAM-based access control
- **Credentials** - SSH keys, HTTPS, Git credentials
- **No charges** - Included in AWS Free Tier

**vs GitHub:**
- CodeCommit: AWS-native, tighter integration, compliance benefits
- GitHub: Large ecosystem, public repos, broader community

## 10. Explain webhook triggers in CodePipeline

**Answer:**
- Webhook allows pipeline to trigger on GitHub/GitLab push events
- Alternative to polling source repository
- **Faster response** - Immediate trigger vs periodic checks
- **More efficient** - No unnecessary polling

**Setup:**
1. Configure webhook in source provider (GitHub settings)
2. AWS generates secret token
3. Pipeline triggers within seconds of push
4. Filters by branch, event type

## 11. How would you implement parallel execution in CodePipeline?

**Answer:**
- Multiple actions in same stage run in parallel
- Different stages must complete before next stage starts
- Example:
  ```
  Build Stage:
  ├─ Build Docker image (parallel)
  ├─ Run unit tests (parallel)
  └─ Run integration tests (parallel)
  
  Deploy Stage:
  ├─ Deploy to staging (parallel)
  └─ Run smoke tests (parallel)
  ```

**Benefits:**
- Faster pipeline execution
- Better resource utilization
- Reduced deployment time

## 12. What are deployment approvals and when to use them?

**Answer:**
- Manual approval action stops pipeline
- Specified users must approve in SNS or CodePipeline console
- Common gates before production deployment

**Use cases:**
- Before production deployment
- After staging validation
- Before critical infrastructure changes
- Compliance requirements

**Implementation:**
```
Staging Deploy → Manual Approval (email sent to approver) → Production Deploy
```

## 13. How do you handle rollbacks in CI/CD pipelines?

**Answer:**
**CloudFormation deployments:**
- Automatic rollback on failure
- Revert to previous stack version

**CodeDeploy:**
- Keep previous version deployed
- Quick revert to previous appspec.yml
- Load balancer traffic switching

**Lambda deployments:**
- Gradual shifts allow quick rollback
- Previous version still running
- Traffic weighted towards stable version

**Database changes:**
- Database migrations harder to rollback
- Blue/green database approach
- Careful planning of schema changes

## 14. Explain deployment stages and gates in detail

**Answer:**
```
Dev → Build → QA testing → Staging → Manual Approval → Production → Monitor
```

**Dev:**
- Developers push code to topic branch
- Unit tests run
- Code review required

**Build:**
- Merge to main triggers CodeBuild
- Compile, unit tests, code analysis

**QA/Staging:**
- Deploy to staging environment
- Integration tests, load tests, UAT
- If Pass → Staging deployment stage

**Production:**
- Manual approval gate (required for compliance)
- Canary deployment to 5% of traffic
- Monitor CloudWatch metrics
- Gradual traffic shift

## 15. How would you setup a complete CI/CD pipeline for microservices?

**Answer:**
```
Source (Git repo with multiple services)
  ↓
Trigger on change
  ↓
CodeBuild:
  - Unit tests for each service
  - Build Docker images
  - Push to ECR
  ↓
Deploy to Staging (ECS/EKS):
  - Integration tests
  - Load tests
  - Verify service mesh
  ↓
Manual Approval
  ↓
Deploy to Production:
  - Canary deployment
  - Health checks
  - Auto-rollback on failure
  ↓
Monitor:
  - CloudWatch metrics
  - X-Ray traces
  - Log aggregation
```

**Key considerations:**
- Service discovery across microservices
- Database migration strategy
- Secrets management for each service
- Cross-service testing
- Monitoring and observability
