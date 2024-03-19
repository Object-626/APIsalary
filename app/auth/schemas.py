from pydantic import BaseModel, EmailStr


class TokenData(BaseModel):
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserSalaryPromotion(BaseModel):
    salary: str
    data_promotion: str

