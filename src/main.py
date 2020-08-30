import logging

from aiohttp import web

from src.handlers import routes
from src.db import fill_db
from src.log import logger
from data.config import OVERALL_LOG_LEVEL


async def db_init(app):
    """
    If db doesn't exist, create it and transfer data from file.
    """
    if fill_db():
        logger.debug("Database created.")
    else:
        logger.debug("Database already exists.")


def start_server(host: str = "0.0.0.0", port: int = 8080):
    """
    Start aiohttp server.

    :param host: address of the server.
    :param port: port of the server.
    """
    app = web.Application()

    for route in routes:
        logger.debug("Adding route: {}.".format(route))

    app.add_routes(routes)

    app.on_startup.append(db_init)

    logger.info("Starting server on {}:{}.".format(host, port))
    web.run_app(app, host=host, port=port)


def main():
    """
    Set logging level and launch server.
    """
    logging.basicConfig(level=OVERALL_LOG_LEVEL)

    start_server()


if __name__ == "__main__":
    main()
