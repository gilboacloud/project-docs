"""
Flowdoc API Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.document import DocumentService
from src.api.schemas.document import DocumentSchema

documents_bp = Blueprint('documents', __name__)
document_schema = DocumentSchema()

@documents_bp.route('/documents', methods=['POST'])
@jwt_required
def upload_document():
    """Upload a new document"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    user_id = get_jwt_identity()
    
    try:
        result = DocumentService.process_uploaded_document(file, user_id)
        return jsonify(document_schema.dump(result)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@documents_bp.route('/documents/<int:document_id>', methods=['GET'])
@jwt_required
def get_document(document_id):
    """Get document details"""
    try:
        document = DocumentService.get_document(document_id, get_jwt_identity())
        return jsonify(document_schema.dump(document))
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@documents_bp.route('/documents/<int:document_id>/process', methods=['POST'])
@jwt_required
def process_document(document_id):
    """Start document processing"""
    try:
        result = DocumentService.start_processing(document_id, get_jwt_identity())
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400