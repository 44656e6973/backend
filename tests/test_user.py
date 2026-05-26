import pytest
from django.urls import reverse
from ideaboard.models import User

@pytest.mark.django_db
def test_get_own_profile(auth_client, user):
    """Авторизованный пользователь может видеть свой профиль"""
    url = reverse("user-me")
    response = auth_client.get(url)
    
    assert response.status_code == 200
    assert response.data['username'] == user.username
    assert response.data['email'] == user.email
    assert 'password' not in response.data

@pytest.mark.django_db
def test_unauthorized_access_to_profile(api_client):
    """Неавторизованный пользователь не может видеть профиль"""
    url = reverse("user-me")
    response = api_client.get(url)
    
    assert response.status_code == 401 

@pytest.mark.django_db
def test_update_own_profile(auth_client, user):
    """Пользователь может обновить свои данные (например, аватар)"""
    url = reverse("user-me")
    data = {
        "avatar_URL": "https://new-avatar.com/pic.jpg"
    }
    
    response = auth_client.patch(url, data, format="json")
    
    assert response.status_code == 200
    assert response.data['avatar_URL'] == "https://new-avatar.com/pic.jpg"
    
    user.refresh_from_db()
    assert user.avatar_URL == "https://new-avatar.com/pic.jpg"