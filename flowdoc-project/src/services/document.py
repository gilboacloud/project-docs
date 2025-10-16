"""
Flowdoc Document Service
"""
from typing import Dict, Optional, BinaryIO
from datetime import datetime
import os
import logging
from src.services.aws import AWSService
from src.services.workflow import WorkflowService
from src.models.models import Document, db

logger = logging.getLogger(__name__)

class DocumentService:
    """Service for handling document operations"""
    
    def __init__(self):
        self.aws_service = AWSService()
        self.workflow_service = WorkflowService()
        
    def process_uploaded_document(self, file_obj: BinaryIO, user_id: int) -> Document:
        """Process and store an uploaded document"""
        try:
            # Upload to S3
            s3_result = self.aws_service.upload_file(file_obj, user_id, file_obj.filename)
            
            # Create document record
            document = Document(
                title=file_obj.filename,
                filename=file_obj.filename,
                s3_key=s3_result['s3_key'],
                content_type=file_obj.content_type,
                status='uploaded',
                user_id=user_id
            )
            
            db.session.add(document)
            db.session.commit()
            
            # Trigger workflow
            self.workflow_service.document_uploaded(
                document.id,
                user_id,
                file_obj.filename
            )
            
            return document
            
        except Exception as e:
            logger.error(f"Error processing document upload: {e}")
            db.session.rollback()
            raise
    
    def get_document(self, document_id: int, user_id: int) -> Optional[Document]:
        """Retrieve document details"""
        return Document.query.filter_by(
            id=document_id,
            user_id=user_id
        ).first()
    
    def start_processing(self, document_id: int, user_id: int) -> Dict:
        """Start document processing workflow"""
        document = self.get_document(document_id, user_id)
        if not document:
            raise ValueError("Document not found")
            
        try:
            # Start OCR if enabled
            if os.getenv('FLOWDOC_ENABLE_OCR', 'true').lower() == 'true':
                ocr_result = self.aws_service.start_textract_job(
                    document.s3_key,
                    document_id
                )
                document.ocr_status = 'processing'
            else:
                ocr_result = {'status': 'disabled'}
                document.ocr_status = 'skipped'
            
            document.status = 'processing'
            db.session.commit()
            
            return {
                'document_id': document_id,
                'status': document.status,
                'ocr_status': document.ocr_status,
                'ocr_result': ocr_result
            }
            
        except Exception as e:
            logger.error(f"Error starting document processing: {e}")
            db.session.rollback()
            raise