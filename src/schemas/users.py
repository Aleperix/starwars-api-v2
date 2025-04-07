from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    email: str

class UserIn(BaseUser):
    password: str

class UserOut(BaseUser):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str

class ANLogin(BaseModel):
    access_token: str
    token_type: str
    user: UserOut


class TokenData(BaseModel):
    username: str | None = None
