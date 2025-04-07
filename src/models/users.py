from ..config.db import Base, db
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from sqladmin import ModelView
import enum

class UserRoleEnum(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(64), unique=False, nullable=False)
    is_active = Column(Boolean(), unique=False, nullable=False)
    role = Column(Enum(UserRoleEnum))

    refresh_tokens = relationship('UserRefreshToken', back_populates='user', lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_active": self.is_active,
            "avatar": self.avatar
            # do not serialize the password, its a security breach
        }
class UserAdmin(ModelView, model=User):
    form_columns = ['username', 'role', 'email', 'password', 'is_active']
    column_details_list = form_columns
    column_list = ["id"] + form_columns
    icon="fa-solid fa-user"
    category = "Accounts"
    
class UserRefreshToken(Base):
    __tablename__ = "user_refresh_token"

    id = Column(Integer, primary_key=True)
    token = Column(String(256), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    device_id = Column(String(256), nullable=False)
    ip_address = Column(String(256), nullable=False)
    user = relationship('User')

    def __repr__(self):
        return f'<UserRefreshToken {self.id}>'

class UserRefreshTokenAdmin(ModelView, model=UserRefreshToken):
    form_columns = ['token', 'user', "device_id", "ip_address"]
    column_list = ["id", "device_id", "ip_address"] + form_columns
    icon="fa-solid fa-circle-xmark"
    category = "Accounts"