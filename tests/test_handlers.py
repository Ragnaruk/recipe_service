import json


async def test_handler_index(aiohttp_client, get_app):
    client = await aiohttp_client(get_app)

    response = await client.get("/")

    assert response.status == 200


async def test_handler_recipes_correct(aiohttp_client, get_app):
    client = await aiohttp_client(get_app)

    payload = json.dumps(
        {
            "мясо": 200,
            "огурец": 1,
            "картофель": 10,
        }
    )

    response = await client.post("/recipes/possible", data=payload)

    assert response.status == 200

    expected_result = json.dumps(
        [
            {"name": "Салат «Русский»", "quantity": 0.5},
            {"name": "Салат «Ленинградский»", "quantity": 0.4},
        ],
        ensure_ascii=False,
    )
    result = await response.text()

    assert expected_result == result


async def test_handler_recipes_invalid_decode(aiohttp_client, get_app):
    client = await aiohttp_client(get_app)

    payload = "Hello"

    response = await client.post("/recipes/possible", data=payload)

    assert response.status == 400

    expected_result = json.dumps({"error": "Failed to decode JSON."})
    result = await response.text()

    assert expected_result == result


async def test_handler_recipes_invalid_data(aiohttp_client, get_app):
    client = await aiohttp_client(get_app)

    payload = json.dumps(
        {
            "мясо": 200,
            "огурец": 1,
            "test": 1,
        }
    )

    response = await client.post("/recipes/possible", data=payload)

    assert response.status == 400

    expected_result = json.dumps({"error": "JSON contains invalid data."})
    result = await response.text()

    assert expected_result == result


async def test_handler_last_recommended_recipes(aiohttp_client, get_app):
    client = await aiohttp_client(get_app)

    response = await client.get("/recipes/last")

    assert response.status == 200

    expected_result = json.dumps({"last_recommended_recipes": []}, ensure_ascii=False)
    result = await response.text()

    assert expected_result == result


async def test_handler_popular_components(aiohttp_client, get_app):
    client = await aiohttp_client(get_app)

    response = await client.get("/components/popular")

    assert response.status == 200

    expected_result = json.dumps(
        {
            "most_popular_components": [
                {"яйцо": 0},
                {"рыба": 0},
                {"огурец": 0},
                {"мясо": 0},
                {"картофель": 0},
            ]
        },
        ensure_ascii=False,
    )
    result = await response.text()

    assert expected_result == result
