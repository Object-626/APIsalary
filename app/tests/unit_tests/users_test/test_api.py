from httpx import AsyncClient
from app.tests.conftest import ac
import pytest
from httpx import AsyncClient


"""Тесты работают только если убрать Depends в соответствующем роутере"""


async def test_register(ac: AsyncClient):
    response = await ac.post("/users/", json={
        "email": "kot@pes.com",
        "password": "xvost",
        "salary": "20000",
        "data_promotion": "2025-11-09",
        "role": "user"
    })
    assert response.status_code == 200


async def test_login(ac: AsyncClient):
    result = await ac.post("/login", json={
        "email": "Pasha@gmail.com",
        "password": "test"
    })
    assert result.status_code == 200









