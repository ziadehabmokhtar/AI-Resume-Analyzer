def test_rag_and_career(client):
    h = {
        "Authorization": "Bearer "
        + client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        ).json()["access_token"]
    }
    r = client.post(
        "/api/career/ask",
        headers=h,
        json={"question": "What skills are useful for a backend Python career?"},
    )
    assert r.status_code == 200
    assert "answer" in r.json()
    assert isinstance(r.json()["sources"], list)
