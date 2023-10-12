from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db
from app.schema import LoginSchema, RegisterSchema
from app.models import Author

from app.security import create_access_token


router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@router.post("/login")
def login(author: LoginSchema):
    author_obj = author.dict()
    author = Author.get(username=author_obj.get("username"))

    if not author:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=dict(message="Username not found."),
        )
    # if not Author.verify_password(author_obj.get("password"), author.password):
    #     return JSONResponse(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         content=dict(message="Incorrect password"),
    #     )

    token = create_access_token(data=dict(sub=author.username))
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            message="Login successful",
            user=author.username,
            token=token
        )
    )


@router.post("/register")
def register(author: RegisterSchema):
    author = author.dict()

    if Author.exists(username=author.get("username")):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=dict(message="User exists with that username"),
        )

    db_item = Author(**author)
    db.session.add(db_item)
    db.session.commit()
    db.session.refresh(db_item)
    token = create_access_token(data=dict(sub=db_item.username))
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=dict(
            message="Author created successfully.",
            user=author.get("username"),
            token=token
        )
    )
