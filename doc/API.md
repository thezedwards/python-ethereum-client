# API Documentation

API documentation for the Ethereum JSON RPC Python client. The Python client supports both the RPC method name and a PEP8-compliant name for method dispatch.

**Table Of Contents**

- [Data](#data)
- [Client](#client)
- [AsyncioClient](#asyncioclient)
- [Core](#core)
  - [Web3](#web3)
  - [Net](#net)
  - [Eth](#eth)
  - [Eth Pubsub](#eth-pubsub)
  - [Personal](#personal)
  - [Parity](#parity)
  - [Parity Accounts](#parity-accounts)
  - [Parity Set](#parity-set)
  - [Pubsub](#pubsub)
  - [Signer](#signer)
  - [Trace](#trace)
  - [Admin](#admin)
  - [Debug](#debug)
  - [Miner](#miner)
  - [Txpool](#txpool)
  - [SHH](#shh)

# Client

`Client` is the default client, making synchronous requests to the JSON RPC API, and supports the HTTP protocol. Each `Client` method returns a `requests.Response` object, which may be queried for the request status, body, and other information.

# AsyncioClient

`AsyncioClient` is the asynchronous client for the JSON RPC API, and supports both the HTTP and Websockets (Parity-only) protocols. Each `AsyncioClient` method returns a couroutine to `aiohttp.ClientResponse` object, which may be queried for the request status, body, and other information (all of which return coroutines).

# Core

The core module describes the shared methods between `Client` and `AsyncioClient`, part of the public API.

## Local

Local functions to facilitate API use.

**Variables:**

- **LOCALHOST_HTTP_ENDPOINT**: Default endpoint using localhost.
- **DEFAULT_BLOCK**: Latest block specifier.
- **DEFAULT_CORS**: Default cross-origin resource sharing string.
- **DEFAULT_HOST**: Default host for endpoint.
- **DEFAULT_HTTP_PORT**: Default port for HTTP endpoint.
- **DEFAULT_WS_PORT**: Default port for Websocket endpoint.

**Functions:**

- **map_position**(_key_, _position_)  
    Get storage lookup position from map position and key.
    - **key**: key for value in map
    - **position**: map position

**Methods:**

- **rpc_name**(_self_, _name_):
    Get JSON-RPC API method name.
    - **name**: Python or JSON-RPC API method name

- **python_name**(_self_, _name_):
    Get Python API method name.
    - **name**: Python or JSON-RPC API method name

## Web3

Core Web3 helper methods.

**Methods:**

- **web3_client_version**(_self_)  
  **web3_clientVersion**(_self_)  
    Get client version.

- **web3_sha3**(_self_, _string_)  
    Get Keccak-256 hash of string.
    - **string**: string to hash

## Net

Network information methods.

**Methods:**

- **net_listening**(_self_)  
    Get if client is actively listening for connections.

- **net_peer_count**(_self_)  
  **net_peerCount**(_self_)  
    Get number of peers connected to client.

- **net_version**(_self_)  
    Get network identifier.

## Eth

**Methods:**

- **eth_accounts**(_self_)  
    Get list of addresses owned by the client.

- **eth_block_number**(_self_)  
  **eth_blockNumber**(_self_)  
    Get the most recent block identifier.

- **eth_call**(_self_, _from__=None, _to_=None, _gas_=None, _gas_price_=None, _value_=None, _data_=None, _block_=None)  
    Get the value of the executed contract.
    - **from**: (optional) address of sender
    - **to**: address of recipient
    - **gas**: (optional) gas provided for the transaction
    - **gas_price**: (optional) gas price for each paid gas
    - **value**: (optional) value to send with transactions
    - **data**: (optional) compile contract data or hash of method
    - **block**: block number or tag to query

- **eth_coinbase**(_self_)  
    Get the client coinbase address.

- **eth_compile_lll**(_self_, _code_)  
  **eth_compileLLL**(_self_, _code_)  
    Get compiled LLL code (Ethereum only).
    - **code**: LLL source code to compile

- **eth_compile_serpent**(_self_, _code_)  
  **eth_compileSerpent**(_self_, _code_)  
    Get compiled Serpent code (Ethereum only).
    - **code**: Serpent source code to compile

- **eth_compile_solidity**(_self_, _code_)  
  **eth_compileSolidity**(_self_, _code_)  
    Get compiled Solidity code (Ethereum only).
    - **code**: Solidity source code to compile

- **eth_estimate_gas**(_self_, _from__=None, _to_=None, _gas_=None, _gas_price_=None, _value_=None, _data_=None)  
  **eth_estimateGas**(_self_, _from__=None, _to_=None, _gas_=None, _gas_price_=None, _value_=None, _data_=None)  
    Get estimated quantity of gas used for contract.
    - **from**: (optional) address of sender
    - **to**: address of recipient
    - **gas**: (optional) gas provided for the transaction
    - **gas_price**: (optional) gas price for each paid gas
    - **value**: (optional) value to send with transactions
    - **data**: (optional) compile contract data or hash of method

- **eth_gas_price**(_self_)  
  **eth_gasPrice**(_self_)  
    Get the current gas price.

- **eth_get_balance**(_self_, _address_, _block_ = DEFAULT_BLOCK)  
  **eth_getBalance**(_self_, _address_, _block_ = DEFAULT_BLOCK)  
    Get the balance of the address.
    - **address**: address of account
    - **block**: block number or tag to query

- **eth_get_block_by_hash**(_self_, _hash__, _use_full_ = False)  
  **eth_getBlockByHash**(_self_, _hash__, _use_full_ = False)  
    Get block information by hash.
    - **hash_**: block hash
    - **use_full**: return full transaction objects

- **eth_get_block_by_number**(_self_, _block_ = DEFAULT_BLOCK, _use_full_ = False)  
  **eth_getBlockByNumber**(_self_, _block_ = DEFAULT_BLOCK, _use_full_ = False)  
    Get block information by number.
    - **block**: block number or tag
    - **use_full**: return full transaction objects

- **eth_get_block_transaction_count_by_hash**(_self_, _hash__)  
  **eth_getBlockTransactionCountByHash**(_self_, _hash__)  
    Get number of transactions in block by hash.
    - **hash_**: block hash

- **eth_get_block_transaction_count_by_number**(_self_, _block_ = DEFAULT_BLOCK)  
  **eth_getBlockTransactionCountByNumber**(_self_, _block_ = DEFAULT_BLOCK)  
    Get number of transactions in block by number.
    - **block**: block number or tag

- **eth_get_code**(_self_, _address_, _block_ = DEFAULT_BLOCK)  
  **eth_getCode**(_self_, _address_, _block_ = DEFAULT_BLOCK)  
    Get the code at a given address.
    - **address**: address of account
    - **block**: block number or tag to query

- **eth_get_compilers**(_self_)  
  **eth_getCompilers**(_self_)  
    Get list of available compilers (Ethereum only).

- **eth_get_filter_changes**(_self_, _filter_id_)  
  **eth_getFilterChanges**(_self_, _filter_id_)  
    Get list of logs matching filter ID since the last poll.
    - **filter_id**: ID of filter to poll

- **eth_get_filter_logs**(_self_, _filter_id_)  
  **eth_getFilterLogs**(_self_, _filter_id_)  
    Get list of all logs matching filter ID.
    - **filter_id**: ID of filter to poll

- **eth_get_logs**(_self_, _from_block_=None, _to_block_=None, _address_=None, _topics_=None)  
  **eth_getLogs**(_self_, _from_block_=None, _to_block_=None, _address_=None, _topics_=None)  
    Get list of all logs matching a filter.
    - **from_block**: (optional) block number or tag to query
    - **to_block**: (optional) block number or tag to query
    - **address**: (optional) contract address or list of addresses
    - **topics**: (optional) list of `DATA` topics

- **eth_get_storage_at**(_self_, _address_, _position_, _block_ = DEFAULT_BLOCK)  
  **eth_getStorageAt**(_self_, _address_, _position_, _block_ = DEFAULT_BLOCK)  
    Get list of all logs matching a filter.
    - **address**: address of account
    - **position**: position in the storage
    - **block**: block number or tag to query

- **eth_get_transaction_by_block_hash_and_index**(_self_, _hash__, _index_=0)  
  **eth_getTransactionByBlockHashAndIndex**(_self_, _hash__, _index_=0)  
    Get transaction information by block hash and transaction index.
    - **hash_**: block hash
    - **index**: transaction index

- **eth_get_transaction_by_block_number_and_index**(_self_, _block_ = DEFAULT_BLOCK, _index_=0)  
  **eth_getTransactionByBlockNumberAndIndex**(_self_, _block_ = DEFAULT_BLOCK, _index_=0)  
    Get transaction information by block number and transaction index.
    - **block**: block number or tag
    - **index**: transaction index

- **eth_get_transaction_by_hash**(_self_, _hash__)  
  **eth_getTransactionByHash**(_self_, _hash__)  
    Get transaction information by hash.
    - **hash_**: transaction hash

- **eth_get_transaction_count**(_self_, _address_, _block_ = DEFAULT_BLOCK)  
  **eth_getTransactionCount**(_self_, _address_, _block_ = DEFAULT_BLOCK)  
    Get number of transactions sent from address.
    - **address**: address of account
    - **block**: block number or tag to query

- **eth_get_transaction_receipt**(_self_, _hash__)  
  **eth_getTransactionReceipt**(_self_, _hash__)  
    Get receipt about transaction by hash.
    - **hash_**: transaction hash

- **eth_get_uncle_by_block_hash_and_index**(_self_, _hash__, _index_=0)  
  **eth_getUncleByBlockHashAndIndex**(_self_, _hash__, _index_=0)  
    Get uncle information by block hash and uncle index.
    - **hash_**: block hash
    - **index**: uncle index

- **eth_get_uncle_by_block_number_and_index**(_self_, _block_ = DEFAULT_BLOCK, _index_=0)  
  **eth_getUncleByBlockNumberAndIndex**(_self_, _block_ = DEFAULT_BLOCK, _index_=0)  
    Get uncle information by block number and uncle index.
    - **block**: block number or tag
    - **index**: uncle index

- **eth_get_uncle_count_by_block_hash**(_self_, _hash__)  
  **eth_getUncleCountByBlockHash**(_self_, _hash__)  
    Get number of unckes by block hash.
    - **hash_**: block hash

- **eth_get_uncle_count_by_block_number**(_self_, _block_ = DEFAULT_BLOCK)  
  **eth_getUncleCountByBlockNumber**(_self_, _block_ = DEFAULT_BLOCK)  
    Get number of unckes by block number.
    - **block**: block number or tag

- **eth_get_work**(_self_)  
  **eth_getWork**(_self_)  
    Get current block, seed hash, and boundary condition.

- **eth_hashrate**(_self_)  
    Get the number of hashes per second the node is mining.

- **eth_mining**(_self_)  
    Get if the node is actively mining.

- **eth_new_block_filter**(_self_)  
  **eth_newBlockFilter**(_self_)  
    Create and return ID to new block filter.

- **eth_new_filter**(_self_, _from_block_=None, _to_block_=None, _address_=None, _topics_=None)  
  **eth_newFilter**(_self_, _from_block_=None, _to_block_=None, _address_=None, _topics_=None)  
    Create and return ID to new filter.
    - **from_block**: (optional) block number or tag to query
    - **to_block**: (optional) block number or tag to query
    - **address**: (optional) contract address or list of addresses
    - **topics**: (optional) list of `DATA` topics

- **eth_new_pending_transaction_filter**(_self_)  
  **eth_newPendingTransactionFilter**(_self_)  
    Create and return ID to new pending transaction filter.

- **eth_protocol_version**(_self_)  
  **eth_protocolVersion**(_self_)  
    Get the current Ethereum protocol version.

- **eth_send_raw_transaction**(_self_, _data_)  
  **eth_sendRawTransaction**(_self_, _data_)  
    Post raw transaction, returning the hash to the new transaction.
    - **data**: signed transaction data

- **eth_send_transaction**(_self_, _from_, _to_=None, _gas_=None, _gas_price_=None, _value_=None, _data_=None, _nonce_=None)  
  **eth_sendTransaction**(_self_, _from_, _to_=None, _gas_=None, _gas_price_=None, _value_=None, _data_=None, _nonce_=None)  
    Create and post transaction, returning the hash to the new transaction.
    - **from**: address of sender
    - **to**: (optional) address of recipient
    - **gas**: (optional) gas provided for the transaction
    - **gas_price**: (optional) gas price for each paid gas
    - **value**: (optional) value to send with transactions
    - **data**: (optional) compile contract data or hash of method
    - **nonce**: (optional) user-provided nonce to override transactions

- **eth_sign**(_self_, _address_, _message_)  
    Get uncle information by block number and uncle index.
    - **address**: address of account
    - **message**: message to sign

- **eth_sign_transaction**(_self_, _from_, _to_=None, _gas_=None, _gas_price_=None, _value_=None, _data_=None, _nonce_=None, _condition_=None)  
  **eth_signTransaction**(_self_, _from_, _to_=None, _gas_=None, _gas_price_=None, _value_=None, _data_=None, _nonce_=None, _condition_=None)  
    Create but do not post transaction, returning the signed transaction data (Parity only).
    - **from**: address of sender
    - **to**: (optional) address of recipient
    - **gas**: (optional) gas provided for the transaction
    - **gas_price**: (optional) gas price for each paid gas
    - **value**: (optional) value to send with transactions
    - **data**: (optional) compile contract data or hash of method
    - **nonce**: (optional) user-provided nonce to override transactions
    - **condition**: (optional) conditional submission of transaction

- **eth_submit_hash_rate**(_self_, _hash_rate_, _client_id_)  
  **eth_submitHashrate**(_self_, _hash_rate_, _client_id_)  
    Submit hash rate and get if submission was valid.
    - **hash_rate**: number of hashes per second
    - **client_id**: random hex string identifying client

- **eth_submit_work**(_self_, _nonce_, _pow_hash_, _mix_digest_)  
  **eth_submitWork**(_self_, _nonce_, _pow_hash_, _mix_digest_)  
    Submit proof of work and get if submission was valid.
    - **nonce**: nonce found
    - **pow_hash**: proof of work hash
    - **mix_digest**: mix digest

- **eth_syncing**(_self_)  
    Get data about the sync status.

- **eth_uninstall_filter**(_self_, _filter_id_)  
  **eth_uninstallFilter**(_self_, _filter_id_)  
    Uninstall filter by ID and get if uninstallation was successful.
    - **filter_id**: ID of filter to poll

# Eth Pubsub

**Methods:**

- **eth_subscribe**(_self_, _type__, _from_block_=None, _to_block_=None, _address_=None, _topics_=None)  
    Create subscription to a filter, returning the subscription ID (Parity only).
    - **type_**: subscription type ({'logs', 'newHeads'})
    - **from_block**: (optional) block number or tag to query
    - **to_block**: (optional) block number or tag to query
    - **address**: (optional) contract address or list of addresses
    - **topics**: (optional) list of `DATA` topics

- **eth_unsubscribe**(_self_, _subscription_id_)  
    Unsubscribe by subscription ID and get if request was successful (Parity only).
    - **subscription_id**: ID for subscription to unsubscribe

# Personal

**Methods:**

- **personal_ec_recover**(_self_, _message_, _signature_)  
  **personal_ecRecover**(_self_, _message_, _signature_)  
    Get address used to sign message (Parity/Geth only).
    - **message**: hex representation of message
    - **signature**: signature generated via `personal_sign`

- **personal_import_raw_key**(_self_, _private_key_, _password_)  
  **personal_importRawKey**(_self_, _private_key_, _password_)  
    Import raw key and encrypt it with password and get address of newly created account (Geth only).
    - **private_key**: hex-representation of private key
    - **password**: account password

- **personal_list_accounts**(_self_)  
  **personal_listAccounts**(_self_)  
    Get list of all locally-stored account addresses (Parity/Geth only).

- **personal_lock_account**(_self_, _address_)
  **personal_lockAccount**(_self_, _address_)
    Lock account by address (Geth only).
    - **address**: address of account

- **personal_new_account**(_self_, _password_)  
  **personal_newAccount**(_self_, _password_)  
    Create new account and get the account address (Parity/Geth only).
    - **password**: account password

- **personal_send_transaction**(_self_, _from_, _to_=None, _gas_=None, _gas_price_=None, _value_=None, _data_=None, _nonce_=None, _condition_=None, _password_=None)
  **personal_sendTransaction**(_self_, _from_, _to_=None, _gas_=None, _gas_price_=None, _value_=None, _data_=None, _nonce_=None, _condition_=None, _password_=None)
    Create and post transaction, returning the hash to the new transaction (Parity only).
    - **from**: address of sender
    - **to**: (optional) address of recipient
    - **gas**: (optional) gas provided for the transaction
    - **gas_price**: (optional) gas price for each paid gas
    - **value**: (optional) value to send with transactions
    - **data**: (optional) compile contract data or hash of method
    - **nonce**: (optional) user-provided nonce to override transactions
    - **condition**: (optional) conditional submission of transaction
    - **password**: account password

- **personal_sign**(_self_, _message_, _address_, _password_)  
    Sign message and get signature (Geth only).
    - **message**: hex representation of message
    - **address**: address of account
    - **password**: account password

- **personal_unlock_account**(_self_, _adddress_, _password_, _duration_=None)
  **personal_unlockAccount**(_self_, _adddress_, _password_, _duration_=None)
    Unlock account and get if the account was successfully unlocked (Parity only).
    - **address**: address of account
    - **password**: account password
    - **duration**: (optional) duration in seconds to unlock account for

# Parity

**Methods:**

- **parity_accounts_info**(_self_)  
  **parity_accountsInfo**(_self_)  
    Get metadata about the release status (Parity only).

- **parity_chain**(_self_)  
    Get name of connected chain (Parity only).

- **parity_chain_status**(_self_)  
  **parity_chainStatus**(_self_)  
    Get status of connected chain (Parity only).

- **parity_change_vault**(_self_, _address_, _vault_)
  **parity_changeVault**(_self_, _address_, _vault_)
    Change current vault for account and get if change was successful (Parity only).
    - **address**: address of account
    - **vault**: vault name

- **parity_change_vault_password**(_self_, _vault_, _password_)
  **parity_changeVaultPassword**(_self_, _vault_, _password_)
    Change vault password and get if change was successful (Parity only).
    - **vault**: vault name
    - **password**: new vault password

- **parity_check_request**(_self_, _request_id_)  
  **parity_checkRequest**(_self_, _request_id_)  
    Get transaction hash if request was accepted, or an error (Parity only).
    - **request_id**: ID of request

- **parity_cid_v0**(_self_, _data_)  
  **parity_cidV0**(_self_, _data_)  
    Get base58-encoded v0 IPFS (InterPlanetary File System) content ID (Parity only).
    - **data**: hex representation of a Protobuf-encoded string

- **parity_close_vault**(_self_, _vault_)
  **parity_closeVault**(_self_, _vault_)
    Close vault and get if closure was successful (Parity only).
    - **vault**: vault name

- **parity_compose_transaction**(_self_, _from_, _to_=None, _gas_=None, _gas_price_=None, _value_=None, _data_=None, _nonce_=None, _condition_=None)  
  **parity_composeTransaction**(_self_, _from_, _to_=None, _gas_=None, _gas_price_=None, _value_=None, _data_=None, _nonce_=None, _condition_=None)  
    Create transaction from partial data, returning the unsigned transaction object (Parity only).
    - **from**: address of sender
    - **to**: (optional) address of recipient
    - **gas**: (optional) gas provided for the transaction
    - **gas_price**: (optional) gas price for each paid gas
    - **value**: (optional) value to send with transactions
    - **data**: (optional) compile contract data or hash of method
    - **nonce**: (optional) user-provided nonce to override transactions
    - **condition**: (optional) conditional submission of transaction

- **parity_consensus_capability**(_self_)  
  **parity_consensusCapability**(_self_)  
    Get current consensus capability (Parity only).

- **parity_dapps_url**(_self_)  
  **parity_dappsUrl**(_self_)  
    Get hostname and port of dapps server (Parity only).

- **parity_decrypt_message**(_self_, _address_, _message_)  
  **parity_decryptMessage**(_self_, _address_, _message_)  
    Get decrypted message (Parity only).
    - **address**: address of account that can decrypt message
    - **message**: hex representation of encrypted message bytes

- **parity_default_account**(_self_)  
  **parity_defaultAccount**(_self_)  
    Get default account address for transactions (Parity only).

- **parity_default_extra_data**(_self_)  
  **parity_defaultExtraData**(_self_)  
    Get default extra data (Parity only).

- **parity_dev_logs**(_self_)  
  **parity_devLogs**(_self_)  
    Get list of recent stdout logs (Parity only).

- **parity_dev_logs_levels**(_self_)  
  **parity_devLogsLevels**(_self_)  
    Get the current logging level (Parity only).

- **parity_encrypt_message**(_self_, _hash_, _message_)  
  **parity_encryptMessage**(_self_, _hash_, _message_)  
    Get decrypted message (Parity only).
    - **hash**: last 64 bytes of EC public key
    - **message**: hex representation of message to encrypt

- **parity_enode**(_self_)  
    Get the enode URI (Parity only).

- **parity_extra_data**(_self_)  
  **parity_extraData**(_self_)  
    Get the currently set extra data (Parity only).

- **parity_future_transactions**(_self_)  
  **parity_futureTransactions**(_self_)  
    Get list of all future transactions currently in queue (Parity only).

- **parity_gas_ceil_target**(_self_)  
  **parity_gasCeilTarget**(_self_)  
    Get the current gas ceiling target (Parity only).

- **parity_gas_floor_target**(_self_)  
  **parity_gasFloorTarget**(_self_)  
    Get the current gas floor target (Parity only).

- **parity_gas_price_histogram**(_self_)  
  **parity_gasPriceHistogram**(_self_)  
    Get historic gas prices (Parity only).

- **parity_generate_secret_phrase**(_self_)  
  **parity_generateSecretPhrase**(_self_)  
    Create and get secret phrase associated with account. (Parity only).

- **parity_get_block_header_by_number**(_self_, _block_)  
  **parity_getBlockHeaderByNumber**(_self_, _block_)  
    Get block header by number (Parity only).
    - **block**: block number or tag to query

- **parity_get_vault_meta**(_self_, _vault_)
  **parity_getVaultMeta**(_self_, _vault_)
    Close metadata for vault (Parity only).
    - **vault**: vault name

- **parity_hardware_accounts_info**(_self_)  
  **parity_hardwareAccountsInfo**(_self_)  
    Get metadata for attached hardware wallets (Parity only).

- **parity_list_accounts**(_self_, _quantity_, _address_, _block_=None)  
  **parity_listAccounts**(_self_, _quantity_, _address_, _block_=None)  
    Get list of addresses, or null (Parity only).
    - **quantity**: number of addresses to get
    - **address**: offset address to start at, or `None`
    - **block**: block number or tag

- **parity_list_opened_vaults**(_self_)  
  **parity_listOpenedVaults**(_self_)  
    Get list of opened vaults (Parity only).

- **parity_list_storage_keys**(_self_, _address_, _quantity_, _hash__=None, _block_=None)  
  **parity_listStorageKeys**(_self_, _address_, _quantity_, _hash__=None, _block_=None)  
    Get list of storage keys from account (Parity only).
    - **address**: address of account
    - **quantity**: number of storage keys to get
    - **hash_**: offset storage key, or null
    - **block**: block number or tag

- **parity_list_vaults**(_self_)  
  **parity_listVaults**(_self_)  
    Get list of vaults (Parity only).

- **parity_local_transactions**(_self_)  
  **parity_localTransactions**(_self_)  
    Get list of current and previous local transactions (Parity only).

- **parity_min_gas_price**(_self_)  
  **parity_minGasPrice**(_self_)  
    Get the current minimal gas price (Parity only).

- **parity_mode**(_self_)  
    Get the mode (Parity only).

- **parity_new_vault**(_self_, _vault_, _password_)
  **parity_newVault**(_self_, _vault_, _password_)
    Create new vault with password and get if vault creation was successful (Parity only).
    - **vault**: new vault name
    - **password**: new vault password

- **parity_net_chain**(_self_)  
  **parity_netChain**(_self_)  
    Get name of connected chain (Parity only) (**Deprecated**).

- **parity_net_peers**(_self_)  
  **parity_netPeers**(_self_)  
    Get number of connected peers (Parity only).

- **parity_net_port**(_self_)  
  **parity_netPort**(_self_)  
    Get network port node is listening to (Parity only).

- **parity_next_nonce**(_self_, _address_)  
  **parity_nextNonce**(_self_, _address_)  
    Get next valid transaction nonce from account (Parity only).
    - **address**: address of account

- **parity_node_kind**(_self_)  
  **parity_nodeKind**(_self_)  
    Get the node kind and availability (Parity only).

- **parity_node_name**(_self_)  
  **parity_nodeName**(_self_)  
    Get the node name (Parity only).

- **parity_pending_transactions**(_self_)  
  **parity_pendingTransactions**(_self_)  
    Get a list of pending transactions (Parity only).

- **parity_pending_transactions_stats**(_self_)  
  **parity_pendingTransactionsStats**(_self_)  
    Get a dict of pending transaction hashes to stats (Parity only).

- **parity_phrase_to_address**(_self_. _phrase_)  
  **parity_phraseToAddress**(_self_. _phrase_)  
    Get account address from secret phrase (Parity only).
    - **phrase**: secret phrase

- **parity_open_vault**(_self_, _vault_, _password_)
  **parity_openVault**(_self_, _vault_, _password_)
    Open vault and get if vault opening was successful (Parity only).
    - **vault**: new vault name
    - **password**: new vault password

- **parity_post_sign**(_self_, _address_, _message_)
  **parity_postSign**(_self_, _address_, _message_)
    Sign standard Ethereum message and get the request ID (Parity only).
    - **address**: address of account
    - **message**: message to be signed

- **parity_post_transaction**(_self_, _from_, _to_=None, _gas_=None, _gas_price_=None, _value_=None, _data_=None, _nonce_=None, _condition_=None)  
  **parity_postTransaction**(_self_, _from_, _to_=None, _gas_=None, _gas_price_=None, _value_=None, _data_=None, _nonce_=None, _condition_=None)  
    Post transaction without waiting for signer, returning request ID (if the account is locked) or the transaction hash (if the account is unlocked) (Parity only).
    - **from**: address of sender
    - **to**: (optional) address of recipient
    - **gas**: (optional) gas provided for the transaction
    - **gas_price**: (optional) gas price for each paid gas
    - **value**: (optional) value to send with transactions
    - **data**: (optional) compile contract data or hash of method
    - **nonce**: (optional) user-provided nonce to override transactions
    - **condition**: (optional) conditional submission of transaction

- **parity_registry_address**(_self_)  
  **parity_registryAddress**(_self_)  
    Get address for global registry (Parity only).

- **parity_releases_info**(_self_)  
  **parity_releasesInfo**(_self_)  
    Get information about the release status (Parity only).

- **parity_remove_transaction**(_self_, _hash__)  
  **parity_removeTransaction**(_self_, _hash__)  
    Remove locally-scheduled transaction and get transaction data (Parity only).
    - **hash_**: transaction hash

- **parity_rpc_settings**(_self_)  
  **parity_rpcSettings**(_self_)  
    Get current RPC API settings (Parity only).

- **parity_set_vault_meta**(_self_, _vault_, _metadata_)
  **parity_setVaultMeta**(_self_, _vault_, _metadata_)
    Set vault metadata and get if change was successful (Parity only).
    - **vault**: new vault name
    - **metadata**: JSON string or dict of vault metadata

- **parity_sign_message**(_self_, _address_, _password_, _hash__)
  **parity_signMessage**(_self_, _address_, _password_, _hash__)
    Sign and get signature to message (Parity only).
    - **address**: address of account
    - **password**: account password
    - **hash_**: hex representation of hashed message

- **parity_transactions_limit**(_self_)  
  **parity_transactionsLimit**(_self_)  
    Get max number of transactions in queue (Parity only).

- **parity_unsigned_transactions_count**(_self_)  
  **parity_unsignedTransactionsCount**(_self_)  
    Get the number of unsigned transactions if using a trusted signer (Parity only).

- **parity_version_info**(_self_)  
  **parity_versionInfo**(_self_)  
    Get information about the Parity version (Parity only).

- **parity_ws_url**(_self_)  
  **parity_wsUrl**(_self_)  
    Get hostname and port of Websockets server (Parity only).

# Parity Accounts

**Methods:**

- **parity_all_accounts_info**(_self_)  
  **parity_allAccountsInfo**(_self_)  
    Get dict of account info (Parity only).

- **parity_change_password**(_self_, _address_, _old_password_, _new_password_)  
  **parity_changePassword**(_self_, _address_, _old_password_, _new_password_)  
    Change password and get if change was successful (Parity only).
    - **address**: address of account
    - **old_password**: old account password
    - **new_password**: new account password

- **parity_derive_address_hash**(_self_, _address_, _password_, _derived_hash_, _derived_type_ = 'hard', _save_account_ = False)  
  **parity_deriveAddressHash**(_self_, _address_, _password_, _derived_hash_, _derived_type_ = 'hard', _save_account_ = False)  
    Derive account address and get derived account address (Parity only).
    - **address**: address of account
    - **password**: account password
    - **derivation_hash**: derivation hash
    - **derivation_type**: derivation type
    - **save_account**: save account for later use

- **parity_derive_address_index**(_self_, _address_, _password_, _derivation_, _save_account_ = False)  
  **parity_deriveAddressIndex**(_self_, _address_, _password_, _derivation_, _save_account_ = False)  
    Derive account address from sequence and get derived account address (Parity only).
    - **address**: address of account
    - **password**: account password
    - **derivation**: sequence of dicts with the derivation type and index
    - **save_account**: save account for later use

- **parity_export_accoun**(_self_, _address_, _password_)  
  **parity_exportAccount**(_self_, _address_, _password_)  
    Export account to wallet file (as JSON) (Parity only).
    - **address**: address of account
    - **password**: account password

- **parity_get_dapp_addresses**(_self_, _dapp_)  
  **parity_getDappAddresses**(_self_, _dapp_)  
    Get list of account address for a dapp (Parity only).
    - **dapp**: dapp identifier ("web")

- **parity_get_dapp_default_address**(_self_, _dapp_)  
  **parity_getDappDefaultAddress**(_self_, _dapp_)  
    Get the default account address for a dapp (Parity only).
    - **dapp**: dapp identifier ("web")

- **parity_get_new_dapps_addresses**(_self_)  
  **parity_getNewDappsAddresses**(_self_)  
    Get list of account address for new dapps (Parity only).

- **parity_get_new_dapps_default_address**(_self_)  
  **parity_getNewDappsDefaultAddress**(_self_)  
    Get the default account address for new dapps (Parity only).

- **parity_import_geth_accounts**(_self_, \*_addresses_)  
  **parity_importGethAccounts**(_self_, \*_addresses_)  
    Import geth account addresses and return a list of imported addresses (Parity only).
    - **addresses**: sequence of account addresses

- **parity_kill_account**(_self_, _address_, _password_)  
  **parity_killAccount**(_self_, _address_, _password_)  
    Delete account and get if deletion was successful (Parity only).
    - **address**: address of account
    - **password**: account password

- **parity_list_geth_accounts**(_self_)  
  **parity_listGethAccounts**(_self_)  
    Get list of available geth accounts (Parity only).

- **parity_list_recent_dapps**(_self_)  
  **parity_listRecentDapps**(_self_)  
    Get list of recently active dapps (Parity only).

- **parity_new_account_from_phrase**(_self_, _phrase_, _password_)  
  **parity_newAccountFromPhrase**(_self_, _phrase_, _password_)  
    Create new account and get account address (Parity only).
    - **phrase**: secret phrase
    - **password**: account password

- **parity_new_account_from_secret**(_self_, _secret_, _password_)  
  **parity_newAccountFromSecret**(_self_, _secret_, _password_)  
    Create new account and get account address (Parity only).
    - **secret**: hex-representation of 32-byte secret
    - **password**: account password

- **parity_new_account_from_wallet**(_self_, _wallet_, _password_)  
  **parity_newAccountFromWallet**(_self_, _wallet_, _password_)  
    Create new account and get account address (Parity only).
    - **wallet**: JSON string or dict of wallet data
    - **password**: account password

- **parity_remove_address**(_self_, _address_)  
  **parity_removeAddress**(_self_, _address_)  
    Remove account from address book and get if removal was successful (Parity only).
    - **address**: address of account

- **parity_set_account_meta**(_self_, _address_, _metadata_)  
  **parity_setAccountMeta**(_self_, _address_, _metadata_)  
    Set new metadata for account and get if call was successful (Parity only).
    - **address**: address of account
    - **metadata**: JSON string or dict of account metadata

- **parity_set_account_name**(_self_, _address_, _name_)  
  **parity_setAccountName**(_self_, _address_, _name_)  
    Set new name for account and get if call was successful (Parity only).
    - **address**: address of account
    - **name**: account name

- **parity_set_new_dapps_addresses**(_self_, _dapp_, \*_addresses_)  
  **parity_setNewDappsAddresses**(_self_, _dapp_, \*_addresses_)  
    Set new address list for dapp and get if call was successful (Parity only).
    - **dapp**: dapp identifier ("web")
    - **addresses**: sequence of account addresses

- **parity_set_new_dapps_default_address**(_self_, _dapp_, _address_)  
  **parity_setNewDappsDefaultAddress**(_self_, _dapp_, _address_)  
    Set new default address for dapp and get if call was successful (Parity only).
    - **dapp**: dapp identifier ("web")
    - **address**: address of account

- **parity_set_new_dapps_addresses**(_self_, \*_addresses_)  
  **parity_setNewDappsAddresses**(_self_, \*_addresses_)  
    Set new address list for dapps and get if call was successful (Parity only).
    - **addresses**: sequence of account addresses

- **parity_set_new_dapps_default_address**(_self_, _address_)  
  **parity_setNewDappsDefaultAddress**(_self_, _address_)  
    Set new default address for dapps and get if call was successful (Parity only).
    - **address**: address of account

- **parity_test_password**(_self_, _address_, _password_)  
  **parity_testPassword**(_self_, _address_, _password_)  
    Get if account can be unlocked with address and password (Parity only).
    - **address**: address of account
    - **password**: account password

# Parity Set

**Methods:**

- **parity_accept_non_reserved_peers**(_self_)  
  **parity_acceptNonReservedPeers**(_self_)  
    Accept non-reserved peers and get if call was successful (Parity only).

- **parity_add_reserved_peer**(_self_, _enode_)  
  **parity_addReservedPeer**(_self_, _enode_)  
    Add reserved peer and get if call was successful (Parity only).
    - **enode**: address of node

- **parity_dapps_list**(_self_)  
  **parity_dappsList**(_self_)  
    Get list of local dapps (Parity only).

- **parity_drop_non_reserved_peers**(_self_)  
  **parity_dropNonReservedPeers**(_self_)  
    Drop non-reserved peers and get if call was successful (Parity only).

- **parity_execute_upgrade**(_self_)  
  **parity_executeUpgrade**(_self_)  
    Execute Parity version upgrade get if call was successful (Parity only).

- **parity_hash_content**(_self_, _uri_)  
  **parity_hashContent**(_self_, _uri_)  
    Get hash of file contents pointed to at the URI (Parity only).
    - **uri**: URI to content data

- **parity_remove_reserved_peer**(_self_, _enode_)  
  **parity_removeReservedPeer**(_self_, _enode_)  
    Remove reserved peer and get if call was successful (Parity only).
    - **enode**: address of node

- **parity_set_author**(_self_, _address_)  
  **parity_setAuthor**(_self_, _address_)  
    Change author for mined blocks and get if call was successful (Parity only).
    - **address**: account address

- **parity_set_chain**(_self_, _chain_)  
  **parity_setChain**(_self_, _chain_)  
    Change network specification and get if call was successful (Parity only).
    - **chain**: chain name

- **parity_set_engine_signer**(_self_, _address_, _password_)  
  **parity_setEngineSigner**(_self_, _address_, _password_)  
    Set authority account for consensus messages and get if call was successful (Parity only).
    - **address**: address of account
    - **password**: account password

- **parity_set_extra_data**(_self_, _data_)  
  **parity_setExtraData**(_self_, _data_)  
    Set set extra data for mined blocks and get if call was successful (Parity only).
    - **data**: hex-representation of binary data

- **parity_set_gas_ceil_target**(_self_, _gas_=0)  
  **parity_setGasCeilTarget**(_self_, _gas_=0)  
    Set gas ceiling target and get if call was successful (Parity only).
    - **gas**: gas amount

- **parity_set_gas_floor_target**(_self_, _gas_=0)  
  **parity_setGasFloorTarget**(_self_, _gas_=0)  
    Set gas floor target and get if call was successful (Parity only).
    - **gas**: gas amount

- **parity_set_max_transaction_gas**(_self_, _gas_)  
  **parity_setMaxTransactionGas**(_self_, _gas_)  
    Set maximum gas limit per transaction and get if call was successful (Parity only).
    - **gas**: gas amount

- **parity_set_min_gas_price**(_self_, _gas_price_)  
  **parity_setMinGasPrice**(_self_, _gas_price_)  
    Set minimum gas price for transaction acceptance and get if call was successful (Parity only).
    - **gas_price**: gas price for each paid gas

- **parity_set_mode**(_self_, _mode_)  
  **parity_setMode**(_self_, _mode_)  
    Change Parity mode and get if call was successful (Parity only).
    - **mode**: parity mode ({'active', 'passive', 'dark', 'offline'})

- **parity_set_transactions_limit**(_self_, _limit_)  
  **parity_setTransactionsLimit**(_self_, _limit_)  
    Set maximum number of transactions in local queue and get if call was successful (Parity only).
    - **limit**: maximum number of transactions in queue

- **parity_upgrade_ready**(_self_)  
  **parity_upgradeReady**(_self_)  
    Get if Parity client has upgrade ready (Parity only).

# Pubsub

**Methods:**

- **parity_subscribe**(_self_, _method_, \*_args_, \*\*_kwds_)  
    Create subscription to JSON-RPC method and return subscription ID (Parity only).
    - **method**: Python or JSON-RPC method name
    - **args**: positional arguments for method call
    - **kwds**: keyword arguments for method call

- **parity_unsubscribe**(_self_, _subscription_id_)  
    Unsubscribe by subscription ID and get if request was successful (Parity only).
    - **subscription_id**: ID for subscription to unsubscribe

# Signer

**Methods:**

- **signer_confirm_request**(_self_, _request_id_, _gas_=None, _gas_price_=None, _condition_=None, _password_=None)  
  **signer_confirmRequest**(_self_, _request_id_, _gas_=None, _gas_price_=None, _condition_=None, _password_=None)  
    Get confirmation status of request as dict (Parity only).
    - **request_id**: ID of request
    - **gas**: (optional) gas provided for the transaction
    - **gas_price**: (optional) gas price for each paid gas
    - **condition**: (optional) conditional submission of transaction
    - **password**: account password

- **signer_confirm_request_raw**(_self_, _request_id_, _data_)  
  **signer_confirmRequestRaw**(_self_, _request_id_, _data_)  
    Get confirmation status of request as dict (Parity only).
    - **request_id**: ID of request
    - **data**: signed request data

- **signer_confirm_request_with_token**(_self_, _request_id_, _gas_=None, _gas_price_=None, _condition_=None, _password_=None)  
  **signer_confirmRequestWithToken**(_self_, _request_id_, _gas_=None, _gas_price_=None, _condition_=None, _password_=None)  
    Get confirmation status of request as dict (Parity only).
    - **request_id**: ID of request
    - **gas**: (optional) gas provided for the transaction
    - **gas_price**: (optional) gas price for each paid gas
    - **condition**: (optional) conditional submission of transaction
    - **password**: account password

- **signer_generate_authorization_token**(_self_)  
- **signer_generateAuthorizationToken**(_self_)  
    Create and get authorization token (Parity only).

- **signer_generate_web_proxy_access_token**(_self_, _domain_)  
- **signer_generateWebProxyAccessToken**(_self_, _domain_)  
    Create and get web proxy access token (Parity only).
    - **domain**: domain for which token is valid

- **signer_reject_request**(_self_, _request_id_)  
  **signer_rejectRequest**(_self_, _request_id_)  
    Reject request in local queue and get if call was successful (Parity only).
    - **request_id**: ID of request

- **signer_requests_to_confirm**(_self_)  
- **signer_requestsToConfirm**(_self_)  
    Get list of transactions pending authorization (Parity only).

- **signer_subscribe_pending**(_self_)  
- **signer_subscribePending**(_self_)  
    Create subscription to pending transactions and get subscription ID (Parity only).

- **signer_unsubscribe_pending**(_self_, _subscription_id_)  
- **signer_unsubscribePending**(_self_, _subscription_id_)  
    Unsubscribe from pending transactions and get if call was successful (Parity only).

# Trace

**Methods:**

- **trace_block**(_self_, _block_ = DEFAULT_BLOCK)  
    Get list of traces created at block.
    - **block**: block number or tag

- **trace_call**(_self_, _from__=None, _to_=None, _gas_=None, _gas_price_=None, _value_=None, _data_=None, _block_=None)  
    Execute new call and get list of traces to the call.
    - **from**: (optional) address of sender
    - **to**: address of recipient
    - **gas**: (optional) gas provided for the transaction
    - **gas_price**: (optional) gas price for each paid gas
    - **value**: (optional) value to send with transactions
    - **data**: (optional) compile contract data or hash of method
    - **block**: block number or tag to query

- **trace_filter**(_self_, _from_block_=None, _to_block_=None, _address_=None, _topics_=None)  
    Get list of traces matching a filter.
    - **from_block**: (optional) block number or tag to query
    - **to_block**: (optional) block number or tag to query
    - **address**: (optional) contract address or list of addresses
    - **topics**: (optional) list of `DATA` topics

- **trace_get**(_self_, _hash__. _index_=0)  
    Get trace at position.
    - **hash_**: transaction hash
    - **index**: trace index

- **trace_raw_transaction**(_self_, _data_, _traces_)  
  **trace_RawTransaction**(_self_, _data_, _traces_)  
    Get list of traces from call to `eth_sendRawTransaction`, without executing the call.
    - **data**: signed transaction data
    - **traces**: list of trace types (at least 1)

- **trace_replay_transaction**(_self_, _hash__, _traces_)  
  **trace_replayTransaction**(_self_, _hash__, _traces_)  
    Get list of traces to the replayed transaction.
    - **hash_**: transaction hash
    - **traces**: list of trace types (at least 1)

- **trace_transaction**(_self_, _hash__)  
    Get list of traces to transaction by hash.
    - **hash_**: transaction hash

# Admin

**Methods:**

- **admin_add_peer**(_self_, _enode_)  
  **admin_addPeer**(_self_, _enode_)  
    Add peer and get if call was successful (Geth only).
    - **enode**: address of node

- **admin_datadir**(_self_)  
    Get path to data directory (Geth only).

- **admin_node_info**(_self_)  
- **admin_nodeInfo**(_self_)  
    Get dict containing node information (Geth only).

- **admin_peers**(_self_)  
    Get list containing node information for all peers (Geth only).

- **admin_set_solc**(_self_, _path_)  
  **admin_setSolc**(_self_, _path_)  
    Set solidity compiler and get version string from set compiler (Geth only).
    - **path**: path to solidity compiler

- **admin_start_rpc**(_self_, _host_ = DEFAULT_HOST, _port_ = DEFAULT_HTTP_PORT, _cors_ = DEFAULT_CORS, _apis_ = DEFAULT_APIS)  
- **admin_startRPC**(_self_, _host_ = DEFAULT_HOST, _port_ = DEFAULT_HTTP_PORT, _cors_ = DEFAULT_CORS, _apis_ = DEFAULT_APIS)  
    Start HTTP RTPC listenr and get if listener was opened (Geth only).
    - **host**: network interface for listener
    - **port**: network port for listener
    - **cors**: cross-origin resource sharing header to use
    - **apis**: comma-separated modules to support over interface

- **admin_start_ws**(_self_, _host_ = DEFAULT_HOST, _port_ = DEFAULT_WS_PORT, _cors_ = DEFAULT_CORS, _apis_ = DEFAULT_APIS)  
- **admin_startWs**(_self_, _host_ = DEFAULT_HOST, _port_ = DEFAULT_WS_PORT, _cors_ = DEFAULT_CORS, _apis_ = DEFAULT_APIS)  
    Start Websocket RTPC listenr and get if listener was opened (Geth only).
    - **host**: network interface for listener
    - **port**: network port for listener
    - **cors**: cross-origin resource sharing header to use
    - **apis**: comma-separated modules to support over interface

- **admin_stop_rpc**(_self_)  
- **admin_stopRPC**(_self_)  
    Stop HTTP RPC listener and get if call was successful (Geth only).

- **admin_stop_ws**(_self_)  
- **admin_stopWS**(_self_)  
    Stop Websocket RPC listener and get if call was successful (Geth only).

# Debug

**Methods:**

- **debug_backtrace_at**(_self_, _filename_, _line_)  
- **debug_backtraceAt**(_self_, _filename_, _line_)  
    Set logging backtrace location (Geth only).
    - **filename**: Go module name
    - **line**: line in module

- **debug_block_profile**(_self_, _path_, _seconds_)  
  **debug_blockProfile**(_self_, _path_, _seconds_)  
    Profile blocks and write output to path for duration (Geth only).
    - **path**: path to output file
    - **seconds**: number of seconds to do profiling for

- **debug_cpu_profile**(_self_, _path_, _seconds_)  
  **debug_cpuProfile**(_self_, _path_, _seconds_)  
    Profile CPU and write output to path for duration (Geth only).
    - **path**: path to output file
    - **seconds**: number of seconds to do profiling for

- **debug_dump_block**(_self_, _block_)  
- **debug_dumpBlock**(_self_, _block_)  
    Get dict with account information in block (Geth only).
    - **block**: block number or tag

- **debug_gc_stats**(_self_)  
- **debug_gcStats**(_self_)  
    Get dict of runtime GC statistics (Geth only).

- **debug_get_block_rlp**(_self_, _block_)  
- **debug_getBlockRlp**(_self_, _block_)  
    Get block RLP by number or tag (Geth only).
    - **block**: block number or tag

- **debug_go_trace**(_self_, _path_, _seconds_)  
  **debug_goTrace**(_self_, _path_, _seconds_)  
    Trace go runtime and write output to path for duration (Geth only).
    - **path**: path to output file
    - **seconds**: number of seconds to do tracing for

- **debug_mem_stats**(_self_)  
- **debug_memStats**(_self_)  
    Get dict of runtime memory statistics (Geth only).

- **debug_seed_hash**(_self_, _block_)  
- **debug_seedHash**(_self_, _block_)  
    Get seed hash by block RLP (Geth only).
    - **block**: block number or tag

- **debug_set_head**(_self_, _block_)  
- **debug_setHead**(_self_, _block_)  
    Set current head of local chain by block RLP (Geth only).
    **Warning:** This is destructive. Don't use it.
    - **block**: block number or tag

- **debug_set_block_profile_rate**(_self_, _rate_)  
  **debug_setBlockProfileRate**(_self_, _rate_)  
    Set block profiling collection rate (Geth only).
    - **rate**: number of samples per second

- **debug_stacks**(_self_)  
    Get representation of all go routine stacks (Geth only).

- **debug_start_cpu_profile**(_self_, _path_)  
  **debug_startCPUProfile**(_self_, _path_)  
    Profile CPU and write output to path (Geth only).
    - **path**: path to output file

- **debug_start_go_trace**(_self_, _path_)  
  **debug_startGoTrace**(_self_, _path_)  
    Trace go runtime and write output to path (Geth only).
    - **path**: path to output file

- **debug_stop_cpu_profile**(_self_)  
- **debug_stopCPUProfile**(_self_)  
    Stop profiling CPU (Geth only).

- **debug_stop_go_trace**(_self_)  
- **debug_stopGoTrace**(_self_)  
    Stop tracing go runtime (Geth only).

- **debug_trace_block**(_self_, _block_, \*\*_config_)  
- **debug_traceBlock**(_self_, _block_, \*\*_config_)  
    Get full stack trace for transactions in block by block RLP (Geth only).
    - **block**: block number or tag
    - **config**: transaction trace configuration options
      - **disable_memory**=False
      - **disable_stack**=False
      - **disable_storage**=False

- **debug_trace_block_by_number**(_self_, _block_, \*\*_config_)  
- **debug_traceBlockByNumber**(_self_, _block_, \*\*_config_)  
    Get full stack trace for transactions in block by block RLP (Geth only).
    - **block**: block number or tag
    - **config**: transaction trace configuration options
      - **disable_memory**=False
      - **disable_stack**=False
      - **disable_storage**=False

- **debug_trace_block_by_hash**(_self_, _hash__, \*\*_config_)  
- **debug_traceBlockByHash**(_self_, _hash__, \*\*_config_)  
    Get full stack trace for transactions in block by block hash (Geth only).
    - **hash_**: block hash
    - **config**: transaction trace configuration options
      - **disable_memory**=False
      - **disable_stack**=False
      - **disable_storage**=False

- **debug_trace_block_from_file**(_self_, _path_, \*\*_config_)  
- **debug_traceBlockFromFile**(_self_, _path_, \*\*_config_)  
    Get full stack trace for transactions in block by block RLP from file (Geth only).
    - **path**: path to file containing block RLP
    - **config**: transaction trace configuration options
      - **disable_memory**=False
      - **disable_stack**=False
      - **disable_storage**=False

- **debug_trace_transaction**(_self_, _hash__, \*\*_config_)  
- **debug_traceTransaction**(_self_, _hash__, \*\*_config_)  
    Get full stack trace for transaction by hash (Geth only).
    - **hash_**: transaction hash
    - **config**: transaction trace configuration options
      - **disable_memory**=False
      - **disable_stack**=False
      - **disable_storage**=False

- **debug_verbosity**(_self_, _log_level_)  
    Set logging level (Geth only).
    - **log_level**: log up to given level

- **debug_vmodule**(_self_, _log_pattern_)  
    Set logging verbosity pattern (Geth only).
    - **log_pattern**: logging verbosity pattern

- **debug_write_block_profile**(_self_, _path_)  
  **debug_writeBlockProfile**(_self_, _path_)  
    Profile go routine blocking and write output to path (Geth only).
    - **path**: path to output file

- **debug_write_mem_profile**(_self_, _path_)  
  **debug_writeMemProfile**(_self_, _path_)  
    Profile memory and write output to path (Geth only).
    - **path**: path to output file

# Miner

**Methods:**

- **miner_set_extra**(_self_, _data_)  
  **miner_setExtra**(_self_, _data_)  
    Set extra data for mined blocks and get if call was successful (Geth only).
    - **data**: hex-representation of binary data

- **miner_set_gas_price**(_self_, _gas_price_)  
  **miner_setGasPrice**(_self_, _gas_price_)  
    Set minimal accepted gas price when mining transactions (Geth only).
    - **gas_price**: gas price for each paid gas

- **miner_start**(_self_, _threads_)  
    Start mining on node (Geth only).
    - **threads**: number of threads for mining process

- **miner_stop**(_self_)  
    Stop mining on node (Geth only).

- **miner_set_ether_base**(_self_, _address_)  
  **miner_setEtherBase**(_self_, _address_)  
    Set account to receive mining rewards (Geth only).
    - **address**: address of account

# Txpool

**Methods:**

- **txpool_content**(_self_)  
    Get dict containing information for all pending transactions for next block (Geth only).

- **txpool_inspect**(_self_)  
    Get dict containing brief information for all pending transactions for next block (Geth only).

- **txpool_status**(_self_)  
    Get number of pending and queued transactions (Geth only).


# SHH

**Methods:**

- **shh_add_private_key**(_self_, _private_key_)  
  **shh_addPrivateKey**(_self_, _private_key_)  
    Import private key and return identity for key (Parity only).
    - **private_key**: hex-representation of private key

- **shh_add_sym_key**(_self_, _sym_key_)  
  **shh_addSymKey**(_self_, _sym_key_)  
    Import symmetric key and return identity for key (Parity only).
    - **sym_key**: hex-representation of symmetric key

- **shh_add_to_group**(_self_, _address_)  
  **shh_addToGroup**(_self_, _address_)  
    Add identity to group and get if addition was successful (Ethereum only).
    - **address**: SHH identity address

- **shh_delete_key**(_self_, _key_id_)  
  **shh_deleteKey**(_self_, _key_id_)  
    Delete key by ID and get if deletion was successful (Parity only).
    - **key_id**: hex-representation of key ID

- **shh_delete_message_filter**(_self_, _filter_id_)  
  **shh_deleteMessageFilter**(_self_, _filter_id_)  
    Delete filter by identity and get if deletion was successful (Parity only).
    - **filter_id**: hex-representation of filter ID

- **shh_get_filter_changes**(_self_, _filter_id_)  
  **shh_getFilterChanges**(_self_, _filter_id_)  
    Get list of messages matching the filter since last poll (Ethereum only).
    - **filter_id**: ID of filter to match

- **shh_get_filter_messages**(_self_, _filter_id_)  
  **shh_getFilterMessages**(_self_, _filter_id_)  
    Get list of messages matching the filter since last poll (Parity only).
    - **filter_id**: hex-representation of filter ID

- **shh_get_messages**(_self_, _filter_id_)  
  **shh_getMessages**(_self_, _filter_id_)  
    Get list of messages matching the filter (Ethereum only).
    - **filter_id**: ID of filter to match

- **shh_get_private_key**(_self_, _key_id_)  
  **shh_getPrivateKey**(_self_, _key_id_)  
    Get private key by identity (Parity only).
    - **key_id**: hex-representation of key ID

- **shh_get_public_key**(_self_, _key_id_)  
  **shh_getPublicKey**(_self_, _key_id_)  
    Get public key by identity (Parity only).
    - **key_id**: hex-representation of key ID

- **shh_get_sym_key**(_self_, _key_id_)  
  **shh_getSymKey**(_self_, _key_id_)  
    Get symmetric key by identity (Parity only).
    - **key_id**: hex-representation of key ID

- **shh_has_identity**(_self_, _address_)  
  **shh_hasIdentity**(_self_, _address_)  
    Get if client holds private keys to SHH identity (Ethereum only).
    - **address**: SHH identity address

- **shh_info**(_self_)  
    Get info about the whisper node (Parity only).

- **shh_new_filter**(_self_, _topics_, _to_=None)  
  **shh_newFilter**(_self_, _topics_, _to_=None)  
    Add identity to group and get if addition was successful (Ethereum only).
    - **topics**: list of `DATA` topics
    - **to**: (optional) recipient SHH identifier

- **shh_new_group**(_self_)  
  **shh_newGroup**(_self_)  
    Create and get address to group (Ethereum only).

- **shh_new_identity**(_self_)  
  **shh_newIdentity**(_self_)  
    Create and get SHH identifier (Ethereum only).

- **new_key_pair**(_self_)  
  **shh_newKeyPair**(_self_)  
    Create new asymmetric key pair and get key identity (Parity only).

- **shh_new_message_filter**(_self_, _topics_, _decrypt_with_=None, _from__=None)  
- **shh_newMessageFilter**(_self_, _topics_, _decrypt_with_=None, _from__=None)  
    Create new message filter and get filter ID.
    - **topics**: list of `DATA` topics
    - **decrypt_with**: (optional) key ID for description
    - **from_**: (optional) only accept messages signed by this key

- **new_sym_key**(_self_)  
  **shh_newSymKey**(_self_)  
    Create new symmetric key pair and get key identity (Parity only).

- **shh_post**(_self_, _topics_, _payload_, _priority_, _ttl_, _from__=None, _to_=None)  
    Post message and get if message was sent.
    - **topics**: list of `DATA` topics
    - **payload**: message body
    - **priority**: priority value
    - **ttl**: time-to-live in seconds
    - **from_**: (optional) sender SHH identifier
    - **to**: (optional) recipient SHH identifier

- **shh_subscribe**(_self_, _topics_, _decrypt_with_=None, _from__=None)  
    Create new message filter subscription and get subscription ID.
    - **topics**: list of `DATA` topics
    - **decrypt_with**: (optional) key ID for description
    - **from_**: (optional) only accept messages signed by this key

- **shh_uninstall_filter**(_self_, _filter_id_)  
  **shh_uninstallFilter**(_self_, _filter_id_)  
    Uninstall filter and get if uninstallation was successful (Ethereum only).
    - **filter_id**: ID of filter to uninstall

- **shh_unsubscribe**(_self_, _subscription_id_)  
    Unsubscribe by subscription ID and get if request was successful (Parity only).
    - **subscription_id**: ID for subscription to unsubscribe

- **shh_version**(_self_)  
    Get whisper protocol version (Ethereum only).
