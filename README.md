# Insurance Management System

This project is an Insurance Management API that fetches insurance file URLs stored in an AWS S3 bucket. It uses FastAPI for the API framework, PostgreSQL as the database, and handles AWS access keys and tokens through environment variables. The system generates a presigned URL with an expiry time when needed; otherwise, the actual S3 URL will be returned from the postgredb.

## Assumptions
- Data about the customer and there insurance policy exist in the database.
- Response will only have s3 url that user can click to open the file
## Features

- Store and manage insurance file metadata in a PostgreSQL database.
- Generate presigned URLs for temporary access to S3 files.
- Retrieve insurance file URLs from the database.

## Technology Stack

- **FastAPI**: A modern web framework for building APIs with Python 3.7+.
- **PostgreSQL**: A powerful, open-source relational database.
- **AWS S3**: Object storage service for storing files.
- **Docker**: Container platform for deploying applications.

## Setting Up the Environment
### Essential Dependency
- WSL/UNIX environment
- Docker
- Python3.12

### Optional Dependency
- AWS Access key and token to stor

## SET UP PROJECT
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ashutoshkesarwani999/insurance-api.git
   cd insurance-api
2. **Build the docker Image**
   docker-compose up --build
3. **Insert Test data to the Postgre database**
   python tests/test_data/insurance_test_data.py

### Testing API
4. **Test GET Request for all insurance policy of customer**
   curl -X GET "http://localhost:8000/v1/insurance/2" -H "Content-Type: application/json"
5. **Test GET Request for specific insurance policy of customer**
   curl -X GET "http://localhost:8000/v1/insurance/get_policy/1/101" -H "Content-Type: application/json"
6. **Test health of the API**
   curl -X GET "http://localhost:8000/v1/health/" -H "Content-Type: application/json"


### BDD Test
7. **Excecute BDD Test for Insurance Management API**
   behave features/insurance-feature.feature

## Continuos Integration
The repo has a github/workflows/ci.yaml that defines the basic setup of build process.

## Continuos Deployment
This system has cloudformation templates that can create all the necessary resource for the api here
`infrastructure/`

## Possible improvements if I had more time
- Add authentication for the customer
- Add comprehensive Test cases
- Dig more into object oriented design
- Deploy the API on cloud.
- Integration GITHUB Action with AWS and deploy build do AWS

