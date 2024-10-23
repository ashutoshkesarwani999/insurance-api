
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
aws cloudformation deploy \
  --stack-name insurance-api-network-stage1 \
  --template-file infrastructure/stage1-vpc-network.yaml \
  --parameter-overrides \
    ParameterKey=VpcCIDR,ParameterValue=10.0.0.0/16 \
    ParameterKey=PublicSubnet1CIDR,ParameterValue=10.0.1.0/24 \
    ParameterKey=PublicSubnet2CIDR,ParameterValue=10.0.2.0/24
```

## Stage 2: Private Subnets and NAT Setup
Create private subnets and configure NAT for the Insurance API, enabling instances in the private subnets to access the internet for updates and other outbound traffic.
```bash
aws cloudformation deploy \
  --stack-name insurance-api-network-stage2 \
  --template-file infrastructure/stage2-private-subnets-nat.yaml \
  --parameter-overrides \
    ParameterKey=Stage1StackName,ParameterValue=insurance-api-network-stage1 \
    ParameterKey=PrivateSubnet1CIDR,ParameterValue=10.0.11.0/24 \
    ParameterKey=PrivateSubnet2CIDR,ParameterValue=10.0.12.0/24
```

## Stage 3: Route Tables Setup
Create route tables and associate them with the VPC and subnets to ensure proper routing of traffic between public and private networks

```bash
aws cloudformation deploy \
  --stack-name insurance-api-network-stage3 \
  --template-file infrastructure/stage3-route-tables.yaml \
  --parameter-overrides \
    ParameterKey=Stage1StackName,ParameterValue=insurance-api-network-stage1 \
    ParameterKey=Stage2StackName,ParameterValue=insurance-api-network-stage2
```

## Stage 4: Data and Authentication Setup
Create a VPC and public subnets for the Insurance API.

```bash
aws cloudformation deploy \
  --stack-name insurance-api-data-auth-stage4 \
  --template-file infrastructure/stage4-data-auth-stack.yaml \
  --capabilities CAPABILITY_IAM

```

## Stage 5:  Set up ECR Repository
Create a ECR Repository

```bash
aws cloudformation deploy \
  --stack-name insurance-api-ecr-stage5 \
  --template-file infrastructure/stage5-ecr-repo.yaml \
  --capabilities CAPABILITY_IAM
```

## Stage 6:  Application Stack Setup
Deploy the application stack for the Insurance API using existing VPC and subnet resources.

```bash
aws cloudformation deploy \
  --stack-name insurance-api-application-stage6 \
  --template-file infrastructure/stage6-application-stack.yaml \
  --capabilities CAPABILITY_IAM
```



## Stage 7:  Cloudwatch Alarm Setup
Deploy the cloudwatch Alarm listening to High CPU, Internal Errors etc
```bash
aws cloudformation deploy \
  --stack-name insurance-api-stack-stage7 \
  --template-file infrastructure/stage7-alarm-stack.yaml \
  --capabilities CAPABILITY_IAM
```