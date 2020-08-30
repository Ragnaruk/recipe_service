from aiohttp import web

from src.recipes import (
    proceed_payload,
    get_recipes_from_components,
    get_last_recommended_recipes,
    get_most_popular_components,
)
from src.exceptions import JSONValidationError
from src.log import logger


routes = web.RouteTableDef()


@routes.get("/")
async def handler_index(request: web.Request):
    page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Recipe Service</title>
    </head>
    <body>
        <p><a href="/recipes/possible">POST /recipes/possible</a>
        <p><a href="/recipes/last">GET /recipes/last</a>
        <p><a href="/components/popular">GET /components/popular</a>
    </body>
    </html>
    """

    return web.Response(text=page, content_type="text/html")


@routes.post("/recipes/possible")
async def handler_recipes(request: web.Request):
    """
    Receives json with components and returns json with possible recipes.

    :param request: web.Request of aiohttp module.
    :return: web.json_response.
    """
    logger.debug("Requesting possible recipes from ingredient list.")

    payload = await request.text()

    try:
        fridge_components = await proceed_payload(payload)
        logger.debug("Received payload: {}".format(fridge_components))
    except JSONValidationError:
        return web.json_response({"error": "Incorrect JSON object."})
    else:
        possible_recipes = await get_recipes_from_components(fridge_components)
        logger.debug("Possible recipes: {}".format(possible_recipes))

        return web.json_response(possible_recipes)


@routes.get("/recipes/last")
async def handler_last_recommended_recipes(request: web.Request):
    """
    Returns recipes recommended in the last hour.

    :param request: web.Request of aiohttp module.
    :return: web.json_response.
    """
    logger.debug("Requesting last recommended recipes.")

    recommended_recipes = await get_last_recommended_recipes()
    logger.debug("Recommended recipes: {}".format(recommended_recipes))

    return web.json_response(recommended_recipes)


@routes.get("/components/popular")
async def handler_popular_components(request: web.Request):
    """
    Returns 10 most popular components in users' fridges.

    :param request: web.Request of aiohttp module.
    :return: web.json_response.
    """
    logger.debug("Requesting most popular components.")

    most_popular_components = await get_most_popular_components()
    logger.debug("Most popular components: {}".format(most_popular_components))

    return web.json_response(most_popular_components)
