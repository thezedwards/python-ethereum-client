from test_base import TestBase


class TestParitySet(TestBase):

    def test_parity_accept_non_reserved_peers(self):
        cb = lambda: self.client.parity_accept_non_reserved_peers()
        self.mock(cb, True)

    def test_parity_add_reserved_peer(self):
        enode = 'enode://1ba7d1d8e9cd395c07e89830c2b9b34e5b3aa7e2928508aa7c3e9a353531255fed38ea0d6af3a599434ad4455a6554af3fcbc52afc1c18aa9b3272f48cb84402@127.0.0.1:8745'
        cb = lambda: self.client.parity_add_reserved_peer(enode)
        self.mock(cb, True)

    def test_parity_dapps_list(self):
        cb = lambda: self.client.parity_dapps_list()
        self.mock(cb, True)

    def test_parity_drop_non_reserved_peers(self):
        cb = lambda: self.client.parity_drop_non_reserved_peers()
        self.mock(cb, True)

    def test_parity_execute_upgrade(self):
        cb = lambda: self.client.parity_execute_upgrade()
        self.mock(cb, True)

    def test_parity_hash_content(self):
        uri = 'https://httpbin.org/robots.txt'
        cb = lambda: self.client.parity_hash_content(uri)
        self.mock(cb, True)

    def test_parity_remove_reserved_peer(self):
        enode = 'enode://1ba7d1d8e9cd395c07e89830c2b9b34e5b3aa7e2928508aa7c3e9a353531255fed38ea0d6af3a599434ad4455a6554af3fcbc52afc1c18aa9b3272f48cb84402@127.0.0.1:8745'
        cb = lambda: self.client.parity_remove_reserved_peer(enode)
        self.mock(cb, True)

    def test_parity_set_author(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        cb = lambda: self.client.parity_set_author(address)
        self.mock(cb, True)

    def test_parity_set_chain(self):
        chain = 'morden'
        cb = lambda: self.client.parity_set_chain(chain)
        self.mock(cb, True)

    def test_parity_set_engine_signer(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        password = 'password'
        cb = lambda: self.client.parity_set_engine_signer(address, password)
        self.mock(cb, True)

    def test_parity_set_extra_data(self):
        data = '0x'
        cb = lambda: self.client.parity_set_extra_data(data)
        self.mock(cb, True)

    def test_parity_set_gas_ceil_target(self):
        gas_price = 10000000
        cb = lambda: self.client.parity_set_gas_ceil_target(gas_price)
        self.mock(cb, True)

    def test_parity_set_gas_floor_target(self):
        gas_price = 10000
        cb = lambda: self.client.parity_set_gas_floor_target(gas_price)
        self.mock(cb, True)

    def test_parity_set_max_transaction_gas(self):
        gas_price = 1000000
        cb = lambda: self.client.parity_set_max_transaction_gas(gas_price)
        self.mock(cb, True)

    def test_parity_set_min_gas_price(self):
        gas_price = 10000
        cb = lambda: self.client.parity_set_min_gas_price(gas_price)
        self.mock(cb, True)

    def test_parity_set_mode(self):
        mode = 'active'
        cb = lambda: self.client.parity_set_mode(mode)
        self.mock(cb, True)

    def test_parity_set_transactions_limit(self):
        limit = 500
        cb = lambda: self.client.parity_set_transactions_limit(limit)
        self.mock(cb, True)

    def test_parity_upgrade_ready(self):
        cb = lambda: self.client.parity_upgrade_ready()
        self.mock(cb, True)
