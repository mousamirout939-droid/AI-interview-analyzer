"""
test_auth.py
==============
Covers registration, login, logout, and basic access-control behavior.
"""


def register(client, email="jane@example.com", password="Password1"):
    return client.post("/auth/register", data={
        "full_name": "Jane Doe",
        "email": email,
        "password": password,
        "confirm_password": password,
    }, follow_redirects=True)


def test_register_creates_user(client, db):
    response = register(client)
    assert response.status_code == 200

    from APP.database import User
    user = User.query.filter_by(email="jane@example.com").first()
    assert user is not None
    assert user.check_password("Password1")


def test_register_rejects_mismatched_passwords(client, db):
    response = client.post("/auth/register", data={
        "full_name": "Jane Doe",
        "email": "jane2@example.com",
        "password": "Password1",
        "confirm_password": "Different1",
    }, follow_redirects=True)
    assert b"Passwords do not match" in response.data


def test_login_and_logout(client, db):
    register(client, email="login@example.com")
    client.get("/auth/logout", follow_redirects=True)

    response = client.post("/auth/login", data={
        "email": "login@example.com",
        "password": "Password1",
    }, follow_redirects=True)
    assert response.status_code == 200

    logout_response = client.get("/auth/logout", follow_redirects=True)
    assert logout_response.status_code == 200


def test_dashboard_requires_login(client, db):
    response = client.get("/dashboard/", follow_redirects=True)
    assert b"Log In" in response.data or b"Log in" in response.data
