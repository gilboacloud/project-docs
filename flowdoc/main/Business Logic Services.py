# services.py - Business Logic Services
import boto3
import json
import uuid
import os
import logging
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class AWSService:
	"""Service for handling AWS operations"""
	def __init__(self):
		self.s3_client = boto3.client('s3')
		self.lambda_client = boto3.client('lambda')
		self.bucket_name = os.getenv('S3_BUCKET')
		self.ocr_lambda_name = os.getenv('OCR_LAMBDA_NAME', 'docuflow-ocr-processor')

	def get_content_type(self, filename: str) -> str:
		ext = filename.lower().split('.')[-1]
		return {'pdf': 'application/pdf', 'jpg': 'image/jpeg', 'png': 'image/png'}.get(ext, 'application/octet-stream')

	def upload_file_to_s3(self, file_obj, user_id: int, filename: str) -> dict:
		try:
			unique_filename = f"{uuid.uuid4()}_{filename}"
			s3_key = f"uploads/{user_id}/{unique_filename}"
			self.s3_client.upload_fileobj(
				file_obj,
				self.bucket_name,
				s3_key,
				ExtraArgs={'ContentType': self.get_content_type(filename)}
			)
			return {'success': True, 's3_key': s3_key, 's3_bucket': self.bucket_name}
		except Exception as e:
			logger.error(f"S3 upload failed: {e}")
			return {'success': False, 'error': str(e)}

	def trigger_ocr_lambda(self, document_id: str, s3_bucket: str, s3_key: str) -> dict:
		try:
			payload = json.dumps({'document_id': document_id, 's3_bucket': s3_bucket, 's3_key': s3_key})
			self.lambda_client.invoke(FunctionName=self.ocr_lambda_name, InvocationType='Event', Payload=payload)
			return {'success': True}
		except Exception as e:
			logger.error(f"Lambda invoke error: {e}")
			return {'success': False, 'error': str(e)}

class DocumentService:
	"""Service for document-related business logic"""
	def __init__(self, aws_service: AWSService):
		self.aws_service = aws_service
		self.allowed_extensions = {'pdf', 'jpg', 'jpeg', 'png'}

	def is_file_allowed(self, filename: str) -> bool:
		return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

	def process_uploaded_document(self, file_obj, filename: str, user_id: int) -> dict:
		return self.aws_service.upload_file_to_s3(file_obj, user_id, filename)
	
	def generate_form_schema(self, ocr_data: dict) -> dict:
		# Simplified schema generation based on OCR'd lines of text
		schema = {'elements': []}
		lines = ocr_data.get('lines', [])
		for i, line in enumerate(lines):
			text = line.get('text', '').strip()
			if ':' in text or '___' in text: # Simple heuristic for a form field
				schema['elements'].append({
					'id': f"element_{i}",
					'type': 'text',
					'label': text.split(':')[0].strip(),
					'geometry': line.get('geometry', {})
				})
		return schema

class WorkflowService:
	"""Service for N8N workflow integration"""
	def __init__(self):
		self.n8n_webhook_url = os.getenv('N8N_WEBHOOK_URL')

	def trigger_workflow(self, event_type: str, data: dict) -> None:
		if not self.n8n_webhook_url or os.getenv('FLASK_CONFIG') == 'testing':
			return
		try:
			payload = {'event': event_type, 'data': data, 'timestamp': datetime.utcnow().isoformat()}
			requests.post(self.n8n_webhook_url, json=payload, timeout=5)
		except Exception as e:
			logger.error(f"N8N workflow trigger failed: {e}")

	def document_uploaded(self, doc_id: str, user_id: int, filename: str) -> None:
		self.trigger_workflow('document.uploaded', {'document_id': doc_id, 'user_id': user_id, 'filename': filename})

	def ocr_completed(self, doc_id: str, success: bool) -> None:
		self.trigger_workflow('document.ocr.completed', {'document_id': doc_id, 'success': success})


class CacheService:
	def __init__(self):
		self.redis_client = None

	def get(self, key: str) -> dict | None:
		try:
			value = self.redis_client.get(key)
			return json.loads(value) if value else None
		except Exception as e:
			logger.error(f"Cache get error for key '{key}': {e}")
			return None

	def set(self, key: str, value: dict, ttl: int = 3600) -> None:
		try:
			self.redis_client.setex(key, ttl, json.dumps(value, default=str))
		except Exception as e:
			logger.error(f"Cache set error for key '{key}': {e}")

	def delete(self, pattern: str) -> None:
		try:
			keys = self.redis_client.keys(pattern)
			if keys:
				self.redis_client.delete(*keys)
		except Exception as e:
			logger.error(f"Cache delete error for pattern '{pattern}': {e}")


# Initialize services
aws_service = AWSService()
document_service = DocumentService(aws_service)
workflow_service = WorkflowService()
notification_service = object() # Placeholder for NotificationService
signature_service = object() # Placeholder for SignatureService
cache_service = CacheService()