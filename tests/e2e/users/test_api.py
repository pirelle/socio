def test_add_user(client, add_user_data):
    response = client.post("users/", data=add_user_data.model_dump_json())
    assert response.status_code == 201
    assert response.json() == {"user_id": 1}

    response = client.get("users/")
    assert response.status_code == 200
    assert len(response.json()) == 1
