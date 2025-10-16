from datetime import datetime
from src import db

class User(db.Model):
    """User model."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    documents = db.relationship('Document', backref='owner', lazy=True)
    assignments = db.relationship('DocumentAssignment', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    @property
    def is_admin(self):
        return self.role == 'admin'

class Document(db.Model):
    """Document model."""
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    s3_key = db.Column(db.String(500), nullable=False)
    content_type = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')
    ocr_status = db.Column(db.String(20))
    ocr_confidence = db.Column(db.Float)
    form_schema = db.Column(db.JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assignments = db.relationship('DocumentAssignment', backref='document', lazy=True)
    submissions = db.relationship('DocumentSubmission', backref='document', lazy=True)

class DocumentAssignment(db.Model):
    """Document assignment model."""
    __tablename__ = 'document_assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')

class DocumentSubmission(db.Model):
    """Document submission model."""
    __tablename__ = 'document_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    form_data = db.Column(db.JSON)
    signature_data = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='submitted')
    
class Workflow(db.Model):
    """Workflow model."""
    __tablename__ = 'workflows'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    trigger_type = db.Column(db.String(50), nullable=False)
    config = db.Column(db.JSON)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)