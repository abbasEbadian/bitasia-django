from http import HTTPStatus

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    d = {"result": "error", "error": {}}
    if response is not None:
        if response.status_code in [401, 403, 404]:
            return response
        if isinstance(exc.detail, dict):
            print(exc.detail)
            for key, value in exc.detail.items():
                if key == "API_ERROR":
                    q = {**value}
                    if "description_en" in q:
                        del q["description_en"]
                    d["error"] = q

    return Response(d, status=200)


class JSONErrorMiddleware:
    """Without this middleware, APIs would respond with
    html/text whenever there's an error."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.status_code_description = {
            v.value: v.description for v in HTTPStatus
        }

    def __call__(self, request):
        response = self.get_response(request)
        # If the content_type isn't 'application/json', do nothing.
        if not request.content_type == "application/json":
            return response

        status_code = response.status_code
        if (
                not HTTPStatus.BAD_REQUEST
                    < status_code
                    <= HTTPStatus.INTERNAL_SERVER_ERROR
        ):
            return response

        # Return a JSON error response if any of 403, 404, or 500 occurs.
        r = JsonResponse(
            {
                "error": {
                    "status_code": status_code,
                    "message": self.status_code_description[status_code],
                    "detail": {"url": request.get_full_path()},
                }
            },
        )
        r.status_code = response.status_code
        return r
