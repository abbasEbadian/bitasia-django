from rest_framework import status
from rest_framework.exceptions import APIException


class CustomError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Value already exists.'

    def __init__(self, detail):
        if "status_code" in detail:
            self.status_code = detail["status_code"]
        self.detail = {"API_ERROR": detail}
