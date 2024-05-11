import requests
import allure
import pytest

from data import Urls, TestData
from data import ErrorsMessages as EM


class TestCreateUser:

    @allure.title('Проверка успешного создания пользователя')
    @allure.description('Позитивный сценарий тестирования ручки "Создание пользователя" POST /api/auth/register. '
                        'Проверяет, что пользователь может быть создан, '
                        'что тело ответа содержит все необходимые поля, '
                        'и что успешный запрос возвращает "success": true')
    def test_successful_user_creation(self, create_user):
        response = create_user[0]
        assert response.status_code == 200
        assert response.json().get('success') is True
        assert 'user' in response.json()
        assert 'accessToken' in response.json()
        user_data = response.json()['user']
        assert 'email' in user_data
        assert 'name' in user_data
        assert 'refreshToken' in response.json()

    @allure.title('Проверка повторного создания существующего пользователя')
    @allure.description('Негативный сценарий тестирования ручки "Создание пользователя" POST /api/auth/register. '
                        'Проверяет невозможность создания существующего пользователя, '
                        'что тело ответа содержит все необходимые поля, '
                        'и что запрос возвращает "success": false')
    def test_create_exists_user(self, create_user):
        repeating_user_payload = {
            "email": f'{create_user[1]}',
            "password": TestData.test_user_password,
            "name": TestData.test_user_name
        }
        response = requests.post(Urls.register_url, data=repeating_user_payload)
        assert response.status_code == 403
        assert response.json().get('success') is False
        assert response.json()['message'] == EM.create_exists_user_error_403

    @allure.title('Проверка создания пользователя с отсутствующими полями')
    @allure.description('Негативный сценарий тестирования ручки "Создание пользователя" POST /api/auth/register. '
                        'Параметризованный тест, проверяет невозможность создания пользователя, '
                        'когда отсутствует одно из обязательных полей, '
                        'и что запрос возвращает "success": false')
    @pytest.mark.parametrize('payload', TestData.creation_missing_fields)
    def test_create_user_with_missing_field(self, payload):
        response = requests.post(Urls.register_url, data=payload)
        assert response.status_code == 403
        assert response.json().get('success') is False
        assert response.json()['message'] == EM.create_user_required_fields_error_403