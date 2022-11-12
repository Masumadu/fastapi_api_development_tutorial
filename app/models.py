from email.policy import default

from sqlalchemy.orm import relationship
from sqlalchemy import Index
from .database import Base
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import ForeignKey


class Post(Base):

    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=('now()'))

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User")


class User(Base):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True, unique=True)
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
