from backend.agents.job_matching import JobMatchingAgent


def auth(client):
    r = client.post(
        "/api/auth/login", json={"email": "test@example.com", "password": "password123"}
    )
    return {"Authorization": "Bearer " + r.json()["access_token"]}


def test_job_crud_search(client):
    h = auth(client)
    r = client.post(
        "/api/jobs",
        headers=h,
        json={
            "title": "Python Developer",
            "company": "Demo",
            "description": "Build Python APIs and tests.",
            "required_skills": ["Python", "FastAPI"],
            "location": "Remote",
            "experience_level": "Junior",
            "education_required": "Bachelor",
        },
    )
    assert r.status_code == 201
    jid = r.json()["id"]
    assert client.get("/api/jobs?q=Python", headers=h).status_code == 200
    assert client.get(f"/api/jobs/{jid}", headers=h).status_code == 200
    assert (
        client.put(
            f"/api/jobs/{jid}",
            headers=h,
            json={
                "title": "Python Developer 2",
                "company": "Demo",
                "description": "Build Python APIs and tests.",
                "required_skills": ["Python"],
                "location": "Remote",
                "experience_level": "Junior",
                "education_required": "Bachelor",
            },
        ).status_code
        == 200
    )
    assert client.delete(f"/api/jobs/{jid}", headers=h).status_code == 200


def test_matching_formula():
    m = JobMatchingAgent().calculate(
        {
            "technical_skills": ["Python", "SQL"],
            "soft_skills": [],
            "experience": ["developer"],
            "education": ["Bachelor"],
        },
        {
            "required_skills": ["Python", "SQL", "FastAPI"],
            "experience_level": "Junior",
            "education_required": "Bachelor",
        },
    )
    assert 0 <= m["score"] <= 100
    assert "python" in m["matching_skills"] and "fastapi" in m["missing_skills"]
