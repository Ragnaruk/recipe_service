import json

from aiohttp import web


class JSONValidationError(web.HTTPError):
    def __init__(self, message="Invalid JSON payload.", status_code=400, **kwargs):
        self.status_code = status_code

        msg = {"error": message}

        if kwargs:
            msg["error_details"] = kwargs

        self.text = json.dumps(msg)
        self.content_type = "application/json"
