from pydantic import BaseModel


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
    count: int
    id: int


class AuthorSchema(BaseModel):
    first_name: str
    last_name: str = None
    id: int = None

    class Config:
        orm_mode = True


class EditAuthorSchema(BaseModel):
    first_name: str = None
    last_name: str = None

    class Config:
        orm_mode = True


class BookSchema(BaseModel):
    books: list = []

    class Config:
        orm_mode = True


class EditBookSchema(BaseModel):
    title: str


class GetBookSchema(BaseModel):
    title: str
    isbn: str = None
    pages: int = None
    publish_year: int = None
    cost: float = None
    currency: str = None
    author: str = None
    id: int = None
