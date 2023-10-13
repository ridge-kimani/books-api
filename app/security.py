from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "a14f2e60ba7ec9d33409c48f779c39a0a61c76dbda704e7d3792221b46c67d44"
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
