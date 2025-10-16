import boto3
from botocore.exceptions import ClientError
from typing import BinaryIO, Dict, Any
import json

class DocumentService:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.textract = boto3.client('textract')
        self.bucket_name = 'flowdoc-documents'

    def process_document(self, file: BinaryIO, metadata: str) -> Dict[str, Any]:
        try:
            # Upload to S3
            s3_key = f"documents/{file.filename}"
            self.s3.upload_fileobj(file, self.bucket_name, s3_key)

            # Start OCR if it's a supported format
            if self._is_ocr_supported(file.filename):
                self._start_ocr_job(s3_key)

            return {
                's3_key': s3_key,
                'filename': file.filename,
                'metadata': json.loads(metadata)
            }
        except Exception as e:
            raise Exception(f"Document processing failed: {str(e)}")

    def _is_ocr_supported(self, filename: str) -> bool:
        supported_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff']
        return any(filename.lower().endswith(ext) for ext in supported_extensions)

    def _start_ocr_job(self, s3_key: str):
        try:
            response = self.textract.start_document_text_detection(
                DocumentLocation={
                    'S3Object': {
                        'Bucket': self.bucket_name,
                        'Name': s3_key
                    }
                }
            )
            return response['JobId']
        except ClientError as e:
            raise Exception(f"OCR job failed to start: {str(e)}")