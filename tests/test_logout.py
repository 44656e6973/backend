import pytest
from django.urls import reverse
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken


@pytest.mark.django_db
def test_logout_deletes_user_tokens(auth_client, user):
    assert OutstandingToken.objects.filter(user=user).exists()

    response = auth_client.post(reverse("logout"))

    assert response.status_code == 200
    assert response.data["deleted_tokens"] > 0
    assert not OutstandingToken.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_refresh_token_is_rejected_after_logout(auth_client):
    auth_client.post(reverse("logout"))

    response = auth_client.post(
        reverse("token_refresh"),
        {"refresh": auth_client.refresh_token},
        format="json",
    )

    assert response.status_code == 400
