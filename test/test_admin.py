from test_base import TestBase


class TestAdmin(TestBase):

    def test_admin_add_peer(self):
        enode = 'enode://1ba7d1d8e9cd395c07e89830c2b9b34e5b3aa7e2928508aa7c3e9a353531255fed38ea0d6af3a599434ad4455a6554af3fcbc52afc1c18aa9b3272f48cb84402@127.0.0.1:8745'
        cb = lambda: self.client.admin_add_peer(enode)
        self.mock(cb, True)

    def test_admin_datadir(self):
        cb = lambda: self.client.admin_datadir()
        self.mock(cb, True)

    def test_admin_node_info(self):
        cb = lambda: self.client.admin_node_info()
        self.mock(cb, True)

    def test_admin_peers(self):
        cb = lambda: self.client.admin_peers()
        self.mock(cb, True)

    def test_admin_set_solc(self):
        path = '/usr/bin/solc'
        cb = lambda: self.client.admin_set_solc(path)
        self.mock(cb, True)

    def test_admin_start_rpc(self):
        cb = lambda: self.client.admin_start_rpc()
        self.mock(cb, True)

    def test_admin_start_ws(self):
        cb = lambda: self.client.admin_start_ws()
        self.mock(cb, True)

    def test_admin_stop_rpc(self):
        cb = lambda: self.client.admin_stop_rpc()
        self.mock(cb, True)

    def test_admin_stop_ws(self):
        cb = lambda: self.client.admin_stop_ws()
        self.mock(cb, True)
