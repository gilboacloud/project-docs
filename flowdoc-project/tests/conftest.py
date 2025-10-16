"""
Flowdoc Test Configuration
"""
import os
import pytest
from src import create_app, db

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.getenv(
            'FLOWDOC_TEST_DATABASE_URL',
            'postgresql://flowdoc:password@localhost/flowdoc_test'
        )
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()