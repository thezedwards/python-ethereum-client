from test_base import TestBase


class TestPersonal(TestBase):

    def test_personal_list_accounts(self):
        cb = lambda: self.client.personal_list_accounts()
        self.mock(cb, True)

    def test_personal_new_account(self):
        cb = lambda: self.client.personal_new_account('password')
        self.mock(cb, True)

    def test_personal_send_transaction(self):
        from_ = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        to = '0x43b810d42d7650d19930581f6a77126ffe5c6bf6'
        gas = 90000
        cb = lambda: self.client.personal_send_transaction(
            from_, to, gas, password='password')
        self.mock(cb, True)

    def test_personal_unlock_account(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        password = 'password'
        duration = 20
        cb = lambda: self.client.personal_unlock_account(address, password, duration)
        self.mock(cb, True)
