def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_docs_endpoint(client):
    response = client.get("/docs")

    assert response.status_code == 200
    assert "Swagger UI" in response.text
    assert response.headers["content-type"].startswith("text/html")


def test_syncdb_endpoint(client):
    response = client.get("/syncdb")

    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_asyncdb_endpoint(client):
    response = client.get("/asyncdb")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
