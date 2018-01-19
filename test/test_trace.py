from test_base import TestBase


class TestTrace(TestBase):

    def test_trace_block(self):
        block = 'latest'
        cb = lambda: self.client.trace_block(block)
        self.mock(cb, True)

    def test_trace_call(self):
        from_ = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        to = '0x43b810d42d7650d19930581f6a77126ffe5c6bf6'
        gas = 90000
        block = 'latest'
        cb = lambda: self.client.trace_call(from_, to, gas, block=block)
        self.mock(cb, True)

    def test_trace_filter(self):
        from_block = 5
        to_block = 15
        address = '0xdae1bfb92c7c0fd23396619ee1a0d643bf609c2e'
        cb = lambda: self.client.trace_filter(from_block, to_block, address)
        self.mock(cb, True)

    def test_trace_get(self):
        hash_ = '0x43f101b4482a22be8061915133c5a32cd0303a14ac695f23bfe3748d59acd46c'
        index = 0
        cb = lambda: self.client.trace_get(hash_, index)
        self.mock(cb, True)

    def test_trace_raw_transaction(self):
        data = '0xbabe'
        traces = ['vmTrace', 'trace']
        cb = lambda: self.client.trace_raw_transaction(data, traces)
        self.mock(cb, True)


    def test_trace_replay_transaction(self):
        hash_ = '0x43f101b4482a22be8061915133c5a32cd0303a14ac695f23bfe3748d59acd46c'
        traces = ['vmTrace', 'trace']
        cb = lambda: self.client.trace_replay_transaction(hash_, traces)
        self.mock(cb, True)

    def test_trace_transaction(self):
        hash_ = '0x43f101b4482a22be8061915133c5a32cd0303a14ac695f23bfe3748d59acd46c'
        cb = lambda: self.client.trace_transaction(hash_)
        self.mock(cb, True)
