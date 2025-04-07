import os
from datetime import datetime, timedelta, UTC

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import or_
from ..schemas.users import UserIn, UserOut, TokenData
from ..models.users import User
from ..config.db import db

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # Tiempo de expiración para el access token
REFRESH_TOKEN_EXPIRE_DAYS = 7  # Tiempo de expiración para el refresh token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    expire = datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)  # Refresh tokens duran más
    to_encode = {**data, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    db_user = db.query(User).filter(or_(User.username == token_data.username, User.email == token_data.username)).first()
    if db_user is None:
        raise credentials_exception
    return {"user": db_user, "token": token}

def login_user_is_active(is_active: bool):
    print(is_active)
    if not is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

async def get_current_user_is_active(current_user: UserOut = Depends(get_current_user)):
    login_user_is_active(current_user["user"].is_active)
    return current_user

async def token_is_valid(current_user: UserOut = Depends(get_current_user)):
    return current_user

