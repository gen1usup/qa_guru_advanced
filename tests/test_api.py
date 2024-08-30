from http import HTTPStatus

import pytest
import requests
from models.User import User



@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()['items']

def test_smoke(app_url):
    response = requests.get(f'{app_url}/status')
    assert response.json()['users'] == True


def test_users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK

    users = response.json()['items']

    for user in users:
        User.model_validate(user)


def test_users_no_duplicates(users):

    users_ids = [user["id"] for user in users]
    assert len(users_ids) == len(set(users_ids))


@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_user(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK

    user = response.json()
    User.model_validate(user)


@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY



@pytest.mark.parametrize("page, size, expected_count", [
    (1, 5, 5),   # Первая страница, размер 5, ожидаем 5 объектов
    (2, 5, 5),   # Вторая страница, размер 5, ожидаем 5 объектов
    (3, 5, 2),   # Третья страница, размер 5, ожидаем 2 объекта (всего 12 объектов)
    (1, 10, 10), # Первая страница, размер 10, ожидаем 10 объектов
    (2, 10, 2),  # Вторая страница, размер 10, ожидаем 2 объекта
])
def test_pagination(app_url, page, size, expected_count):
    response = requests.get(f"{app_url}/api/users/", params={"page": page, "size": size})
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert len(data["items"]) == expected_count  # Проверяем количество объектов на странице


@pytest.mark.parametrize("size, expected_pages", [
    (5, 3),   # При размере 5 ожидаем 3 страницы
    (10, 2),  # При размере 10 ожидаем 2 страницы
    (20, 1),  # При размере 20 ожидаем 1 страницу
])
def test_pagination_page_count(app_url, size, expected_pages):
    response = requests.get(f"{app_url}/api/users/", params={"page": 1, "size": size})
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data["pages"] == expected_pages  # Проверяем количество страниц


@pytest.mark.parametrize("page_1_size, page_2_size", [
    (5, 5),
    (10, 2),
])
def test_pagination_different_pages(app_url, page_1_size, page_2_size):
    response_page_1 = requests.get(f"{app_url}/api/users/", params={"page": 1, "size": page_1_size})
    response_page_2 = requests.get(f"{app_url}/api/users/", params={"page": 2, "size": page_2_size})

    assert response_page_1.status_code == HTTPStatus.OK
    assert response_page_2.status_code == HTTPStatus.OK

    data_page_1 = response_page_1.json()
    data_page_2 = response_page_2.json()

    # Проверяем, что данные на страницах разные
    assert data_page_1["items"] != data_page_2["items"]

