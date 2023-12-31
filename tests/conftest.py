# configure test, to share multiple test files
import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from backend.database import engine

os.getenv["ENV_STATE"] = "test"

from backend.main import app  # noqa: E402


# run once for the entire test session
# when we have an async function in FastApi, we need some sort of
# async platform that it runs on. This is for the async tests
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    # yield allows to execute some code before and after the test
    yield TestClient(app)


# clean all tables before run the test
@pytest.fixture(autouse=True)  # -> runs in every test
async def db() -> AsyncGenerator:
    engine.connect()
    yield
    engine.dispose()


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac
