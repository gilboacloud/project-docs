tree.txt

flowdoc-consolidated/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── documents.py
│   │   │   └── workflows.py
│   │   └── schemas/
│   │       ├── __init__.py
│   │       └── models.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── extensions.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── document.py
│   │   ├── user.py
│   │   └── workflow.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── aws.py
│   │   ├── cache.py
│   │   ├── document.py
│   │   ├── notification.py
│   │   └── workflow.py
│   └── utils/
│       ├── __init__.py
│       ├── auth.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api/
│   ├── test_models/
│   └── test_services/
├── infrastructure/
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   └── kubernetes/
│       ├── config/
│       │   ├── configmap.yaml
│       │   └── secrets.yaml
│       └── deployments/
│           ├── api.yaml
│           ├── redis.yaml
│           └── workflow.yaml
├── migrations/
│   └── versions/
├── docs/
│   ├── api/
│   ├── architecture/
│   └── workflows/
├── scripts/
│   ├── setup.sh
│   └── deploy.sh
├── .env.example
├── .gitignore
├── README.md
├── SETUP.md
├── requirements.txt
└── main.py