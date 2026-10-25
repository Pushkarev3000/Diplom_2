#почему-то allure отчет не хотел работать без кода ниже, не мог найти импортированные urls
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

import requests
import pytest
from faker import Faker
import random
import string
from urls import USER_REGISTER, INGREDIENTS, LOGIN, USER_DATA

@pytest.fixture
def unique_user_data():
    __fake = Faker()
    __email = __fake.email()
    __password = ''

    for i in range(6):
        __password += random.choice(string.ascii_letters)
    __password += random.choice(string.digits)
    __password += random.choice(string.punctuation)

    payload = {
        "email": __email,
        "password": __password,
        "name": __password
    }
    return payload

@pytest.fixture
def registered_user(unique_user_data, delete_user):
    """Регистрирует пользователя и возвращает его данные + токен"""
    res = requests.post(USER_REGISTER, json=unique_user_data)
    assert res.status_code == 200, f"Не удалось зарегистрировать пользователя: {res.text}"
    login_data = {
        "password": unique_user_data["password"],
        "email": unique_user_data["email"]
    }
    # login_res = requests.post(LOGIN, json=login_data)
    # assert login_res.status_code == 200, f"Не залогиниться под пользователем: {res.text}"
    token = res.json()["accessToken"].split()[1]
    token_header = {"Authorization": f"Bearer {token}"}
    yield {**unique_user_data, "token": token_header}
    delete_user(token_header)

@pytest.fixture
def ingredient_hashes():
    """Получает список ингредиентов и возвращает их хеши"""
    res = requests.get(INGREDIENTS)
    assert res.status_code == 200
    ingredients = res.json()["data"]
    hashes = [ing["_id"] for ing in ingredients[:2]]
    return hashes

@pytest.fixture
def delete_user():
    token_list = []

    def add_token(token):
        token_list.append(token)

    yield add_token
    requests.delete(USER_DATA, headers=token_list[0])


