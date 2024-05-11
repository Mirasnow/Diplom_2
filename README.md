## Дипломный проект. Задание 2: API

### Автотесты для проверки ручек API для Stellar Burgers.

### Структура проекта:

tests - пакет, содержащий тесты, разделенные по классам:

1. test_create_user.py

Проверяет ручку "Создание пользователя" POST /api/auth/register.

Класс TestCreateUser содержит тесты:

- test_successful_user_creation
- test_create_exists_user
- test_create_user_with_missing_field

2. test_login_user.py

Проверяет ручку "Авторизация пользователя" POST /api/auth/login.

Класс TestLoginUser содержит тесты:

- test_successful_login
- test_invalid_email_or_password

3. test_change_user_data.py

Проверяет ручку "Обновление данных пользователя" PATCH /api/auth/user.

Класс TestChangeUserData содержит тесты:

- test_successful_user_data_change_with_auth
- test_failed_user_data_change_without_auth

4. test_create_order.py

Проверяет ручку "Создание заказа" POST /api/v1/orders.

Класс TestCreateOrder содержит тесты:

- test_create_order_with_authorization_and_ingredients
- test_create_order_without_authorization
- test_create_order_without_ingredients
- test_order_creation_with_wrong_ingredients_hash_failed

5. test_get_user_orders.py

Проверяет ручку "Получение заказов конкретного пользователя" GET /api/orders.

Класс TestGetUserOrders содержит тесты:

- test_get_user_orders_with_authorization
- test_get_user_orders_without_authorization

6. conftest.py

Содержит фикстуру create_user


Также в корневой папке проекта находятся:
файл data.py c тестовыми данными,
файл requirements.txt c зависимостями проекта и
файл .gitignore.


### Запуск автотестов:
**Установка зависимостей** 

> `$ pip install -r requirements.txt`

**Генерация Allure-отчёта**

> `$ pytest tests.py --alluredir=allure_results`

> `$ allure serve allure_results`
 
 