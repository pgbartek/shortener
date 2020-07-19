from fastapi.testclient import TestClient
import pytest

from shortener.app import app


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client
