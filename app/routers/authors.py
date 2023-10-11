from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..schema import LoginSchema, RegisterSchema

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@router.post("/login")
def login(author: LoginSchema):
    return JSONResponse(status_code=status.HTTP_200_OK, content=dict(message="Success"))

