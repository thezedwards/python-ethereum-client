from test_base import TestBase


class TestTxpool(TestBase):

    def test_txpool_content(self):
        cb = lambda: self.client.txpool_content()
        self.mock(cb, True)

    def test_txpool_inspect(self):
        cb = lambda: self.client.txpool_inspect()
        self.mock(cb, True)

    def test_txpool_status(self):
        cb = lambda: self.client.txpool_status()
        self.mock(cb, True)
