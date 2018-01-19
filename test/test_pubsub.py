from test_base import TestBase


class TestPubsub(TestBase):

    def test_parity_subscribe(self):
        cb = lambda: self.client.parity_subscribe("net_listening")
        self.mock(cb, True)

    def test_parity_unsubscribe(self):
        cb = lambda: self.client.parity_unsubscribe(4714555447970118045)
        self.mock(cb, True)
