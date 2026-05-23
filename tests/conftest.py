import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from core.factories import UserFactory

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def auth_client(api_client, user):
    # 1. Логинимся
    login_url = reverse("token_obtain_pair")  # имя URL из вашего urls.py
    response = api_client.post(login_url, {
        "username": user.username,
        "password": "testpassafsd123"  # пароль из UserFactory
    }, format="json")
    
    assert response.status_code == 200, f"Не удалось залогиниться: {response.data}"
    
    access_token = response.data["access"]
    refresh_token = response.data["refresh"]
    
    # 2. Прописываем токен в заголовки
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    
    # 3. Сохраняем токены на клиенте для удобства
    api_client.access_token = access_token
    api_client.refresh_token = refresh_token
    
    return api_client