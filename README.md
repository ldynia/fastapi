# FastAPI Template

FastAPI startup template.

## Tutorials

- [FastAPI with Async SQLAlchemy, SQLModel, and Alembic](https://testdriven.io/blog/fastapi-sqlmodel/)
- [Using SQLModel Asynchronously with FastAPI](https://daniel.feldroy.com/posts/til-2025-08-using-sqlmodel-asynchronously-with-fastapi-and-air-with-postgresql)
  - [Github](https://github.com/pydanny/daniel.feldroy.com/blob/6a1c7e06c3d17dbb99b2a22d3f166c98c595db80/posts/til/til-2025-08-using-sqlmodel-asynchronously-with-fastapi-and-air-with-postgresql.md?plain=1#L69)
- [Building a RESTful API with FastAPI and PostgreSQL](https://www.sqlservercentral.com/articles/building-a-restful-api-with-fastapi-and-postgresql)
- [BugBytes](https://www.youtube.com/watch?v=O-tYPuj-p1c)
  - [BugBytes Alembic](https://www.youtube.com/watch?v=zTSmvUVbk8M)
  - [BugBytes AsynchSQL](https://www.youtube.com/watch?v=T0JXFhJ7pM0&t=640s)
  - [UV](https://www.youtube.com/watch?v=k0F9YaAbNwo)

## Setup

```
docker compose build --build-arg UID=$(id -u) --build-arg GID=$(id -g)
docker compose up --wait
```

## Migrations

```
docker compose exec app uv run alembic revision --autogenerate -m "Initial migration"
docker compose exec app uv run alembic upgrade head
docker compose exec app uv run alembic downgrade -1
```

## Endpoints

| Protocol | Method |   Endpoint   |         Description            |
|----------|--------|--------------|--------------------------------|
|   HTTP   |  GET   | /            | Root                           |
|   HTTP   |  GET   | /docs        | Open API documentation         |
|   HTTP   |  GET   | /syncdb      | Sync database                  |
|   HTTP   |  GET   | /asyncdb     | Async database                 |
|   HTTP   |  GET   | /sse/stream  | Server-sent events (streaming) |
|   WS     |  GET   | /ws/echo     | WebSocket                      |

## Tests

```
docker compose exec app uv run pytest -sv tests/
docker compose exec app uv run pytest -sv --cov=main tests/
docker compose exec app uv run pytest -sv --cov=main --cov-report=html tests/
```

## Dependency management

```
docker compose exec app uv sync
docker compose exec app uv tree
```
