from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder

from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db
from app.models import Author, User, Book
from app.schema import AuthorSchema, EditAuthorSchema, GetAuthorSchema
from app.security import get_current_user


router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@router.get("/")
def get_all(current_user: User = Depends(get_current_user)):
    all_authors = Author.get_all(current_user.id)

    authors = [
        GetAuthorSchema(count=count, id=author.id, name=author.name, updated=author.updated or author.created)
        for author, count in all_authors
    ]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(detail="Authors get successful.", authors=jsonable_encoder(authors)),
    )


@router.get("/{author_id}")
def get(author_id, current_user: User = Depends(get_current_user)):
    author = Author.get(author_id, current_user.id)

    if not author:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=dict(detail="Author not found."))

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            detail="Author get Successful.",
            author=jsonable_encoder(
                GetAuthorSchema(id=author.id, name=author.name, updated=author.updated or author.created)
            ),
        ),
    )


@router.post("/")
def create(author: AuthorSchema, current_user: User = Depends(get_current_user)):
    author = author.dict()
    db_item = Author(**author, created_by=current_user.id).save(db)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=dict(
            detail="Author created successfully.",
            author=jsonable_encoder(
                GetAuthorSchema(id=db_item.id, name=db_item.name, updated=db_item.created)
            ),
        ),
    )


@router.put("/{author_id}")
def edit(author_id, author: EditAuthorSchema, current_user: User = Depends(get_current_user)):
    author = author.dict()
    author_obj = Author.get(author_id, current_user.id)
    if not author_obj:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=dict(detail="Author not found."))

    author_obj.first_name = author.get("first_name")
    author_obj.last_name = author.get("last_name")
    db.session.commit()
    db.session.refresh(author_obj)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            detail="Author edited successfully.",
            author=jsonable_encoder(
                GetAuthorSchema(
                    **author,
                    name=author_obj.name,
                    id=author_obj.id,
                    updated=author_obj.updated or author_obj.created
                )
            ),
        )
    )


@router.delete("/{author_id}")
def delete(author_id, current_user: User = Depends(get_current_user)):
    author_obj = Author.get(author_id, current_user.id)
    if not author_obj:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=dict(detail="Author not found."))

    author_obj.delete(db)
    return JSONResponse(status_code=status.HTTP_200_OK, content=dict(detail="Author deleted successfully."))
