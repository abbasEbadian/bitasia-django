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

forget_password_change_view_schema = {
    "operation_id": _("Forget password"),
    "tags": ["User - Forget password"],
    "method": "POST",
    "request_body": openapi.Schema(type=openapi.TYPE_OBJECT,
                                   required=["password_1", "password_2", "otp", "mobile"],
                                   properties={
                                       "password_1": openapi.Schema(type=openapi.TYPE_STRING),
                                       "password_2": openapi.Schema(type=openapi.TYPE_STRING),
                                       "mobile": openapi.Schema(type=openapi.TYPE_STRING),
                                       "otp": openapi.Schema(type=openapi.TYPE_STRING),
                                   })
}

reset_password_change_view_schema = {
    "operation_id": _("Reset password"),
    "tags": ["User - Reset password"],
    "method": "POST",
    "request_body": openapi.Schema(type=openapi.TYPE_OBJECT,
                                   required=["password_1", "password_2", "otp"],
                                   properties={
                                       "password_1": openapi.Schema(type=openapi.TYPE_STRING),
                                       "password_2": openapi.Schema(type=openapi.TYPE_STRING),
                                       "otp": openapi.Schema(type=openapi.TYPE_STRING),
                                   })
}
