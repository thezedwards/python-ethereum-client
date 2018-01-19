import os
import unittest
import ethrpc
import requests
import requests_mock

# Note:
# All the data used in these tests is invalid, from the
# block hashes, to block numbers, to addresses.
# They were generated from random binary data:
#   `lambda n: binascii.b2a_hex(os.urandom(n))`


class TestBase(unittest.TestCase):

    def setUp(self):
        self.use_mock = bool(int(os.environ.get('REQUESTS_MOCK', '0')))
        if self.use_mock:
            self.endpoint = 'mock://127.0.0.1:8545'
        else:
            self.endpoint = ethrpc.LOCALHOST_HTTP_ENDPOINT
        self.client = ethrpc.Client(self.endpoint)

    def mock(self, callback, mock_only = False):
        '''Conditional utilization of mock unittests.'''

        url = self.endpoint
        if self.use_mock:
            with requests_mock.Mocker() as mockery:
                mockery.post(self.endpoint, status_code=200)
                response = callback()
                self.assertIsInstance(response, requests.Response)
                self.assertEqual(response.url.rstrip('/'), url)
                self.assertEqual(response.status_code, 200)

        elif not mock_only:
            response = callback()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.url.rstrip('/'), url)
