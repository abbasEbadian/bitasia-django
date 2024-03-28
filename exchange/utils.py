from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    print(response, exc, context)

    # Now add the HTTP status code to the response.
    d = {"result": "error", "error": {}}
    if response is not None:
        if response.status_code in [401, 403, 404]:
            return response
        print(isinstance(exc.detail, dict))
        if isinstance(exc.detail, dict):
            print(exc.detail)
            for key, value in exc.detail.items():
                if key == "API_ERROR":
                    q = {**value}
                    if "description_en" in q:
                        del q["description_en"]
                    d["error"] = q

    return Response(d, status=400)
