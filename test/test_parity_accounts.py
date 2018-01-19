from test_base import TestBase


class TestParityAccounts(TestBase):

    def test_parity_all_accounts_info(self):
        cb = lambda: self.client.parity_all_accounts_info()
        self.mock(cb, True)

    def test_parity_change_password(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        old_password = 'password'
        new_password = '123456'
        cb = lambda: self.client.parity_change_password(address, old_password, new_password)
        self.mock(cb, True)

    def test_parity_derive_address_hash(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        password = 'password'
        derived_hash = '0x96ee0e9574959ad9e2b7b287ea59bc8741d228b6ffc9eaee8e17bb59948103bf'
        cb = lambda: self.client.parity_derive_address_hash(address, password, derived_hash)
        self.mock(cb, True)

    def test_parity_derive_address_index(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        password = 'password'
        derived = [{'index': 1, 'type': 'soft'},{'index': 2,'type': 'hard'}]
        cb = lambda: self.client.parity_derive_address_index(address, password, derived)
        self.mock(cb, True)

    def test_parity_export_account(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        password = 'password'
        cb = lambda: self.client.parity_export_account(address, password)
        self.mock(cb, True)

    def test_parity_get_dapp_addresses(self):
        dapp = 'web'
        cb = lambda: self.client.parity_get_dapp_addresses(dapp)
        self.mock(cb, True)

    def test_parity_get_dapp_default_address(self):
        dapp = 'web'
        cb = lambda: self.client.parity_get_dapp_default_address(dapp)
        self.mock(cb, True)

    def test_parity_get_new_dapps_addresses(self):
        cb = lambda: self.client.parity_get_new_dapps_addresses()
        self.mock(cb, True)

    def test_parity_get_new_dapps_default_address(self):
        cb = lambda: self.client.parity_get_new_dapps_default_address()
        self.mock(cb, True)

    def test_parity_import_geth_accounts(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        cb = lambda: self.client.parity_import_geth_accounts(address)
        self.mock(cb, True)

    def test_parity_kill_account(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        password = 'password'
        cb = lambda: self.client.parity_kill_account(address, password)
        self.mock(cb, True)

    def test_parity_list_geth_accounts(self):
        cb = lambda: self.client.parity_list_geth_accounts()
        self.mock(cb, True)

    def test_parity_list_recent_dapps(self):
        cb = lambda: self.client.parity_list_recent_dapps()
        self.mock(cb, True)

    def test_parity_new_account_from_phrase(self):
        phrase = 'this is a really long secret phrase of random words'
        password = 'password'
        cb = lambda: self.client.parity_new_account_from_phrase(phrase, password)
        self.mock(cb, True)

    def test_parity_new_account_from_secret(self):
        secret = '0x6bd03adce3f5828ce200cb040e1c5e4de8b8c99d726eee21521c62e4d27218aa'
        password = 'password'
        cb = lambda: self.client.parity_new_account_from_secret(secret, password)
        self.mock(cb, True)

    def test_parity_new_account_from_wallet(self):
        wallet = ''
        password = 'password'
        cb = lambda: self.client.parity_new_account_from_wallet(wallet, password)
        self.mock(cb, True)

    def test_parity_remove_address(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        cb = lambda: self.client.parity_remove_address(address)
        self.mock(cb, True)

    def test_parity_set_account_meta(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        metadata = {'hint': 'never'}
        cb = lambda: self.client.parity_set_account_meta(address, metadata)
        self.mock(cb, True)

    def test_parity_set_account_name(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        name = 'name'
        cb = lambda: self.client.parity_set_account_name(address, name)
        self.mock(cb, True)

    def test_parity_set_dapp_addresses(self):
        dapp = 'web'
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        cb = lambda: self.client.parity_set_dapp_addresses(dapp, address)
        self.mock(cb, True)

    def test_parity_set_dapp_default_address(self):
        dapp = 'web'
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        cb = lambda: self.client.parity_set_dapp_default_address(dapp, address)
        self.mock(cb, True)

    def test_parity_set_new_dapps_addresses(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        cb = lambda: self.client.parity_set_new_dapps_addresses(address)
        self.mock(cb, True)

    def test_parity_set_new_dapps_default_address(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        cb = lambda: self.client.parity_set_new_dapps_default_address(address)
        self.mock(cb, True)

    def test_parity_test_password(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        password = 'password'
        cb = lambda: self.client.parity_test_password(address, password)
        self.mock(cb, True)
