import json
from types import SimpleNamespace
from unittest.mock import call

from users.schemas import PublicUserSchema


def test_users(client, user_service):
    users_list = [
        PublicUserSchema(
            id=1,
            first_name="",
            last_name="",
        )
    ]
    user_service.get_users.return_value = users_list
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [json.loads(users_list[0].model_dump_json())]


def test_add_user(client, user_service, add_user_data):
    user_service.add_user.return_value = 777
    response = client.post("/users/", data=add_user_data.model_dump_json())
    assert response.status_code == 201
    assert response.json() == {"user_id": 777}


def test_token_no_user(client, user_service):
    user_service.authenticate_user.return_value = None
    response = client.post("/token", data={"username": "1", "password": "2"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User with these credentials not found"}
    assert user_service.authenticate_user.call_args_list == [call("1", "2")]


def test_token(client, user_service):
    user_service.authenticate_user.return_value = SimpleNamespace(email="asdf@asdf.com")
    user_service.create_access_token.return_value = "sometoken"

    response = client.post("/token", data={"username": "1", "password": "2"})
    assert response.status_code == 200
    assert response.json() == {
        "access_token": user_service.create_access_token.return_value,
        "token_type": "bearer",
    }
