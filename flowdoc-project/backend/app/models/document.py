from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .. import db

class Document(db.Model):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    s3_key = Column(String(512), unique=True, nullable=False)
    mime_type = Column(String(100), nullable=False)
    size = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="documents")
    shares = relationship("DocumentShare", back_populates="document")
    ocr_results = relationship("OCRResult", back_populates="document")