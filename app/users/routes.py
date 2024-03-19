from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from app.users.models import Users, UserCreate, UserResponse
from app.database import async_session_maker
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select
router = APIRouter()


@router.post("/users/", response_model=UserResponse)  # Используйте здесь свой URL
async def create_user(user: UserCreate):
    hashed_password = generate_password_hash(user.password)

    async with async_session_maker() as session:  # Убедитесь, что async_session_maker создан правильно
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
    async with async_session_maker() as session:  # Используйте здесь ваш асинхронный sessionmaker
        # Пытаемся найти пользователя по email в базе данных
        query = select(Users).where(Users.email == user_email)
        result = await session.execute(query)
        user = result.scalars().first()

        # Если пользователь не найден, возвращаем ошибку
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Если пользователь найден, удаляем его
        await session.delete(user)
        await session.commit()

        # Подтверждаем удаление
        return {"detail": f"User with email {user_email} has been deleted"}
