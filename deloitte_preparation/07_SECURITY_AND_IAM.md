# AWS DevOps Interview Prep: Security & IAM

## 1. What is IAM and its core concepts?

**Answer:** Identity and Access Management controls access to AWS resources:

**Components:**
- **Users** - Individual accounts with long-term credentials
- **Groups** - Collections of users with common permissions
- **Roles** - Temporary credentials for services/accounts
- **Policies** - JSON documents defining permissions

**Key difference:**
- **Users** - People or applications with long-term access
- **Roles** - For services (EC2, Lambda) or cross-account access

**Security best practices:**
- Never use root account (except account setup)
- Enable MFA for all users
- Use roles for applications, not long-term keys
- Rotate credentials regularly
- Principle of least privilege

## 2. Explain IAM policy structure

**Answer:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/*"
    },
    {
      "Effect": "Deny",
      "Action": "iam:DeleteUser",
      "Resource": "*"
    }
  ]
}
```

**Components:**
- **Effect** - Allow or Deny
- **Action** - AWS API actions (service:action format)
- **Resource** - ARN of resources policy applies to
- **Condition** - Optional conditions (IP address, time, tag)
- **Principal** - In resource-based policies (who can access)

**Policy types:**
- **Identity-based** - Attached to user/role
- **Resource-based** - Attached to resource (S3 bucket, SQS queue)

## 3. What are IAM roles and when to use them?

**Answer:**
Temporary credentials for services or cross-account access:

**EC2 instance role example:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "rds:*",
      "Resource": "*"
    }
  ]
}
```

**Application uses:**
```python
import boto3
# Credentials automatically from instance role
s3 = boto3.client('s3')
s3.list_buckets()
```

**vs Access keys:**
- Roles: Temporary, auto-rotated, no storage needed
- Keys: Long-term, require secure storage, rotation burden

**Cross-account access:**
```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::ACCOUNT-B:root"
  },
  "Action": "sts:AssumeRole",
  "Condition": {
    "StringEquals": {
      "sts:ExternalId": "unique-id"
    }
  }
}
```

## 4. Explain policy simulator and testing IAM policies

**Answer:**
**Policy Simulator** (AWS console):
- Test if user has permission to perform action
- Simulates permission evaluation
- Shows exactly why access granted/denied

**CLI testing:**
```bash
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::account:user/test-user \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::my-bucket/*
```

**Best practices:**
- Always test before deploying policies
- Test with actual resource ARNs
- Check for unintended Deny effects
- Verify implicit denies don't affect normal operations

## 5. What is AWS Security Groups and NACLs comparison?

**Answer:**
| Feature | Security Group | NACL |
|---------|---|---|
| **Level** | Instance | Subnet |
| **Stateful** | Yes (return traffic allowed) | No (explicit rules both directions) |
| **Default** | Deny all inbound | Allow all |
| **Rule type** | Allow only | Allow/Deny |
| **Performance** | Negligible impact | Minimal performance overhead |
| **Use case** | Instance-level firewall | Subnet-level traffic control |
| **Rules** | Unordered, all evaluated | Ordered, first match wins |

**Example security group (inbound):**
```
HTTP (80): Allow from 0.0.0.0/0
HTTPS (443): Allow from 0.0.0.0/0
SSH (22): Allow from 10.0.0.0/8 (internal only)
```

**NACL rule:**
```
100 Allow TCP 80 from 0.0.0.0/0
110 Allow TCP 443 from 0.0.0.0/0
120 Deny TCP 23 from 0.0.0.0/0 (block Telnet)
```

## 6. How do you implement VPC security best practices?

**Answer:**
**Network segmentation:**
- Public subnet: Web servers (ALB), NAT gateway
- Private subnet: Application servers
- Database subnet: RDS (no internet)
- Management subnet: Bastion host

**Security groups:**
```
Internet → ALB (80/443) → 
Web SG (allow 80/443 from ALB) → 
App servers in private subnet →
Database SG (allow 3306 from App SG) → 
RDS instance
```

**NACLs:**
- Ephemeral port range (1024-65535) for return traffic
- Stateless, so explicit rules needed

**Additional controls:**
- VPC Flow Logs (monitor traffic)
- VPN/Direct Connect (encrypted connections)
- Bastion host for administrative access
- No internet gateway for database subnet

## 7. Explain S3 bucket security

**Answer:**
**Public access prevention:**
```bash
# Block all public access
aws s3api put-public-access-block \
  --bucket my-bucket \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

**Encryption:**
- **SSE-S3** - S3 manages encryption key
- **SSE-KMS** - Customer manages key in KMS
- **Client-side encryption** - Encrypt before upload

```bash
# Enable default encryption
aws s3api put-bucket-encryption \
  --bucket my-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "aws:kms",
        "KMSMasterKeyID": "arn:aws:kms:...:key/12345"
      }
    }]
  }'
```

**Access control:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::account:role/ec2-role"},
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

**Versioning & MFA Delete:**
```bash
# Enable versioning (prevents accidental deletion)
aws s3api put-bucket-versioning \
  --bucket my-bucket \
  --versioning-configuration Status=Enabled

# MFA delete requires root account MFA
```

## 8. What is Secrets Manager and when to use it?

**Answer:**
Managed service for secrets (passwords, API keys, database credentials):

**Creating secret:**
```bash
aws secretsmanager create-secret \
  --name prod/db-password \
  --description "RDS master password" \
  --secret-string "MyPassword123!"
```

**Retrieving secret:**
```python
import boto3
client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='prod/db-password')
password = response['SecretString']
```

**Automatic rotation:**
```bash
aws secretsmanager rotate-secret \
  --secret-id prod/db-password \
  --rotation-rules AutomaticallyAfterDays=30 \
  --rotation-lambda-arn arn:aws:lambda:...
```

**vs Parameter Store:**
- Secrets Manager: Passwords, keys, secrets (higher cost)
- Parameter Store: Configuration values (free tier available)

## 9. Explain KMS (Key Management Service)

**Answer:** Managed encryption key service:

**Key concepts:**
- **Customer Master Key (CMK)** - Main encryption key
- **Data key** - Encrypts actual data (encrypted by CMK)
- **Key rotation** - Automatic annual rotation
- **Audit** - CloudTrail logs all usage

**Encryption with KMS:**
```python
import boto3
kms = boto3.client('kms')

# Encrypt data
response = kms.encrypt(
    KeyId='arn:aws:kms:region:account:key/12345',
    Plaintext=b'sensitive data'
)
encrypted_data = response['CiphertextBlob']

# Decrypt data (requires KMS permission)
response = kms.decrypt(CiphertextBlob=encrypted_data)
plaintext = response['Plaintext']
```

**Key management:**
- CloudHSM for FIPS 140-2 compliance
- Multi-region keys for DR
- Cross-account access via key policy

## 10. How do you implement compliance and auditing?

**Answer:**
**CloudTrail:**
```bash
# Enable CloudTrail logging
aws cloudtrail create-trail \
  --name my-trail \
  --s3-bucket-name my-bucket \
  --is-multi-region-trail

# Start logging
aws cloudtrail start-logging --trail-name my-trail

# Query logs
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=CreateUser
```

**CloudTrail captures:**
- Who (principal/IAM user)
- What (API action)
- When (timestamp)
- Where (source IP)
- Resources affected

**Config:**
```
Real-time compliance monitoring
Tracks resource configuration changes
Evaluates against rules (e.g., "all RDS encrypted", "public S3 buckets")
Auto-remediation available
```

**Compliance frameworks:**
- PCI-DSS (payment processing)
- HIPAA (healthcare)
- SOC 2 (security controls)
- GDPR (data protection)

## 11. What are encryption best practices in transit and at rest?

**Answer:**
**At rest (stored data):**
- S3: SSE-KMS encryption
- RDS: Enable encryption
- EBS: Encrypted volumes
- DynamoDB: Encryption by default
- Database connections: SSL/TLS

**In transit (moving data):**
- HTTPS (443): All customer-facing communication
- TLS 1.2+: Encryption protocol version
- VPN: Private connection to AWS
- Direct Connect: Dedicated network connection
- Signed URLs: Time-limited S3 access

**Implementation:**
```python
# Generate signed URL for temporary access
s3 = boto3.client('s3')
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'my-bucket', 'Key': 'data.txt'},
    ExpiresIn=3600  # 1 hour
)
```

## 12. Explain SSL/TLS certificates in AWS

**Answer:**
**ACM (AWS Certificate Manager):**
- Free SSL/TLS certificates
- Automatic renewal
- Integrates with ALB, CloudFront, API Gateway

**Certificate options:**
- **Domain validation** - Email/DNS proof of ownership
- **Wildcard** - *.example.com covers all subdomains
- **Multi-domain** - Single cert for multiple domains

**Implementation:**
```
1. Request certificate in ACM
2. Validate ownership (DNS or email)
3. Attach to ALB
4. ALB handles SSL termination
5. Traffic encrypted between client and ALB
```

**Self-signed certificates (for internal):**
```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

## 13. How would you implement least privilege for microservices?

**Answer:**
**Service-specific roles:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::orders-bucket/orders/*"
    },
    {
      "Effect": "Allow",
      "Action": "sqs:SendMessage",
      "Resource": "arn:aws:sqs:region:account:order-queue"
    },
    {
      "Effect": "Deny",
      "Action": "iam:*",
      "Resource": "*"
    }
  ]
}
```

**Database permissions:**
```sql
-- Application user (read-only for reporting)
CREATE USER app_user IDENTIFIED BY 'password';
GRANT SELECT ON orders.* to app_user;

-- Admin user (full access)
CREATE USER admin IDENTIFIED BY 'password';
GRANT ALL on orders.* TO admin;
```

**Container permissions:**
- Run as non-root user
- Read-only filesystems where possible
- Restrict Linux capabilities
- Network policies for pod-to-pod communication

## 14. What is AWS Well-Architected Framework security pillar?

**Answer:**
**Principles:**
1. **Implement AAA** - Authentication, Authorization, Accounting
2. **Separate responsibilities** - Different roles, different permissions
3. **Enable traceability** - CloudTrail, CloudWatch Logs
4. **Apply principle of least privilege** - Minimum needed permissions
5. **Protect data in transit & at rest** - Encryption
6. **Prepare for security events** - Incident response plan
7. **Compliance** - Know your requirements

**Controls:**
- **Preventive** - Block bad things (Security Groups, IAM)
- **Detective** - Find bad things (CloudTrail, GuardDuty)
- **Responsive** - Fix things (Auto Scaling, Backup)

## 15. How do you secure CI/CD pipelines?

**Answer:**
**Code stage:**
```
Git hooks → Prevent secrets in code
CodeCommit → IAM authentication only
Branch protection → Require code review
```

**Build stage:**
```
CodeBuild with IAM role → Limited permissions
Artifact encryption → KMS-encrypted
ECR image scanning → Detect vulnerabilities
```

**Deploy stage:**
```
Approval gates → Manual review
Least privilege → Temporary credentials
Audit logging → CloudTrail logs
Blue/green → Minimize blast radius
```

**Secrets management:**
```bash
# Don't do this
export DOCKER_PASSWORD=mypassword123

# Do this
aws secretsmanager get-secret-value --secret-id docker-credentials
aws ssm get-parameter --name /docker/password --with-decryption
```

**Example secure pipeline step:**
```yaml
build:
  commands:
    - IMAGE_NAME=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME
    - aws ecr get-login-password | docker login --username AWS --password-stdin $IMAGE_NAME
    - docker build -t $IMAGE_NAME:latest .
    - docker push $IMAGE_NAME:latest
    - aws ecr start-image-scan --repository-name $IMAGE_REPO_NAME --image-id imageTag=latest
```
