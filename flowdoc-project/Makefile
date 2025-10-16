# Development tasks

.PHONY: install test run clean

# Installation
install:
	@echo "Installing dependencies..."
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

# Development
run-backend:
	@echo "Starting backend server..."
	cd backend && flask run

run-frontend:
	@echo "Starting frontend development server..."
	cd frontend && npm start

# Testing
test-backend:
	@echo "Running backend tests..."
	cd backend && pytest

test-frontend:
	@echo "Running frontend tests..."
	cd frontend && npm test

# Docker
docker-build:
	@echo "Building Docker images..."
	docker-compose -f infrastructure/docker/docker-compose.yml build

docker-up:
	@echo "Starting Docker containers..."
	docker-compose -f infrastructure/docker/docker-compose.yml up -d

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose -f infrastructure/docker/docker-compose.yml down

# Deployment
deploy-dev:
	@echo "Deploying to development..."
	./scripts/deploy/deploy-dev.sh

deploy-prod:
	@echo "Deploying to production..."
	./scripts/deploy/deploy-prod.sh

# Cleanup
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete