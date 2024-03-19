from typing import List
from fastapi import FastAPI
from app.users.models import Users
from app.auth.auth import router as auth_router
from app.users.routes import router as user_router

app = FastAPI(
    title="Зарплата сотрудников"
)

app.include_router(auth_router)
app.include_router(user_router)


# fake_users = [
#     {"id": 1, "email": "oleg@mail.com", "password": "1234"},
#     {"id": 2, "email": "vova@mail.com", "password": "0987"},
#     {"id": 3, "email": "petya@mail.com", "password": "5434"}
# ]
#
#
# # @app.get("/users/{user_id}")
# # def get_users_one(user_id: int):
# #     return [user for user in fake_users if user.get("id") == user_id]
#
# @app.post("/users")
# def register(users: List[Users]):
#     fake_users.extend(users)
#     return {"data": fake_users}
