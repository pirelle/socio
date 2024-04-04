def test_add_user(client, psql_create_db, add_user_data):
    response = client.post("users/", data=add_user_data.model_dump_json())
    breakpoint()
    ...
