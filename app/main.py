from fastapi import FastAPI
from app.users.routes import router as user_router
from app.auth.auth import router as auth_router


app = FastAPI(
    title="Зарплата сотрудников"
)
app.include_router(user_router)
app.include_router(auth_router)


