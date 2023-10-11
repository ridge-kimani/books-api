from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import DBSessionMiddleware, db
from .routers import authors

import os
from dotenv import load_dotenv


load_dotenv(".env")

app = FastAPI()

app.include_router(authors.router)
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URI"])


@app.get("/healthcheck")
async def root():
    return JSONResponse(status_code=status.HTTP_200_OK, content=dict(message="API Status OK"))
