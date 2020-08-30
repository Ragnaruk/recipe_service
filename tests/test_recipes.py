import pytest
import json

from src.recipes import (
    process_payload,
    get_recipes_from_components,
    get_most_popular_components,
    get_last_recommended_recipes,
)
from src.exceptions import JSONValidationError


async def test_proceed_payload_correct():
    payload = {
        "мясо": 200,
        "огурец": 1,
    }

    processed_payload = await process_payload(json.dumps(payload))

    assert payload == processed_payload


async def test_proceed_payload_invalid_component():
    payload = {
        "мясо": 200,
        "огурец": 1,
        "test": 1,
    }

    with pytest.raises(JSONValidationError):
        await process_payload(json.dumps(payload))


async def test_proceed_payload_invalid_format_not_dict():
    payload = [("мясо", 200), ("огурец", 1)]

    with pytest.raises(JSONValidationError):
        await process_payload(json.dumps(payload))


async def test_proceed_payload_invalid_format_not_int():
    payload = {
        "мясо": "1",
    }

    with pytest.raises(JSONValidationError):
        await process_payload(json.dumps(payload))


async def test_get_recipes_from_components_possible():
    fridge_components = {
        "мясо": 200,
        "огурец": 1,
        "картофель": 10,
    }

    expected_result = [
        {"name": "Салат «Русский»", "quantity": 0.5},
        {"name": "Салат «Ленинградский»", "quantity": 0.4},
    ]
    result = await get_recipes_from_components(fridge_components)

    assert expected_result == result


async def test_get_recipes_from_components_not_possible():
    fridge_components = {
        "мясо": 10000,
    }

    expected_result = []
    result = await get_recipes_from_components(fridge_components)

    assert expected_result == result


async def test_get_most_popular_components_none():
    expected_result = {
        "most_popular_components": [
            {"яйцо": 0},
            {"рыба": 0},
            {"огурец": 0},
            {"мясо": 0},
            {"картофель": 0},
        ]
    }
    result = await get_most_popular_components()

    assert expected_result == result


async def test_get_most_popular_components_some():
    fridge_components = {
        "мясо": 200,
        "огурец": 1,
        "картофель": 10,
    }

    await get_recipes_from_components(fridge_components)

    expected_result = {
        "most_popular_components": [
            {"огурец": 1},
            {"мясо": 1},
            {"картофель": 1},
            {"яйцо": 0},
            {"рыба": 0},
        ]
    }
    result = await get_most_popular_components()

    assert expected_result == result


async def test_get_last_recommended_recipes_none():
    expected_result = {"last_recommended_recipes": []}
    result = await get_last_recommended_recipes()

    assert expected_result == result


async def test_get_last_recommended_recipes_some():
    fridge_components = {
        "мясо": 200,
        "огурец": 1,
        "картофель": 10,
    }

    await get_recipes_from_components(fridge_components)

    expected_result = {
        "last_recommended_recipes": ["Салат «Ленинградский»", "Салат «Русский»"]
    }
    result = await get_last_recommended_recipes()

    assert expected_result == result
