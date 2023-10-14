import os

from dotenv import load_dotenv
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.middleware.cors import CORSMiddleware

from .routers import users, authors, books
from .security import oauth2_scheme, SECRET_KEY, ALGORITHM


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
    return JSONResponse(status_code=status.HTTP_200_OK, content=dict(message="API Status OK"))

