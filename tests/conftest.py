import os

os.environ["DATABASE_URL"] = "sqlite:///./test_resume_analyzer.db"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-that-is-at-least-32-bytes-long"
import pytest
from fastapi.testclient import TestClient
from backend.database.session import Base, engine
from backend.main import app


@pytest.fixture(scope="session")
def client():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(engine)
