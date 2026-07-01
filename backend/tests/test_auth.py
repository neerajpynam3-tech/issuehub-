from tests.conftest import signup_and_login


def test_signup_creates_user(client):
    response = client.post(
        "/api/auth/signup",
        json={"name": "Alice", "email": "alice@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "alice@example.com"
    assert "password" not in body  # never leak credentials


def test_duplicate_email_is_rejected(client):
    payload = {"name": "Bob", "email": "bob@example.com", "password": "password123"}
    client.post("/api/auth/signup", json=payload)
    response = client.post("/api/auth/signup", json=payload)
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "email_taken"


def test_login_returns_token(client):
    client.post(
        "/api/auth/signup",
        json={"name": "Cara", "email": "cara@example.com", "password": "password123"},
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "cara@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert response.json()["access_token"]


def test_login_with_wrong_password_fails(client):
    client.post(
        "/api/auth/signup",
        json={"name": "Dan", "email": "dan@example.com", "password": "password123"},
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "dan@example.com", "password": "wrong-password"},
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "invalid_credentials"


def test_me_requires_authentication(client):
    response = client.get("/api/me")
    assert response.status_code == 401


def test_me_returns_profile(client):
    headers = signup_and_login(client, "Eve", "eve@example.com")
    response = client.get("/api/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "eve@example.com"
