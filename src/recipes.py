import json

from time import time

from src.exceptions import JSONValidationError
from src.db import get_query_results, execute_query
from src.log import logger


async def proceed_payload(payload: str):
    """
    Receive a string payload and return a json or an JSONValidationError exception.
    Payload should be a valid JSON and a dictionary.

    :param payload: stringified json.
    :return: payload json.
    """
    try:
        data = json.loads(payload)

        # Check correct data format
        assert isinstance(data, dict)

        # Check that ingredients are in db
        components = await get_query_results("SELECT component FROM components")
        components_list = [x[0] for x in components]

        for key in data:
            assert key in components_list
    except json.JSONDecodeError:
        raise JSONValidationError
    except AssertionError:
        raise JSONValidationError

    return data


async def get_recipes_from_components(fridge_components: dict):
    """
    Return possible recipes and the quantity that can be cooked from components list.

    :param fridge_components: dict of components and their quantity.
    :return: list of recipes.
    """
    available_components = set(fridge_components.keys())

    # Updated counters of users' components
    for component in available_components:
        await execute_query(
            "UPDATE components SET total_encountered = 1 + "
            "(SELECT total_encountered FROM components WHERE component = ?) "
            "WHERE component = ?",
            component,
        )

    recipes = await get_query_results("SELECT recipe_name, components FROM recipes")

    # Select recipes that are possible to prepare with users' components
    selected_recipes = []
    for recipe in recipes:
        recipe_components = json.loads(recipe[1])
        recipe_components_names = set([x["item"] for x in recipe_components])

        # If user has all components of the recipe,
        # find minimum amount that can be prepared
        minimum_quantity = 0
        if recipe_components_names.issubset(available_components):
            for item, quantity in recipe_components:
                available_quantity = fridge_components[item]
                needed_quantity = quantity

                if minimum_quantity:
                    minimum_quantity = min(
                        minimum_quantity, available_quantity / needed_quantity
                    )
                else:
                    # First cycle
                    minimum_quantity = available_quantity / needed_quantity

        selected_recipes.append({"name": recipe[0], "quantity": minimum_quantity})

    selected_recipes_names = [x["name"] for x in selected_recipes]

    # Update last recommended time for recipes
    for recipe_name in selected_recipes_names:
        current_time = int(time())

        await execute_query(
            "UPDATE recipes SET last_recommended = ? WHERE recipe_name = ?",
            (current_time, recipe_name),
        )

    return selected_recipes


async def get_last_recommended_recipes(time_period: int = 3600):
    """
    Return recipes which have been recommended in the last time_period

    :param time_period: seconds from current time.
    :return:
    """
    recipes = await get_query_results(
        "SELECT recipe_name, last_recommended FROM recipes"
    )

    current_time = int(time())
    cutoff_point = current_time - time_period

    recommended_recipes = []
    for recipe_name, last_recommended in recipes:
        if last_recommended > cutoff_point:
            recommended_recipes.append(recipe_name)

    return {"last_recommended_recipes": recommended_recipes}


async def get_most_popular_components(number_of_products: int = 2):
    """
    Return number_of_products most popular products in users' fridges.

    :param number_of_products: number of products to return.
    :return: list of products.
    """
    components = await get_query_results("SELECT * FROM components")

    components.sort(key=lambda x: x[1], reverse=True)

    popular_components = [
        {name: count} for name, count in components[0:number_of_products]
    ]

    return {"most_popular_components": popular_components}
