# hello/db.py

from hello.extensions import SessionLocal


def get_db():
    """
    Dependency to yield a SQLAlchemy Session.
    Used by FastAPI and Strawberry context_getter.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
