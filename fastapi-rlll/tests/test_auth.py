from httpx import AsyncClient


async def test_register_success(client: AsyncClient):
    response = await client.post(
        "/api/user/register", json={"username": "alice", "password": "supersecret"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
    assert "id" in data


async def test_register_duplicate_username(client: AsyncClient):
    payload = {"username": "bob", "password": "supersecret"}
    await client.post("/api/user/register", json=payload)
    response = await client.post("/api/user/register", json=payload)
    assert response.status_code == 400


async def test_login_success(client: AsyncClient):
    await client.post(
        "/api/user/register", json={"username": "carol", "password": "supersecret"}
    )
    response = await client.post(
        "/api/user/login", data={"username": "carol", "password": "supersecret"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


async def test_login_wrong_password(client: AsyncClient):
    await client.post(
        "/api/user/register", json={"username": "dave", "password": "supersecret"}
    )
    response = await client.post(
        "/api/user/login", data={"username": "dave", "password": "wrongpassword"}
    )
    assert response.status_code == 401
