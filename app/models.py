from sqlalchemy import Column, DateTime, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from passlib.context import CryptContext

Base = declarative_base()

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    _password = Column(LargeBinary(), nullable=False)
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
        self._password = context.hash(password)

    def verify_password(self, password):
        """
        Verify an author's password
        :param password:
        :return: bool
        """
        return context.verify(self.password, password)
