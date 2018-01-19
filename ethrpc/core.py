'''
    core
    ----

    Core module for the Ethereum RPC client.

    Describes an abstract base class for the client, along with various
    helpers, to wrap the Ethereum RPC without specifying the actual
    API for HTTP requests. Two primary clients wrap this base class:
    a synchronous client (`Client`), using `requests` for HTTP requests,
    and an asynchronous client (`AsyncioClient`), using `aiohttp` for
    HTTP requests.
'''

__copyright__ = "2018 QChain Inc. All Rights Reserved."
__version__ = "0.1.0"
__license__ = "License: Apache v2, see LICENSE."
__author__ = "QChain Inc."
__email__ = "alex@qchain.co"
__maintainer__ = "Alex Huszagh"
__all__ = [
    'map_position',
    'DEFAULT_BLOCK',
    'DEFAULT_HOST',
    'DEFAULT_HTTP_PORT',
    'DEFAULT_WS_PORT',
    'LOCALHOST_HTTP_ENDPOINT',
    'AbstractClient',
]

import abc
import binascii
import functools
import six
import textwrap
import warnings
from bidict import bidict
from Crypto.Hash import keccak

# HELPERS

def deprecated(f):
    """Decorator to mark functions or methods as deprecated."""

    @functools.wraps(f)
    def wrapped(*args, **kwds):
        message = "Calling deprecated function {}".format(f.__name__)
        warnings.warn(message, DeprecationWarning, stacklevel=2)
        return f(*args, **kwds)

    return wrapped


def remove_hex_prefix(string):
    '''Remove 0x prefix from hex strings, if present.'''

    if string.startswith('0x'):
        return string[2:]
    return string


def format_quantity(quantity):
    '''Format quantity, which is a numerical value'''

    return hex(quantity)


def format_hashrate(hash_rate):
    '''Format numerical value to 32-byte hex representation'''

    return "0x{0:064x}".format(hash_rate)


def format_block(block):
    '''Format block, which should be a string tag or quantity.'''

    if isinstance(block, int):
        return format_quantity(block)
    else:
        return block


def format_filter(from_block, to_block, address, topics):
    '''Format filter, which contains 4 optional parameters.'''

    obj = {}
    if from_block is not None:
        obj['fromBlock'] = format_block(from_block)
    if to_block is not None:
        obj['toBlock'] = format_block(to_block)
    if address is not None:
        obj['address'] = address
    if topics is not None:
        obj['topics'] = list(topics)

    return obj


def format_transaction(from_, to, gas, gas_price, value, data,
                       nonce=None, condition=None):
    '''Format transaction, which contains up to 6 optional parameters.'''

    obj = {}
    if from_ is not None:
        obj['from'] = from_
    if to is not None:
        obj['to'] = to
    if gas is not None:
        obj['gas'] = format_quantity(gas)
    if gas_price is not None:
        obj['gasPrice'] = format_quantity(gas_price)
    if value is not None:
        obj['value'] = format_quantity(value)
    if data is not None:
        obj['data'] = data
    if nonce is not None:
        obj['nonce'] = format_quantity(nonce)
    if condition is not None:
        obj['condition'] = condition

    return obj


def format_request(gas=None, gas_price=None, condition=None):
    '''Format signer request, which contains 0-3 parameters.'''

    obj = {}
    if gas is not None:
        obj['gas'] = format_quantity(gas)
    if gas_price is not None:
        obj['gasPrice'] = format_quantity(gas_price)
    if condition is not None:
        obj['condition'] = condition

    return obj


def format_shh(topics, payload, priority, ttl, from_=None, to=None):
    '''Format SHH, which contains 4-6 parameters.'''

    obj = {
        "topics": list(topics),
        "payload": payload,
        "priority": format_quantity(priority),
        "ttl": format_quantity(ttl),
    }

    if from_ is not None:
        obj["from"] = from_
    if to is not None:
        obj["to"] = to

    return obj


def format_message_filter(topics, decrypt_with=None, from_=None):
    '''Format SHH message filter, which contains 2-3 parameters.'''

    obj = {
        "topics": list(topics),
        'decryptWith': decrypt_with
    }
    if from_ is not None:
        obj["from"] = from_

    return obj

# API

DEFAULT_APIS = 'eth,net,web3'
DEFAULT_BLOCK = 'latest'
DEFAULT_CORS = ''
DEFAULT_HTTP_PORT = 8545
DEFAULT_WS_PORT = 8546
DEFAULT_HOST = "localhost"
LOCALHOST_HTTP_ENDPOINT = 'localhost:8545'


def map_position(key, position):
    """
    Convert map position to a normalized position for storage lookup.
    :param key: key to retrieve in the map.
    :param position: map position.
    :return: hex string position for storage lookup.
    """

    # pad on the left to 64 chars (32 hex chars).
    key64 = remove_hex_prefix(key).rjust(64, '0')
    position64 = '{0:064x}'.format(position)

    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(binascii.unhexlify(key64 + position64))
    return '0x' + keccak_hash.hexdigest()


