import pytest
from django.urls import reverse
from ideaboard.models import Idea, Tag
from tests.test_ideas import test_create_idea
from core.factories import UserFactory, IdeaFactory, TagFactory
@pytest.mark.django_db
def test_like_idea(auth_client, user):
    test_create_idea(auth_client, user) 
    idea = Idea.objects.first()

    url = reverse("idea-likes", kwargs={"idea_pk": idea.id})

    data = {"idea": idea.id}
    response = auth_client.post(url)
    assert response.status_code in [200, 201]
