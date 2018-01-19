from test_base import TestBase


class TestDebug(TestBase):

    def test_debug_backtrace_at(self):
        filename = 'server.go'
        line = 443
        cb = lambda: self.client.debug_backtrace_at(filename, line)
        self.mock(cb, True)

    def test_debug_block_profile(self):
        path = '/home/user/block.profile'
        seconds = 200
        cb = lambda: self.client.debug_block_profile(path, seconds)
        self.mock(cb, True)

    def test_debug_cpu_profile(self):
        path = '/home/user/cpu.profile'
        seconds = 200
        cb = lambda: self.client.debug_cpu_profile(path, seconds)
        self.mock(cb, True)

    def test_debug_dump_block(self):
        block = 'latest'
        cb = lambda: self.client.debug_dump_block(block)
        self.mock(cb, True)

    def test_debug_gc_stats(self):
        cb = lambda: self.client.debug_gc_stats()
        self.mock(cb, True)

    def test_debug_get_block_rlp(self):
        block = 'latest'
        cb = lambda: self.client.debug_get_block_rlp(block)
        self.mock(cb, True)

    def test_debug_go_trace(self):
        path = '/home/user/go.trace'
        seconds = 200
        cb = lambda: self.client.debug_go_trace(path, seconds)
        self.mock(cb, True)

    def test_debug_mem_stats(self):
        cb = lambda: self.client.debug_mem_stats()
        self.mock(cb, True)

    def test_debug_seed_hash(self):
        block = 'latest'
        cb = lambda: self.client.debug_seed_hash(block)
        self.mock(cb, True)

    def test_debug_set_head(self):
        block = 'latest'
        cb = lambda: self.client.debug_set_head(block)
        self.mock(cb, True)

    def test_debug_set_block_profile_rate(self):
        rate = 5
        cb = lambda: self.client.debug_set_block_profile_rate(rate)
        self.mock(cb, True)

    def test_debug_stacks(self):
        cb = lambda: self.client.debug_stacks()
        self.mock(cb, True)

    def test_debug_start_cpu_profile(self):
        path = '/home/user/cpu.profile'
        cb = lambda: self.client.debug_start_cpu_profile(path)
        self.mock(cb, True)

    def test_debug_start_go_trace(self):
        path = '/home/user/go.trace'
        cb = lambda: self.client.debug_start_go_trace(path)
        self.mock(cb, True)

    def test_debug_stop_cpu_profile(self):
        cb = lambda: self.client.debug_stop_cpu_profile()
        self.mock(cb, True)

    def test_debug_stop_go_trace(self):
        cb = lambda: self.client.debug_stop_go_trace()
        self.mock(cb, True)

    def test_debug_trace_block(self):
        block = 'latest'
        cb = lambda: self.client.debug_trace_block(block)
        self.mock(cb, True)

    def test_debug_trace_block_by_number(self):
        block = 'latest'
        cb = lambda: self.client.debug_trace_block_by_number(block)
        self.mock(cb, True)

    def test_debug_trace_block_by_number(self):
        hash_ = '0x96ee0e9574959ad9e2b7b287ea59bc8741d228b6ffc9eaee8e17bb59948103bf'
        cb = lambda: self.client.debug_trace_block_by_number(hash_)
        self.mock(cb, True)

    def test_debug_trace_block_from_file(self):
        path = '/home/user/block.rlp'
        cb = lambda: self.client.debug_trace_block_from_file(path)
        self.mock(cb, True)

    def test_debug_trace_transaction(self):
        hash_ = '0x43f101b4482a22be8061915133c5a32cd0303a14ac695f23bfe3748d59acd46c'
        cb = lambda: self.client.debug_trace_transaction(hash_)
        self.mock(cb, True)

    def test_debug_verbosity(self):
        log_level = 5
        cb = lambda: self.client.debug_verbosity(log_level)
        self.mock(cb, True)

    def test_debug_vmodule(self):
        log_pattern = 'p2p=5'
        cb = lambda: self.client.debug_vmodule(log_pattern)
        self.mock(cb, True)

    def test_debug_write_block_profile(self):
        path = '/home/user/block.profile'
        cb = lambda: self.client.debug_write_block_profile(path)
        self.mock(cb, True)

    def test_debug_write_mem_profile(self):
        path = '/home/user/mem.profile'
        cb = lambda: self.client.debug_write_mem_profile(path)
        self.mock(cb, True)
