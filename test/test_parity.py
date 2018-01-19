from test_base import TestBase


class TestParity(TestBase):

    def test_parity_accounts_info(self):
        cb = lambda: self.client.parity_accounts_info()
        self.mock(cb, True)

    def test_parity_chain(self):
        cb = lambda: self.client.parity_chain()
        self.mock(cb, True)

    def test_parity_chain_status(self):
        cb = lambda: self.client.parity_chain_status()
        self.mock(cb, True)

    def test_parity_change_vault(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        vault = 'Vault'
        cb = lambda: self.client.parity_change_vault(address, vault)
        self.mock(cb, True)

    def test_parity_change_vault_password(self):
        vault = 'Vault'
        password = 'password'
        cb = lambda: self.client.parity_change_vault_password(vault, password)
        self.mock(cb, True)

    def test_parity_check_request(self):
        cb = lambda: self.client.parity_check_request(15)
        self.mock(cb, True)

    def test_parity_cid_v0(self):
        cb = lambda: self.client.parity_cid_v0('70617468')
        self.mock(cb, True)

    def test_parity_close_vault(self):
        vault = 'Vault'
        cb = lambda: self.client.parity_close_vault(vault)
        self.mock(cb, True)

    def test_parity_compose_transaction(self):
        from_ = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        to = '0x43b810d42d7650d19930581f6a77126ffe5c6bf6'
        gas = 90000
        cb = lambda: self.client.parity_compose_transaction(from_, to, gas)
        self.mock(cb, True)

    def test_parity_consensus_capability(self):
        cb = lambda: self.client.parity_consensus_capability()
        self.mock(cb, True)

    def test_parity_dapps_url(self):
        cb = lambda: self.client.parity_dapps_url()
        self.mock(cb, True)

    def test_parity_decrypt_message(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        message = '0xbabe'
        cb = lambda: self.client.parity_decrypt_message(address, message)
        self.mock(cb, True)

    def test_parity_default_account(self):
        cb = lambda: self.client.parity_default_account()
        self.mock(cb, True)

    def test_parity_default_extra_data(self):
        cb = lambda: self.client.parity_default_extra_data()
        self.mock(cb, True)

    def test_parity_dev_logs(self):
        cb = lambda: self.client.parity_dev_logs()
        self.mock(cb, True)

    def test_parity_dev_logs_levels(self):
        cb = lambda: self.client.parity_dev_logs_levels()
        self.mock(cb, True)

    def test_parity_encrypt_message(self):
        hash_ = '0x429a5a2ea186fac99c9a5123adaa0af075e9e5ebf9be097c02670afa6ef6e27657491f641e4d3cfd32ee58bc0475d8b355d4ede06f222d01478d533c257e94c86dc5b24eae635afdfc85a135d9269cdd565ac94cf81b210548a8d4f7e587ae9cb67d1ebf7a042e5ed9412dd563b61f57981f69c0bb3c955e8be2241d3324c953'
        message = '48656c6c20576f726c6421'
        cb = lambda: self.client.parity_encrypt_message(hash_, message)
        self.mock(cb, True)

    def test_parity_enode(self):
        cb = lambda: self.client.parity_enode()
        self.mock(cb, True)

    def test_parity_extra_data(self):
        cb = lambda: self.client.parity_extra_data()
        self.mock(cb, True)

    def test_parity_future_transactions(self):
        cb = lambda: self.client.parity_future_transactions()
        self.mock(cb, True)

    def test_parity_gas_ceil_target(self):
        cb = lambda: self.client.parity_gas_ceil_target()
        self.mock(cb, True)

    def test_parity_gas_floor_target(self):
        cb = lambda: self.client.parity_gas_floor_target()
        self.mock(cb, True)

    def test_parity_gas_price_histogram(self):
        cb = lambda: self.client.parity_gas_price_histogram()
        self.mock(cb, True)

    def test_parity_generate_secret_phrase(self):
        cb = lambda: self.client.parity_generate_secret_phrase()
        self.mock(cb, True)

    def test_parity_get_block_header_by_number(self):
        block = 'latest'
        cb = lambda: self.client.parity_get_block_header_by_number(block)
        self.mock(cb, True)

    def test_parity_get_vault_meta(self):
        vault = 'Vault'
        cb = lambda: self.client.parity_get_vault_meta(vault)
        self.mock(cb, True)

    def test_parity_hardware_accounts_info(self):
        cb = lambda: self.client.parity_hardware_accounts_info()
        self.mock(cb, True)

    def test_parity_list_accounts(self):
        quantity = 5
        address = None
        cb = lambda: self.client.parity_list_accounts(quantity, address)
        self.mock(cb, True)

    def test_parity_list_opened_vaults(self):
        cb = lambda: self.client.parity_list_opened_vaults()
        self.mock(cb, True)

    def test_parity_list_storage_keys(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        quantity = 5
        cb = lambda: self.client.parity_list_storage_keys(address, quantity)
        self.mock(cb, True)

    def test_parity_list_vaults(self):
        cb = lambda: self.client.parity_list_vaults()
        self.mock(cb, True)

    def test_parity_local_transactions(self):
        cb = lambda: self.client.parity_local_transactions()
        self.mock(cb, True)

    def test_parity_min_gas_price(self):
        cb = lambda: self.client.parity_min_gas_price()
        self.mock(cb, True)

    def test_parity_mode(self):
        cb = lambda: self.client.parity_mode()
        self.mock(cb, True)

    def test_parity_new_vault(self):
        vault = 'Vault'
        password = 'password'
        cb = lambda: self.client.parity_new_vault(vault, password)
        self.mock(cb, True)

    def test_parity_net_chain(self):
        cb = lambda: self.client.parity_net_chain()
        self.mock(cb, True)

    def test_parity_net_peers(self):
        cb = lambda: self.client.parity_net_peers()
        self.mock(cb, True)

    def test_parity_net_port(self):
        cb = lambda: self.client.parity_net_port()
        self.mock(cb, True)

    def test_parity_next_nonce(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        cb = lambda: self.client.parity_next_nonce(address)
        self.mock(cb, True)

    def test_parity_node_kind(self):
        cb = lambda: self.client.parity_node_kind()
        self.mock(cb, True)

    def test_parity_node_name(self):
        cb = lambda: self.client.parity_node_name()
        self.mock(cb, True)

    def test_parity_pending_transactions(self):
        cb = lambda: self.client.parity_pending_transactions()
        self.mock(cb, True)

    def test_parity_pending_transactions_stats(self):
        cb = lambda: self.client.parity_pending_transactions_stats()
        self.mock(cb, True)

    def test_parity_phrase_to_address(self):
        phrase = 'this is a really long secret phrase of random words'
        cb = lambda: self.client.parity_phrase_to_address(phrase)
        self.mock(cb, True)

    def test_parity_open_vault(self):
        vault = 'Vault'
        password = 'password'
        cb = lambda: self.client.parity_open_vault(vault, password)
        self.mock(cb, True)

    def test_parity_post_sign(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        message = '0xbabe'
        cb = lambda: self.client.parity_post_sign(address, message)
        self.mock(cb, True)

    def test_parity_post_transaction(self):
        from_ = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        to = '0x43b810d42d7650d19930581f6a77126ffe5c6bf6'
        gas = 90000
        cb = lambda: self.client.parity_post_transaction(from_, to, gas)
        self.mock(cb, True)

    def test_parity_registry_address(self):
        cb = lambda: self.client.parity_registry_address()
        self.mock(cb, True)

    def test_parity_releases_info(self):
        cb = lambda: self.client.parity_releases_info()
        self.mock(cb, True)

    def test_parity_remove_transaction(self):
        hash_ = '0x43f101b4482a22be8061915133c5a32cd0303a14ac695f23bfe3748d59acd46c'
        cb = lambda: self.client.parity_remove_transaction(hash_)
        self.mock(cb, True)

    def test_parity_rpc_settings(self):
        cb = lambda: self.client.parity_rpc_settings()
        self.mock(cb, True)

    def test_parity_set_vault_meta(self):
        vault = 'Vault'
        metadata = '{"passwordHint": "Never use hints."}'
        cb = lambda: self.client.parity_set_vault_meta(vault, metadata)
        self.mock(cb, True)

    def test_parity_sign_message(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        password = 'password'
        hash_ = '0xbabe'
        cb = lambda: self.client.parity_sign_message(address, password, hash_)
        self.mock(cb, True)

    def test_parity_transactions_limit(self):
        cb = lambda: self.client.parity_transactions_limit()
        self.mock(cb, True)

    def test_parity_unsigned_transactions_count(self):
        cb = lambda: self.client.parity_unsigned_transactions_count()
        self.mock(cb, True)

    def test_parity_version_info(self):
        cb = lambda: self.client.parity_version_info()
        self.mock(cb, True)

    def test_parity_ws_url(self):
        cb = lambda: self.client.parity_ws_url()
        self.mock(cb, True)
