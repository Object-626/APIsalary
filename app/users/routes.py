import asyncio
from sqlalchemy.exc import IntegrityError
from app.auth.auth import get_current_user_from_cookie, get_current_active_admin
from app.auth.schemas import UserSalaryPromotion
from app.users.models import Users, UserCreate, UserResponse
from app.database import async_session_maker
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.future import select
from passlib.context import CryptContext
from fastapi_cache.decorator import cache


router = APIRouter(tags=["Это БАЗА!"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/users/", response_model=UserResponse, dependencies=[Depends(get_current_active_admin)])
async def create_user(user: UserCreate = Depends()):
    hashed_password = pwd_context.hash(user.password)

    async with async_session_maker() as session:
        new_user = Users(email=user.email, hashed_password=hashed_password,
                         salary=user.salary, data_promotion=user.data_promotion, role=user.role)
        session.add(new_user)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        return new_user


@router.delete("/users/{user_email}")
async def delete_user_by_email(user_email: str):
    async with async_session_maker() as session:

        query = select(Users).where(Users.email == user_email)
        result = await session.execute(query)
        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого пользователя нет")

        await session.delete(user)
        await session.commit()
        return {"detail": f"Пользователь с почтой {user_email} удалён"}


@router.get("/me/", response_model=UserResponse)
@cache(expire=30)
async def read_users_me(current_user: Users = Depends(get_current_user_from_cookie)):
    await asyncio.sleep(3)
    return current_user


@router.get("/users/me/salary-promotion", response_model=UserSalaryPromotion)
@cache(expire=30)
async def read_users_salary_promotion(current_user: Users = Depends(get_current_user_from_cookie)):
    await asyncio.sleep(3)
    return {
        "salary": current_user.salary,
        "data_promotion": current_user.data_promotion
    }
