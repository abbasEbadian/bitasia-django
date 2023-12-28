import re
import string
import random
import environ
import ghasedakpack
import os
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
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp


def send_otp_sms(mobile):
    otp = generate_otp()
    print({'receptor': mobile, 'type': '1', 'template': otp_template_id, 'param1': mobile})
    # sms.verification({'receptor': mobile, 'type': '1', 'template': otp_template_id, 'param1': mobile})
    # print(sms.status({'id': 'messageId', 'type': '1'}))سث
    return [otp, True]
