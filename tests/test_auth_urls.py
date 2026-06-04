import pytest


@pytest.mark.django_db
def test_token_obtain_pair_accepts_url_without_trailing_slash(api_client, user):
    response = api_client.post(
        "/api/token",
        {
            "username": user.username,
            "password": "testpassafsd123",
        },
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_token_refresh_accepts_url_without_trailing_slash(auth_client):
    response = auth_client.post(
        "/api/token/refresh",
        {"refresh": auth_client.refresh_token},
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data


@pytest.mark.django_db
def test_custom_login_accepts_url_without_trailing_slash(api_client, user):
    response = api_client.post(
        "/api/v1/auth/login",
        {
            "email": user.email,
            "password": "testpassafsd123",
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.data["user"]["email"] == user.email
    assert "access" in response.data
    assert "refresh" in response.data
