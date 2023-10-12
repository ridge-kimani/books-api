from sqlalchemy import Column, DateTime, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from passlib.context import CryptContext
from fastapi_sqlalchemy import db

Base = declarative_base()

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    _password = Column(String, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    @hybrid_property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @staticmethod
    def hash_password(password):
        return context.hash(password)

    @staticmethod
    def verify_password(password, hashed):
        """
        Verify an author's password
        :param hashed:
        :param password:
        :return: bool
        """
        return context.verify(password, hashed)

    @staticmethod
    def exists(username):
        """
        Used to check if the user exists in the database
        :param username:
        :return: bool
        """
        user = Author.get(username)
        return True if user else False

    @staticmethod
    def get(username):
        user = db.session.query(Author).filter(Author.username == username).first()
        return user
