import pytest
from starlette.testclient import TestClient

from hello.app import app
from hello.db import SessionLocal


@pytest.fixture(scope="session")
def client():
    """
    Create a TestClient once per test session.
    """
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def db():
    """
    Create a new database session for a test, then clean up.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
