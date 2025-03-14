import os
import pytest
from app import app as flask_app
from models import db

@pytest.fixture(scope="session")
def testing_app():
    flask_app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
        }
    )
    print(flask_app.config)
    return flask_app

@pytest.fixture
def client(testing_app):
    # Create tables in test database
    with testing_app.app_context():
        db.create_all()
        yield testing_app.test_client()
        # Clean up after tests
        db.session.remove()
        db.drop_all()