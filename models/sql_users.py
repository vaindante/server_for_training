from sqlalchemy import Column, Integer, String, Boolean, text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import expression

from .base import Base


class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    email = Column(String(40), unique=True, index=True)
    name = Column(String(100))
    hashed_password = Column("hashed_password", String())
    is_active = Column(Boolean(), server_default=expression.true(), nullable=False)


class Tokens(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    token = Column(
        "token",
        UUID(as_uuid=False),
        server_default=text("gen_random_uuid()"),
        unique=True,
        nullable=False,
        index=True,
    )
    expires = Column(DateTime())
    user_id = Column("user_id", ForeignKey("accounts.id"))


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(40), unique=True, index=True)
    name = Column(String(100))
    created_at = Column(DateTime())
    created_by = Column(Integer, ForeignKey("accounts.id"), primary_key=True)
    is_active = Column(
        "is_active",
        Boolean(),
        server_default=expression.true(),
        nullable=False,
    )
