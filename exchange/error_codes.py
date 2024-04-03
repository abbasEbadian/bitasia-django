#

from django.utils.translation import gettext as _, gettext_lazy
from rest_framework import status

AUTH_ERRORS = {
    "ERROR_INVALID_MOBILE": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": _("Invalid mobile."),
        "description": _("Provided mobile should contain exactly 11 DIGITS and start with 09"),
        "description_en": "Provided mobile should contain exactly 11 DIGITS and start with 09"
    },
    "ERROR_INVALID_PASSWORD_PATTERN": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": _("Invalid password pattern."),
        "description": _("Provided password should contain at least 6 characters"),
        "description_en": "Provided password should contain at least 6 characters"
    },
    "ERROR_INVALID_PASSWORD": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": _("Empty password."),
        "description": _("Password can not be empty."),
        "description_en": "Password can not be empty."
    },
    "ERROR_WRONG_PASSWORD": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "message": _("Wrong password."),
        "description": _("Provided password is wrong."),
        "description_en": "Provided password is wrong."
    },

    "ERROR_MOBILE_ALREADY_EXISTS": {
        "status_code": status.HTTP_409_CONFLICT,
        "message": _("Mobile already exists."),
        "description": _("There is an account registered with this mobile."),
        "description_en": "There is an account registered with this mobile."
    },
    "ERROR_USER_DOES_NOT_EXIST": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": _("User does not exist"),
        "description": _("There is not any account registered with this mobile."),
        "description_en": "There is not any account registered with this mobile."
    },
    "ERROR_INVALID_OTP": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": _("Empty OTP."),
        "description": _("OTP must be 4 digits."),
        "description_en": "OTP must be 4 digits."
    },
    "ERROR_WRONG_OTP": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "message": _("Wrong OTP."),
        "description": _("Provided OTP is wrong."),
        "description_en": "Provided OTP is wrong."
    },
    "ERROR_INVALID_FIRST_NAME": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": _("Invalid first name"),
        "description": _("First name must be at least 3 characters."),
        "description_en": "First name must be at least 3 characters."
    },
    "ERROR_INVALID_LAST_NAME": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": _("Invalid last name"),
        "description": _("Last name must be at least 6 characters."),
        "description_en": "Last name must be at least 6 characters."
    },
    "ERROR_INVALID_BIRTHDATE": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": _("Invalid birthdate"),
        "description": _("birthdate must follow format: YYYY-MM-DD"),
        "description_en": "birthdate must follow format: YYYY-MM-DD",
    },
    "ERROR_INVALID_GENDER": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": _("Invalid gender"),
        "description": _("gender must be provided (male or female)"),
        "description_en": "gender must be provided (male or female)",
    },
    "ERROR_INVALID_RULE": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": _("Invalid rule id"),
        "description": _("Invalid rule id"),
        "description_en": "invalid rule id",
    },
    "GENERAL_UNMET_PARAMS_ERROR": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": _("invalid parameters"),
        "description": _("Provided values are not satisfying"),
        "description_en": "Provided values are not satisfying",
    },
    "DUPLICATE_CREDITCARD_ERROR": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": _("Credit card or IBAN already exists."),
        "description": _("Credit card or IBAN already exists."),
        "description_en": "Credit card or IBAN already exists."
    }
}

SMS_ERRORS = {
    "ERROR_FAIL_TO_SEND_SMS": {
        "code": "9001",
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": _("Failed to send sms."),
        "description": _("Cant connect to SMS provider."),
        "description_en": _("Cant connect to SMS provider."),
    }
}

PAYMENT_ERRORS = {
    "ERROR_INVALID_AMOUNT": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": _("Invalid amount"),
        "description": _("Amount must be greater than 10000 R"),
        "description_en": "Amount must be greater than 10000 R"
    },
    "ERROR_INVALID_CARD": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": _("Invalid card"),
        "description": _("Provided card is not valid or is not approved"),
        "description_en": "Provided card is not valid or is not approved",
    },
    "ERROR_GATEWAY": {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": _("Gateway error"),
        "description": _("Some error occurred while connecting to payment gateway"),
        "description_en": "Some error occurred while connecting to payment gateway"
    },

}

API_ERRORS = {
    **AUTH_ERRORS,
    **SMS_ERRORS
}


class ERRORS:
    @staticmethod
    def empty_field_error(field_name):
        return ({
            "status_code": status.HTTP_200_OK,
            "message": f'{_("Invalid ")} {field_name}',
            "description": f'{_(field_name)} Can\'t be empty.',
        })

    @staticmethod
    def custom_message_error(message):
        return ({
            "status_code": status.HTTP_200_OK,
            "message": f'{message}'
        })

    @staticmethod
    def length_error(field_name, minL, maxL):
        msg = gettext_lazy('%(f)s must have %(mn)d to %(mx)d digits')
        if minL == maxL:
            msg = gettext_lazy('%(f)s must have %(mn)d digits')

        return {
            "status_code": status.HTTP_200_OK,
            "message": msg % {"f": field_name, "mn": minL, "mx": maxL},
            "description": msg % {"f": field_name, "mn": minL, "mx": maxL},
        }

    ERROR_DUPLICATE_CREDITCARD = API_ERRORS["DUPLICATE_CREDITCARD_ERROR"]
    ERROR_INVALID_MOBILE = API_ERRORS["ERROR_INVALID_MOBILE"]
    ERROR_INVALID_PASSWORD_PATTERN = API_ERRORS["ERROR_INVALID_PASSWORD_PATTERN"]
    ERROR_INVALID_PASSWORD = API_ERRORS["ERROR_INVALID_PASSWORD"]
    ERROR_WRONG_PASSWORD = API_ERRORS["ERROR_WRONG_PASSWORD"]
    ERROR_MOBILE_ALREADY_EXISTS = API_ERRORS["ERROR_MOBILE_ALREADY_EXISTS"]
    ERROR_USER_DOES_NOT_EXIST = API_ERRORS["ERROR_USER_DOES_NOT_EXIST"]
    ERROR_INVALID_OTP = API_ERRORS["ERROR_INVALID_OTP"]
    ERROR_WRONG_OTP = API_ERRORS["ERROR_WRONG_OTP"]
    ERROR_INVALID_FIRST_NAME = API_ERRORS["ERROR_INVALID_FIRST_NAME"]
    ERROR_INVALID_LAST_NAME = API_ERRORS["ERROR_INVALID_LAST_NAME"]
    ERROR_FAIL_TO_SEND_SMS = API_ERRORS["ERROR_FAIL_TO_SEND_SMS"]
    ERROR_INVALID_BIRTHDATE = API_ERRORS["ERROR_INVALID_BIRTHDATE"]
    ERROR_INVALID_GENDER = API_ERRORS["ERROR_INVALID_GENDER"]
    ERROR_INVALID_RULE = API_ERRORS["ERROR_INVALID_RULE"]
    GENERAL_UNMET_PARAMS_ERROR = API_ERRORS["GENERAL_UNMET_PARAMS_ERROR"]

    ERROR_INVALID_AMOUNT = PAYMENT_ERRORS["ERROR_INVALID_AMOUNT"]
    ERROR_INVALID_CARD = PAYMENT_ERRORS["ERROR_INVALID_CARD"]
    ERROR_GATEWAY = PAYMENT_ERRORS["ERROR_GATEWAY"]
