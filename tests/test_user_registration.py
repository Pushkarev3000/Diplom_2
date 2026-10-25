import allure
import requests
from urls import USER_REGISTER

@allure.feature('Тесты на регистрацию пользователя')
class TestUserRegistration:

    @allure.story("Тестируем позитивный сценарий: успешное создание пользователя")
    def test_create_unique_user(self, unique_user_data, delete_user):
        """Создать уникального пользователя"""
        response = requests.post(USER_REGISTER, json=unique_user_data)
        assert response.status_code == 200
        data = response.json()
        token_header ={"Authorization": f"Bearer {data["accessToken"].split()[1]}"}
        assert data["success"] is True
        assert data["user"]["email"] == unique_user_data["email"]
        delete_user(token_header)

    @allure.story("Тестируем негативный сценарий: уже есть пользователь с таким email")
    def test_create_existing_user(self, registered_user):
        """Создать пользователя, который уже зарегистрирован"""
        response = requests.post(USER_REGISTER, json={
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"]
        })
        assert response.status_code == 403
        assert response.json().get('message') == "User already exists"

    @allure.story("Тестируем негативный сценарий: создание без email")
    def test_create_user_missing_field(self, unique_user_data):
        """Создать пользователя без одного обязательного поля (например, без email)"""
        payload = unique_user_data.copy()
        del payload["email"]
        response = requests.post(USER_REGISTER, json=payload)
        assert response.status_code == 403
        assert response.json().get('message') == "Email, password and name are required fields"