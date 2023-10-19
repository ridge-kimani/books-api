import os

from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.middleware.cors import CORSMiddleware
from .models import User, Author, Book
from .routers import users, authors, books
from .security import oauth2_scheme, SECRET_KEY, ALGORITHM
from .seed import *

load_dotenv(".env")

app = FastAPI()

app.include_router(users.router)
app.include_router(authors.router)
app.include_router(books.router)
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URI"])
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)


@app.get("/healthcheck")
async def root():
    return JSONResponse(status_code=status.HTTP_200_OK, content=dict(detail="API Status OK"))


@app.post("/seed")
def seed_data():
    user = USER.get("username")
    password = User.hash_password(USER.pop("password"))
    if User.exists(user):
        user = User.get(username=user)

    else:
        user = User(**USER, password=password).save(db)

    author = Author(**AUTHOR, created_by=user.id).save(db)

    instances = []
    for book in BOOKS:
        model_instance = Book(**book, author_id=author.id, created_by=user.id)
        instances.append(model_instance)

    db.session.add_all(instances)
    db.session.commit()
    db.session.close()

    return JSONResponse(status_code=200, content=dict(detail='Seed successful'))
