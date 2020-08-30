import pytest
import json

from pathlib import Path

from data.config import FILE_PATH
from src.db import fill_db, get_query_results, execute_query


db_path = Path(__file__).parent / "test.db"


@pytest.fixture(scope="module", autouse=True)
async def init_db():
    fill_db(db_path=db_path)

    yield

    db_path.unlink()


@pytest.mark.asyncio()
async def test_get_query_results():
    """
    Test db creation, insertion, and selection of data.
    """
    recipes = await get_query_results("SELECT * FROM recipes", db_path=db_path)

    with FILE_PATH.open(encoding="UTF-8") as f:
        original_recipes = json.load(f)["recipes"]

    formatted_recipes = []
    for recipe in original_recipes:
        formatted_recipes.append(
            (recipe["name"], json.dumps(recipe["components"], ensure_ascii=False), 0)
        )

    assert recipes == formatted_recipes


@pytest.mark.asyncio()
async def test_execute_query():
    """
    Test insert query execution.
    """
    recipes_before = await get_query_results("SELECT * FROM recipes", db_path=db_path)

    new_recipe_name = "test_recipe"
    new_recipe_components = [{"item": "мясо", "q": 1000}]

    await execute_query(
        "INSERT INTO recipes (recipe_name, components) VALUES (?,?)",
        (new_recipe_name, json.dumps(new_recipe_components)),
        db_path=db_path,
    )

    recipes_after = await get_query_results("SELECT * FROM recipes", db_path=db_path)

    recipes_before.append((new_recipe_name, json.dumps(new_recipe_components), 0))

    assert recipes_before == recipes_after
