from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from typer.testing import CliRunner

from main import app


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def runner() -> CliRunner:
    return CliRunner()
