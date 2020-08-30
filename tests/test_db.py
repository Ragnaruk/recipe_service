import json

from data.config import FILE_PATH
from src.db import db_fill, get_query_results, execute_query


async def test_db_fill():
    """
    Test db recreation.
    """
    recipes_before = await get_query_results("SELECT * FROM recipes")

    new_recipe_name = "test_recipe"
    new_recipe_components = [{"item": "мясо", "q": 1000}]

    await execute_query(
        "INSERT INTO recipes (recipe_name, components) VALUES (?,?)",
        (new_recipe_name, json.dumps(new_recipe_components)),
    )

    recipes_middle = await get_query_results("SELECT * FROM recipes")

    db_fill(force_recreate=True)

    recipes_after = await get_query_results("SELECT * FROM recipes")

    assert recipes_before != recipes_middle
    assert recipes_before == recipes_after


async def test_get_query_results():
    """
    Test db creation, insertion, and selection of data.
    """
    recipes = await get_query_results("SELECT * FROM recipes")

    with FILE_PATH.open(encoding="UTF-8") as f:
        original_recipes = json.load(f)["recipes"]

    formatted_recipes = []
    for recipe in original_recipes:
        formatted_recipes.append(
            (recipe["name"], json.dumps(recipe["components"], ensure_ascii=False), 0)
        )

    assert recipes == formatted_recipes


async def test_execute_query():
    """
    Test insert query execution.
    """
    recipes_before = await get_query_results("SELECT * FROM recipes")

    new_recipe_name = "test_recipe"
    new_recipe_components = [{"item": "мясо", "q": 1000}]

    await execute_query(
        "INSERT INTO recipes (recipe_name, components) VALUES (?,?)",
        (new_recipe_name, json.dumps(new_recipe_components)),
    )

    recipes_after = await get_query_results("SELECT * FROM recipes")

    recipes_before.append((new_recipe_name, json.dumps(new_recipe_components), 0))

    assert recipes_before == recipes_after
