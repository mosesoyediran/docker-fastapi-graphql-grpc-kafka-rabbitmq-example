from hello.extensions import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    """
    SQLAlchemy ORM model for the users table.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), nullable=False)
