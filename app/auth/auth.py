from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.token import create_access_token
from app.auth.schemas import UserLogin
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth.schemas import Token
from sqlalchemy.future import select
from app.users.models import Users
from app.database import async_session_maker
from passlib.context import CryptContext

router = APIRouter(tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(email: str, password: str):
    async with async_session_maker() as session:
        result = await session.execute(select(Users).where(Users.email == email))
        user = result.scalars().first()

        if user and pwd_context.verify(password, user.hashed_password):
            return user
    return False


@router.post("/token", response_model=Token)
async def login_for_access_token(user_login: UserLogin = Depends()):
    user = await authenticate_user(user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
