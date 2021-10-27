from sqlalchemy import Column, String, DateTime, Integer

from .base import Base


class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    created_at = Column(DateTime())
    comments = Column(String())
