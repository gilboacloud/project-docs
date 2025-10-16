from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..services.document_service import DocumentService

documents_bp = Blueprint('documents', __name__)
document_service = DocumentService()

@documents_bp.route('/upload', methods=['POST'])
@jwt_required
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    metadata = request.form.get('metadata', '{}')
    
    try:
        result = document_service.process_document(file, metadata)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@documents_bp.route('/', methods=['GET'])
@jwt_required
def get_documents():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    try:
        documents = document_service.get_documents(page, limit)
        return jsonify(documents), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500