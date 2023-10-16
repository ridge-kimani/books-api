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


class AuthorSchema(BaseModel):
    first_name: str
    created_by: int

    class Config:
        orm_mode = True


class EditAuthorSchema(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class BookSchema(BaseModel):
    books: list = []

    class Config:
        orm_mode = True


class EditBookSchema(BaseModel):
    title: str
