import json

from exceptions import JSONValidationError
from db import select_component_list


async def proceed_payload(payload: str):
    """
    Receive a string payload and return a json or an JSONValidationError exception.
    Payload should be a valid JSON and a dictionary.

    :param payload: stringified json.
    :return: payload json.
    """
    try:
        data = json.loads(payload)

        assert isinstance(data, dict)

        component_list = await select_component_list()
        for key in data:
            assert key in component_list
    except json.JSONDecodeError:
        raise JSONValidationError
    except AssertionError:
        raise JSONValidationError

    return data
