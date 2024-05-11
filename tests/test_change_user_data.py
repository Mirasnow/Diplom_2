import requests
import allure
import pytest

from data import Urls, TestData
from data import ErrorsMessages as EM


class TestChangeUserData:

    @allure.title('Проверка успешного изменения данных пользователя с авторизацией')
    @allure.description('Позитивный сценарий тестирования ручки "Обновление данных пользователя" PATCH /api/auth/user. '
                        'Проверяет, что данные пользователя могут быть изменены с авторизацией, '
                        'что тело ответа содержит все необходимые поля, '
                        'и что успешный запрос возвращает "success": true')
    @pytest.mark.parametrize('changed_field', ['email', 'password', 'name'])
    def test_successful_user_data_change_with_auth(self, create_user, changed_field):
        payload = {'email': create_user[1],
                   'password': TestData.test_user_password,
                   'name': TestData.test_user_name
                   }
        payload[changed_field] = f'{payload[changed_field]}a'
        headers = {'Authorization': f'{create_user[2]}'}
        response = requests.patch(Urls.change_user_data_url, data=payload, headers=headers)
        assert response.status_code == 200
        assert response.json().get('success') is True
        assert 'user' in response.json()
        user_data = response.json()['user']
        assert 'email' in user_data
        assert 'name' in user_data

    @allure.title('Проверка попытки изменения данных пользователя без авторизации')
    @allure.description('Позитивный сценарий тестирования ручки "Обновление данных пользователя" PATCH /api/auth/user. '
                        'Проверяет, что данные пользователя не могут быть изменены без авторизации, '
                        'что тело ответа содержит все необходимые поля, '
                        'и что запрос возвращает "success": false')
    @pytest.mark.parametrize('changed_field', ['email', 'password', 'name'])
    def test_failed_user_data_change_without_auth(self, create_user, changed_field):
        payload = {'email': create_user[1],
                   'password': TestData.test_user_password,
                   'name': TestData.test_user_name
                   }
        payload[changed_field] = f'{payload[changed_field]}a'
        response = requests.patch(Urls.change_user_data_url, data=payload)
        assert response.status_code == 401
        assert response.json().get('success') is False
        assert response.json()['message'] == EM.authorised_error_401