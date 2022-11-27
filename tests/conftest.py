from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
import pytest
from app import utils
from app import oauth2
from app import models
from .database import engine, TestingSessionLocal


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(session):
    user_data = {
        "first_name": "John",
        "last_name": "sam",
        "email": "test@example.com",
        "password": "12345",
        "phone_number": "123"
    }
    hash_password = utils.hash_password(user_data.get("password"))
    user_data["password"] = hash_password
    new_user = models.User(**user_data)
    session.add(new_user)
    session.commit()
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {
        "first_name": "John",
        "last_name": "sam",
        "email": "test@test.com",
        "password": "12345",
        "phone_number": "45555"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    return res.json()


@pytest.fixture
def token(test_user):
    token = oauth2.create_access_token(data={"user_id": test_user.id})
    return token


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, session):
    post_data = [
        {
            "title": "first post",
            "content": "first content",
            "owner_id": test_user.id,
        },
        {
            "title": "second post",
            "content": "second content",
            "owner_id": test_user.id,
        },
        {
            "title": "third post",
            "content": "third content",
            "owner_id": test_user.id,
        }
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, post_data)
    session.add_all(list(post_map))
    session.commit()
    posts = session.query(models.Post).all()

    return posts
