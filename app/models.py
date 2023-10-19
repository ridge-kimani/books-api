from fastapi_sqlalchemy import db

from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func, literal
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

Base = declarative_base()

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BaseModel(Base):
    __abstract__ = True

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    def save(self, instance):
        instance.session.add(self)
        instance.session.commit()
        instance.session.refresh(self)
        return self.get(self.id)

    def delete(self, instance):
        instance.session.delete(self)
        instance.session.commit()
        return True


class BaseUser(BaseModel):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)

    @hybrid_property
    def name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name


class User(BaseUser):
    __tablename__ = "users"

    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

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
        user = User.get(username)
        return True if user else False

    @staticmethod
    def get(username):
        user = db.session.query(User).filter(User.username == username).first()
        return user

    def save(self, instance):
        instance.session.add(self)
        instance.session.commit()
        instance.session.refresh(self)
        return self.get(self.username)


class Book(BaseModel):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    isbn = Column(String, nullable=True)
    pages = Column(Integer, nullable=True)
    publish_year = Column(Integer, nullable=True)
    cost = Column(Float, nullable=True)
    currency = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    created_by = Column(Integer, ForeignKey("users.id"))

    @staticmethod
    def get(book_id):
        book = db.session.query(Book).filter(Book.id == book_id).first()
        return book

    @staticmethod
    def get_all_by_user(user_id):
        books = db.session.query(Book).filter(Book.created_by == user_id).all()
        return books

    @staticmethod
    def get_by_author(book_id, author_id):
        book = db.session.query(Book).filter(and_(Book.id == book_id, Book.author_id == author_id)).first()
        return book

    @staticmethod
    def get_all_by_author(author_id, user_id):
        books = db.session.query(Book).filter(and_(Book.author_id == author_id, Book.created_by == user_id)).all()
        return books

    @hybrid_property
    def serialize(self):
        return dict(
            title=self.title,
            isbn=self.isbn,
            pages=self.pages,
            currency=self.currency,
            cost=self.cost,
            publish_year=self.publish_year,
        )


class Author(BaseUser):
    __tablename__ = "authors"

    books = relationship("Book", backref="author")
    created_by = Column(Integer, ForeignKey("users.id"))

    @staticmethod
    def get(author_id, created_by):
        author = db.session.query(Author).filter(and_(Author.id == author_id, Author.created_by == created_by)).first()
        return author

    @staticmethod
    def get_all(user_id):
        books = db.session.query(Book).filter(and_(Book.created_by == user_id)).first()
        if books:
            authors = (
                db.session.query(Author, func.count(Book.id).label("book_count"))
                .join(Book)
                .group_by(Author)
                .filter(and_(Author.created_by == user_id, Book.title.isnot(None)))
                .all()
            )
            return authors

        else:
            authors = (
                db.session.query(Author, literal(0).label("book_count"))
                .filter(Author.created_by == user_id)
                .all()
            )
            return authors

    @hybrid_property
    def serialize(self):
        return dict(name=self.name, created=self.created, updated=self.updated)

    def save(self, instance):
        instance.session.add(self)
        instance.session.commit()
        instance.session.refresh(self)
        return self.get(self.id, self.created_by)
