from test_base import TestBase


class TestPubsub(TestBase):

    def test_eth_subscribe(self):
        cb = lambda: self.client.eth_subscribe("newHeads")
        self.mock(cb, True)

    def test_eth_unsubscribe(self):
        cb = lambda: self.client.eth_unsubscribe(4714555447970118045)
        self.mock(cb, True)
