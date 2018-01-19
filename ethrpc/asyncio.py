'''
    asyncio
    -------

    Module for the asynchronous Ethereum RPC client.
'''

__copyright__ = "2018 QChain Inc. All Rights Reserved."
__version__ = "0.1.0"
__license__ = "License: Apache v2, see LICENSE."
__author__ = "QChain Inc."
__email__ = "alex@qchain.co"
__maintainer__ = "Alex Huszagh"
__all__ = [
    'loop',
    'run',
    'map',
    'AsyncioClient',
]

import aiohttp
import asyncio
from .core import AbstractClient, LOCALHOST_HTTP_ENDPOINT


def loop():
    """
    Represents the global event loop.
    :return: Event loop for ethrpc client.
    """
    return asyncio.get_event_loop()


def run(future):
    """
    Run future until complete.
    :return: Return future's result, or raise exception.
    """
    return loop().run_until_complete(future)


def map(futures):
    """
    Asynchronously map list of futures.
    :return: Return value of all futures, or raise exception.
    """
    return run(asyncio.gather(*futures))


class AsyncioClient(AbstractClient):
    """
    Asynchronous variant of the main API client.
    Uses a session for connection pooling.
    """

    def __init__(self, endpoint = LOCALHOST_HTTP_ENDPOINT,
                 max_concurrency = 100):
        """
        Initialize client.
        :param endpoint: address of the Ethereum RPC.
        """
        super(AsyncioClient, self).__init__(endpoint)
        self.session = aiohttp.ClientSession(loop=loop())
        self.semaphore = asyncio.Semaphore(max_concurrency)

    def __del__(self):
        self.session.close()

    async def call(self, payload):
        """
        Make calls to the API via the HTTP POST method and JSON payload.
        :return: coroutine to the response object
        """
        async with self.semaphore:
            return await self.session.post(self.endpoint, json=payload)
