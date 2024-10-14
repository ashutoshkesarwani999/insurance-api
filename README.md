# Insurance Management System

This project is an Insurance Management API that fetches insurance file URLs stored in an AWS S3 bucket. It uses FastAPI for the API framework, PostgreSQL as the database, and handles AWS access keys and tokens through environment variables. The system generates a presigned URL with an expiry time when needed; otherwise, the actual S3 URL will be returned from the postgredb.

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

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd insurance-api
