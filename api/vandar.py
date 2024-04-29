import os
from pathlib import Path

import environ
import requests

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

json_headers = {
    'Content-Type': 'application/json'
}


class Vandar:
    VANDAR_BAE_URL = "https://api.vandar.io"
    VANDAR_TOKEN = env('VANDAR_TOKEN')

    @staticmethod
    def refresh_token(self):
        url = "/v3/refreshtoken"
        body = {
            "refreshtoken": self.VANDAR_TOKEN
        }
        req = requests.post(url, json=body)

    @staticmethod
    def create_payment(self):
        pass
        # returns {status:1, token: 'token'}
        """
        url: 'https://ipg.vandar.io/api/v3/send',
        {
            api_key: 'کلید درگاه پرداخت دریافتی از پنل',
            amount: 1000,
            callback_url: 'https://example.com/callback',
            mobile_number: '09123456789',
            factorNumber: '12345',
            description: 'توضیحات دلخواه',
            valid_card_number: ['شماره کارت معتبر']
        }"""

        """{
              "status": 1,
              "token": "توکن پرداخت است و باید سمت پذیرنده نگهداری شود"
            }"""

        """
        url: 'https://ipg.vandar.io/v3/:token'
        """

    @staticmethod
    def verify_payment(self):
        pass
        """
          url: 'https://ipg.vandar.io/api/v3/verify'
          {
                api_key: 'کلید درگاه پرداخت دریافتی از پنل',
                token: 'توکن پرداختی که در مرحله یک دریافت کردید'
        }"""

        """{
          "status": 1,
          "amount": "1000.00",
          "realAmount": 500,
          "wage": "500",
          "transId": 159178352177,
          "factorNumber": "12345",
          "mobile": "09123456789",
          "description": "description",
          "cardNumber": "603799******7999",
          "paymentDate": "2020-06-10 14:36:30",
          "cid": null,
          "message": "ok"
        }"""
