from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.auth.token import create_access_token
from app.auth.schemas import UserLogin
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth.schemas import Token
from sqlalchemy.future import select
from app.users.models import Users
from app.database import async_session_maker
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.config import SECRET_KEY, ALGORITHM
from app.auth.schemas import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Users:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    async with async_session_maker() as session:
        result = await session.execute(select(Users).where(Users.email == email))
        user = result.scalar()

    if user is None:
        raise credentials_exception
    return user


router = APIRouter(tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(email: str, password: str):
    async with async_session_maker() as session:
        result = await session.execute(select(Users).where(Users.email == email))
        user = result.scalars().first()

        if user and pwd_context.verify(password, user.hashed_password):
            return user
    return False


@router.post("/token")
async def login_for_access_token(response: Response, user_login: UserLogin = Depends()):
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
    token_expiration = datetime.utcnow() + access_token_expires
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        expires=access_token_expires.total_seconds(),
        httponly=True  # Важно для безопасности, делает куку недоступной для клиентских скриптов
    )
    return {"access_token": access_token, "token_type": "bearer"}

