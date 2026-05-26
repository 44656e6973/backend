# tests/test_tags.py
import pytest
from django.urls import reverse
from ideaboard.models import Tag
from core.factories import TagFactory

@pytest.mark.django_db
def test_list_tags_unauthorized(api_client):
    """Неавторизованный пользователь не видит теги"""
    TagFactory.create_batch(3)
    url = reverse("tag-list")
    
    response = api_client.get(url)
    assert response.status_code == 401  # Unauthorized

@pytest.mark.django_db
def test_list_tags_authorized(auth_client):
    """Авторизованный пользователь видит список тегов"""
    TagFactory.create_batch(3)
    url = reverse("tag-list")
    
    response = auth_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3
    assert response.data[0]["name"]  # Проверяем структуру

@pytest.mark.django_db
def test_tag_creation_blocked(auth_client):
    """Попытка создания тега возвращает 405 (метод не поддерживается)"""
    url = reverse("tag-list")
    response = auth_client.post(url, {"name": "blocked"}, format="json")
    
    assert response.status_code == 405  # Method Not Allowed

@pytest.mark.django_db
def test_tag_deletion_blocked(auth_client):
    """Попытка удаления тега возвращает 405"""
    tag = TagFactory()
    url = reverse("tag-detail", kwargs={"pk": tag.id})
    
    response = auth_client.delete(url)
    assert response.status_code == 405