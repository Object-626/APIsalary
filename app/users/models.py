from sqlalchemy import Integer, String, Column
from app.database import Base
from pydantic import BaseModel, EmailStr
from enum import Enum

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    salary = Column(String, nullable=False)
    data_promotion = Column(String, nullable=False)
    role = Column(String, nullable=False)


class Role(str, Enum):
    admin = "admin"
    user = "user"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    salary: str
    data_promotion: str
    role: Role


class UserResponse(BaseModel):
    email: EmailStr
    salary: str
    data_promotion: str

