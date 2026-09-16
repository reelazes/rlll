from httpx import AsyncClient


async def register_and_login(client: AsyncClient, username: str) -> str:
    await client.post(
        "/api/user/register", json={"username": username, "password": "supersecret"}
    )
    response = await client.post(
        "/api/user/login", data={"username": username, "password": "supersecret"}
    )
    return response.json()["access_token"]


async def test_create_post_requires_auth(client: AsyncClient):
    response = await client.post("/api/posts/", json={"title": "t", "content": "c"})
    assert response.status_code == 401


async def test_create_and_get_post(client: AsyncClient):
    token = await register_and_login(client, "author1")
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = await client.post(
        "/api/posts/", json={"title": "Hello", "content": "World"}, headers=headers
    )
    assert create_resp.status_code == 201
    post = create_resp.json()
    assert post["title"] == "Hello"

    get_resp = await client.get(f"/api/posts/{post['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == post["id"]


async def test_cannot_delete_others_post(client: AsyncClient):
    token1 = await register_and_login(client, "owner")
    token2 = await register_and_login(client, "intruder")

    create_resp = await client.post(
        "/api/posts/",
        json={"title": "Mine", "content": "Body"},
        headers={"Authorization": f"Bearer {token1}"},
    )
    post_id = create_resp.json()["id"]

    delete_resp = await client.delete(
        f"/api/posts/{post_id}", headers={"Authorization": f"Bearer {token2}"}
    )
    assert delete_resp.status_code == 403


async def test_owner_can_delete_post(client: AsyncClient):
    token = await register_and_login(client, "self_owner")
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = await client.post(
        "/api/posts/", json={"title": "Bye", "content": "Body"}, headers=headers
    )
    post_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/api/posts/{post_id}", headers=headers)
    assert delete_resp.status_code == 204


async def test_update_post(client: AsyncClient):
    token = await register_and_login(client, "editor")
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = await client.post(
        "/api/posts/", json={"title": "Old", "content": "Body"}, headers=headers
    )
    post_id = create_resp.json()["id"]

    update_resp = await client.patch(
        f"/api/posts/{post_id}", json={"title": "New"}, headers=headers
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "New"
    assert update_resp.json()["content"] == "Body"


async def test_pagination(client: AsyncClient):
    token = await register_and_login(client, "paginator")
    headers = {"Authorization": f"Bearer {token}"}
    for i in range(3):
        await client.post(
            "/api/posts/", json={"title": f"Post {i}", "content": "x"}, headers=headers
        )

    response = await client.get("/api/posts/?limit=2&offset=0")
    assert response.status_code == 200
    assert len(response.json()) == 2
