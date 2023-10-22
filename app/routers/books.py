from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db

from app.models import Book, User, Author
from app.schema import BookSchema, EditBookSchema, GetBookSchema
from app.security import get_current_user


router = APIRouter(prefix="/authors/{author_id}/books", tags=["books"])


@router.get("/")
def get_all(author_id, current_user: User = Depends(get_current_user)):
    author_obj = Author.get(author_id, current_user.id)
    if not author_obj:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=dict(detail="Author not found."))

    all_books = Book.get_all_by_author(author_id, current_user.id)

    books = [
        GetBookSchema(
            title=book.title,
            author=book.author.name,
            isbn=book.isbn,
            publish_year=book.publish_year,
            cost=book.cost,
            currency=book.currency or "$",
            pages=book.pages,
            id=book.id,
            updated=book.updated or book.created
        )
        for book in all_books
    ]
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=dict(detail="Books get successful.", books=jsonable_encoder(books))
    )


@router.get("/{book_id}")
def get(author_id, book_id, current_user: User = Depends(get_current_user)):
    author_obj = Author.get(author_id, current_user.id)
    if not author_obj:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=dict(detail="Author not found."))

    book = Book.get_by_author(book_id, author_id)

    if not book:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=dict(detail="Book not found."))

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            detail="Fetch book successful.",
            book=dict(id=book.id, title=book.title, author_id=book.author_id, updated=book.updated or book.created)
        ),
    )


@router.post("/")
def create(author_id, books: BookSchema, current_user: User = Depends(get_current_user)):
    author_obj = Author.get(author_id, current_user.id)
    if not author_obj:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=dict(detail="Author not found."))

    data = books.dict()
    instances = []
    for book in data.get("books"):
        book.pop('author_id')
        model_instance = Book(**book, author_id=author_id, created_by=current_user.id)
        instances.append(model_instance)

    db.session.add_all(instances)
    db.session.commit()
    books = []
    for book in instances:
        db.session.refresh(book)
        book = GetBookSchema(
            title=book.title,
            author=book.author.name,
            isbn=book.isbn,
            publish_year=book.publish_year,
            cost=book.cost,
            currency=book.currency or "$",
            pages=book.pages,
            id=book.id,
            updated=book.updated or book.created
        )
        books.append(book)
    db.session.close()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=dict(detail="Books created successfully.", books=jsonable_encoder(books)),
    )


@router.put("/{book_id}")
def edit(author_id, book_id, book: EditBookSchema, current_user: User = Depends(get_current_user)):
    author_obj = Author.get(author_id, current_user.id)
    if not author_obj:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=dict(detail="Author not found."))

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
                currency=updated_book.currency,
                id=updated_book.id,
            ),
        ),
    )


@router.delete("/{book_id}")
def delete(author_id, book_id, current_user: User = Depends(get_current_user)):
    author_obj = Author.get(author_id, current_user.id)
    if not author_obj:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=dict(detail="Author not found."))

    Book.get_by_author(book_id, author_id).delete(db)
    return JSONResponse(status_code=status.HTTP_200_OK, content=dict(detail="Book deleted successfully"))
