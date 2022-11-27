import pytest
from app import schema


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts")

    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)


def test_unauthorized_user_posts(client, test_posts):
    res = client.get("/posts")
    assert res.status_code == 401


def test_unauthorized_user_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/900")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schema.PostVote(**res.json())
    assert res.status_code == 200

@pytest.mark.parametrize(
    "title, content, published",
    [
        ("awesome new title", "awesome new content", True),
        ("awesome old title", "awesome old content", False),
        ("awesome fine title", "awesome fine content", True)
    ]
)
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post(
        "/posts/",
        json={"title": title, "content": content, "published": published}
    )
    created_post = schema.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title


def test_unauthorized_user_create_posts(client, test_posts):
    res = client.post(
        "/posts/",
        json={"title": "title", "content": "content"}
    )
    assert res.status_code == 401


def test_unauthorized_user_delete_posts(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_non_exist_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{len(test_posts) + 1}")
    assert res.status_code == 404


def test_update_posts(authorized_client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.patch(
        f"/posts/{test_posts[0].id}", json=data
    )
    updated_post = schema.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data.get("title")


def test_unauthorized_user_update_posts(client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = client.patch(
        f"/posts/{test_posts[0].id}", json=data
    )
    assert res.status_code == 401


def test_delete_post_not_exist(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{len(test_posts)+1}")
    assert res.status_code == 404
