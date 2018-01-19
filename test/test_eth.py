from test_base import TestBase


class TestEth(TestBase):

    def test_eth_accounts(self):
        cb = lambda: self.client.eth_accounts()
        self.mock(cb)

    def test_eth_block_number(self):
        cb = lambda: self.client.eth_block_number()
        self.mock(cb)

    def test_eth_call(self):
        from_ = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        to = '0x43b810d42d7650d19930581f6a77126ffe5c6bf6'
        gas = 90000
        block = 'latest'
        cb = lambda: self.client.eth_call(from_, to, gas, block=block)
        self.mock(cb, True)

    def test_eth_coinbase(self):
        cb = lambda: self.client.eth_coinbase()
        self.mock(cb)

    def test_eth_compile_lll(self):
        code = "(for [i]:0 (< @i 10) [i](+ @i 1) )"
        cb = lambda: self.client.eth_compile_lll(code)
        self.mock(cb)

    def test_eth_compile_serpent(self):
        code = "def add(x, y):  return(x+y)"
        cb = lambda: self.client.eth_compile_serpent(code)
        self.mock(cb)

    def test_eth_compile_solidity(self):
        code = "contract test { function add(uint x, uint y) returns(uint a) { return x + y; } }"
        cb = lambda: self.client.eth_compile_solidity(code)
        self.mock(cb)

    def test_eth_estimate_gas(self):
        from_ = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        to = '0x43b810d42d7650d19930581f6a77126ffe5c6bf6'
        gas = 90000
        cb = lambda: self.client.eth_estimate_gas(from_, to, gas)
        self.mock(cb, True)

    def test_eth_gas_price(self):
        cb = lambda: self.client.eth_gas_price()
        self.mock(cb)

    def test_eth_get_balance(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        block = 'latest'
        cb = lambda: self.client.eth_get_balance(address, block)
        self.mock(cb, True)

    def test_eth_get_block_by_hash(self):
        hash_ = '0x96ee0e9574959ad9e2b7b287ea59bc8741d228b6ffc9eaee8e17bb59948103bf'
        cb = lambda: self.client.eth_get_block_by_hash(hash_)
        self.mock(cb, True)

    def test_eth_get_block_by_number(self):
        number = 1024
        cb = lambda: self.client.eth_get_block_by_number(number)
        self.mock(cb, True)

    def test_eth_get_block_transaction_count_by_hash(self):
        hash_ = '0x96ee0e9574959ad9e2b7b287ea59bc8741d228b6ffc9eaee8e17bb59948103bf'
        cb = lambda: self.client.eth_get_block_transaction_count_by_hash(hash_)
        self.mock(cb, True)

    def test_eth_get_block_transaction_count_by_number(self):
        number = 1024
        cb = lambda: self.client.eth_get_block_transaction_count_by_number(number)
        self.mock(cb, True)

    def test_eth_get_code(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        block = 'latest'
        cb = lambda: self.client.eth_get_code(address, block)
        self.mock(cb, True)

    def test_eth_get_compilers(self):
        cb = lambda: self.client.eth_get_compilers()
        self.mock(cb)

    def test_eth_get_filter_changes(self):
        filter_id = 15
        cb = lambda: self.client.eth_get_filter_changes(filter_id)
        self.mock(cb, True)

    def test_eth_get_filter_logs(self):
        filter_id = 15
        cb = lambda: self.client.eth_get_filter_logs(filter_id)
        self.mock(cb, True)

    def test_eth_get_logs(self):
        from_block = 5
        to_block = 15
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        cb = lambda: self.client.eth_get_logs(from_block, to_block, address)
        self.mock(cb, True)

    def test_eth_get_storage_at(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        position = 0
        block = 'latest'
        cb = lambda: self.client.eth_get_storage_at(address, position, block)
        self.mock(cb, True)

    def test_eth_get_transaction_by_block_hash_and_index(self):
        hash_ = '0x96ee0e9574959ad9e2b7b287ea59bc8741d228b6ffc9eaee8e17bb59948103bf'
        index = 0
        cb = lambda: self.client.eth_get_transaction_by_block_hash_and_index(hash_, index)
        self.mock(cb, True)

    def test_eth_get_transaction_by_block_number_and_index(self):
        number = 1024
        index = 0
        cb = lambda: self.client.eth_get_transaction_by_block_number_and_index(number, index)
        self.mock(cb, True)

    def test_eth_get_transaction_by_hash(self):
        hash_ = '0x43f101b4482a22be8061915133c5a32cd0303a14ac695f23bfe3748d59acd46c'
        cb = lambda: self.client.eth_get_transaction_by_hash(hash_)
        self.mock(cb, True)

    def test_eth_get_transaction_count(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        block = 'latest'
        cb = lambda: self.client.eth_get_transaction_count(address, block)
        self.mock(cb, True)

    def test_eth_get_transaction_receipt(self):
        hash_ = '0x43f101b4482a22be8061915133c5a32cd0303a14ac695f23bfe3748d59acd46c'
        cb = lambda: self.client.eth_get_transaction_receipt(hash_)
        self.mock(cb, True)

    def test_eth_get_uncle_by_block_hash_and_index(self):
        hash_ = '0x96ee0e9574959ad9e2b7b287ea59bc8741d228b6ffc9eaee8e17bb59948103bf'
        index = 0
        cb = lambda: self.client.eth_get_uncle_by_block_hash_and_index(hash_, index)
        self.mock(cb, True)

    def test_eth_get_uncle_by_block_number_and_index(self):
        number = 1024
        index = 0
        cb = lambda: self.client.eth_get_uncle_by_block_number_and_index(number, index)
        self.mock(cb, True)

    def test_eth_get_uncle_count_by_block_hash(self):
        hash_ = '0x96ee0e9574959ad9e2b7b287ea59bc8741d228b6ffc9eaee8e17bb59948103bf'
        cb = lambda: self.client.eth_get_uncle_count_by_block_hash(hash_)
        self.mock(cb, True)

    def test_eth_get_uncle_count_by_block_number(self):
        number = 1024
        cb = lambda: self.client.eth_get_uncle_count_by_block_number(number)
        self.mock(cb, True)

    def test_eth_get_work(self):
        cb = lambda: self.client.eth_get_work()
        self.mock(cb)

    def test_eth_hashrate(self):
        cb = lambda: self.client.eth_hashrate()
        self.mock(cb)

    def test_eth_mining(self):
        cb = lambda: self.client.eth_mining()
        self.mock(cb)

    def test_eth_new_block_filter(self):
        cb = lambda: self.client.eth_new_block_filter()
        self.mock(cb)

    def test_eth_new_filter(self):
        from_block = 5
        to_block = 15
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        cb = lambda: self.client.eth_new_filter(from_block, to_block, address)
        self.mock(cb, True)

    def test_eth_new_pending_transaction_filter(self):
        cb = lambda: self.client.eth_new_pending_transaction_filter()
        self.mock(cb)

    def test_eth_protocol_version(self):
        cb = lambda: self.client.eth_protocol_version()
        self.mock(cb)

    def test_eth_send_raw_transaction(self):
        data = '0x972fc7d321ebabd2537f7f08e729a48aac9be4f025d52227cc8da00fb31ce10eb180baf5efef98f8050dbdb0dc2bc6858394'
        cb = lambda: self.client.eth_send_transaction(data)
        self.mock(cb, True)

    def test_eth_send_transaction(self):
        from_ = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        to = '0x43b810d42d7650d19930581f6a77126ffe5c6bf6'
        gas = 90000
        cb = lambda: self.client.eth_send_transaction(from_, to, gas)
        self.mock(cb, True)

    def test_eth_sign(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        message = '0xbabe'
        cb = lambda: self.client.eth_sign(address, message)
        self.mock(cb, True)

    def eth_sign_transaction(self):
        from_ = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        to = '0x43b810d42d7650d19930581f6a77126ffe5c6bf6'
        gas = 90000
        cb = lambda: self.client.eth_send_transaction(from_, to, gas)
        self.mock(cb, True)

    def test_eth_submit_hashrate(self):
        hash_rate = 6000000
        client_id = '0x94c875b1fd501f7bb4c3b4e5cc88ad9b10e89bb5ad9e2de7781dce0751e5acd4'
        cb = lambda: self.client.eth_submit_hashrate(hash_rate, client_id)
        self.mock(cb, True)

    def test_eth_submit_work(self):
        nonce = 1
        pow_hash = '0d18a80d33ff2da85a423098459f49a3f7af67a42f4ec11d1c0b4140fe1b22f9'
        mix_digest = '0x4e015e9147a487a0947f8f9bdec076d08991b743a952a0466f2c42968a292516'
        cb = lambda: self.client.eth_submit_work(nonce, pow_hash, mix_digest)
        self.mock(cb, True)

    def test_eth_syncing(self):
        cb = lambda: self.client.eth_syncing()
        self.mock(cb)

    def test_eth_uninstall_filter(self):
        filter_id = 15
        cb = lambda: self.client.eth_uninstall_filter(filter_id)
        self.mock(cb, True)
