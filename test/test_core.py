import unittest
import ethrpc


class TestCore(unittest.TestCase):

    def test_map_position(self):
        key = "0xc8d6ce812a5824aa257ec33257bfd97dc9b78968"
        position = 0
        expected = "0x5e2e105ad8200f9b677b33e64aa53efd5c6c72828759504366e650c535d42c0c"
        self.assertEqual(ethrpc.map_position(key, position), expected)

    def test_abstract_client(self):
        with self.assertRaises(TypeError):
            ethrpc.AbstractClient()
