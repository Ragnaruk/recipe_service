import logging

from aiohttp import web
from aiohttp_cache import setup_cache

from data.config import LOGGING_LEVEL
from handlers import routes
from db import fill_db


def main(logging_level: logging = LOGGING_LEVEL):
    logging.basicConfig(level=logging_level)

    # Transfer data from file to db
    fill_db()

    app = web.Application()

    setup_cache(app)
    app.add_routes(routes)

    web.run_app(app, port=8888)


if __name__ == "__main__":
    main()
