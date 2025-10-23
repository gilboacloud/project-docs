# models.py - SQLAlchemy Database Models
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True, nullable=False)
	name = db.Column(db.String(255), nullable=False)
	password_hash = db.Column(db.String(255), nullable=False)
	role = db.Column(db.String(50), default='user')
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	
	def set_password(self, password: str) -> None:
		self.password_hash = generate_password_hash(password)
	
	def check_password(self, password: str) -> bool:
		return check_password_hash(self.password_hash, password)

	def to_dict(self) -> dict:
		return {'id': self.id, 'email': self.email, 'name': self.name, 'role': self.role}

class Document(db.Model):
	__tablename__ = 'documents'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	type = db.Column(db.String(50), nullable=False)
	status = db.Column(db.String(50), default='draft')
	s3_key = db.Column(db.String(500))
	s3_bucket = db.Column(db.String(255))
	ocr_data = db.Column(db.JSON)
	form_schema = db.Column(db.JSON)
	created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	
	def to_dict(self) -> dict:
		return {
			'id': self.id, 'name': self.name, 'type': self.type, 'status': self.status,
			's3_key': self.s3_key, 'created_by': self.created_by
		}

class DocumentAssignment(db.Model):
	__tablename__ = 'document_assignments'
	id = db.Column(db.Integer, primary_key=True)
	document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	assigned_at = db.Column(db.DateTime, default=datetime.utcnow)

class DocumentSubmission(db.Model):
	__tablename__ = 'document_submissions'
	id = db.Column(db.Integer, primary_key=True)
	document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	form_data = db.Column(db.JSON)
	signature_data = db.Column(db.Text)
	submitted_at = db.Column(db.DateTime, default=datetime.utcnow)