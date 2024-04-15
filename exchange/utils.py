from django.utils.translation import gettext as _
from rest_framework import status as drf_status

from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    print(f"{response=}\n{exc}\n{context=}")

    d = {"result": "error", "error": {}}
    status = drf_status.HTTP_400_BAD_REQUEST
    if response is not None:
        if response.status_code in [401, 403, 404]:
            return response
        if isinstance(exc.detail, dict):
            for key, value in exc.detail.items():
                if key == "API_ERROR":
                    q = {**value}
                    if "description_en" in q:
                        del q["description_en"]
                    d["error"] = q
                else:
                    value = isinstance(value, list) and value[0] or value
                    print(value)
                    d["error"]["status_code"] = 400
                    d["error"]["message"] = f"{key}: {value}"
        print(f"{exc=} {exc.detail}")
    else:
        status = drf_status.HTTP_500_INTERNAL_SERVER_ERROR
        d["error"] = {
            "status_code": 500,
            "message": _("Something went wrong in server. Contact admin."),
            "description": repr(exc)
        }
    return Response(d, status=status)
