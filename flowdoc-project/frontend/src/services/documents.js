// Document service for handling document operations
import axios from 'axios';

class DocumentService {
    static async uploadDocument(file, metadata) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('metadata', JSON.stringify(metadata));

        try {
            const response = await axios.post('/api/documents/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            return response.data;
        } catch (error) {
            console.error('Document upload failed:', error);
            throw error;
        }
    }

    static async getDocumentList(page = 1, limit = 10) {
        try {
            const response = await axios.get(`/api/documents?page=${page}&limit=${limit}`);
            return response.data;
        } catch (error) {
            console.error('Failed to fetch documents:', error);
            throw error;
        }
    }

    static async getDocumentDetails(documentId) {
        try {
            const response = await axios.get(`/api/documents/${documentId}`);
            return response.data;
        } catch (error) {
            console.error('Failed to fetch document details:', error);
            throw error;
        }
    }

    static async shareDocument(documentId, shareConfig) {
        try {
            const response = await axios.post(`/api/documents/${documentId}/share`, shareConfig);
            return response.data;
        } catch (error) {
            console.error('Failed to share document:', error);
            throw error;
        }
    }
}