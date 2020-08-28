"""
Рецептов мало, поэтому нет смысла использовать внешние базы данных
 вроде Redis или PostgreSQL.

sqlitedict позволяет работать с базой данных из нескольких потоков,
 но не дает повышенной производительности по сравнению с доступом
 из одного потока.
"""
import json

from aiohttp_cache import cache
from pathlib import Path
from time import time
from sqlitedict import SqliteDict

from data.config import FILE_PATH, DB_PATH
from log import log


def fill_db(file_path: Path = FILE_PATH, db_path: Path = DB_PATH):
    """
    Transfer data from text file to db.

    Schema:
    - recipes (list)
    -- name
    -- components (list)
    --- item
    --- q
    - components (dict)
    -- item : times_encountered

    :param file_path: path to file with data.
    :param db_path: path to database.
    """

    def get_recipes():
        with file_path.open() as f:
            return json.load(f)

    db_path.touch(exist_ok=True)

    with SqliteDict(db_path, autocommit=True) as db:
        # List of recipes
        db["recipes"] = []

        # Dict of components and an integer to count their encounters
        db["component_encounters"] = {}

        # List of component names to validate input
        db["component_list"] = []

        for recipe in get_recipes()["recipes"]:
            recipe["last_recommended"] = 0

            db["recipes"].append(recipe)

            for component in recipe["components"]:
                if component["item"] not in db["component_list"]:
                    db["component_list"].append(component["item"])
                    db["component_encounters"][component["item"]] = 0


@cache()
def select_component_list(db_path: Path = DB_PATH):
    """
    Return list of all possible components.

    :param db_path: path to database.
    :return: list of components.
    """
    with SqliteDict(db_path, flag="r") as db:
        return db["component_list"]


def select_recommended_recipes(cutoff_point: int, db_path: Path = DB_PATH):
    """
    Return recipes which has been recommended since cutoff_point.

    :param cutoff_point: time limit.
    :param db_path: path to database.
    :return: iterator of rows.
    """
    with SqliteDict(db_path, flag="r") as db:
        for recipe in db["recipes"]:
            last_recommended = recipe["last_recommended"]

            if last_recommended > cutoff_point:
                yield recipe["name"]


@cache()
def select_recipes_by_components(components: list, db_path: Path = DB_PATH):
    """
    Return all recipes containing only components on the components list.
    Also, update component_encounters values.

    :param components: list of components.
    :param db_path: path to database.
    :return: iterator of recipes.
    """
    with SqliteDict(db_path, autocommit=True) as db:
        for component in components:
            db["component_encounters"][component] += 1

        for recipe in db["recipes"]:
            recipe_components = [c["item"] for c in recipe["components"]]

            if set(recipe_components).issubset(set(components)):
                recipe["last_recommended"] = time()

                yield recipe


def select_component_encounters(db_path: Path = DB_PATH):
    """
    Return dict of component encounters.

    :param db_path: path to database.
    :return: dict of component encounters.
    """
    with SqliteDict(db_path, flag="r") as db:
        return db["component_encounters"]
