import pytest
from django.urls import reverse
from ideaboard.models import Idea, Tag
from core.factories import UserFactory, IdeaFactory, TagFactory

@pytest.mark.django_db
def test_registration(api_client):
    url = reverse("register")  
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepassword123",
        "password_confirm": "securepassword123"
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == 200
    