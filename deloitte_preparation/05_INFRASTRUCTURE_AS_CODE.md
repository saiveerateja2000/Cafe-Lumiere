# AWS DevOps Interview Prep: Infrastructure as Code

## 1. What is Infrastructure as Code (IaC) and why is it important?

**Answer:** IaC is managing infrastructure through code/definitions rather than manual configuration:

**Benefits:**
- **Reproducibility** - Same infrastructure every time
- **Version control** - Track infrastructure changes
- **Automation** - Consistent, repeatable deployments
- **Disaster recovery** - Quick infrastructure recreation
- **Scalability** - Easy to replicate environments
- **Cost optimization** - Identify unused resources
- **Compliance** - Enforce standards across infrastructure
- **Documentation** - Code serves as infrastructure documentation

**DevOps value:** Faster deployments, fewer errors, knowledge sharing

## 2. Compare CloudFormation and Terraform

**Answer:**
| Feature | CloudFormation | Terraform |
|---------|---|---|
| **Type** | AWS-native | Multi-cloud |
| **Language** | JSON/YAML | HCL |
| **State management** | Built-in | Separate state file |
| **Multi-cloud** | No | Yes (AWS, Azure, GCP) |
| **Modules** | Nested stacks | Terraform modules |
| **Learning curve** | Medium | Medium-High |
| **Ecosystem** | Large AWS community | Broader multi-cloud |

**When to use:**
- CloudFormation: AWS-only, tight integration, compliance needs
- Terraform: Multi-cloud, greatest flexibility, infrastructure variety

## 3. Explain CloudFormation stack concepts

**Answer:**
**Stack** - Collection of AWS resources:
- Single unit of deployable resources
- Resources linked together
- Templates define stack behavior

**Template:**
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Simple EC2 stack'
Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0c55b159cbfafe1f0
      InstanceType: t3.micro
Outputs:
  InstanceId:
    Value: !Ref MyInstance
```

**Stack lifecycle:**
- CREATE_IN_PROGRESS → CREATE_COMPLETE
- UPDATE_IN_PROGRESS → UPDATE_COMPLETE
- DELETE_IN_PROGRESS → DELETE_COMPLETE

**Drift detection:** Detects manual changes outside CloudFormation

## 4. What are CloudFormation parameters and how do you use them?

**Answer:**
```yaml
Parameters:
  EnvironmentName:
    Type: String
    Default: dev
    AllowedValues: [dev, staging, production]
    Description: Environment name
  
  InstanceType:
    Type: String
    Default: t3.micro
    AllowedValues:
      - t3.micro
      - t3.small
      - t3.medium

Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0c55b159cbfafe1f0
      InstanceType: !Ref InstanceType
      Tags:
        - Key: Environment
          Value: !Ref EnvironmentName
```

**Benefits:**
- Reusable templates across environments
- User input at stack creation
- Constraint validation

## 5. Explain CloudFormation functions

**Answer:**
- **!Ref** - Reference parameter or resource
- **!GetAtt** - Get resource attribute
- **!Sub** - String substitution with variables
- **!Join** - Join list of values
- **!Select** - Select item from list
- **!If** - Conditional value
- **!GetAZs** - List of availability zones
- **!ImportValue** - Import exported value from another stack

**Example:**
```yaml
VpcId: !Ref MyVPC
InstanceId: !Ref MyInstance
PrivateIp: !GetAtt MyInstance.PrivateIp
StackName: !Sub '${AWS::StackName}-db'
ServiceUrl: !Sub 'https://${ApiGateway}.execute-api.${AWS::Region}.amazonaws.com'
```

## 6. What are CloudFormation nested stacks?

**Answer:**
- Stack that creates another stack
- Parent template references child templates stored in S3
- Useful for reusable components

**Example:**
```yaml
Resources:
  VPCStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/vpc.yaml
      Parameters:
        CidrBlock: 10.0.0.0/16
```

**Advantages:**
- Modular design
- Reusable stacks
- Easier maintenance
- Separate concerns (networking, compute, database)

**vs Modules:** Nested stacks for CloudFormation, modules for Terraform

## 7. Explain Terraform state and why it's important

**Answer:**
Terraform state file (`terraform.tfstate`):
- Maps configuration to real infrastructure
- Contains all deployed resource IDs, attributes
- Used to determine what changes to make
- **JSON format** but should not edit manually

**State management:**
```
Local state (development) → Remote state (team, production)
Usually S3 + DynamoDB lock
```

**Remote state example:**
```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock"
    encrypt        = true
  }
}
```

**Best practices:**
- Store in remote backend (never commit to Git)
- Enable encryption
- Use state locking (DynamoDB)
- Restrict access via IAM
- Enable versioning

## 8. What is Terraform modularity and how to structure projects?

**Answer:**
**Project structure:**
```
terraform/
├── main.tf              # Main configuration
├── variables.tf         # Variable definitions
├── outputs.tf           # Output definitions
├── terraform.tfvars     # Variable values
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── compute/
│   │   └── ...
│   └── database/
│       └── ...
└── envs/
    ├── dev/
    │   └── terraform.tfvars
    ├── staging/
    │   └── terraform.tfvars
    └── prod/
        └── terraform.tfvars
