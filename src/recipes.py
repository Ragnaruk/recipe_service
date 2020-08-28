from time import time

from db import (
    select_recipes_by_components,
    select_recommended_recipes,
    select_component_encounters,
)
from log import log


async def get_recipes_from_components(fridge_components: dict):
    """
    Return possible recipes and the quantity that can be cooked from components list.

    :param fridge_components: dict of components and their quantity.
    :return: list of recipes.
    """
    components = sorted(list(fridge_components.keys()))

    possible_recipes = []
    for recipe in select_recipes_by_components(components):
        minimum_quantity = 0
        for component in recipe["components"]:
            needed_quantity = component["q"]
            available_quantity = fridge_components[component["item"]]

            minimum_quantity = min(
                minimum_quantity, available_quantity / needed_quantity
            )

        possible_recipes.append({"name": recipe["name"], "quantity": minimum_quantity})

    return possible_recipes


async def get_last_recommended_recipes(time_period: int = 3600):
    """
    Return recipes which have been recommended in the last time_period

    :param time_period: seconds from current time.
    :param db_path: path to database.
    :return:
    """
    current_time = int(time())
    cutoff_point = current_time - time_period

    recommended_recipes = []
    for recipe_name in select_recommended_recipes(cutoff_point):
        recommended_recipes.append(recipe_name)

    return {"last_recommended_recipes": recommended_recipes}


async def get_most_popular_components(number_of_products: int = 10):
    """
    Return number_of_products most popular products in users' fridges.

    :param number_of_products: number of products to return.
    :return: list of products.
    """
    component_encounters = select_component_encounters()
    components = [(k, v) for (k, v) in component_encounters.items()]
    components.sort(key=lambda x: x[1])

    popular_components = [x[0] for x in components[0:10]]

    return {"most_popular_components": popular_components}
