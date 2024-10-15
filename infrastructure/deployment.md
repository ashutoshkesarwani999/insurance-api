
# Resources and Deployment step to deploy the cloudformation template

## Ensure you have access to these resources before running deploy
- Install aws cli
- Configure aws cli with the access key and token before executing the command

### Resources to create

- **EC2**
  - VPC
  - Subnets
  - Internet Gateway
  - Route Tables

- **ECS**
  - Cluster
  - Task Definitions
  - Services

- **ECR**
  - Repositories

- **RDS**
  - Database Instances

- **ElastiCache**
  - Redis Clusters

- **S3**
  - Buckets

- **Cognito**
  - User Pools

- **IAM**
  - Roles
  - Policies

- **CloudFormation**

- **Secrets Manager**

## Create secrets for db
aws secretsmanager create-secret \
    --name "test/InsuranceAPI/DBCredentials" \
    --description "Database credentials for Insurance API" \
    --secret-string '{"user":"postgres","password":"password123","db":"dbtest", "port":5432,"host":0.0.0.0}'



## Stage 1: VPC Network Setup
Create a VPC and public subnets for the Insurance API.

```bash
aws cloudformation create-stack \
  --stack-name insurance-api-network-stage1 \
  --template-body file://infrastructure/stage1-vpc-network.yaml \
  --parameters \
    ParameterKey=VpcCIDR,ParameterValue=10.0.0.0/16 \
    ParameterKey=PublicSubnet1CIDR,ParameterValue=10.0.1.0/24 \
    ParameterKey=PublicSubnet2CIDR,ParameterValue=10.0.2.0/24
```

## Stage 2: Private Subnets and NAT Setup
Create private subnets and configure NAT for the Insurance API, enabling instances in the private subnets to access the internet for updates and other outbound traffic.
```bash
aws cloudformation create-stack \
  --stack-name insurance-api-network-stage2 \
  --template-body file://infrastructure/stage2-private-subnets-nat.yaml \
  --parameters \
    ParameterKey=Stage1StackName,ParameterValue=insurance-api-network-stage1 \
    ParameterKey=PrivateSubnet1CIDR,ParameterValue=10.0.11.0/24 \
    ParameterKey=PrivateSubnet2CIDR,ParameterValue=10.0.12.0/24
```

## Stage 3: Route Tables Setup
Create route tables and associate them with the VPC and subnets to ensure proper routing of traffic between public and private networks

```bash
aws cloudformation create-stack \
  --stack-name insurance-api-network-stage3 \
  --template-body file://infrastructure/stage3-route-tables.yaml \
  --parameters \
    ParameterKey=Stage1StackName,ParameterValue=insurance-api-network-stage1 \
    ParameterKey=Stage2StackName,ParameterValue=insurance-api-network-stage2
```

## Stage 4: Data and Authentication Setup
Create a VPC and public subnets for the Insurance API.

```bash
aws cloudformation create-stack \
  --stack-name insurance-api-data-auth-stage4 \
  --template-body file://infrastructure/stage4-data-auth-stack.yaml \
  --capabilities CAPABILITY_IAM

```

## Stage 1:  Application Stack Setup
Create a VPC and public subnets for the Insurance API.

```bash
aws cloudformation create-stack \
  --stack-name insurance-api-stack-stage5 \
  --template-body file://infrastructure/stage5-application-stack.yaml \
  --parameters \
    ParameterKey=VpcId,ParameterValue=vpc-04ec12b1002fa802e \
    ParameterKey=PublicSubnet1,ParameterValue=subnet-09cde4b37ef982775 \
    ParameterKey=PublicSubnet2,ParameterValue=subnet-009b8950ec72bd4c9 \
    ParameterKey=PrivateSubnet1,ParameterValue=subnet-03a49c58bf0ea5a5d \
    ParameterKey=PrivateSubnet2,ParameterValue=subnet-01a2e986959db9245 \
  --capabilities CAPABILITY_IAM
```
