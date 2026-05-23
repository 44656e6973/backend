import pytest
from django.urls import reverse
from ideaboard.models import Idea, Tag
from core.factories import UserFactory, IdeaFactory, TagFactory

@pytest.mark.django_db
def test_create_idea(auth_client, user):
    url = reverse("idea-list")  # Замените на имя вашего URL
    
    tags = TagFactory.create_batch(2)
    data = {
        "title": "Test Idea",
        "description": "Description",
        "tags": [t.id for t in tags]
    }
    
    response = auth_client.post(url, data, format="json")
    
    assert response.status_code == 201
    assert response.data["title"] == "Test Idea"
    assert response.data["author"]["id"] == user.id
    assert Idea.objects.count() == 1

@pytest.mark.django_db
def test_list_ideas_public(api_client):
    IdeaFactory.create_batch(3)
    url = reverse("idea-list")
    
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3