import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture(scope="module", autouse=True)
def setup():
    # Запускаем FastAPI сервер в отдельном процессе
    import subprocess
    import time
    process = subprocess.Popen(["uvicorn", "main:app"])
    time.sleep(2)  # Ждем немного, чтобы сервер успел запуститься
    yield
    process.terminate()

def test_create_user():
    url = f"{BASE_URL}/user"
    payload = {
        "name": "John Doe",
        "phone": "+123456789"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["phone"] == "+123456789"
    assert "id" in data
    assert "date_added" in data

def test_get_user():
    url = f"{BASE_URL}/user/1"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "John Doe"
    assert data["phone"] == "+123456789"
    assert "date_added" in data

def test_get_user_not_found():
    url = f"{BASE_URL}/user/999"
    response = requests.get(url)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"
