from pydantic import BaseModel
from datetime import datetime


class LoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class RegisterSchema(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class GetAuthorSchema(BaseModel):
    name: str
    count: int = None
    id: int
    updated: datetime = None


class AuthorSchema(BaseModel):
    first_name: str
    last_name: str = None
    id: int = None
    updated: datetime = None

    class Config:
        orm_mode = True


class EditAuthorSchema(BaseModel):
    first_name: str = None
    last_name: str = None

    class Config:
        orm_mode = True


class CreateBookSchema(BaseModel):
    title: str
    isbn: str = None
    pages: int = None
    publish_year: int = None
    cost: float = None
    currency: str = None

    class Config:
        orm_mode = True


class EditBookSchema(BaseModel):
    title: str = None
    isbn: str = None
    pages: int = None
    publish_year: int = None
    cost: float = None
    currency: str = None
    id: str = None


class BookSchema(BaseModel):
    books: list[EditBookSchema] = []

    class Config:
        orm_mode = True




class GetBookSchema(BaseModel):
    title: str
    isbn: str = None
    pages: int = None
    publish_year: int = None
    cost: float = None
    currency: str = None
    author: str = None
    id: int = None
    updated: datetime = None
