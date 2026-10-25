import allure
import requests
from urls import ORDER

@allure.feature('Тесты на получение списка заказов пользователя')
class TestOrdersList:

    @allure.story("Тестируем позитивный сценарий: успешное получение списка заказов авторизованного пользователя")
    def test_get_orders_authorized(self, registered_user, ingredient_hashes):
        """Получение заказов авторизованным пользователем"""
        payload = {"ingredients": ingredient_hashes}
        response_1 = requests.post(ORDER, json=payload, headers=registered_user["token"])
        response_2 = requests.get(ORDER, headers=registered_user["token"])
        data = response_1.json()
        order = data.get("order")
        assert response_2.status_code == 200
        data = response_2.json()
        orders = data.get("orders")
        assert order['name'] == orders[0]['name']
        assert order['number'] == orders[0]['number']
        assert isinstance(orders, list)

    @allure.story("Тестируем негативный сценарий: получение списка заказов неавторизованного пользователя")
    def test_get_orders_unauthorized(self):
        """Получение заказов неавторизованным пользователем"""
        response = requests.get(ORDER)
        assert response.status_code == 401
        assert response.json().get('message') == "You should be authorised"
