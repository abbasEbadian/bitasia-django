import os
import random
import re
import string

import environ
import ghasedakpack
from django.conf import settings
from django.utils.translation import gettext as _

from authentication.exception import CustomError
from exchange.error_codes import ERRORS

BASE_DIR = settings.BASE_DIR
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
sms = ghasedakpack.Ghasedak(env("SMS_API_KEY"))

LOGIN = "login"
RESET = "reset_password"
FORGET = "forget_password"
TRANSFER = "transfer"
WITHDRAW = "withdraw"


def check_mobile(mobile=''):
    pattern = re.compile(r"^09\d{9}$")
    pattern.match(mobile)
    return not not pattern.match(mobile)


def check_email(email=''):
    pattern = re.compile(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$")
    pattern.match(email)
    return not not pattern.match(email)


def generate_otp(length=5):
    characters = string.digits.replace('0', '')
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp


def get_otp_template(otp_type):
    temp_map = {
        "login": 'generate0otp0code',
        "reset_password": 'operation0password0otp',
        "forget_password": 'operation0password0otp',
        "transfer": 'operation0transfer0otp',
        "withdraw": 'operation0withdraw0otp',
    }
    return temp_map[otp_type]


def send_otp_sms(mobile, otp_type=LOGIN):
    otp = generate_otp()
    template = get_otp_template(otp_type=otp_type)
    try:
        res = sms.verification({'receptor': mobile, 'type': '1', 'template': template, 'param1': otp})
    except Exception as e:
        raise CustomError(ERRORS.custom_message_error(_("Cant connect to sms provider.")))
    return [otp, res]
