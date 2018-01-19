'''
    python-ethereum-client
    ----------------------

    Python client bindings for the Ethereum RPC API.
'''

__copyright__ = "2018 QChain Inc. All Rights Reserved."
__version__ = "0.1.0"
__license__ = "License: Apache v2, see LICENSE."
__author__ = "QChain Inc."
__email__ = "alex@qchain.co"
__maintainer__ = "Alex Huszagh"

from .core import *
from .client import *
try:
    from .asyncio import *
except:
    pass
