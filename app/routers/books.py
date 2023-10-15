from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db

from app.models import Book, User
from app.schema import BookSchema, EditBookSchema
from app.security import get_current_user


router = APIRouter(prefix="/authors/{author_id}/books", tags=["books"])


@router.get("/")
def get_all(current_user: User = Depends(get_current_user)):
    return JSONResponse(status_code=status.HTTP_200_OK, content=dict(detail="Successful"))


@router.get("/{book_id}")
def get(author_id, book_id, current_user: User = Depends(get_current_user)):
    book = Book.get_by_author(book_id, author_id)

    if not book:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=dict(detail="Book not found."))

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            detail="Successful",
            book=dict(id=book.id, title=book.title, author_id=author_id)
        ),
    )


@router.post("/")
def create(author_id, book: BookSchema, current_user: User = Depends(get_current_user)):
    book = book.dict()
    db_item = Book(**book, author_id=author_id).save(db)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=dict(detail="Book created successfully.", book=dict(id=db_item.id, name=db_item.title)),
    )


@router.put("/{book_id}")
def edit(author_id, book_id, book: EditBookSchema, current_user: User = Depends(get_current_user)):
    book = book.dict()
    book_obj = Book.get(book_id)
    book_obj.title = book.get("title", book_obj.title)
    book_obj.isbn = book.get("isbn", book_obj.isbn)
    book_obj.pages = book.get("pages", book_obj.pages)
    book_obj.publish_year = book.get("publish_year", book_obj.publish_year)
    book_obj.cost = book.get("cost", book_obj.cost)
    book_obj.currency = book.get("currency", book_obj.currency)
    book_obj.author_id = book.get("author_id", author_id)
    db.session.commit()
    db.session.refresh(book_obj)
    updated_book = Book.get(book_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            detail="Book edited successfully.",
            book=dict(
                title=updated_book.title,
                isbn=updated_book.isbn,
                pages=updated_book.pages,
                publish_year=updated_book.publish_year,
                cost=updated_book.cost,
                currency=updated_book.currency
            )

        )
    )


@router.delete("/{book_id}")
def delete(author_id, book_id, current_user: User = Depends(get_current_user)):
    Book.get_by_author(book_id, author_id).delete(db)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(detail="Book deleted successfully"))
