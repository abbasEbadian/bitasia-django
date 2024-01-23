from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.openapi import IN_FORM

from exchange.error_codes import ERROR_INVALID_GENDER

register_schema = {
    "operation_id": "Register",
    "security": [],
    "request_body": openapi.Schema(type=openapi.TYPE_OBJECT, required=["mobile", 'password', "first_name", "last_name"],
                                   properties={
                                       "mobile": openapi.Schema(type=openapi.TYPE_STRING),
                                       "password": openapi.Schema(type=openapi.TYPE_STRING),
                                       "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                                       "last_name": openapi.Schema(type=openapi.TYPE_STRING),
                                   }),
    "responses": {
        "201": openapi.Response(description=_("Created successfully"), ),
        "400": openapi.Response(description=_("Invalid data"), examples={
            "application/json": {
                "result": "error",
                "error": {
                    "status_code": 400,
                    "message": _("Invalid last name"),
                    "description": _("Last name must be at least 6 characters."),
                }
            }
        }),
        "409": openapi.Response(description=_("This mobile already exists"), examples={
            "application/json": {
                "result": "error",
                "error": {
                    "status_code": 409,
                    "message": _("Mobile already exists."),
                    "description": _("There is an account registered with this mobile."),
                }
            }
        }),
        "500": openapi.Response(description="Server error, CONTACT ADMIN")
    }
}

create_otp_schema_dict = {
    "security": [],
    "operation_id": "Login",
    "request_body": openapi.Schema(type=openapi.TYPE_OBJECT, required=["mobile", 'password'],
                                   properties={
                                       "mobile": openapi.Schema(type=openapi.TYPE_STRING, title='Mobile number',
                                                                description="11 digits"),
                                       "password": openapi.Schema(type=openapi.TYPE_STRING, title='User password'),
                                   }),
    "responses": {
        "201": openapi.Response(description=_("OTP Created successfully")),
        "400": openapi.Response(
            description="Error",
            examples={
                "application/json": {
                    "result": "error",
                    "error": {
                        "status_code": 400,
                        "message": _("Empty password."),
                        "description": _("Password can not be empty."),
                    }
                }
            },
        ),
    }
}

verify_otp_schema = {
    "operation_id": "verify otp",
    "security": [],
    "request_body": openapi.Schema(type=openapi.TYPE_OBJECT, required=["mobile", 'otp'],
                                   properties={
                                       "mobile": openapi.Schema(type=openapi.TYPE_STRING, title='Mobile number',
                                                                description="11 digits"),
                                       "otp": openapi.Schema(type=openapi.TYPE_STRING,
                                                             title="OneTimePassword",
                                                             description="Code sent to mobile", ),
                                   }),
    "responses": {
        "200": openapi.Response(
            description="verified otp",
            examples={
                "application/json": {
                    "expiry": "2023-12-29T06:48:01.863787+03:30",
                    "token": "4af8c1e27d872509c2e273b1a27df41e0daeb0367a7e08ecb8ad6eddad1f149z"
                }
            },
        ),
        "400": openapi.Response(
            description="Error",
            examples={
                "application/json": {
                    "result": "error",
                    "message": {
                        "status_code": 401,
                        "message": _("Wrong OTP."),
                        "description": _("Provided OTP is wrong."),
                    }
                }
            },
        ),
    }
}

verify_account_schema = {
    "operation_id": "Verify account",
    'security': [{"Token": []}],
    "tags": ["Verify Account"],
    "manual_parameters": [
        openapi.Parameter(name="national_card_image", in_=IN_FORM, type=openapi.TYPE_FILE),
        openapi.Parameter(name="birth_card_image", in_=IN_FORM, type=openapi.TYPE_FILE),
    ],
    "responses": {
        "200": openapi.Response(
            description="Updated successfully",
            examples={
                "application/json": {
                    "result": "success",
                    "message": "Updated successfully"
                }
            },
        ),
        "400": openapi.Response(
            description="Error",
            examples={
                "application/json": {
                    "result": "error",
                    "message": {**ERROR_INVALID_GENDER}
                }
            },
        ),
    }
}
