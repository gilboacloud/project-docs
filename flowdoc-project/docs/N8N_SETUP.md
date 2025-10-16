# N8N Workflow Configuration

## Local Development
```bash
# N8N Server
FLOWDOC_N8N_HOST=localhost
FLOWDOC_N8N_PORT=5678
FLOWDOC_N8N_USER=admin
FLOWDOC_N8N_PASSWORD=your-secure-password
FLOWDOC_N8N_ENCRYPTION_KEY=your-encryption-key

# N8N Database
FLOWDOC_N8N_DB_TYPE=postgresdb
FLOWDOC_N8N_DB_HOST=db
FLOWDOC_N8N_DB_NAME=flowdoc_n8n
FLOWDOC_N8N_DB_USER=flowdoc
FLOWDOC_N8N_DB_PASSWORD=password

# N8N Webhook Configuration
FLOWDOC_N8N_WEBHOOK_URL=http://flowdoc-n8n:5678/
```

## Production Deployment
```bash
# Access N8N Editor
http://your-domain:5678/

# Default Credentials
Username: admin
Password: set via FLOWDOC_N8N_PASSWORD
```

## Available Workflows

1. Document Processing
   - Trigger: Document Upload
   - Actions: OCR, Metadata Extraction
   - Endpoint: `/webhook/document-processing`

2. Notification System
   - Trigger: Document Status Change
   - Actions: Email, Slack Notifications
   - Endpoint: `/webhook/notifications`

3. Form Generation
   - Trigger: OCR Completion
   - Actions: Form Schema Creation
   - Endpoint: `/webhook/form-generation`

## Security Notes

1. Always change default credentials
2. Use strong encryption key
3. Enable HTTPS in production
4. Restrict webhook access

## Integration Points

1. Main Application
```python
FLOWDOC_N8N_WEBHOOK_URL = os.getenv('FLOWDOC_N8N_WEBHOOK_URL')
FLOWDOC_N8N_API_KEY = os.getenv('FLOWDOC_N8N_API_KEY')
```

2. Workflow Service
```python
def trigger_workflow(self, workflow_type: str, data: Dict) -> None:
    if not self.n8n_webhook_url:
        logger.warning("N8N webhook URL not configured")
        return
        
    headers = {
        'Authorization': f"Bearer {self.n8n_api_key}"
    }
    
    response = requests.post(
        f"{self.n8n_webhook_url}/webhook/{workflow_type}",
        json=data,
        headers=headers
    )
```

## Monitoring

Monitor N8N status:
```bash
# Docker
docker logs flowdoc-n8n

# Kubernetes
kubectl logs -n flowdoc deployment/flowdoc-n8n
```

## Backup and Restore

1. Backup workflows:
```bash
docker exec flowdoc-n8n n8n export:workflow --all
```

2. Restore workflows:
```bash
docker exec flowdoc-n8n n8n import:workflow --input=workflows.json
```