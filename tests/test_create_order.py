import requests
import allure

from data import Urls
from data import ErrorsMessages as EM

class TestCreateOrder:

    @allure.title('Проверка успешного создания заказа с авторизацией и ингредиентами')
    @allure.description('Позитивный сценарий тестирования ручки "Создание заказа" POST /api/orders.'
                        'Проверяет создание заказа с авторизацией и ингредиентами,'
                        'что тело ответа содержит все основные обязательные поля,'
                        'и что успешный запрос возвращает "success": true')
    def test_create_order_with_authorization_and_ingredients(self, create_user):
        payload = {'ingredients': ['61c0c5a71d1f82001bdaaa6c']}
        headers = {'Authorization': f'{create_user[2]}'}
        response = requests.post(Urls.create_order_url, data=payload, headers=headers)
        assert response.status_code == 200
        assert response.json().get('success') is True
        assert 'name' in response.json()
        assert 'order' in response.json()
        order_data = response.json().get('order')
        assert 'number' in order_data

    @allure.title('Проверка попытки создания заказа без авторизации')
    @allure.description('Негативный сценарий тестирования ручки "Создание заказа" POST /api/orders.'
                        'Проверяет, что создание заказа без авторизации невозможно,'
                        'что тело ответа содержит все основные обязательные поля,'
                        'и что запрос возвращает "success": False')
    def test_create_order_without_authorization(self):
        payload = {'ingredients': ['61c0c5a71d1f82001bdaaa6c']}
        response = requests.post(Urls.create_order_url, data=payload)
        assert response.status_code == 401
        assert response.json().get('success') is False
        assert response.json()['message'] == EM.authorised_error_401

    @allure.title('Проверка попытки создания заказа без ингредиентов')
    @allure.description('Негативный сценарий тестирования ручки "Создание заказа" POST /api/orders.'
                        'Проверяет создание заказа без ингредиентов,'
                        'и что запрос возвращает "success": false')
    def test_create_order_without_ingredients(self, create_user):
        payload = {}
        headers = {'Authorization': f'{create_user[2]}'}
        response = requests.post(Urls.create_order_url, data=payload, headers=headers)
        assert response.status_code == 400
        assert response.json().get('success') is False
        assert response.json()['message'] == EM.create_order_error_400

    @allure.title('Проверка неудачной попытки создания заказа с неправильным хешем ингредиента')
    @allure.description('Негативный сценарий тестирования ручки "Создание заказа" POST /api/orders.'
                        'Проверяет неудачную попытку создания заказа с неправильным хешем ингредиента,'
                        'и что запрос возвращает код 500')
    def test_order_creation_with_wrong_ingredients_hash_failed(self, create_user):
        payload = {'ingredients': ['wronghash']}
        headers = {'Authorization': f'{create_user[2]}'}
        response = requests.post(Urls.create_order_url, data=payload, headers=headers)
        assert response.status_code == 500