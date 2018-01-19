'''
    client
    ------

    Module for the synchronous Ethereum RPC client.
'''

__copyright__ = "2018 QChain Inc. All Rights Reserved."
__version__ = "0.1.0"
__license__ = "License: Apache v2, see LICENSE."
__author__ = "QChain Inc."
__email__ = "alex@qchain.co"
__maintainer__ = "Alex Huszagh"
__all__ = [
    'Client',
]

import requests
from .core import AbstractClient, LOCALHOST_HTTP_ENDPOINT


class Client(AbstractClient):
    """
    Synchronous variant of the main API client.
    Uses a session for connection pooling.
    """

    def __init__(self, endpoint = LOCALHOST_HTTP_ENDPOINT):
        """
        Initialize client.
        :param endpoint: address of the Ethereum RPC.
        """
        super(Client, self).__init__(endpoint)
        self.session = requests.Session()

    def call(self, payload):
        """
        Make calls to the API via the HTTP POST method and JSON payload.
        :return: response object
        """
        return self.session.post(self.endpoint, json=payload)

    def __del__(self):
        self.session.close()
