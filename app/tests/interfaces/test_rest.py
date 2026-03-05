def test_livez_endpoint(client):
    response = client.get("/livez")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readyz_endpoint(client):
    response = client.get("/readyz")

    assert response.status_code == 200
    assert "ready" in response.json()["database"]
    assert "ready" in response.json()["cache"]


def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Hello": "FastAPI"}


def test_docs_endpoint(client):
    response = client.get("/docs")

    assert response.status_code == 200
    assert "Swagger UI" in response.text
    assert response.headers["content-type"].startswith("text/html")


def test_syncdb_endpoint(client):
    response = client.get("/syncdb")

    assert response.status_code == 200
    assert response.json() == {"Hello": "Sync DB"}


def test_asyncdb_endpoint(client):
    response = client.get("/asyncdb")
    assert response.status_code == 200
    assert response.json() == {"Hello": "Async DB"}
