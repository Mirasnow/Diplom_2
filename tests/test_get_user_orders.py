import requests
import allure

from data import Urls
from data import ErrorsMessages as EM


class TestGetUserOrders:

    @allure.title('Проверка получения заказов авторизованным пользователем')
    @allure.description('Позитивный сценарий тестирования ручки "Получение заказов конкретного пользователя" GET /api/orders.'
                        'Проверяет, что код ответа равен 200, '
                        'и что запрос возвращает "success": true')
    def test_get_user_orders_with_authorization(self, create_user):
        payload = {'ingredients': ['61c0c5a71d1f82001bdaaa6c']}
        headers = {'Authorization': f'{create_user[2]}'}
        requests.post(Urls.create_order_url, data=payload, headers=headers)
        response = requests.get(Urls.get_user_orders, headers=headers)
        assert response.status_code == 200
        assert response.json().get('success') is True


    @allure.title('Проверка попытки получения заказов неавторизованным пользователем')
    @allure.description('Негативный сценарий тестирования ручки "Получение заказов конкретного пользователя" GET /api/orders.'
                        'Проверяет, что код ответа равен 401, '
                        'и что запрос возвращает "success": false')
    def test_get_user_orders_without_authorization(self, create_user):
        payload = {'ingredients': ['61c0c5a71d1f82001bdaaa6c']}
        headers = {'Authorization': f'{create_user[2]}'}
        requests.post(Urls.create_order_url, data=payload, headers=headers)
        headers = {}
        response = requests.get(Urls.get_user_orders, headers=headers)
        assert response.status_code == 401
        assert response.json().get('success') is False
        assert response.json()['message'] == EM.authorised_error_401