from django.utils.translation import gettext as _
from drf_yasg import openapi

common_responses = {
    "403": openapi.Response(
        description="Permission Denied",
    ),
    "401": openapi.Response(
        description="Unauthorized",
    ),
    "500": openapi.Response(
        description="SERVER ERROR - contact to admin",
    ),
}

list_user_schema = {
    "operation_id": "List of users",
    'operation_description': "Admin can get list of users",
}
create_user_schema = {
    'operation_id': "Create new user",
    'operation_description': "Admin can create new users.",
    'security': [{"Token": []}],
    'responses': {
        "201": openapi.Response(
            description="Created Successfully",
        ),
        "400": openapi.Response(
            description="Invalid data",
            examples={
                "application/json": {
                    "result": "error",
                    "message": _("Invalid Mobile")
                }
            },
        ),
        **common_responses
    }
}
