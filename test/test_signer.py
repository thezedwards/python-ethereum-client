from test_base import TestBase


class TestSigner(TestBase):

    def test_signer_confirm_request(self):
        request_id = 1
        password = 'password'
        cb = lambda: self.client.signer_confirm_request(request_id, password=password)
        self.mock(cb, True)

    def test_signer_confirm_request_raw(self):
        request_id = 1
        data = '0x'
        cb = lambda: self.client.signer_confirm_request_raw(request_id, data)
        self.mock(cb, True)

    def test_signer_confirm_request_with_token(self):
        request_id = 1
        password = 'password'
        cb = lambda: self.client.signer_confirm_request_with_token(request_id, password=password)
        self.mock(cb, True)

    def test_signer_generate_authorization_token(self):
        cb = lambda: self.client.signer_generate_authorization_token()
        self.mock(cb, True)

    def test_signer_generate_web_proxy_access_token(self):
        domain = 'https://parity.io'
        cb = lambda: self.client.signer_generate_web_proxy_access_token(domain)
        self.mock(cb, True)

    def test_signer_reject_request(self):
        request_id = 1
        cb = lambda: self.client.signer_reject_request(request_id)
        self.mock(cb, True)

    def test_signer_requests_to_confirm(self):
        cb = lambda: self.client.signer_requests_to_confirm()
        self.mock(cb, True)

    def test_signer_subscribe_pending(self):
        cb = lambda: self.client.signer_subscribe_pending()
        self.mock(cb, True)

    def test_signer_unsubscribe_pending(self):
        subscription_id = 1
        cb = lambda: self.client.signer_unsubscribe_pending(subscription_id)
        self.mock(cb, True)
