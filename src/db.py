"""
Рецептов мало, поэтому нет смысла использовать внешние базы данных
 вроде Redis или PostgreSQL.

https://github.com/omnilib/aiosqlite
"""
import aiosqlite
import sqlite3
import json

from pathlib import Path

from data.config import DB_PATH, FILE_PATH


async def get_db(db_path: Path = DB_PATH) -> aiosqlite.Connection:
    """
    Get aiosqlite connection proxy.

    :param db_path: path to database.
    :return: aiosqlite connection proxy.
    """
    return aiosqlite.connect(db_path)


async def execute_query(query: str, parameters: tuple = (), db_path: Path = DB_PATH):
    """
    Execute and commit query.

    :param query: query to execute.
    :param parameters: parameters to insert into query.
    :param db_path: path to database.
    :return: query results.
    """
    async with await get_db(db_path) as db:
        await db.execute(query, parameters)
        await db.commit()


async def get_query_results(
    query: str, parameters: tuple = (), db_path: Path = DB_PATH
) -> list:
    """
    Execute query and return results.

    :param query: query to execute.
    :param parameters: parameters to insert into query.
    :param db_path: path to database.
    :return: query results.
    """
    async with await get_db(db_path) as db:
        async with await db.execute(query, parameters) as cursor:
            return await cursor.fetchall()


def fill_db(file_path: Path = FILE_PATH, db_path: Path = DB_PATH) -> bool:
    """
    Create a database and transfer data from text file to it.
    Does nothing if db already exists.

    :param file_path: path to file with data.
    :param db_path: path to database.
    :return: True if db was created, False if it already exists.
    """

    def get_recipes():
        with file_path.open(encoding="UTF-8") as f:
            return json.load(f)["recipes"]

    if db_path.is_file():
        return False

    db_path.touch()

    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS recipes "
            "(recipe_name TEXT PRIMARY KEY,"  # name of the recipe
            " components TEXT NOT NULL,"  # json of ingredients
            " last_recommended INTEGER DEFAULT 0)"  # unix time of the last usage in recommendation
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS components "
            "(component TEXT PRIMARY KEY,"  # name of ingredient
            " total_encountered)"  # number of times it appeared in fridges
        )

        unique_components = set()
        for recipe in get_recipes():
            for component in recipe["components"]:
                unique_components.add(component["item"])

            cursor.execute(
                "INSERT INTO recipes (recipe_name, components) VALUES (?,?)",
                (recipe["name"], json.dumps(recipe["components"], ensure_ascii=False)),
            )

        for component in unique_components:
            cursor.execute(
                "INSERT INTO components (component, total_encountered) VALUES (?,?)",
                (component, 0),
            )

        db.commit()

    return True


if __name__ == "__main__":
    fill_db()
