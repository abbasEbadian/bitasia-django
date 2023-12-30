from django.http import Http404
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        if isinstance(exc, Http404):
            return response
        response.data = {"result": "error"}
        print(type(exc.detail))
        print(exc.detail)
        if isinstance(exc.detail, dict):
            for key, value in exc.detail.items():
                if key == "API_ERROR":
                    q = {**value}
                    del q["description_en"]
                    response.data["error"] = q

    return response
