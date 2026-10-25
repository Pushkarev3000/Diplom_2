import allure
import requests
from urls import ORDER

@allure.feature('Тесты на создание заказа')
class TestOrderCreation:

    @allure.story("Тестируем позитивный сценарий: успешное создание заказа с авторизацией и ингредиентами")
    def test_create_order_authorized(self, registered_user, ingredient_hashes):
        """Создание заказа с авторизацией и ингредиентами"""
        payload = {"ingredients": ingredient_hashes}    
        response = requests.post(ORDER, json=payload, headers=registered_user["token"]) 
        assert response.status_code == 200
        assert "order" in response.json()
        assert "number" in response.json()["order"]
        assert response.json()["order"]["number"] is not None
    
    @allure.story("Тестируем позитивный сценарий: успешное создание заказа без авторизации и с ингредиентами")
    def test_create_order_unauthorized(self, ingredient_hashes):
        """Создание заказа без авторизации"""
        payload = {"ingredients": ingredient_hashes}
        response = requests.post(ORDER, json=payload)
        assert response.status_code == 200
        assert "order" in response.json()
        assert "number" in response.json()["order"]
        assert response.json()["order"]["number"] is not None

    @allure.story("Тестируем негативный сценарий: создание заказа без ингредиентов") 
    def test_create_order_empty_ingredients(self, registered_user):
        """Создание заказа БЕЗ ингредиентов"""
        payload = {"ingredients": []}
        response = requests.post(ORDER, json=payload, headers=registered_user["token"])
        assert response.status_code == 400
        assert response.json().get('message') == "Ingredient ids must be provided"

    @allure.story("Тестируем негативный сценарий: создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_hash(self, registered_user):
        """Создание заказа с неверным хешем ингредиентов"""
        payload = {"ingredients": ["fake_hash_123xyz"]}
        response = requests.post(ORDER, json=payload, headers=registered_user["token"])
        assert response.status_code == 500
        assert "Internal Server Error" in response.text 