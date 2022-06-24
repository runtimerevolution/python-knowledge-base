from dataclasses import dataclass

from django.utils import timezone
from datetime import timedelta


def yesterday():
    dt = timezone.now() + timedelta(days=-1)
    return dt.date()


import base64
import hashlib
import hmac
import json
from datetime import datetime
from pathlib import Path

import pandas
from requests import get
from requests.auth import AuthBase

URL = 'https://api.coinbase.com'

class Auth(AuthBase):
    VERSION = b'2021-03-30'

    def __init__(self, API_KEY, API_SECRET):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET

    def __call__(self, request):
        timestamp = datetime.now().strftime('%s')
        message = f"{timestamp}{request.method}{request.path_url}{request.body or ''}"
        signature = hmac.new(self.API_SECRET.encode(),
                             message.encode('utf-8'),
                             digestmod=hashlib.sha256)
        signature_hex = signature.hexdigest()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_hex,
            'CB-ACCESS-TIMESTAMP': timestamp.encode(),
            'CB-ACCESS-KEY': self.API_KEY.encode(),
            'CB-VERSION': self.VERSION,
            'Content-Type': 'application/json'
        })
        return request


@dataclass
class BaseAPI:
    auth: Auth
    url: str

    def base_request(self, request_path):
        return get(f'{self.url}{request_path}', auth=self.auth)


@dataclass
class Coinbase(BaseAPI):
    def get_transactions(self, id):
        request_path = f'/v2/accounts/{id}/transactions'
        r = self.base_request(request_path)
        return r


cb = Coinbase(Auth('a', 'b'), 'http://example.com')
cb.get_transactions()