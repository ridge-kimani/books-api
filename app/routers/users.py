from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db
from app.schema import LoginSchema, RegisterSchema
from app.models import User, Book

from app.security import create_access_token
from app.schema import GetBookSchema, BookSchema
from app.security import get_current_user


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
            content=dict(detail="Username not found.", field="username"),
        )
    if not User.verify_password(user_obj.get("password"), user.password):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=dict(detail="Incorrect password.", field="password"),
        )

    token = create_access_token(data=dict(sub=user.username, id=user.id))
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(detail="Login successful.", user=dict(id=user.id, username=user.username), token=token),
    )


@router.post("/register")
def register(user: RegisterSchema):
    user = user.dict()

    if User.exists(username=user.get("username")):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=dict(detail="User exists with that username"),
        )

    password = User.hash_password(user.pop("password"))
    db_item = User(**user, password=password).save(db)
    token = create_access_token(data=dict(sub=db_item.username, id=db_item.id))
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=dict(detail="User created successfully.", user=user.get("username"), id=db_item.id, token=token),
    )


@router.get("/books")
def get_all(current_user: User = Depends(get_current_user)):
    all_books = Book.get_all_by_user(current_user.id)
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


@router.put("/books")
def edit_multiple(books: BookSchema, current_user: User = Depends(get_current_user)):
    data = books.dict()
    instances = []

    for book in data.get("books"):
        book_obj = Book.get(book.get("id"))
        book_obj.title = book.get("title", book_obj.title)
        book_obj.isbn = book.get("isbn", book_obj.isbn)
        book_obj.pages = book.get("pages", book_obj.pages)
        book_obj.publish_year = book.get("publish_year", book_obj.publish_year)
        book_obj.cost = book.get("cost", book_obj.cost)
        book_obj.currency = book.get("currency", book_obj.currency)
        book_obj.author_id = book.get("author_id", book_obj.author_id)
        instances.append(book_obj)

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
            updated=book.updated
        )
        books.append(book)
    db.session.close()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=dict(detail="Books updated successfully.", books=jsonable_encoder(books)),
    )