@six.add_metaclass(abc.ABCMeta)
class AbstractClient():
    """
    Abstract base class for the main Ethereum RPC client.
    The documentation for all RPC resources may be found at:
    https://github.com/ethereum/wiki/wiki/JSON-RPC

    Each public method for the JSON-RPC API is implemented in terms of a
    private method returning the formatted parameters for the JSON-RPC
    call.
    """

    __method_table = bidict()

    def __init__(self, endpoint):
        """
        Initialize client.

        :param endpoint: address of the Ethereum RPC.
        """
        self.endpoint = endpoint

    @abc.abstractmethod
    def call(self, payload):
        """
        Make calls to the API via the HTTP POST method and JSON payload.
        Public overload that must be overridden in all subclasses of
        `AbstractClient`.

        :param payload: POST JSON data.
        """

    def rpc_name(self, name):
        """
        Get JSON-RPC API method name.

        :param name: Python or JSON-RPC API method name.
        """
        return self.__method_table.get(name, name)

    def python_name(self, name):
        """
        Get Python API method name.

        :param name: Python or JSON-RPC API method name.
        """
        return self.__method_table.inv.get(name, name)

    # PRIVATE

    def __call(self, method, id_, params):
        """
        Implied call to the JSON RPC via a POST with a JSON payload.

        :param payload: RPC method name.
        :param id_: Integer method identifier.
        :param params: Parameter list for method call.
        """
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": id_
        }
        return self.call(payload)

    @classmethod
    def __method(cls, python_name, rpc_name, rpc_id):
        """
        Wrap JSON-RPC method using decorator-like syntax.

        :param python_name: variable name for Python.
        :param rpc_name: 'method' parameter for RPC call.
        :param rpc_id: 'id' parameter for RPC call.
        """

        # store a bidirectional mapping of the Python and RPC names
        table = getattr(cls, '_{0}__method_table'.format(cls.__name__))
        table[python_name] = rpc_name

        # wrap our implied method
        impl_method = getattr(cls, '_{0}__{1}'.format(cls.__name__, python_name))

        def f(self, *args, **kwds):
            params = impl_method(self, *args, **kwds)
            return self.__call(rpc_name, rpc_id, params)

        # make the method look native
        f.__name__ = python_name
        f.__doc__ = impl_method.__doc__
        setattr(cls, python_name, f)
        setattr(cls, rpc_name, f)

    # WEB3

    def __web3_client_version(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#web3_clientversion
        Response body returns the JSON-formatted client version string
        for the Ethereum RPC.
        """
        return []

    def __web3_sha3(self, string):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#web3_sha3
        Response body returns the Keccak-256 hash of the string
        parameter.
        :param string: string to hash.
        """
        return [string]

    # NET

    def __net_listening(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#net_listening
        Response body returns if the client is actively listening
        for connections.
        """
        return []

    def __net_peer_count(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#net_peercount
        Response body returns the number of peers connected to the client.
        """
        return []

    def __net_version(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#net_version
        Response body returns the network ID.
        """
        return []

    # ETH

    def __eth_accounts(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_accounts
        Response body returns the list of addresses owned by the client.
        """
        return []

    def __eth_block_number(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_blocknumber
        Response body returns the most recent block identifier.
        """
        return []

    def __eth_call(self, from_=None, to=None, gas=None, gas_price=None,
                   value=None, data=None, block=None):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_call
        Execute new message immediately without creating a transaction.
        Response body returns the value of the executed contract.
        Valid tags are {"earliest", "latest", "pending"}.

        :param from_: (optional) address of sender.
        :param to: address of recipient.
        :param gas: (optional) gas provided for the transaction.
        :param gas_price: (optional) gas price for each paid gas.
        :param value: (optional) value to send with transactions.
        :param data: (optional) compile contract data or hash of method.
        :param block: block number or tag to query.
        """
        if block is None:
            raise ValueError("Block parameter must be provided.")
        obj = format_transaction(from_, to, gas, gas_price, value, data)
        return [obj, format_block(block)]

    def __eth_coinbase(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_coinbase
        Response body returns the client coinbase address.
        """
        return []

    def __eth_compile_lll(self, code):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_compilelll
        Response body returns the compiled source code.
        Ethereum only.

        :param code: LLL source code to compile.
        """
        return [code]

    def __eth_compile_serpent(self, code):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_compileserpent
        Response body returns the compiled source code.
        Ethereum only.

        :param code: Serpent source code to compile.
        """
        return [code]

    def __eth_compile_solidity(self, code):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_compilesolidity
        Response body returns the compiled source code.
        Ethereum only.

        :param code: solidity source code to compile.
        """
        return [code]

    def __eth_estimate_gas(self, from_=None, to=None, gas=None,
                           gas_price=None, value=None, data=None):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_estimategas
        Response body returns the estimated quantity of gas used.

        :param from_: (optional) address of sender.
        :param to: (optional) address of recipient.
        :param gas: (optional) gas provided for the transaction.
        :param gas_price: (optional) gas price for each paid gas.
        :param value: (optional) value to send with transactions.
        :param data: (optional) compile contract data or hash of method.
        """
        obj = format_transaction(from_, to, gas, gas_price, value, data)
        return [obj]

    def __eth_gas_price(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_gasprice
        Response body returns the current gas price.
        """
        return []

    def __eth_get_balance(self, address, block = DEFAULT_BLOCK):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getbalance
        Response body returns the balance of the address.
        Valid tags are {"earliest", "latest", "pending"}.

        :param address: address of account.
        :param block: block number or tag to query.
        """
        return [address, format_block(block)]

    def __eth_get_block_by_hash(self, hash_, use_full=False):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getblockbyhash
        Response body returns the information about blocks by hash.

        :param hash_: block hash.
        :param use_full: return full transaction objects.
        """
        return [hash_, use_full]

    def __eth_get_block_by_number(self, block = DEFAULT_BLOCK, use_full=False):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getblockbynumber
        Response body returns the information about blocks by number.
        Valid tags are {"earliest", "latest", "pending"}.

        :param block: block number or tag.
        :param use_full: return full transaction objects.
        """
        return [format_block(block), use_full]

    def __eth_get_block_transaction_count_by_hash(self, hash_):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getblocktransactioncountbyhash
        Response body returns the number of transactions in block by
        block hash.

        :param hash_: hash of block.
        """
        return [hash_]

    def __eth_get_block_transaction_count_by_number(self, block = DEFAULT_BLOCK):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getblocktransactioncountbynumber
        Response body returns the number of transactions in block by
        block number.
        Valid tags are {"earliest", "latest", "pending"}.

        :param block: block number or tag.
        """
        return [format_block(block)]

    def __eth_get_code(self, address, block = DEFAULT_BLOCK):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getcode
        Response body returns the code at a given address.
        Valid tags are {"earliest", "latest", "pending"}.

        :param address: address of account.
        :param block: block number or tag to query.
        """
        return [address, format_block(block)]

    def __eth_get_compilers(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getcompilers
        Response body returns a list of available compilers.
        Ethereum only.
        """
        return []

    def __eth_get_filter_changes(self, filter_id):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getfilterchanges
        Response body returns an list of logs since the last poll.

        :param filter_id: ID for filter to poll.
        """
        return [format_quantity(filter_id)]

    def __eth_get_filter_logs(self, filter_id):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getfilterlogs
        Response body returns an array of all filter logs for ID.

        :param filter_id: ID for filter to poll.
        """
        return [format_quantity(filter_id)]

    def __eth_get_logs(self, from_block=None, to_block=None,
                       address=None, topics=None):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getlogs
        Response body returns an array of logs matching a filter.
        Valid tags for `from_block` and `to_block` are {"earliest",
        "latest", "pending"}.

        :param from_block: (optional) block number or tag to query.
        :param to_block: (optional) block number or tag to query.
        :param address: (optional) contract address or list of addresses.
        :param topics: (optional) list of `DATA` topics.
        """
        obj = format_filter(from_block, to_block, address, topics)
        return [obj]

    def __eth_get_storage_at(self, address, position, block = DEFAULT_BLOCK):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getstorageat
        Response body returns the value from storage position of
        the address.
        Valid tags are {"earliest", "latest", "pending"}.
        To acquire the position of an element in a map, plus use
        `map_position` to convert the position of a an element in a
        map with a given key to the storage position.

        :param address: address of account.
        :param position: position in the storage.
        :param block: block number or tag to query.
        """
        return [address, format_quantity(position), format_block(block)]

    def __eth_get_transaction_by_block_hash_and_index(self, hash_, index = 0):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_gettransactionbyblockhashandindex
        Response body returns the information about transactions by block
        hash and transaction index.

        :param hash_: block hash.
        :param index: transaction index.
        """
        return [hash_, format_quantity(index)]

    def __eth_get_transaction_by_block_number_and_index(self, block = DEFAULT_BLOCK, index = 0):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_gettransactionbyblocknumberandindex
        Response body returns the information about transactions by block
        number and transaction index.
        Valid tags are {"earliest", "latest", "pending"}.

        :param block: block number or tag.
        :param index: transaction index.
        """
        return [format_block(block), format_quantity(index)]

    def __eth_get_transaction_by_hash(self, hash_):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_gettransactionbyhash
        Response body returns the information about transactions by hash.

        :param hash_: transaction hash.
        :param use_full: return full transaction objects.
        """
        return [hash_]

    def __eth_get_transaction_count(self, address, block = DEFAULT_BLOCK):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_gettransactioncount
        Response body returns the number of transactions sent from address.
        Valid tags are {"earliest", "latest", "pending"}.

        :param address: address of account.
        :param block: block number or tag to query.
        """
        return [address, format_block(block)]

    def __eth_get_transaction_receipt(self, hash_):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_gettransactionreceipt
        Response body returns the receipt about a transaction by hash.

        :param hash_: transaction hash.
        """
        return [hash_]

    def __eth_get_uncle_by_block_hash_and_index(self, hash_, index = 0):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getunclebyblockhashandindex
        Response body returns information about an uncle by block hash
        and by uncle index.

        :param hash_: block hash.
        :param index: uncle index.
        """
        return [hash_, format_quantity(index)]

    def __eth_get_uncle_by_block_number_and_index(self, block = DEFAULT_BLOCK, index = 0):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getunclebyblocknumberandindex
        Response body returns information about an uncle by block number
        and by uncle index.
        Valid tags are {"earliest", "latest", "pending"}.

        :param block: block number or tag.
        :param index: uncle index.
        """
        return [format_block(block), format_quantity(index)]

    def __eth_get_uncle_count_by_block_hash(self, hash_):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getunclecountbyblockhash
        Response body returns the number of uncles in block by
        block hash.

        :param hash_: hash of block.
        """
        return [hash_]

    def __eth_get_uncle_count_by_block_number(self, block = DEFAULT_BLOCK):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getunclecountbyblocknumber
        Response body returns the number of uncles in block by
        block number.
        Valid tags are {"earliest", "latest", "pending"}.

        :param block: block number or tag.
        """
        return [format_block(block)]

    def __eth_get_work(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getwork
        Response body returns data about the current block, seed hash,
        and boundary condition.
        """
        return []

    def __eth_hashrate(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_hashrate
        Response body returns the number of hashes per second the node
        is mining.
        """
        return []

    def __eth_mining(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_mining
        Response body returns boolean data if the node is mining.
        """
        return []

    def __eth_new_block_filter(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_newblockfilter
        Response body returns the filter ID.
        """
        return []

    def __eth_new_filter(self, from_block=None, to_block=None,
                         address=None, topics=None):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_newfilter
        Response body returns the filter ID.
        Valid tags for `from_block` and `to_block` are {"earliest",
        "latest", "pending"}.

        :param from_block: (optional) block number or tag to query.
        :param to_block: (optional) block number or tag to query.
        :param address: (optional) contract address or list of addresses.
        :param topics: (optional) list of `DATA` topics.
        """
        obj = format_filter(from_block, to_block, address, topics)
        return [obj]

    def __eth_new_pending_transaction_filter(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_newpendingtransactionfilter
        Response body returns the filter ID.
        """
        return []

    def __eth_protocol_version(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_protocolversion
        Response body returns the current Ethereum protocol version.
        """
        return []

    def __eth_send_raw_transaction(self, data):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_sendrawtransaction
        Response body returns the transaction hash, or the zero hash
        if the transaction is not available yet.

        :param data: signed transaction data.
        """
        return [data]

    def __eth_send_transaction(self, from_, to=None, gas=None,
                               gas_price=None, value=None,
                               data=None, nonce=None):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_sendtransaction
        Response body returns the transaction hash, or the zero hash
        if the transaction is not available yet.

        :param from_: address of sender.
        :param to: (optional) address of recipient.
        :param gas: (optional) gas provided for the transaction.
        :param gas_price: (optional) gas price for each paid gas.
        :param value: (optional) value to send with transactions.
        :param data: (optional) compile contract data or hash of method.
        :param nonce: (optional) user-provided nonce to override transactions.
        """
        obj = format_transaction(from_, to, gas, gas_price, value, data, nonce)
        return [obj]

    def __eth_sign(self, address, message):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_sign
        Response body returns the Ethereum-signed message.

        :param address: address of account.
        :param message: message to sign.
        """
        return [address, message]

    def __eth_sign_transaction(self, from_, to=None, gas=None,
                               gas_price=None, value=None,
                               data=None, nonce=None, condition=None):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-eth-module#eth_signtransaction
        Response body returns the signed transaction data and object,
        for submission with `eth_send_raw_transaction`.
        Parity only.

        :param from_: address of sender.
        :param to: (optional) address of recipient.
        :param gas: (optional) gas provided for the transaction.
        :param gas_price: (optional) gas price for each paid gas.
        :param value: (optional) value to send with transactions.
        :param data: (optional) compile contract data or hash of method.
        :param nonce: (optional) user-provided nonce to override transactions.
        :param condition: (optional) conditional submission of transaction.
        """
        obj = format_transaction(from_, to, gas, gas_price, value, data, nonce, condition)
        return [obj]

    def __eth_submit_hashrate(self, hash_rate, client_id):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_submithashrate
        Response body returns a boolean if the submission went through.

        :param hash_rate: hex representation of hash rate.
        :param client_id: random hex string identifying client.
        """
        return [format_hashrate(hash_rate), client_id]

    def __eth_submit_work(self, nonce, pow_hash, mix_digest):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_submitwork
        Response body returns a boolean if the proof of work is valid.

        :param nonce: nonce found.
        :param pow_hash: proof of work hash.
        :param mix_digest: mix digest.
        """
        return ["0x{0:08x}".format(nonce), pow_hash, mix_digest]

    def __eth_syncing(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_syncing
        Response body returns data about the sync status.
        """
        return []

    def __eth_uninstall_filter(self, filter_id):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_uninstallfilter
        Response body returns a boolean for if the filter was uninstalled.

        :param filter_id: ID for filter to uninstall.
        """
        return [format_quantity(filter_id)]

    # ETH_PUBSUB (PARITY ONLY)

    def __eth_subscribe(self, type_, from_block=None, to_block=None,
                        address=None, topics=None):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-Eth-Pub-Sub-Module#eth_subscribe
        Response body returns a subscription ID.
        Valid tags for `from_block` and `to_block` are {"earliest",
        "latest", "pending"}.
        Parity only.

        :param type_: subscription type ({'logs', 'newHeads'})
        :param from_block: (optional) block number or tag to query.
        :param to_block: (optional) block number or tag to query.
        :param address: (optional) contract address or list of addresses.
        :param topics: (optional) list of `DATA` topics.
        """
        if type_ == 'logs':
            obj = format_filter(from_block, to_block, address, topics)
        elif type_ == 'newHeads':
            obj = {}
        else:
            raise ValueError("Unexpected eth_subscribe type.")
        return [type_, obj]

    def __eth_unsubscribe(self, subscription_id):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-Eth-Pub-Sub-Module#eth_unsubscribe
        Response body returns if the unsubscribe request was successful.
        Parity only.

        :param subscription_id: ID for subscription to unsubscribe.
        """
        return [format_quantity(subscription_id)]

    # PERSONAL (PARITY/GETH ONLY)

    def __personal_ec_recover(self, message, signature):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#personal_ecrecover
        Response body returns the address used to sign message.
        Geth only.

        :param message: hex representation of message.
        :param signature: signature generated via `personal_sign`.
        """
        return [message, signature]

    def __personal_import_raw_key(self, private_key, password):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#personal_importrawkey
        Response body returns the address of the new account.
        Parity/Geth only.

        :param private_key: hex-representation of private key.
        :param password: password for to encrypt key with.
        """
        return [private_key, password]

    def __personal_list_accounts(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-personal-module#personal_listaccounts
        Response body returns a list of all locally-stored account addresses.
        Parity or Geth only.
        """
        return []

    def __personal_lock_account(self, address):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#personal_lockaccount
        Geth only.

        :param address: address of account.
        """
        return [password]

    def __personal_new_account(self, password):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-personal-module#personal_newaccount
        Response body returns the new account address.
        Parity/Geth only.

        :param password: account password.
        """
        return [password]

    def __personal_send_transaction(self, from_, to=None, gas=None,
                                    gas_price=None, value=None,
                                    data=None, nonce=None,
                                    condition=None, password=None):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-personal-module#personal_sendtransaction
        Response body returns the transaction hash, or the zero hash
        if the transaction is not available yet.
        Parity only.

        :param from_: address of sender.
        :param to: (optional) address of recipient.
        :param gas: (optional) gas provided for the transaction.
        :param gas_price: (optional) gas price for each paid gas.
        :param value: (optional) value to send with transactions.
        :param data: (optional) compile contract data or hash of method.
        :param nonce: (optional) user-provided nonce to override transactions.
        :param condition: (optional) conditional submission of transaction.
        :param password: account password.
        """
        if password is None:
            raise ValueError("Password parameter must be provided.")
        obj = format_transaction(from_, to, gas, gas_price, value, data, nonce, condition)
        return [obj, password]

    def __personal_sign(self, message, address, password):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#personal_sign
        Response body returns the signed message.
        Geth only.

        :param message: hex representation of message.
        :param address: account address.
        :param password: account password.
        """
        return [message, address, password]

    def __personal_unlock_account(self, adddress, password, duration=None):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-personal-module#personal_unlockaccount
        Response body returns a boolean if the account was unlocked.
        Parity/Geth only.

        :param address: account address.
        :param password: account password.
        :param duration: (optional) duration in seconds to unlock account for.
        """
        params = [adddress, password]
        if duration is None:
            params.append(duration)
        else:
            params.append(hex(duration))
        return params

    # PARTIY (PARITY ONLY)

    def __parity_accounts_info(self):
        """
        httpshttps://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_accountsinfo
        Response body returns metadata about accounts.
        Parity only.
        """
        return []

    def parity_accounts_info(self, *args, **kwds):
        params = self.__parity_accounts_info(*args, **kwds)
        return self.__call("parity_accountsInfo", 1, params)

    def __parity_chain(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_chain
        Response body returns name of connected chain.
        Parity only.
        """
        return []

    def __parity_chain_status(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_chainstatus
        Response body returns status of connected chain.
        Parity only.
        """
        return []

    def __parity_change_vault(self, address, vault):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_changevault
        Response body returns if the vault change was successful.
        Parity only.

        :param address: address of account.
        :param vault: vault name.
        """
        return [address, vault]

    def __parity_change_vault_password(self, vault, password):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_changevaultpassword
        Response body returns if the password change was successful.
        Parity only.

        :param vault: vault name.
        :param password: new vault password.
        """
        return [vault, password]

    def __parity_check_request(self, request_id):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_checkrequest
        Response body returns the transaction hash if request was accepted,
        or an error.

        :param request_id: ID of request.
        """
        return [format_quantity(request_id)]

    def __parity_cid_v0(self, data):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_cidv0
        Response body returns the base58-encoded v0 IPFS (InterPlanetary
        File System) content ID from a Protobuf-encoded data.

        :param data: hex representation of a Protobuf-encoded string.
        """
        return [data]

    def __parity_close_vault(self, vault):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_closevault
        Response body returns if the vault closure was successful.
        Parity only.

        :param vault: vault name.
        """
        return [vault]

    def __parity_compose_transaction(self, from_, to=None, gas=None,
                                     gas_price=None, value=None,
                                     data=None, nonce=None, condition=None):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_composetransaction
        Response body returns the unsigned transaction object created
        from partial data, which may be signed externally.
        Parity only.

        :param from_: address of sender.
        :param to: (optional) address of recipient.
        :param gas: (optional) gas provided for the transaction.
        :param gas_price: (optional) gas price for each paid gas.
        :param value: (optional) value to send with transactions.
        :param data: (optional) hash of method signature and parameters.
        :param nonce: (optional) user-provided nonce to override transactions.
        :param condition: (optional) conditional submission of transaction.
        """
        obj = format_transaction(from_, to, gas, gas_price, value, data, nonce, condition)
        return [obj]

    def __parity_consensus_capability(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_consensuscapability
        Response body returns the information on the current consensus
        capability.
        Parity only.
        """
        return []

    def __parity_dapps_url(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_dappsurl
        Response body returns hostname and port of dapps server.
        Parity only.
        """
        return []

    def __parity_decrypt_message(self, address, message):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_decryptmessage
        Response body returns the decrypted message.
        Parity only.

        :param address: address of account that can decrypt message.
        :param message: hex representation of encrypted message bytes.
        """
        return [address, message]

    def __parity_default_account(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_defaultaccount
        Response body returns default account address for transactions.
        Parity only.
        """
        return []

    def __parity_default_extra_data(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_defaultextradata
        Response body returns default extra data.
        Parity only.
        """
        return []

    def __parity_dev_logs(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_devlogs
        Response body returns a list of recent stdout logs.
        Parity only.
        """
        return []

    def __parity_dev_logs_levels(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_devlogslevels
        Response body returns a string about the current logging level.
        Parity only.
        """
        return []

    def __parity_encrypt_message(self, hash_, message):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_encryptmessage
        Response body returns the decrypted message.
        Parity only.

        :param hash_: last 64 bytes of EC public key.
        :param message: hex representation of message to encrypt.
        """
        return [hash_, message]

    def __parity_enode(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_enode
        Response body returns the enode URI.
        Parity only.
        """
        return []

    def __parity_extra_data(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_extradata
        Response body returns the currently set extra data.
        Parity only.
        """
        return []

    def __parity_future_transactions(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_futuretransactions
        Response body returns list of all future transactions currently
        in queue.
        Parity only.
        """
        return []

    def __parity_gas_ceil_target(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_gasceiltarget
        Response body returns the current gas ceiling target.
        Parity only.
        """
        return []

    def __parity_gas_floor_target(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_gasfloortarget
        Response body returns the current gas floor target.
        Parity only.
        """
        return []

    def __parity_gas_price_histogram(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_gaspricehistogram
        Response body returns historic gas prices.
        Parity only.
        """
        return []

    def __parity_generate_secret_phrase(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_generatesecretphrase
        Response body returns the secret phrase now associated with account.
        Parity only.
        """
        return []

    def __parity_get_block_header_by_number(self, block = DEFAULT_BLOCK):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_getblockheaderbynumber
        Response body returns the block header by number.
        Valid tags are {"earliest", "latest", "pending"}.
        Parity only.

        :param block: block number or tag.
        """
        return [format_block(block)]

    def __parity_get_vault_meta(self, vault):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_getvaultmeta
        Response body returns metadata for vault.
        Parity only.

        :param vault: vault name.
        """
        return [vault]

    def __parity_hardware_accounts_info(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_hardwareaccountsinfo
        Response body returns metadata for attached hardware wallets.
        Parity only.
        """
        return []

    def __parity_list_accounts(self, quantity, address=None, block=None):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_listaccounts
        Response body returns a list of addresses, or null.
        FatDB must be enabled (`--fat-db`).
        Parity only.

        :param quantity: number of addresses to get.
        :param address: offset address to start at, or `None`.
        :param block: block number or tag.
        """
        params = [format_quantity(quantity), address]
        if block is not None:
            params.append(format_block(block))
        return params

    def __parity_list_opened_vaults(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_listopenedvaults
        Response body returns a list of opened vaults.
        Parity only.
        """
        return []

    def __parity_list_storage_keys(self, address, quantity, hash_=None, block=None):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_liststoragekeys
        Response body returns a list of storage keys from account.
        FatDB must be enabled (`--fat-db`).
        Valid tags are {"earliest", "latest", "pending"}.
        Parity only.

        :param address: address of account.
        :param quantity: number of storage keys to get.
        :param hash_: offset storage key, or null.
        :param block: block number or tag.
        """
        params = [address, format_quantity(quantity), hash_]
        if block is not None:
            params.append(format_block(block))
        return params

    def __parity_list_vaults(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_listvaults
        Response body returns a list of vaults.
        Parity only.
        """
        return []

    def __parity_local_transactions(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_localtransactions
        Response body returns a list of current and previous local
        transactions.
        Parity only.
        """
        return []

    def __parity_min_gas_price(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_mingasprice
        Response body returns the current minimal gas price.
        Parity only.
        """
        return []

    def __parity_mode(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_mode
        Response body returns the mode.
        Parity only.
        """
        return []

    def __parity_new_vault(self, vault, password):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_newvault
        Response body returns if a new vault was created.
        Parity only.

        :param vault: new vault name.
        :param password: new vault password.
        """
        return [vault, password]

    @deprecated
    def __parity_net_chain(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_netchain
        Response body returns name of connected chain.
        Parity only.
        """
        return []

    def __parity_net_peers(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_netpeers
        Response body returns the number of connected peers.
        Parity only.
        """
        return []

    def __parity_net_port(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_netport
        Response body returns the network port node is listening to.
        Parity only.
        """
        return []

    def __parity_next_nonce(self, address):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_nextnonce
        Response body returns the valid transaction nonce from account.
        Parity only.

        :param address: address of account.
        """
        return [address]

    def __parity_node_kind(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_nodekind
        Response body returns the node kind and availability.
        Parity only.
        """
        return []

    def __parity_node_name(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_nodename
        Response body returns the node name.
        Parity only.
        """
        return []

    def __parity_pending_transactions(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_pendingtransactions
        Response body returns a list of pending transactions.
        Parity only.
        """
        return []

    def __parity_pending_transactions_stats(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_pendingtransactionsstats
        Response body returns a dict of pending transaction hashes to stats.
        Parity only.
        """
        return []

    def __parity_phrase_to_address(self, phrase):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_phrasetoaddress
        Response body returns the account address from a secret phrase.
        Parity only.

        :param phrase: secret phrase.
        """
        return [phrase]

    def __parity_open_vault(self, vault, password):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_openvault
        Response body returns if the vault was successfully opened.
        Parity only.

        :param vault: new vault name.
        :param password: new vault password.
        """
        return [vault, password]

    def __parity_post_sign(self, address, message):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_postsign
        Response body returns the request ID.
        Parity only.

        :param address: address of account.
        :param message: message to be signed.
        """
        return [address, message]

    def __parity_post_transaction(self, from_, to=None, gas=None,
                                  gas_price=None, value=None,
                                  data=None, nonce=None, condition=None):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_posttransaction
        Response body returns the request ID from a transaction posted
        without waiting for the signer. If the account is unlocked,
        returns the transaction hash instead.
        Parity only.

        :param from_: address of sender.
        :param to: (optional) address of recipient.
        :param gas: (optional) gas provided for the transaction.
        :param gas_price: (optional) gas price for each paid gas.
        :param value: (optional) value to send with transactions.
        :param data: (optional) hash of method signature and parameters.
        :param nonce: (optional) user-provided nonce to override transactions.
        :param condition: (optional) conditional submission of transaction.
        """
        obj = format_transaction(from_, to, gas, gas_price, value, data, nonce, condition)
        return [obj]

    def __parity_registry_address(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_registryaddress
        Response body returns the address for the global registry.
        Parity only.
        """
        return []

    def __parity_releases_info(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_releasesinfo
        Response body returns information about the release status.
        Parity only.
        """
        return []

    def __parity_remove_transaction(self, hash_):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_releasesinfo
        Response body returns the transaction data for the removed
        transaction, or null.
        Parity only.

        :param hash_: transaction hash.
        """
        return [hash_]

    def __parity_rpc_settings(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_rpcsettings
        Response body returns current RPC API settings.
        Parity only.
        """
        return []

    def __parity_set_vault_meta(self, vault, metadata):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_setvaultmeta
        Response body returns if vault metadata was successfully set.
        Parity only.

        :param vault: vault name.
        :param metadata: JSON string or dict of vault metadata.
        """
        return [vault, metadata]

    def __parity_sign_message(self, address, password, hash_):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_signmessage
        Response body returns generated signature for the message.
        Parity only.

        :param address: address of account.
        :param password: account password.
        :param hash_: hex representation of hashed message.
        """
        return [address, password, hash_]

    def __parity_transactions_limit(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_transactionslimit
        Response body returns the max number of transactions in queue.
        Parity only.
        """
        return []

    def __parity_unsigned_transactions_count(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_unsignedtransactionscount
        Response body returns the number of unsigned transactions if using
        a trusted signer.
        Parity only.
        """
        return []

    def __parity_version_info(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_versioninfo
        Response body returns information about the Parity version.
        Parity only.
        """
        return []

    def __parity_ws_url(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity-module#parity_wsurl
        Response body returns hostname and port of Websockets server.
        Parity only.
        """
        return []

    # PARTIY ACCOUNTS (PARITY ONLY)

    def __parity_all_accounts_info(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_allaccountsinfo
        Response body returns a dict of account info.
        Parity only.
        """
        return []

    def __parity_change_password(self, address, old_password, new_password):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_changepassword
        Response body returns if password change was successful.
        Parity only.

        :param address: address of account.
        :param old_password: old account password.
        :param new_password: new account password.
        """
        return [address, old_password, new_password]

    def __parity_derive_address_hash(self, address, password, derivation_hash,
                                     derivation_type = 'hard', save_account = False):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_changepassword
        Response body returns the derived account address.
        Parity only.

        :param address: address of account.
        :param password: account password.
        :param derivation_hash: derivation hash.
        :param derivation_type: derivation type.
        :param save_account: save account for later use.
        """
        derived = {'hash': derivation_hash, 'type': derivation_type}
        return [address, password, derived, save_account]

    def __parity_derive_address_index(self, address, password, derivation, save_account = False):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_deriveaddressindex
        Response body returns the derived account address.
        Parity only.

        :param address: address of account.
        :param password: account password.
        :param derivation: sequence of dicts with the derivation type and index.
        :param save_account: save account for later use.
        """
        return [address, password, list(derivation), save_account]

    def __parity_export_account(self, address, password):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_exportaccount
        Response body returns the standard wallet file for the account.
        Parity only.

        :param address: address of account.
        :param password: account password.
        """
        return [address, password]

    def __parity_get_dapp_addresses(self, dapp):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_getdappaddresses
        Response body returns a list of account addresses matching the dapp.
        Parity only.

        :param dapp: dapp identifier ("web").
        """
        return [dapp]

    def __parity_get_dapp_default_address(self, dapp):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_getdappdefaultaddress
        Response body returns the default account address for the dapp.
        Parity only.

        :param dapp: dapp identifier ("web").
        """
        return [dapp]

    def __parity_get_new_dapps_addresses(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_getnewdappsaddresses
        Response body returns a list of account addresses for new dapps.
        Parity only.
        """
        return []

    def __parity_get_new_dapps_default_address(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_getnewdappsdefaultaddress
        Response body returns the default account address for new dapps.
        Parity only.
        """
        return []

    def __parity_import_geth_accounts(self, *addresses):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_importgethaccounts
        Response body returns a list of the imported geth account addresses.
        Parity only.

        :param addresses: sequence of geth account addresses.
        """
        return [list(addresses)]

    def __parity_kill_account(self, address, password):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_killaccount
        Response body returns if the account deletion was successful.
        Parity only.

        :param address: address of account.
        :param password: account password.
        """
        return [address, password]

    def __parity_list_geth_accounts(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_listgethaccounts
        Response body returns a list of the available geth accounts.
        Parity only.
        """
        return []

    def __parity_list_recent_dapps(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_listrecentdapps
        Response body returns a list of the most recent active dapps.
        Parity only.
        """
        return []

    def __parity_new_account_from_phrase(self, phrase, password):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_newaccountfromphrase
        Response body returns the address of the newly created account.
        Parity only.

        :param phrase: secret phrase.
        :param password: account password.
        """
        return [phrase, password]

    def __parity_new_account_from_secret(self, secret, password):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_newaccountfromsecret
        Response body returns the address of the newly created account.
        Parity only.

        :param secret: hex-representation of 32-byte secret.
        :param password: account password.
        """
        return [secret, password]

    def __parity_new_account_from_wallet(self, wallet, password):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_newaccountfromwallet
        Response body returns the address of the newly created account.
        Parity only.

        :param wallet: JSON string or dict of wallet data.
        :param password: account password.
        """
        return [wallet, password]

    def __parity_remove_address(self, address):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_removeaddress
        Response body returns if the account removal from the addressbook
        was successful.
        Parity only.

        :param address: account address.
        """
        return [address]

    def __parity_set_account_meta(self, address, metadata):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_setaccountmeta
        Response body returns if the account metadata was successfully set.
        Parity only.

        :param address: account address.
        :param metadata: JSON string or dict of account metadata.
        """
        return [address, metadata]

    def __parity_set_account_name(self, address, name):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_setaccountname
        Response body returns if the account metadata was successfully set.
        Parity only.

        :param address: account address.
        :param name: account name.
        """
        return [address, name]

    def __parity_set_dapp_addresses(self, dapp, *addresses):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_setdappaddresses
        Response body returns if the account list for a dapp was
        successful.
        Parity only.

        :param dapp: dapp identifier ("web").
        :param addresses: sequence of account addresses.
        """
        return [dapp, list(addresses)]

    def __parity_set_dapp_default_address(self, dapp, address):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_setdappdefaultaddress
        Response body returns if the setting the default account for a
        dapp was successful.
        Parity only.

        :param dapp: dapp identifier ("web").
        :param address: account address.
        """
        return [dapp, address]

    def __parity_set_new_dapps_addresses(self, *addresses):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_setnewdappsaddresses
        Response body returns if the setting the list of accounts for new
        dapps was successful.
        Parity only.

        :param addresses: sequence of account addresses.
        """
        return [list(addresses)]

    def __parity_set_new_dapps_default_address(self, address):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_setnewdappsdefaultaddress
        Response body returns if the setting the default account for new
        dapps was successful.
        Parity only.

        :param address: account address.
        """
        return [address]

    def __parity_test_password(self, address, password):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_accounts-module#parity_testpassword
        Response body returns if the the account address/password pair
        can unlock an account without unlocking it.
        Parity only.

        :param address: account address.
        :param password: account password.
        """
        return [address, password]

    # PARTIY SET (PARITY ONLY)

    def __parity_accept_non_reserved_peers(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_acceptnonreservedpeers
        Response body returns if now accepts non-reserved peers.
        Parity only.
        """
        return []

    def __parity_add_reserved_peer(self, enode):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_addreservedpeer
        Response body returns if the reserved peer was added.
        Parity only.

        :param enode: address of node.
        """
        return [enode]

    def __parity_dapps_list(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_dappslist
        Response body returns a list of local dapps.
        Parity only.
        """
        return []

    def __parity_drop_non_reserved_peers(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_dropnonreservedpeers
        Response body returns if all non-reserved peers were successfully
        dropped.
        Parity only.
        """
        return []

    def __parity_execute_upgrade(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_executeupgrade
        Response body returns if the upgrade was successful.
        Parity only.
        """
        return []

    def __parity_hash_content(self, uri):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_hashcontent
        Response body returns the Keccak-256 hash of the contents at the URI.
        Parity only.

        :param uri: URI to content data.
        """
        return [uri]

    def __parity_remove_reserved_peer(self, enode):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_removereservedpeer
        Response body returns if the reserved peer was removed.
        Parity only.

        :param enode: address of node.
        """
        return [enode]

    def __parity_set_author(self, address):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_setauthor
        Response body returns if the author address for mined blocks
        was successfully set.
        Parity only.

        :param address: account address.
        """
        return [address]

    def __parity_set_chain(self, chain):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_setchain
        Response body returns if the network specification was
        successfully set.
        Parity only.

        :param chain: chain name.
        """
        return [chain]

    def __parity_set_engine_signer(self, address, password):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_setenginesigner
        Response body returns if the authority account for consensus
        messages was successfully set.
        Parity only.

        :param address: account address.
        :param password: account password.
        """
        return [address, password]

    def __parity_set_extra_data(self, data):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_setextradata
        Response body returns if the extra data for mined blocks was
        successfully set.
        Parity only.

        :param data: hex-representation of binary data.
        """
        return [data]

    def __parity_set_gas_ceil_target(self, gas=0):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_setgasceiltarget
        Response body returns if the gas ceiling target was successfully
        set.
        Parity only.

        :param gas: gas amount.
        """
        return [format_quantity(gas)]

    def __parity_set_gas_floor_target(self, gas=0):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_setgasfloortarget
        Response body returns if the gas floor target was successfully set.
        Parity only.

        :param gas: gas amount.
        """
        return [format_quantity(gas)]

    def __parity_set_max_transaction_gas(self, gas):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_setmaxtransactiongas
        Response body returns if gas limited per transaction was
        successfully set.
        Parity only.

        :param gas: gas amount.
        """
        return [format_quantity(gas)]

    def __parity_set_min_gas_price(self, gas_price):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_setmingasprice
        Response body returns if the minimum gas price for a transaction
        to be accepted was successfully set.
        Parity only.

        :param gas_price: gas price for each paid gas.
        """
        return [format_quantity(gas_price)]

    def __parity_set_mode(self, mode):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_setmode
        Response body returns if the Parity mode was successfully set.
        Parity only.

        :param mode: parity mode ({'active', 'passive', 'dark', 'offline'}).
        """
        return [mode]

    def __parity_set_transactions_limit(self, limit):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_settransactionslimit
        Response body returns if the transaction limit was successfully set.
        Parity only.

        :param limit: maximum number of transactions in queue.
        """
        return [format_quantity(limit)]

    def __parity_upgrade_ready(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-parity_set-module#parity_upgradeready
        Response body returns if Parity has an upgrade available.
        Parity only.
        """
        return []

    # PUBSUB (PARITY ONLY)

    def __parity_subscribe(self, method, *args, **kwds):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-Parity-Pub-Sub-module#parity_subscribe
        Response body returns a subscription ID.
        Parity only.

        :param method: Python or JSON-RPC method name.
        :param args: positional arguments for method call.
        :param kwds: keyword arguments for method call.
        """

        python_name = self.python_name(method)
        rpc_name = self.rpc_name(method)
        impl_method = getattr(self, '_AbstractClient__' + python_name)
        return [rpc_name, impl_method(*args, **kwds)]

    def __parity_unsubscribe(self, subscription_id):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-Parity-Pub-Sub-module#parity_unsubscribe
        Response body returns if the unsubscribe request was successful.
        Parity only.

        :param subscription_id: ID for subscription to unsubscribe.
        """
        return [format_quantity(subscription_id)]

    # SIGNER (PARITY ONLY)

    def __signer_confirm_request(self, request_id, gas=None, gas_price=None,
                                 condition=None, password=None):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-signer-module#signer_confirmrequest
        Response body returns a dict containing the request confirmation
        status.
        Parity only.

        :param request_id: ID of request.
        :param gas: (optional) gas provided for the transaction.
        :param gas_price: (optional) gas price for each paid gas.
        :param condition: (optional) conditional submission of transaction.
        :param password: account password.
        """
        if password is None:
            raise ValueError("Password parameter must be provided.")

        obj = format_request(gas, gas_price, condition)
        return [format_quantity(request_id), obj, password]

    def __signer_confirm_request_raw(self, request_id, data):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-signer-module#signer_confirmrequestraw
        Response body returns a dict containing the request confirmation
        status.
        Parity only.

        :param request_id: ID of request.
        :param data: signed request data.
        """
        return [format_quantity(request_id), data]

    def __signer_confirm_request_with_token(self, request_id, gas=None, gas_price=None,
                                            condition=None, password=None):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-signer-module#signer_confirmrequestwithtoken
        Response body returns a dict containing the request confirmation
        status.
        Parity only.

        :param request_id: ID of request.
        :param gas: (optional) gas provided for the transaction.
        :param gas_price: (optional) gas price for each paid gas.
        :param condition: (optional) conditional submission of transaction.
        :param password: account password or token.
        """
        if password is None:
            raise ValueError("Password or token parameter must be provided.")

        obj = format_request(gas, gas_price, condition)
        return [format_quantity(request_id), obj, password]

    def __signer_generate_authorization_token(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-signer-module#signer_generateauthorizationtoken
        Response body returns the newly created authorization token.
        Parity only.
        """
        return []

    def __signer_generate_web_proxy_access_token(self, domain):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-signer-module#signer_generatewebproxyaccesstoken
        Response body returns the newly created web proxy token.
        Parity only.

        :param domain: domain for which token is valid.
        """
        return [domain]

    def __signer_reject_request(self, request_id):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-signer-module#signer_rejectrequest
        Response body returns if the request rejection was successful.
        Parity only.

        :param request_id: ID for request.
        """
        return [format_quantity(request_id)]

    def __signer_requests_to_confirm(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-signer-module#signer_requeststoconfirm
        Response body returns a list of transactions pending authorization.
        Parity only.
        """
        return []

    def __signer_subscribe_pending(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-signer-module#signer_subscribepending
        Response body returns a newly created subscription ID for pending
        transactions.
        Parity only.
        """
        return []

    def __signer_unsubscribe_pending(self, subscription_id):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-signer-module#signer_unsubscribepending
        Response body returns if the unsubscribe request was successful.
        Parity only.
        """
        return [format_quantity(subscription_id)]

    # TRACE (PARITY ONLY)

    def __trace_block(self, block = DEFAULT_BLOCK):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-trace-module#trace_block
        Response body returns a list of traces created at block.
        Valid tags are {"earliest", "latest", "pending"}.
        Parity only.

        :param block: block number or tag.
        """
        return [format_block(block)]

    def __trace_call(self, from_=None, to=None, gas=None, gas_price=None,
                     value=None, data=None, block=None):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-trace-module#trace_call
        Execute new call and return response body containing a list of
        traces to the call.
        Valid tags are {"earliest", "latest", "pending"}.
        Parity only.

        :param from_: (optional) address of sender.
        :param to: (optional) address of recipient.
        :param gas: (optional) gas provided for the transaction.
        :param gas_price: (optional) gas price for each paid gas.
        :param value: (optional) value to send with transactions.
        :param data: (optional) compile contract data or hash of method.
        :param block: block number or tag to query.
        """
        if block is None:
            raise ValueError("Block parameter must be provided.")
        obj = format_transaction(from_, to, gas, gas_price, value, data)

        return [obj, format_block(block)]

    def __trace_filter(self, from_block=None, to_block=None,
                       address=None, topics=None):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-trace-module#trace_filter
        Response body returns a list of traces matching a filter.
        Valid tags for `from_block` and `to_block` are {"earliest",
        "latest", "pending"}.
        Parity only.

        :param from_block: (optional) block number or tag to query.
        :param to_block: (optional) block number or tag to query.
        :param address: (optional) contract address or list of addresses.
        :param topics: (optional) list of `DATA` topics.
        """
        obj = format_filter(from_block, to_block, address, topics)
        return [obj]

    def __trace_get(self, hash_, index = 0):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-trace-module#trace_get
        Response body returns trace at position.
        Parity only.

        :param hash_: transaction hash.
        :param index: trace index.
        """
        return [hash_, format_quantity(index)]

    def __trace_raw_transaction(self, data, traces):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-trace-module#trace_rawtransaction
        Response body returns traces to `eth_sendRawTransaction` without
        executing transaction.
        Valid trace types are {"vmTrace", "trace", "stateDiff"}.
        Parity only.

        :param data: signed transaction data.
        :param traces: list of trace types (at least 1).
        """
        return [data, list(traces)]

    def __trace_replay_transaction(self, hash_, traces):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-trace-module#trace_replaytransaction
        Response body returns list of traces to the replayed transaction.
        Valid trace types are {"vmTrace", "trace", "stateDiff"}.
        Parity only.

        :param hash_: transaction hash.
        :param traces: list of trace types (at least 1).
        """
        return [hash_, list(traces)]

    def __trace_transaction(self, hash_):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-trace-module#trace_transaction
        Response body returns list of traces to transaction by hash.
        Parity only.

        :param hash_: transaction hash.
        """
        return [hash_]

    # ADMIN

    def __admin_add_peer(self, enode):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#admin_addpeer
        Response body returns if the reserved peer was added.
        Geth only.

        :param enode: address of node.
        """
        return [enode]

    def __admin_datadir(self):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#admin_datadir
        Response body returns the path to data directory.
        Geth only.
        """
        return []

    def __admin_node_info(self):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#admin_nodeinfo
        Response body returns a dict containing node information.
        Geth only.
        """
        return []

    def __admin_peers(self):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#admin_peers
        Response body returns a list of information for all peers.
        Geth only.
        """
        return []

    def __admin_set_solc(self, path):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#admin_setsolc
        Response body returns the version string from the solidity
        compiler.
        Geth only.

        :param path: path to solidity compiler.
        """
        return [path]

    def __admin_start_rpc(self, host = DEFAULT_HOST, port = DEFAULT_HTTP_PORT,
                          cors = DEFAULT_CORS, apis = DEFAULT_APIS):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#admin_startrpc
        Response body returns if the HTTP RPC listener was opened.
        Geth only.

        :param host: network interface for listener.
        :param port: network port for listener.
        :param cors: cross-origin resource sharing header to use.
        :param apis: comma-separated modules to support over interface.
        """
        return [host, format_quantity(port), cors, apis]

    def __admin_start_ws(self, host = DEFAULT_HOST, port = DEFAULT_WS_PORT,
                          cors = DEFAULT_CORS, apis = DEFAULT_APIS):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#admin_startws
        Response body returns if the Websocket RPC listener was opened.
        Geth only.

        :param host: network interface for listener
        :param port: network port for listener
        :param cors: cross-origin resource sharing header to use
        :param apis: comma-separated modules to support over interface
        """
        return [host, format_quantity(port), cors, apis]

    def __admin_stop_rpc(self):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#admin_stoprpc
        Response body returns if the HTTP RPC listener was stopped.
        Geth only.
        """
        return []

    def __admin_stop_ws(self):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#admin_stopws
        Response body returns if the Websocket RPC listener was stopped.
        Geth only.
        """
        return []

    # DEBUG

    def __debug_backtrace_at(self, filename, line):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_backtraceat
        Geth only.

        :param filename: module filename (`server.go`)
        :param line: line in file (`443`)
        """
        return ['{0}:{1}'.format(filename, line)]

    def __debug_block_profile(self, path, seconds):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_blockprofile
        Geth only.

        :param path: path to write profile to
        :param seconds: number of seconds to do block profiling for
        """
        return [path, format_quantity(seconds)]

    def __debug_cpu_profile(self, path, seconds):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_cpuprofile
        Geth only.

        :param path: path to write profile to
        :param seconds: number of seconds to do cpu profiling for
        """
        return [path, format_quantity(seconds)]

    def __debug_dump_block(self, block = DEFAULT_BLOCK):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_dumpblock
        Response body returns a dict that contains account information
        corresponding to the block.
        Valid tags are {"earliest", "latest", "pending"}.
        Geth only.

        :param block: block number or tag.
        """
        return [format_block(block)]

    def __debug_gc_stats(self):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_gcstats
        Response body returns a dict of GC statistics.
        Geth only.
        """
        return []

    def __debug_get_block_rlp(self, block = DEFAULT_BLOCK):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_getblockrlp
        Response body returns the RLP-encoded block.
        Valid tags are {"earliest", "latest", "pending"}.
        Geth only.

        :param block: block number or tag.
        """
        return [format_block(block)]

    def __debug_go_trace(self, path, seconds):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_gotrace
        Geth only.

        :param path: path to write profile to
        :param seconds: number of seconds to do Go runtime tracing for
        """
        return [path, format_quantity(seconds)]

    def __debug_mem_stats(self):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_memstats
        Response body returns a dict of memory statistics.
        Geth only.
        """
        return []

    def __debug_seed_hash(self, block = DEFAULT_BLOCK):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_seedhash
        Response body returns the seed hash by block.
        Valid tags are {"earliest", "latest", "pending"}.
        Geth only.

        :param block: block number or tag.
        """
        return [format_block(block)]

    def __debug_set_head(self, block = DEFAULT_BLOCK):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_sethead
        Set current head of local change. Use with extreme caution.
        Valid tags are {"earliest", "latest", "pending"}.
        Geth only.

        :param block: block number or tag.
        """
        return [format_block(block)]

    def __debug_set_block_profile_rate(self, rate):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_setblockprofilerate
        Set rate of block profile data collection.
        Geth only.

        :param rate: number of samples per second.
        """
        return [format_quantity(rate)]

    def __debug_stacks(self):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_stacks
        Response body returns a dict of all goroutine stacks.
        Geth only.
        """
        return []

    def __debug_start_cpu_profile(self, path):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_startcpuprofile
        Geth only.

        :param path: path to write profile to
        """
        return [path]

    def __debug_start_go_trace(self, path):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_startgotrace
        Geth only.

        :param path: path to write profile to
        """
        return [path]

    def __debug_stop_cpu_profile(self):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_stopcpuprofile
        Geth only.
        """
        return []

    def __debug_stop_go_trace(self):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_stopgotrace
        Geth only.
        """
        return []

    def __debug_trace_block(self, block = DEFAULT_BLOCK, **config):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_traceblock
        Response body returns a full stack trace for transactions in block.
        Valid tags are {"earliest", "latest", "pending"}.
        Geth only.

        :param block: block number or tag.
        :param config: optional keyword arguments for configuration
            disable_memory (default false)
            disable_stack (default false)
            disable_storage (default false)
        """
        return [format_block(block), config]

    def __debug_trace_block_by_number(self, block = DEFAULT_BLOCK, **config):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_traceblockbynumber
        Response body returns a full stack trace for transactions in
        block by number.
        Valid tags are {"earliest", "latest", "pending"}.
        Geth only.

        :param block: block number or tag.
        :param config: optional keyword arguments for configuration
            disable_memory (default false)
            disable_stack (default false)
            disable_storage (default false)
        """
        return [format_block(block), config]

    def __debug_trace_block_by_hash(self, hash_, **config):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_traceblockbyhash
        Response body returns a full stack trace for transactions in
        block by hash.
        Geth only.

        :param hash_: block hash.
        :param config: optional keyword arguments for configuration
            disable_memory (default false)
            disable_stack (default false)
            disable_storage (default false)
        """
        return [hash_, config]

    def __debug_trace_block_from_file(self, path, **config):
        """
        https://github.com/ethereumproject/sputnikvm-dev/wiki/Debug-RPCs#debug_traceblockfromfile
        Response body returns a full stack trace for transactions in
        block by RLP loaded from file.
        Geth only.

        :param path: file containing block RLP.
        :param config: optional keyword arguments for configuration
            disable_memory (default false)
            disable_stack (default false)
            disable_storage (default false)
        """
        return [path, config]

    def __debug_trace_transaction(self, hash_, **config):
        """
        https://github.com/ethereumproject/sputnikvm-dev/wiki/Debug-RPCs#debug_tracetransaction
        Response body returns a full stack trace for a transaction by
        hash.
        Geth only.

        :param hash_: transaction hash.
        :param config: optional keyword arguments for configuration
            disable_memory (default false)
            disable_stack (default false)
            disable_storage (default false)
        """
        return [hash_, config]

    def __debug_verbosity(self, log_level):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_verbosity
        Geth only.

        :param log_level: log up to and including log level.
        """
        return [format_quantity(log_level)]

    def __debug_vmodule(self, log_pattern):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_vmodule
        Geth only.

        :param log_pattern: logging verbosity pattern.
        """
        return [log_pattern]

    def __debug_write_block_profile(self, path):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_writeblockprofile
        Geth only.

        :param path: path to write profile to
        """
        return [path]

    def __debug_write_mem_profile(self, path):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#debug_writememprofile
        Geth only.

        :param path: path to write profile to
        """
        return [path]

    # MINER

    def __miner_set_extra(self, data):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#miner_setextra
        Response body returns if the extra data for mined blocks was
        successfully set.
        Geth only.

        :param data: hex-representation of binary data.
        """
        return [data]

    def __miner_set_gas_price(self, gas_price):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#miner_setgasprice
        Geth only.

        :param gas_price: gas price for each paid gas.
        """
        return [format_quantity(gas_price)]

    def __miner_start(self, threads):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#miner_start
        Geth only.

        :param threads: number of threads for mining process.
        """
        return [format_quantity(threads)]

    def __miner_stop(self):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#miner_stop
        Geth only.
        """
        return []

    def __miner_set_ether_base(self, address):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#miner_setetherbase
        Geth only.

        :param address: account address.
        """
        return [address]

    # TXPOOL

    def __txpool_content(self):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#txpool_content
        Response body returns a dict with information for all pending
        transactions for the next block.
        Geth only.
        """
        return []

    def __txpool_inspect(self):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#txpool_inspect
        Response body returns a dict with brief information for all pending
        transactions for the next block.
        Geth only.
        """
        return []

    def __txpool_status(self):
        """
        https://github.com/ethereum/go-ethereum/wiki/Management-APIs#txpool_status
        Response body returns the number of pending and queued transactions.
        Geth only.
        """
        return []

    # SHH

    def __shh_add_private_key(self, private_key):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-shh-Module#shh_addprivatekey
        Response body returns an identity for the private key.
        Parity only.

        :param private_key: hex-representation of private key.
        """
        return [private_key]

    def __shh_add_sym_key(self, sym_key):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-shh-Module#shh_addsymkey
        Response body returns an identity for the symmetric key.
        Parity only.

        :param sym_key: hex-representation of symmetric key.
        """
        return [sym_key]

    def __shh_add_to_group(self, address):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#shh_addtogroup
        Response body returns a boolean if the identity was successfully
        added to the group.
        Ethereum only.

        :param address: SHH identity address.
        """
        return [address]

    def __shh_delete_key(self, key_id):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-shh-Module#shh_deletekey
        Response body returns a boolean if the key was successfully
        deleted.
        Parity only.

        :param key_id: hex-representation of key ID.
        """
        return [key_id]

    def __shh_delete_message_filter(self, filter_id):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-shh-Module#shh_deletemessagefilter
        Response body returns a boolean if the message filter was
        successfully deleted.
        Parity only.

        :param filter_id: hex-representation of filter ID.
        """
        return [filter_id]

    def __shh_get_filter_changes(self, filter_id):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#shh_getfilterchanges
        Response body returns an list of messages matching the filter
        since last poll.
        Ethereum only.

        :param filter_id: ID for filter to match.
        """
        return [format_quantity(filter_id)]

    def __shh_get_filter_messages(self, filter_id):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-shh-Module#shh_getfiltermessages
        Response body returns a list of messages matching the filter
        since last poll.
        Parity only.

        :param filter_id: hex-representation of filter ID.
        """
        return [filter_id]

    def __shh_get_messages(self, filter_id):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#shh_getmessages
        Response body returns an list of messages matching the filter.
        Ethereum only.

        :param filter_id: ID for filter to match.
        """
        return [format_quantity(filter_id)]

    def __shh_get_private_key(self, key_id):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-shh-Module#shh_getprivatekey
        Response body returns the private key by identity.
        Parity only.

        :param key_id: hex-representation of key ID.
        """
        return [key_id]

    def __shh_get_public_key(self, key_id):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-shh-Module#shh_getpublickey
        Response body returns the public key by identity.
        Parity only.

        :param key_id: hex-representation of key ID.
        """
        return [key_id]

    def __shh_get_sym_key(self, key_id):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-shh-Module#shh_getsymkey
        Response body returns the symmetric key by identity.
        Parity only.

        :param key_id: hex-representation of key ID.
        """
        return [key_id]

    def __shh_has_identity(self, address):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#shh_hasidentity
        Response body returns a boolean if the client holds the private
        keys to the identity.
        Ethereum only.

        :param address: SHH identity address.
        """
        return [address]

    def __shh_info(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-shh-Module#shh_info
        Response body returns info about the whisper node.
        Parity only.
        """
        return []

    def __shh_new_filter(self, topics, to=None):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#shh_newfilter
        Response body returns an identifier to the created filter.
        Ethereum only.

        :param topics: list of `DATA` topics.
        :param to: (optional) recipient SHH identifier.
        """
        obj = {"topics": list(topics)}
        if to is not None:
            obj["to"] = to

        return obj

    def __shh_new_group(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#shh_newgroup
        Response body returns an address to the new group.
        Ethereum only.
        """
        return []

    def __shh_new_identity(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#shh_newidentity
        Response body returns a newly created SSH identifier.
        Ethereum only.
        """
        return []

    def __shh_new_key_pair(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-shh-Module#shh_newkeypair
        Response body returns an identity to the newly created public/
        private key pair.
        Parity only.
        """
        return []

    def __shh_new_message_filter(self, topics, decrypt_with=None, from_=None):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-shh-Module#shh_newmessagefilter
        Response body returns a newly created filter ID.
        Parity only.

        :param topics: list of `DATA` topics to identify messages.
        :param decrypt_with: (optional) key ID for description.
        :param from_: (optional) only accept messages signed by this key.
        """
        obj = format_message_filter(topics, decrypt_with, from_)
        return [obj]

    def __shh_new_sym_key(self):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-shh-Module#shh_newsymkey
        Response body returns an identity to the newly created symmetric
        key.
        Parity only.
        """
        return []

    def __shh_post(self, topics, payload, priority, ttl, from_=None, to=None):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#shh_post
        Response body returns a boolean if the message was sent.

        :param topics: list of `DATA` topics to identify messages.
        :param payload: message body.
        :param priority: priority value.
        :param ttl: time-to-live in seconds.
        :param from_: (optional) sender SHH identifier.
        :param to: (optional) recipient SHH identifier.
        """
        obj = format_shh(topics, payload, priority, ttl, from_, to)
        return [obj]

    def __shh_subscribe(self, topics, decrypt_with=None, from_=None):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-shh-Module#shh_subscribe
        Response body returns a subscription ID.
        Parity only.

        :param topics: list of `DATA` topics to identify messages.
        :param decrypt_with: (optional) key ID for description.
        :param from_: (optional) only accept messages signed by this key.
        """
        obj = format_message_filter(topics, decrypt_with, from_)
        return [obj]

    def __shh_uninstall_filter(self, filter_id):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#shh_uninstallfilter
        Response body returns a boolean if the filter was successfully
        uninstalled.
        Ethereum only.

        :param filter_id: ID for filter to uninstall.
        """
        return [format_quantity(filter_id)]

    def __shh_unsubscribe(self, subscription_id):
        """
        https://github.com/paritytech/parity/wiki/JSONRPC-shh-Module#shh_unsubscribe
        Response body returns if the unsubscribe request was successful.
        Parity only.

        :param subscription_id: ID for subscription to unsubscribe.
        """
        return [format_quantity(subscription_id)]

    def __shh_version(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#shh_version
        Response body returns the whisper protocol version.
        Ethereum only.
        """
        return []

# DISPATCH
# --------


CLIENT_METHODS = [
    ('web3_client_version', 'web3_clientVersion', 67),
    ('web3_sha3', 'web3_sha3', 64),
    ('net_listening', 'net_listening', 67),
    ('net_peer_count', 'net_peerCount', 74),
    ('net_version', 'net_version', 67),
    ('eth_accounts', 'eth_accounts', 1),
    ('eth_block_number', 'eth_blockNumber', 83),
    ('eth_call', 'eth_call', 1),
    ('eth_coinbase', 'eth_coinbase', 64),
    ('eth_compile_lll', 'eth_compileLLL', 1),
    ('eth_compile_serpent', 'eth_compileSerpent', 1),
    ('eth_compile_solidity', 'eth_compileSolidity', 1),
    ('eth_estimate_gas', 'eth_estimateGas', 1),
    ('eth_gas_price', 'eth_gasPrice', 73),
    ('eth_get_balance', 'eth_getBalance', 1),
    ('eth_get_block_by_hash', 'eth_getBlockByHash', 1),
    ('eth_get_block_by_number', 'eth_getBlockByNumber', 1),
    ('eth_get_block_transaction_count_by_hash', 'eth_getBlockTransactionCountByHash', 1),
    ('eth_get_block_transaction_count_by_number', 'eth_getBlockTransactionCountByNumber', 1),
    ('eth_get_code', 'eth_getCode', 1),
    ('eth_get_compilers', 'eth_getCompilers', 1),
    ('eth_get_filter_changes', 'eth_getFilterChanges', 73),
    ('eth_get_filter_logs', 'eth_getFilterLogs', 73),
    ('eth_get_logs', 'eth_getLogs', 73),
    ('eth_get_storage_at', 'eth_getStorageAt', 1),
    ('eth_get_transaction_by_block_hash_and_index', 'eth_getTransactionByBlockHashAndIndex', 1),
    ('eth_get_transaction_by_block_number_and_index', 'eth_getTransactionByBlockNumberAndIndex', 1),
    ('eth_get_transaction_by_hash', 'eth_getTransactionByHash', 1),
    ('eth_get_transaction_count', 'eth_getTransactionCount', 1),
    ('eth_get_transaction_receipt', 'eth_getTransactionReceipt', 1),
    ('eth_get_uncle_by_block_hash_and_index', 'eth_getUncleByBlockHashAndIndex', 1),
    ('eth_get_uncle_by_block_number_and_index', 'eth_getUncleByBlockNumberAndIndex', 1),
    ('eth_get_uncle_count_by_block_hash', 'eth_getUncleCountByBlockHash', 1),
    ('eth_get_uncle_count_by_block_number', 'eth_getUncleCountByBlockNumber', 1),
    ('eth_get_work', 'eth_getWork', 73),
    ('eth_hashrate', 'eth_hashrate', 71),
    ('eth_mining', 'eth_mining', 71),
    ('eth_new_block_filter', 'eth_newBlockFilter', 73),
    ('eth_new_filter', 'eth_newFilter', 73),
    ('eth_new_pending_transaction_filter', 'eth_newPendingTransactionFilter', 73),
    ('eth_protocol_version', 'eth_protocolVersion', 67),
    ('eth_send_raw_transaction', 'eth_sendRawTransaction', 1),
    ('eth_send_transaction', 'eth_sendTransaction', 1),
    ('eth_sign', 'eth_sign', 1),
    ('eth_sign_transaction', 'eth_signTransaction', 1),
    ('eth_submit_hashrate', 'eth_submitHashrate', 73),
    ('eth_submit_work', 'eth_submitWork', 73),
    ('eth_syncing', 'eth_syncing', 1),
    ('eth_uninstall_filter', 'eth_uninstallFilter', 73),
    ('eth_subscribe', 'eth_subscribe', 1),
    ('eth_unsubscribe', 'eth_unsubscribe', 1),
    ('personal_ec_recover', 'personal_ecRecover', 1),
    ('personal_import_raw_key', 'personal_importRawKey', 1),
    ('personal_list_accounts', 'personal_listAccounts', 1),
    ('personal_lock_account', 'personal_lockAccount', 1),
    ('personal_new_account', 'personal_newAccount', 1),
    ('personal_send_transaction', 'personal_sendTransaction', 1),
    ('personal_sign', 'personal_sign', 1),
    ('personal_unlock_account', 'personal_unlockAccount', 1),
    ('parity_accounts_info', 'parity_accountsInfo', 1),
    ('parity_chain', 'parity_chain', 1),
    ('parity_chain_status', 'parity_chainStatus', 1),
    ('parity_change_vault', 'parity_changeVault', 1),
    ('parity_change_vault_password', 'parity_changeVaultPassword', 1),
    ('parity_check_request', 'parity_checkRequest', 1),
    ('parity_cid_v0', 'parity_cidV0', 1),
    ('parity_close_vault', 'parity_closeVault', 1),
    ('parity_compose_transaction', 'parity_composeTransaction', 1),
    ('parity_consensus_capability', 'parity_consensusCapability', 1),
    ('parity_dapps_url', 'parity_dappsUrl', 1),
    ('parity_decrypt_message', 'parity_decryptMessage', 1),
    ('parity_default_account', 'parity_defaultAccount', 1),
    ('parity_default_extra_data', 'parity_defaultExtraData', 1),
    ('parity_dev_logs', 'parity_devLogs', 1),
    ('parity_dev_logs_levels', 'parity_devLogsLevels', 1),
    ('parity_encrypt_message', 'parity_encryptMessage', 1),
    ('parity_enode', 'parity_enode', 1),
    ('parity_extra_data', 'parity_extraData', 1),
    ('parity_future_transactions', 'parity_futureTransactions', 1),
    ('parity_gas_ceil_target', 'parity_gasCeilTarget', 1),
    ('parity_gas_floor_target', 'parity_gasFloorTarget', 1),
    ('parity_gas_price_histogram', 'parity_gasPriceHistogram', 1),
    ('parity_generate_secret_phrase', 'parity_generateSecretPhrase', 1),
    ('parity_get_block_header_by_number', 'parity_getBlockHeaderByNumber', 1),
    ('parity_get_vault_meta', 'parity_getVaultMeta', 1),
    ('parity_hardware_accounts_info', 'parity_hardwareAccountsInfo', 1),
    ('parity_list_accounts', 'parity_listAccounts', 1),
    ('parity_list_opened_vaults', 'parity_listOpenedVaults', 1),
    ('parity_list_storage_keys', 'parity_listStorageKeys', 1),
    ('parity_list_vaults', 'parity_listVaults', 1),
    ('parity_local_transactions', 'parity_localTransactions', 1),
    ('parity_min_gas_price', 'parity_minGasPrice', 1),
    ('parity_mode', 'parity_mode', 1),
    ('parity_new_vault', 'parity_newVault', 1),
    ('parity_net_chain', 'parity_netChain', 1),
    ('parity_net_peers', 'parity_netPeers', 1),
    ('parity_net_port', 'parity_netPort', 1),
    ('parity_next_nonce', 'parity_nextNonce', 1),
    ('parity_node_kind', 'parity_nodeKind', 1),
    ('parity_node_name', 'parity_nodeName', 1),
    ('parity_pending_transactions', 'parity_pendingTransactions', 1),
    ('parity_pending_transactions_stats', 'parity_pendingTransactionsStats', 1),
    ('parity_phrase_to_address', 'parity_phraseToAddress', 1),
    ('parity_open_vault', 'parity_openVault', 1),
    ('parity_post_sign', 'parity_postSign', 1),
    ('parity_post_transaction', 'parity_postTransaction', 1),
    ('parity_registry_address', 'parity_registryAddress', 1),
    ('parity_releases_info', 'parity_releasesInfo', 1),
    ('parity_remove_transaction', 'parity_removeTransaction', 1),
    ('parity_rpc_settings', 'parity_rpcSettings', 1),
    ('parity_set_vault_meta', 'parity_setVaultMeta', 1),
    ('parity_sign_message', 'parity_signMessage', 1),
    ('parity_transactions_limit', 'parity_transactionsLimit', 1),
    ('parity_unsigned_transactions_count', 'parity_unsignedTransactionsCount', 1),
    ('parity_version_info', 'parity_versionInfo', 1),
    ('parity_ws_url', 'parity_wsUrl', 1),
    ('parity_accept_non_reserved_peers', 'parity_acceptNonReservedPeers', 1),
    ('parity_add_reserved_peer', 'parity_addReservedPeer', 1),
    ('parity_dapps_list', 'parity_dappsList', 1),
    ('parity_drop_non_reserved_peers', 'parity_dropNonReservedPeers', 1),
    ('parity_execute_upgrade', 'parity_executeUpgrade', 1),
    ('parity_hash_content', 'parity_hashContent', 1),
    ('parity_remove_reserved_peer', 'parity_removeReservedPeer', 1),
    ('parity_set_author', 'parity_setAuthor', 1),
    ('parity_set_chain', 'parity_setChain', 1),
    ('parity_set_engine_signer', 'parity_setEngineSigner', 1),
    ('parity_set_extra_data', 'parity_setExtraData', 1),
    ('parity_set_gas_ceil_target', 'parity_setGasCeilTarget', 1),
    ('parity_set_gas_floor_target', 'parity_setGasFloorTarget', 1),
    ('parity_set_max_transaction_gas', 'parity_setMaxTransactionGas', 1),
    ('parity_set_min_gas_price', 'parity_setMinGasPrice', 1),
    ('parity_set_mode', 'parity_setMode', 1),
    ('parity_set_transactions_limit', 'parity_setTransactionsLimit', 1),
    ('parity_upgrade_ready', 'parity_upgradeReady', 1),
    ('parity_subscribe', 'parity_subscribe', 1),
    ('parity_unsubscribe', 'parity_unsubscribe', 1),
    ('parity_all_accounts_info', 'parity_allAccountsInfo', 1),
    ('parity_change_password', 'parity_changePassword', 1),
    ('parity_derive_address_hash', 'parity_deriveAddressHash', 1),
    ('parity_derive_address_index', 'parity_deriveAddressIndex', 1),
    ('parity_export_account', 'parity_exportAccount', 1),
    ('parity_get_dapp_addresses', 'parity_getDappAddresses', 1),
    ('parity_get_dapp_default_address', 'parity_getDappDefaultAddress', 1),
    ('parity_get_new_dapps_addresses', 'parity_getNewDappsAddresses', 1),
    ('parity_get_new_dapps_default_address', 'parity_getNewDappsDefaultAddress', 1),
    ('parity_import_geth_accounts', 'parity_importGethAccounts', 1),
    ('parity_kill_account', 'parity_killAccount', 1),
    ('parity_list_geth_accounts', 'parity_listGethAccounts', 1),
    ('parity_list_recent_dapps', 'parity_listRecentDapps', 1),
    ('parity_new_account_from_phrase', 'parity_newAccountFromPhrase', 1),
    ('parity_new_account_from_secret', 'parity_newAccountFromSecret', 1),
    ('parity_new_account_from_wallet', 'parity_newAccountFromWallet', 1),
    ('parity_remove_address', 'parity_removeAddress', 1),
    ('parity_set_account_meta', 'parity_setAccountMeta', 1),
    ('parity_set_account_name', 'parity_setAccountName', 1),
    ('parity_set_dapp_addresses', 'parity_setDappAddresses', 1),
    ('parity_set_dapp_default_address', 'parity_setDappDefaultAddress', 1),
    ('parity_set_new_dapps_addresses', 'parity_setNewDappsAddresses', 1),
    ('parity_set_new_dapps_default_address', 'parity_setNewDappsDefaultAddress', 1),
    ('parity_test_password', 'parity_testPassword', 1),
    ('signer_confirm_request', 'signer_confirmRequest', 1),
    ('signer_confirm_request_raw', 'signer_confirmRequestRaw', 1),
    ('signer_confirm_request_with_token', 'signer_confirmRequestWithToken', 1),
    ('signer_generate_authorization_token', 'signer_generateAuthorizationToken', 1),
    ('signer_generate_web_proxy_access_token', 'signer_generateWebProxyAccessToken', 1),
    ('signer_reject_request', 'signer_rejectRequest', 1),
    ('signer_requests_to_confirm', 'signer_requestsToConfirm', 1),
    ('signer_subscribe_pending', 'signer_subscribePending', 1),
    ('signer_unsubscribe_pending', 'signer_unsubscribePending', 1),
    ('trace_block', 'trace_block', 1),
    ('trace_call', 'trace_call', 1),
    ('trace_filter', 'trace_filter', 1),
    ('trace_get', 'trace_get', 1),
    ('trace_raw_transaction', 'trace_RawTransaction', 1),
    ('trace_replay_transaction', 'trace_replayTransaction', 1),
    ('trace_transaction', 'trace_transaction', 1),
    ('admin_add_peer', 'admin_addPeer', 1),
    ('admin_datadir', 'admin_datadir', 1),
    ('admin_node_info', 'admin_nodeInfo', 1),
    ('admin_peers', 'admin_peers', 1),
    ('admin_set_solc', 'admin_setSolc', 1),
    ('admin_start_rpc', 'admin_startRPC', 1),
    ('admin_start_ws', 'admin_startWS', 1),
    ('admin_stop_rpc', 'admin_stopRPC', 1),
    ('admin_stop_ws', 'admin_stopWS', 1),
    ('debug_backtrace_at', 'debug_backtraceAt', 1),
    ('debug_block_profile', 'debug_blockProfile', 1),
    ('debug_cpu_profile', 'debug_cpuProfile', 1),
    ('debug_dump_block', 'debug_dumpBlock', 1),
    ('debug_gc_stats', 'debug_gcStats', 1),
    ('debug_get_block_rlp', 'debug_getBlockRlp', 1),
    ('debug_go_trace', 'debug_goTrace', 1),
    ('debug_mem_stats', 'debug_memStats', 1),
    ('debug_seed_hash', 'debug_seedHash', 1),
    ('debug_set_head', 'debug_setHead', 1),
    ('debug_set_block_profile_rate', 'debug_setBlockProfileRate', 1),
    ('debug_stacks', 'debug_stacks', 1),
    ('debug_start_cpu_profile', 'debug_startCPUProfile', 1),
    ('debug_start_go_trace', 'debug_startGoTrace', 1),
    ('debug_stop_cpu_profile', 'debug_stopCPUProfile', 1),
    ('debug_stop_go_trace', 'debug_stopGoTrace', 1),
    ('debug_trace_block', 'debug_traceBlock', 1),
    ('debug_trace_block_by_number', 'debug_traceBlockByNumber', 1),
    ('debug_trace_block_by_hash', 'debug_traceBlockByHash', 1),
    ('debug_trace_block_from_file', 'debug_traceBlockFromFile', 1),
    ('debug_trace_transaction', 'debug_traceTransaction', 1),
    ('debug_verbosity', 'debug_verbosity', 1),
    ('debug_vmodule', 'debug_vmodule', 1),
    ('debug_write_block_profile', 'debug_writeBlockProfile', 1),
    ('debug_write_mem_profile', 'debug_writeMemProfile', 1),
    ('miner_set_extra', 'miner_setExtra', 1),
    ('miner_set_gas_price', 'miner_setGasPrice', 1),
    ('miner_start', 'miner_start', 1),
    ('miner_stop', 'miner_stop', 1),
    ('miner_set_ether_base', 'miner_setEtherBase', 1),
    ('txpool_content', 'txpool_content', 1),
    ('txpool_inspect', 'txpool_inspect', 1),
    ('txpool_status', 'txpool_status', 1),
    ('shh_add_private_key', 'shh_addPrivateKey', 1),
    ('shh_add_sym_key', 'shh_addSymKey', 1),
    ('shh_add_to_group', 'shh_addToGroup', 73),
    ('shh_delete_key', 'shh_deleteKey', 1),
    ('shh_delete_message_filter', 'shh_deleteMessageFilter', 1),
    ('shh_get_filter_changes', 'shh_getFilterChanges', 73),
    ('shh_get_filter_messages', 'shh_getFilterMessages', 1),
    ('shh_get_messages', 'shh_getMessages', 73),
    ('shh_get_private_key', 'shh_getPrivateKey', 1),
    ('shh_get_public_key', 'shh_getPublicKey', 1),
    ('shh_get_sym_key', 'shh_getSymKey', 1),
    ('shh_has_identity', 'shh_hasIdentity', 73),
    ('shh_info', 'shh_info', 1),
    ('shh_new_filter', 'shh_newFilter', 73),
    ('shh_new_group', 'shh_newGroup', 73),
    ('shh_new_identity', 'shh_newIdentity', 73),
    ('shh_new_key_pair', 'shh_newKeyPair', 1),
    ('shh_new_message_filter', 'shh_newMessageFilter', 1),
    ('shh_new_sym_key', 'shh_newSymKey', 1),
    ('shh_post', 'shh_post', 73),
    ('shh_subscribe', 'shh_subscribe', 1),
    ('shh_uninstall_filter', 'shh_uninstallFilter', 73),
    ('shh_unsubscribe', 'shh_unsubscribe', 1),
    ('shh_version', 'shh_version', 67),
]

for _args in CLIENT_METHODS:
    AbstractClient._AbstractClient__method(*_args)
