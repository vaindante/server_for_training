from sqlalchemy import Column, Integer, ForeignKey

from .base import Base
from .sql_books import Books
from .sql_users import Users


class BooksWithUsers(Base):
    __tablename__ = 'books_with_users'
    user_id = Column(Integer, ForeignKey(Users.id), primary_key=True)
    book_id = Column(Integer, ForeignKey(Books.id), primary_key=True)
