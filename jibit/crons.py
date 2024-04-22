import os
from datetime import datetime

import environ
import requests

from config.models import JibitConfiguration
from exchange.settings import BASE_DIR

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
API_KEY = env("JIBIT_API_KEY")
SECRET_KEY = env("JIBIT_SECRET_KEY")
BASE = env("JIBIT_API_BASE")

json_headers = {"Content-Type": "application/json"}
token = BASE + "/v1/tokens/generate"


def update_token():
    print("Updating Jibit...", datetime.now())
    jibit_conf = JibitConfiguration.get_solo()
    res = requests.post(token, json={"apiKey": API_KEY, "secretKey": SECRET_KEY}, headers=json_headers)
    if res.status_code != 200:
        jibit_conf.last_call_success = False
        print("Failed to update Jibit.", res.text)
        return
    res = res.json()
    accessToken = res.get("accessToken")
    refreshToken = res.get("refreshToken")
    jibit_conf.token = accessToken
    jibit_conf.refresh = refreshToken
    jibit_conf.last_call_success = True
    jibit_conf.save()
    print("Updated Jibit.", datetime.now())
