import pytest
import asyncio

from aiohttp import web

from src.handlers import routes
from src.db import db_fill, db_remove


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()

    yield loop

    loop.close()


@pytest.fixture(autouse=True)
def init_db():
    db_fill(force_recreate=True)

    yield

    db_remove()


@pytest.fixture()
def get_app():
    app = web.Application()
    app.add_routes(routes)

    return app
