from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.auth.token import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_active_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)

# Используйте эту зависимость в путях, где требуется аутентификация.