```

**Module usage:**
```hcl
module "vpc" {
  source = "./modules/vpc"
  cidr_block = var.vpc_cidr
  environment = var.environment
}

module "compute" {
  source = "./modules/compute"
  vpc_id = module.vpc.id
  subnet_id = module.vpc.subnet_id
}
```

## 9. Explain Terraform data sources and their use

**Answer:**
Data sources retrieve information from AWS without creating resources:

```hcl
# Get existing AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

# Get existing VPC
data "aws_vpc" "default" {
  default = true
}

# Use in resource
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  subnet_id     = data.aws_vpc.default.id
}
```

**Use cases:**
- Reference existing infrastructure
- Fetch dynamic values (latest AMI ID)
- Query AWS account information
- Avoid hardcoding values

## 10. How would you implement GitOps for infrastructure?

**Answer:**
GitOps principles:
1. **Git is source of truth** - All infrastructure code in Git
2. **Declarative descriptions** - Define desired state
3. **Automated deployment** - Git changes trigger infrastructure updates
4. **Continuous reconciliation** - System verifies desired vs actual state

**Implementation:**
```
1. Developer commits infrastructure code to Git
2. CI/CD pipeline triggered (CodePipeline)
3. Plan stage: terraform plan
4. Review/approval needed
5. Apply stage: terraform apply
6. Infrastructure updated automatically
7. Monitoring detects drift
8. Alert on manual changes
```

**Tools:**
- ArgoCD (Kubernetes-native)
- Flux (Kubernetes)
- Terraform Cloud
- CloudFormation StackSets

## 11. Explain drift detection in CloudFormation

**Answer:**
Drift = Actual infrastructure differs from CloudFormation template

**Detection:**
```bash
aws cloudformation detect-stack-drift --stack-name my-stack
aws cloudformation describe-stack-resource-drifts --stack-name my-stack
```

**Why it matters:**
- Manual changes bypass code review
- Configuration divergence (security risk)
- Compliance violations
- Inconsistent environments

**Best practices:**
- Regular drift detection
- Alerts on drift detected
- Remediate by updating template
- Prevent manual changes via IAM policies

## 12. How do you manage secrets in IaC?

**Answer:**
**NOT in code (Git tracked):**
```
❌ password = "mypassword123"  # Visible in Git history
```

**Better approaches:**

1. **Terraform variables (tfvars):**
```hcl
# .gitignore: terraform.tfvars
# terraform.tfvars (local, not committed)
db_password = "secret123"
```

2. **AWS Secrets Manager:**
```hcl
resource "aws_secretsmanager_secret" "db_password" {
  name                    = "db-password"
  recovery_window_in_days = 7
}

resource "aws_db_instance" "db" {
  master_password = aws_secretsmanager_secret.db_password.arn
}
```

3. **Parameter Store:**
```hcl
data "aws_ssm_parameter" "api_key" {
  name = "/prod/api-key"
}
```

4. **Environment variables:**
```bash
export TF_VAR_db_password="secret123"
terraform apply
```

## 13. What are CloudFormation StackSets and when to use them?

**Answer:**
Deploy stacks across multiple AWS accounts and regions:

```yaml
StackSet:
  AdministrationRoleARN: arn:aws:iam::account:role/AdminRole
  ExecutionRoleARN: arn:aws:iam::member-account:role/ExecutionRole
  
StackInstances:
  - Account: member-account-1
    Region: us-east-1
  - Account: member-account-1
    Region: eu-west-1
  - Account: member-account-2
    Region: us-east-1
```

**Use cases:**
- Multi-account deployments
- Global region deployments
- Organization-wide infrastructure
- Centralized management
- Consistent configuration across accounts

## 14. How would you implement infrastructure testing?

**Answer:**
1. **Syntax validation:**
   ```bash
   terraform fmt -check
   terraform validate
   ```

2. **Linting:**
   ```bash
   tflint
   cfn-lint template.yaml
   ```

3. **Security scanning:**
   ```bash
   checkov -d terraform/
   terrascan scan
   ```

4. **Unit testing:**
   - CloudFormation cfn-python-lint
   - Terraform test (experimental)

5. **Integration testing:**
   - Deploy to test environment
   - Run validation scripts
   - Destroy resources

6. **Policy as code:**
   - Terraform Sentinel
   - AWS CloudFormation Guard

**Example pipeline:**
```
Validate → Lint → Security scan → Plan → Deploy to test → Test → Destroy
```

## 15. Explain immutable infrastructure concept

**Answer:**
Instead of updating servers, replace them entirely:

**Traditional (mutable):**
```
Server 1.0 → SSH → Update config → Server 1.1
(Risk: What exactly changed? Can it be rolled back?)
```

**Immutable:**
```
Build AMI with v1.1 config → 
Deploy new instance from AMI → 
Route traffic to new instance → 
Terminate old instance
```

**Benefits:**
- Predictable, consistent servers
- Easy rollback (old AMI still exists)
- No configuration drift
- Better compliance and security
- Simpler troubleshooting

**Implementation:**
- Packer to build AMIs
- CloudFormation/Terraform to deploy
- Blue/green deployments
- Auto Scaling handles replacement

**Tools:**
- Packer (build images)
- Launch templates (immutable configurations)
- Blue/green deployments (traffic switching)
