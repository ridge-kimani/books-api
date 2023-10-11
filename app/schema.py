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