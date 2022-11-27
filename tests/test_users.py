from app import schema
import pytest


def test_create_user(client):
    res = client.post(
        "/users/",
        json={
            "first_name": "John",
            "last_name": "sam",
            "email": "test@example.com",
            "password": "12345",
            "phone_number": "123"
        }
    )
    new_user = schema.User(**res.json())
    assert new_user.email == "test@example.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/users/login",
        data={
            "username": "test@example.com",
            "password": "12345",
        }
    )
    token = schema.Token(**res.json())
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@test.com", "12345", 403),
        ("test@example.com", "wrongpassword", 403)
    ]
)
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/users/login",
        data={
            "username": email,
            "password": password,
        }
    )
    assert res.status_code == 403
    assert res.json().get("detail") == "invalid credentials"