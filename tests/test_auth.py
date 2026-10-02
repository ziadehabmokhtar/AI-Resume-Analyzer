def test_register_login_me(client):
    r = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert r.status_code == 201
    token = r.json()["access_token"]
    assert token
    r = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    r = client.post(
        "/api/auth/login", json={"email": "test@example.com", "password": "password123"}
    )
    assert r.status_code == 200


def test_duplicate_and_bad_login(client):
    assert (
        client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "password123"},
        ).status_code
        == 409
    )
    assert (
        client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "wrongpass"},
        ).status_code
        == 401
    )
