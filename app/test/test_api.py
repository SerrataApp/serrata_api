from fastapi.testclient import TestClient

import sqlite3 as lite

from app.api import app

client = TestClient(app)


def test_signup():
    response = client.post(
        "/signup",
        json={
            "username": "testuser",
            "email": "testuser@gmail.com",
            "signup_date": "2023-12-07",
            "password": "testpassword",
        },
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


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


def test_add_played_game():
    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    token = response.json()["access_token"]

    response = client.put(
        "/users/me/game",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()


def test_create_game():
    response_token = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    token = response_token.json()["access_token"]

    game_data = {
        "game_mode": 0,
        "time": 0,
        "errors": 0,
        "hint": 0,
        "game_date": "2023-12-07",
        "player_id": 1,
        "public": True,
    }

    response_create_game = client.post(
        "/score/",
        json=game_data,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response_create_game.status_code == 200
    created_game = response_create_game.json()

    assert created_game["game_mode"] == game_data["game_mode"]
    assert created_game["time"] == game_data["time"]
    assert created_game["errors"] == game_data["errors"]
    assert created_game["hint"] == game_data["hint"]
    assert created_game["game_date"] == game_data["game_date"]
    assert created_game["player_id"] == game_data["player_id"]
    assert created_game["public"] == game_data["public"]


def test_get_game():
    response_get_game = client.get(
        "/score/?game_id=1",
    )

    assert response_get_game.status_code == 200
    assert response_get_game.json()


def test_get_games_by_user():
    response_token = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    token = response_token.json()["access_token"]

    response_get_games = client.get(
        "/score/user/?username=testuser",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response_get_games.status_code == 200
    assert response_get_games.json()


def test_get_users_by_name():
    response = client.get(
      "/users/search/?username=t&limit=100"
    )

    assert response.status_code == 200
    assert response.json()


def test_delete_game():
    admin_response_token = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    admin_token = admin_response_token.json()["access_token"]
    #
    # con = lite.connect('sql_app.db')
    #
    # with con:
    #     cur = con.cursor()
    #     cur.execute("UPDATE users SET admin = 1 WHERE id = 2")

    delete_game_response = client.delete(
        f"/score/?game_id=1",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert delete_game_response.status_code == 401


def test_get_games():
    response = client.get(
        "/scores/?skip=0&limit=100"
    )

    assert response.status_code == 200
    assert response.json()


def test_get_games_by_gamemode():
    response = client.get(
        "/scores/mode/?game_mode_id=0"
    )

    assert response.status_code == 200
    assert response.json()


def test_change_stage_game():
    response_token = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    token = response_token.json()["access_token"]

    response_get_game = client.get(
        "/score/?game_id=1",
    )

    etat1 = response_get_game.json()["public"]

    response = client.put(
        "/score/changeState/?game_id=1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()
    etat2 = response.json()["public"]
    assert etat1 != etat2


def test_disable():
    response_token = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    token = response_token.json()["access_token"]

    response = client.put(
        "/admindisable/?user_id=1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.json()


def test_cgu():
    response_token = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    token = response_token.json()["access_token"]

    response = client.put(
        "/users/me/cgu/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()


def test_get_userdata():
    response_token = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    token = response_token.json()["access_token"]

    response = client.get(
        "/adminusers/?user_id=1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.json()

# tester admincgu


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


def test_delete_user():
    client.post(
        "/signup",
        json={
            "username": "testuser",
            "email": "testuser@gmail.com",
            "signup_date": "2023-12-07",
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
