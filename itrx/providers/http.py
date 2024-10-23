import hashlib
import hmac
from json import dumps
import os
import time
from urllib.parse import urljoin

import requests
from requests_ratelimiter import LimiterSession

DEFAULT_TIMEOUT = 10.0


class HTTPProvider:
    """An HTTP Provider for API request.

    :param endpoint_uri: HTTP API URL base. Default value is ``"https://itrx.io/api/v1/"``. Can also be configured via
        the ``ITRX_URI`` environment variable.
    :param api_key: API Key
    :param api_secret: API Secret
    :param timeout: HTTP timeout in seconds
    :param rate_limit: Number of requests per second. Default value is 4.

    """

    def __init__(
        self,
        endpoint_uri: str = None,
        api_key: str = None,
        api_secret: str = None,
        timeout: float = DEFAULT_TIMEOUT,
        rate_limit: int = 4
    ):
        super().__init__()

        if endpoint_uri is None:
            self._endpoint_uri = os.environ.get("ITRX_URI", "https://itrx.io/api/v1/")
        elif isinstance(endpoint_uri, (str,)):
            self._endpoint_uri = endpoint_uri
        else:
            raise TypeError(f"unknown endpoint uri {endpoint_uri}")

        if api_key is None:
            self._api_key = os.environ.get("ITRX_API_KEY", "")
        elif isinstance(api_key, (str,)):
            self._api_key = api_key

        if api_secret is None:
            self._api_secret = os.environ.get("ITRX_API_SECRET", "")
        elif isinstance(api_secret, (str,)):
            self._api_secret = api_secret

        self._timeout = timeout

        self._rate_limit = rate_limit
        self._sess = self._get_session()

    def _headers(self):
        headers = {
            'API-KEY': self._api_key
        }

        return headers

    def _get_session(self) -> requests.Session:
        if self._rate_limit:
            return LimiterSession(per_second=self._rate_limit)
        else:
            return requests.Session()

    def make_request(self, endpoint: str, get=None, post=None, json=None, sign=False) -> dict:
        if post or json:
            method = 'POST'
        else:
            method = 'GET'
            if not get:
                get = {}

        headers = self._headers()

        if json:
            headers['Content-Type'] = 'application/json'

        url = urljoin(self._endpoint_uri, endpoint)

        if sign:
            json_data = dumps(json, sort_keys=True, separators=(',', ':'))
            headers['TIMESTAMP'] = str(int(time.time()))
            message = f"{headers['TIMESTAMP']}&{json_data}"
            headers['SIGNATURE'] = hmac.new(self._api_secret.encode(), message.encode(), hashlib.sha256).hexdigest()

        resp = self._sess.request(method, url, params=get, data=post, json=json, headers=headers, timeout=self._timeout)

        resp.raise_for_status()
        return resp.json()
