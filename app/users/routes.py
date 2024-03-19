from sqlalchemy.exc import IntegrityError

from app.auth.auth import get_current_user_from_cookie
from app.auth.schemas import UserSalaryPromotion
from app.users.models import Users, UserCreate, UserResponse
from app.database import async_session_maker
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.future import select
from passlib.context import CryptContext


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    hashed_password = pwd_context.hash(user.password)

    async with async_session_maker() as session:
        new_user = Users(email=user.email, hashed_password=hashed_password,
                         salary=user.salary, data_promotion=user.data_promotion)
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

        # Если пользователь не найден, возвращаем ошибку
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого пользователя нет")

        # Если пользователь найден, удаляем его
        await session.delete(user)
        await session.commit()

        # Подтверждаем удаление
        return {"detail": f"Пользователь с почтой {user_email} удалён"}


@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: Users = Depends(get_current_user_from_cookie)):
    return current_user


@router.get("/users/me/salary-promotion", response_model=UserSalaryPromotion)
async def read_users_salary_promotion(current_user: Users = Depends(get_current_user_from_cookie)):
    return {
        "salary": current_user.salary,
        "data_promotion": current_user.data_promotion
    }
