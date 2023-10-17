import os

from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .models import User

from dotenv import load_dotenv

load_dotenv(".env")


SECRET_KEY = os.environ["SECRET_KEY"] or "a14f2e60ba7ec9d33409c48f779c39a0a61c76dbda704e7d3792221b46c67d44"

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id = payload.get("id")
        if username is None:
            raise HTTPException(status_code=400, detail="Token not found")
        token_data = User(username=username, id=user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return token_data
