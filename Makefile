APP_NAME := Insurance API
APP_VERSION := 1.0.0
APP_AUTHOR := Ashutosh Kesarwani
APP_DESCRIPTION := FastAPI application for managing insurance files with PostgreSQL and AWS S3 integration.

DOCKER_COMPOSE = docker-compose

.PHONY: metadata
metadata:
	@echo "Application Name: $(APP_NAME)"
	@echo "Version: $(APP_VERSION)"
	@echo "Author: $(APP_AUTHOR)"
	@echo "Description: $(APP_DESCRIPTION)"

# Default target
.PHONY: all
all: build

# Build and start the containers
.PHONY: build
build:
	$(DOCKER_COMPOSE) up --build

# Stop the containers
.PHONY: down
down:
	$(DOCKER_COMPOSE) down

# View logs
.PHONY: logs
logs:
	$(DOCKER_COMPOSE) logs -f
