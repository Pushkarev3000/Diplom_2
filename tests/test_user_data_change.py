import allure
import requests
import pytest
from random import randint
from urls import USER_DATA

@allure.feature('Тесты на проверку изменения данных пользователя')
class TestUserDataChange:

    @allure.story("Тестируем позитивный сценарий: успешный сменна пользовательских данных")
    @pytest.mark.parametrize('payload',
                            [{"password": "Updated"},
                            {"email": f"update_{randint(1000, 9999)}_email@ya.ru"},
                            {"name": "Updated Name"}
                            ]
                            )
    def test_update_profile_authorized(self, registered_user, payload):
        """Изменение данных с авторизацией"""
        response = requests.patch(USER_DATA, json=payload, headers=registered_user["token"])
        assert response.status_code == 200
        key = list(payload.keys())[0]
        if key == 'password':
            assert response.json()["user"].get('name') == registered_user["name"]
        else:
            assert response.json()["user"].get(key) == payload[key]

    @allure.story("Тестируем негативный сценарий: неавторизованная сменна данных")
    @pytest.mark.parametrize('payload',
                            [{"name": "Hacked Name"},
                            {"email": "Hacked@ya.ru"},
                            {"password": "Hacked"}
                            ]
                            )
    def test_update_profile_unauthorized(self, payload):
        """Попытка изменения без авторизации"""
        response = requests.patch(USER_DATA, json=payload)
        assert response.status_code == 401
        assert response.json().get('message') == "You should be authorised"
