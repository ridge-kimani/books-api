from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db
from app.schema import LoginSchema, RegisterSchema
from app.models import User

from app.security import create_access_token


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/login")
def login(user: LoginSchema):
    user_obj = user.dict()
    user = User.get(username=user_obj.get("username"))

    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=dict(message="Username not found."),
        )
    if not User.verify_password(user_obj.get("password"), user.password):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=dict(message="Incorrect password"),
        )

    token = create_access_token(data=dict(sub=user.username))
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            message="Login successful",
            user=dict(id=user.id, username=user.username),
            token=token
        )
    )


@router.post("/register")
def register(user: RegisterSchema):
    user = user.dict()

    if User.exists(username=user.get("username")):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=dict(message="User exists with that username"),
        )

    password = User.hash_password(user.pop('password'))
    db_item = User(**user, password=password).save(db)
    token = create_access_token(data=dict(sub=db_item.username))
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=dict(
            message="User created successfully.",
            user=user.get("username"),
            token=token
        )
    )
