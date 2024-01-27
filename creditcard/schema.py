from django.utils.translation import gettext as _
from drf_yasg import openapi

creditcard_create_schema = {
    "operation_id": _("Create credit card"),
    "security": [{"Token": []}],
    "request_body": openapi.Schema(type=openapi.TYPE_OBJECT, required=["card_number", 'iban'],
                                   properties={
                                       "card_number": openapi.Schema(type=openapi.TYPE_STRING, title='Card number',
                                                                     description="16 digits"),
                                       "iban": openapi.Schema(type=openapi.TYPE_STRING,
                                                              title="IBAN",
                                                              description="IR + 24 digits", ),
                                   }),
    "responses": {
        "200": openapi.Response(
            description="Created",
            examples={
                "application/json": {
                    "result": "success",
                }
            },
        ),
        "400": openapi.Response(
            description="Error",
            examples={
                "application/json": {
                    "result": "error",
                    "error": {
                        "status_code": 400,
                        "message": "message",
                        "description": "desc"
                    }
                }
            },
        )
    }
}
