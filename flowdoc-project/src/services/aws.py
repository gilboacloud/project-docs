from typing import Dict, Optional, Any
import boto3
import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AWSService:
    """Service for handling AWS operations."""
    
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.textract_client = boto3.client('textract')
        self.lambda_client = boto3.client('lambda')
        self.bucket_name = os.getenv('S3_BUCKET', 'flowdoc-documents')
        self.signature_bucket = os.getenv('SIGNATURE_BUCKET', 'flowdoc-signatures')
    
    def upload_file(self, file_obj, user_id: int, filename: str) -> Dict:
        """Upload file to S3."""
        try:
            s3_key = f"users/{user_id}/documents/{datetime.utcnow().strftime('%Y/%m/%d')}/{filename}"
            
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                s3_key,
                ExtraArgs={
                    'ContentType': self._get_content_type(filename)
                }
            )
            
            return {
                's3_key': s3_key,
                'bucket': self.bucket_name,
                'url': f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
            }
            
        except Exception as e:
            logger.error(f"Error uploading file to S3: {e}")
            raise
    
    def start_textract_job(self, s3_key: str, document_id: int) -> Dict:
        """Start OCR processing with Textract."""
        try:
            response = self.textract_client.start_document_text_detection(
                DocumentLocation={
                    'S3Object': {
                        'Bucket': self.bucket_name,
                        'Name': s3_key
                    }
                },
                NotificationChannel={
                    'SNSTopicArn': os.getenv('SNS_TOPIC_ARN'),
                    'RoleArn': os.getenv('TEXTRACT_ROLE_ARN')
                }
            )
            
            job_id = response['JobId']
            
            # Store job info in Lambda for callback
            self.lambda_client.invoke(
                FunctionName=os.getenv('OCR_LAMBDA_NAME', 'flowdoc-ocr-processor'),
                InvocationType='Event',
                Payload=json.dumps({
                    'job_id': job_id,
                    'document_id': document_id,
                    's3_bucket': self.bucket_name,
                    's3_key': s3_key
                })
            )
            
            return {
                'job_id': job_id,
                'status': 'IN_PROGRESS'
            }
            
        except Exception as e:
            logger.error(f"Error starting Textract job: {e}")
            raise
    
    def get_textract_results(self, job_id: str) -> Dict:
        """Get OCR results from Textract."""
        try:
            response = self.textract_client.get_document_text_detection(JobId=job_id)
            
            blocks = []
            while True:
                blocks.extend(response['Blocks'])
                
                if 'NextToken' not in response:
                    break
                    
                response = self.textract_client.get_document_text_detection(
                    JobId=job_id,
                    NextToken=response['NextToken']
                )
            
            return {
                'blocks': blocks,
                'job_status': response['JobStatus'],
                'job_id': job_id
            }
            
        except Exception as e:
            logger.error(f"Error getting Textract results: {e}")
            raise
    
    def _get_content_type(self, filename: str) -> str:
        """Get content type based on file extension."""
        ext = filename.lower().split('.')[-1]
        return {
            'pdf': 'application/pdf',
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg'
        }.get(ext, 'application/octet-stream')