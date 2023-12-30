import os
import random
import re
import string

import environ
import ghasedakpack
from django.conf import settings

BASE_DIR = settings.BASE_DIR
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
sms = ghasedakpack.Ghasedak(env("API_KEY"))

otp_template_id = 'generate0otp0code'


def check_mobile(mobile=''):
    pattern = re.compile(r"^09\d{9}$")
    pattern.match(mobile)
    return not not pattern.match(mobile)


def check_email(email=''):
    pattern = re.compile(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$")
    pattern.match(email)
    return not not pattern.match(email)


def generate_otp(length=4):
    characters = string.digits.replace('0', '')
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp


def send_otp_sms(mobile):
    otp = generate_otp()
    try:
        res = sms.verification({'receptor': mobile, 'type': '1', 'template': otp_template_id, 'param1': otp})
    except Exception as e:
        print(e)
        res = False
    return [otp, res]
