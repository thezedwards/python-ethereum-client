from test_base import TestBase


class TestMiner(TestBase):

    def test_miner_set_extra(self):
        data = '0xbabe'
        cb = lambda: self.client.miner_set_extra(data)
        self.mock(cb, True)

    def test_miner_set_gas_price(self):
        gas_price = 10000
        cb = lambda: self.client.miner_set_gas_price(gas_price)
        self.mock(cb, True)

    def test_miner_start(self):
        threads = 5
        cb = lambda: self.client.miner_start(threads)
        self.mock(cb, True)

    def test_miner_stop(self):
        cb = lambda: self.client.miner_stop()
        self.mock(cb, True)

    def test_miner_set_ether_base(self):
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        cb = lambda: self.client.miner_set_ether_base(address)
        self.mock(cb, True)
