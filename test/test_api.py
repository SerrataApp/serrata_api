from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)


def test_signup():
    response = client.post(
        "/signup",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@example.com"


def test_get_token():
    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_users_me():
    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    token = response.json()["access_token"]

    response = client.get(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@example.com"


def test_delete_user_me():
    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    token = response.json()["access_token"]

    response = client.delete(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@example.com"


def test_delete_user():
    client.post(
        "/signup",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )
    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    token = response.json()["access_token"]

    response = client.delete(
        "/users/",
        headers={"Authorization": f"Bearer {token}"},
        params={"user_id": 1},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Vous n'avez pas les droits pour effectuer cette action"
    client.delete(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"},
    )