# Flowdoc Project Evolution

This directory contains a consolidated view of the Flowdoc application across its different versions and implementations.

## Project Structure

```
flowdoc-consolidated/
├── v1-docfly/                  # First version implementation
│   ├── backend/
│   │   ├── node/              # Node.js backend components
│   │   └── python/            # Python backend components
│   ├── frontend/              # React frontend
│   ├── infrastructure/        # Infrastructure as Code
│   └── workflows/             # N8N workflows
│
├── v2-flowdoc/                # Current version
│   ├── backend/              # Flask backend
│   ├── infrastructure/       # K8s and Docker configs
│   └── docs/                # Documentation
│
└── docs/                     # Project-wide documentation
    ├── architecture/        # Architecture diagrams
    ├── deployment/         # Deployment guides
    └── development/       # Development guidelines

```

## Version Comparison

### V1 (docfly)
- Split backend implementation (Node.js and Python)
- Basic document management features
- AWS integration for OCR

### V2 (flowdoc)
- Consolidated Flask backend
- Enhanced business logic services
- Improved database models
- Kubernetes-native deployment

## Component Mapping

### Backend Services
- V1 Node.js: `docfly/main-api.js`
- V1 Python: `docfly-py/flask-be.py`
- V2: `flowdoc/main/main.py`

### Infrastructure
- V1: 
  - `docfly/backend-dockerfile.dockerfile`
  - `docfly/k8s deployment.yaml`
  - `docfly/tfmain.tf`
- V2:
  - `flowdoc/main/docerfile_new.dockerfile`
  - `flowdoc/main/K8S_Dploy_new`

### Business Logic
- V1: 
  - `docfly-py/services.py`
  - `docfly-py/services2.py`
- V2: `flowdoc/main/Business Logic Services.py`

### Database Models
- V1: Embedded in services
- V2: `flowdoc/main/Database Models.py`

## Key Features

1. Document Management
   - Upload and storage
   - OCR processing
   - Form generation

2. Workflow Automation
   - N8N integration
   - AWS Lambda functions
   - Event-driven processing

3. Infrastructure
   - Kubernetes deployment
   - AWS services integration
   - Redis caching
   - PostgreSQL database

## Migration Notes

When working with this codebase:
1. Prefer V2 (flowdoc) implementations over V1 (docfly)
2. Use the consolidated Flask backend structure
3. Reference the latest database models
4. Follow the updated deployment configurations