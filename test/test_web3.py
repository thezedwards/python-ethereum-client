from test_base import TestBase


class TestWeb3(TestBase):

    def test_web3_client_version(self):
        cb = lambda: self.client.web3_client_version()
        self.mock(cb)

    def test_web3_sha3(self):
        cb = lambda: self.client.web3_sha3('string1')
        self.mock(cb)
