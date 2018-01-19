# python-ethereum-client

Python client for Ethereum JSON RPC API.

**Table Of Contents**

- [Installation](#installation)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [License](#license)

# Installation

Install all the required dependencies ( `bidict`, `PyCryptoDome`, `requests`, and optionally `aiohttp`) and run:

```
pip install git+https://github.com/q-chain/python-ethereum-client --user
```

To run the test suite, you must also install `requests_mock`, which may be run using `python setup.py test` in the repository directory.

# Getting Started

**Client**

Available in both Python2 and Python3.

```python
>>> import ethrpc
>>> client = ethrpc.Client()
>>> print(client.web3_client_version().json())
{'id': 67, 'result': 'Geth/v1.7.3-stable-4bb3c89d/linux-amd64/go1.9', 'jsonrpc': '2.0'}
```

**AsyncioClient**

Only available in Python 3.4.2+ and with `aiohttp` installed.

```python
>>> import ethrpc
>>> client = ethrpc.AsyncioClient()
>>> f1 = client.web3_client_version()
>>> f2 = client.eth_protocol_version()
>>> client_version, protocol_version = ethrpc.map([f1, f2])
>>> print(ethrpc.map([client_version.json(), protocol_version.json()]))
[{'id': 67, 'result': 'Geth/v1.7.3-stable-4bb3c89d/linux-amd64/go1.9', 'jsonrpc': '2.0'}, {'id': 67, 'result': '0x3f', 'jsonrpc': '2.0'}]
```

# API Documentation

See the [API](/doc/API.md) documentation.

# License

Apache v2, see [license](LICENSE).
