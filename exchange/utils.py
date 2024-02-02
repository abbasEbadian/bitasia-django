from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    d = {"result": "error", "error": {}}
    if response is not None:
        if isinstance(exc, Http404):
            return response
        if isinstance(exc.detail, dict):
            for key, value in exc.detail.items():
                if key == "API_ERROR":
                    q = {**value}
                    if "description_en" in q:
                        del q["description_en"]
                    d["error"] = q
    return JsonResponse(d, status=d["error"].get('status_code', status.HTTP_400_BAD_REQUEST))
