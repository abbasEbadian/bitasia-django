from drf_yasg import openapi
from drf_yasg.openapi import Schema
from django.utils.translation import gettext as _

create_otp_schema_dict = {
    "200": openapi.Response(
        description="mobile login",
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
                "reason": _("Invalid Mobile")
            }
        },
    ),


}