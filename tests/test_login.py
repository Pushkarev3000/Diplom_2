import allure
import pytest
import requests
from urls import LOGIN

@allure.feature('Тесты на проверку логина пользователя')
class TestUserLogin:

    @allure.story("Тестируем позитивный сценарий: успешный логин")
    def test_login_existing_user(self, registered_user):
        """Логин под существующим пользователем"""
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = requests.post(LOGIN, json=payload)
        
        assert response.status_code == 200
        assert "accessToken" in response.json()

    @allure.story("Тестируем негативный сценарий: незаполненные логин/пароль")
    @pytest.mark.parametrize('payload',
                            [{"email": "", "password": "12345"},
                            {"email": "test@ya.ru",  "password": ""},
                            {}
                            ]
                            )
    def test_login_invalid_credentials(self, payload):
        """Проверка передачи пустых значений"""
        response = requests.post(LOGIN, json=payload)
        assert response.status_code == 401
        assert response.json().get('message') == "email or password are incorrect"

    @allure.story("Тестируем негативный сценарий: некорректный пароль действующего пользователя")
    def test_login_invalid_password(self, registered_user):
        """Логин с неверным паролем"""
        payload = {
        "email": registered_user["email"],
        "password": "wrong_password_123"
        }
        response = requests.post(LOGIN, json=payload)
        assert response.status_code == 401
        assert response.json().get('message') == "email or password are incorrect"