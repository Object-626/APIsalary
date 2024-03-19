from sqlalchemy import Integer, String, Column
from app.database import Base
from pydantic import BaseModel, EmailStr


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    salary = Column(String, nullable=False)
    data_promotion = Column(String, nullable=False)


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    salary: str
    data_promotion: str


class UserResponse(BaseModel):
    email: EmailStr
    salary: str
    data_promotion: str

