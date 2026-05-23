import pytest
from django.urls import reverse
from ideaboard.models import Idea, Tag
from core.factories import UserFactory, IdeaFactory, TagFactory

@pytest.mark.django_db
def test_registration(api_client):
    url = reverse("registration-list")  
    data = {
        "username": UserFactory.username,
        "email": UserFactory.email,
        "password": "securepassword123"
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == 201
    assert response.data["message"] == "Пользователь успешно зарегистрирован"