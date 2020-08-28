from aiohttp import web

from utils import proceed_payload
from recipes import (
    get_recipes_from_components,
    get_last_recommended_recipes,
    get_most_popular_components,
)
from log import log

routes = web.RouteTableDef()


@routes.post("/recipes/possible")
async def handler_recipes(request: web.Request):
    """
    Receives json with components and returns json with possible recipes.

    :param request: web.Request of aiohttp module.
    :return: web.json_response.
    """
    payload = await request.text()
    fridge_components = await proceed_payload(payload)
    possible_recipes = await get_recipes_from_components(fridge_components)

    return web.json_response(possible_recipes)


@routes.get("/recipes/last_requested")
async def handler_last_recommended_recipes(request: web.Request):
    """
    Returns recipes recommended in the last hour.

    :param request: web.Request of aiohttp module.
    :return: web.json_response.
    """
    recommended_recipes = await get_last_recommended_recipes()

    return web.json_response(recommended_recipes)


@routes.get("/components/popular")
async def handler_popular_components(request: web.Request):
    """
    Returns 10 most popular components in users' fridges.

    :param request: web.Request of aiohttp module.
    :return: web.json_response.
    """
    most_popular_components = await get_most_popular_components()

    return web.json_response(most_popular_components)
