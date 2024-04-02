import json

from fastapi.testclient import TestClient

from main import app


class TestApi:
    async def test_users(self, client, users):
        response = client.get("/users/")
        assert response.status_code == 200
        assert response.json() == [json.loads(users[0].model_dump_json())]

    async def test_token_no_user(self, client, users):
        client = TestClient(app=app)
        response = client.post("/users/token", data={"username": "1", "password": "2"})
        assert response.status_code == 404
        assert response.json() == {"detail": "User with these credentials not found"}

    async def test_token_wrong_password(self, client, users):
        response = client.post(
            "/users/token", data={"username": "test@email.com", "password": "2"}
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "User with these credentials not found"}

    async def test_token(self, client, users):
        response = client.post(
            "/users/token", data={"username": "test@email.com", "password": "password"}
        )
        assert response.status_code == 200
        assert response.json() == {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGVtYWlsLmNvbSJ9.7Lh72XrVoh5YTRN1IrH4ResAmMtk5vL4aKCyMVbaoGc",
            "token_type": "bearer",
        }
