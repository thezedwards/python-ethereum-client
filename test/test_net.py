from test_base import TestBase


class TestNet(TestBase):

    def test_net_listening(self):
        cb = lambda: self.client.net_listening()
        self.mock(cb)

    def test_net_peer_count(self):
        cb = lambda: self.client.net_peer_count()
        self.mock(cb)

    def test_net_version(self):
        cb = lambda: self.client.net_version()
        self.mock(cb)
