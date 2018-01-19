import binascii
from test_base import TestBase


def hexlify(data):
    bytes_ = b'0x' + binascii.hexlify(data)
    return bytes_.decode('ascii')


class TestEth(TestBase):

    def test_shh_add_private_key(self):
        key = '0x8d91f937b49f0dfc5edbea6700d99e8febfd48021baae0301d15e7ee2d78e644'
        cb = lambda: self.client.shh_add_private_key(key)
        self.mock(cb, True)

    def test_shh_add_sym_key(self):
        key = '0x2509d5eeb73edf3342578b38af2a8522569a60c3faba8e940a61eb46323601851b02fd4f92294ed338274b9692fa81b1696c17a377be9246ab7d23543f0554a4'
        cb = lambda: self.client.shh_add_sym_key(key)
        self.mock(cb, True)

    def test_shh_add_to_group(self):
        address = '0x1f611135cd13d541186df4eb80467a92abfc94fa4cf2bb9fc2f59680b8d022a84312bab23f10f94b1720bb7f904a47d999a8b17e705658ecd9ab9466bc8838bdc2'
        cb = lambda: self.client.shh_add_to_group(address)
        self.mock(cb, True)

    def test_shh_delete_key(self):
        key = '0x88ec91bb171b56cb4a176524748746de3d6f0f75b612debd36f2d2af6440665c'
        cb = lambda: self.client.shh_delete_key(key)
        self.mock(cb, True)

    def test_shh_delete_message_filter(self):
        filter_id = '0xefc899b38681d6f90f0029f539d246a7b46b5ce91ff5535d4ab560a0a607cde4'
        cb = lambda: self.client.shh_delete_message_filter(filter_id)
        self.mock(cb, True)

    def test_shh_get_filter_changes(self):
        cb = lambda: self.client.shh_get_filter_changes(15)
        self.mock(cb, True)

    def test_shh_get_filter_messages(self):
        filter_id = '0xefc899b38681d6f90f0029f539d246a7b46b5ce91ff5535d4ab560a0a607cde4'
        cb = lambda: self.client.shh_get_filter_messages(filter_id)
        self.mock(cb, True)

    def test_shh_get_messages(self):
        cb = lambda: self.client.shh_get_messages(15)
        self.mock(cb, True)

    def test_shh_get_private_key(self):
        key_id = '0xfa7d31a4e2dc3b0dbeb39333a691f1f85938087ab750b45304d87d72063b548d'
        cb = lambda: self.client.shh_get_private_key(key_id)
        self.mock(cb, True)

    def test_shh_get_public_key(self):
        key_id = '0xfa7d31a4e2dc3b0dbeb39333a691f1f85938087ab750b45304d87d72063b548d'
        cb = lambda: self.client.shh_get_public_key(key_id)
        self.mock(cb, True)

    def test_shh_get_sym_key(self):
        key_id = '0x68a7d5c58c99ec06d1768b8e10b8de55fc0d3d67f226fe9a2c45ac272483b8c0'
        cb = lambda: self.client.shh_get_sym_key(key_id)
        self.mock(cb, True)

    def test_shh_has_identity(self):
        address = '0x1f611135cd13d541186df4eb80467a92abfc94fa4cf2bb9fc2f59680b8d022a84312bab23f10f94b1720bb7f904a47d999a8b17e705658ecd9ab9466bc8838bdc2'
        cb = lambda: self.client.shh_has_identity(address)
        self.mock(cb, True)

    def test_shh_info(self):
        cb = lambda: self.client.shh_info()
        self.mock(cb, True)

    def test_shh_new_filter(self):
        topics = [hexlify(b'filter')]
        cb = lambda: self.client.shh_new_filter(topics)
        self.mock(cb, True)

    def test_shh_new_group(self):
        cb = lambda: self.client.shh_new_group()
        self.mock(cb, True)

    def test_shh_new_identity(self):
        cb = lambda: self.client.shh_new_identity()
        self.mock(cb, True)

    def test_shh_new_key_pair(self):
        cb = lambda: self.client.shh_new_key_pair()
        self.mock(cb, True)

    def test_shh_new_message_filter(self):
        topics = [hexlify(b'filter')]
        cb = lambda: self.client.shh_new_message_filter(topics)
        self.mock(cb, True)

    def test_shh_new_sym_key(self):
        cb = lambda: self.client.shh_new_sym_key()
        self.mock(cb, True)

    def test_shh_post(self):
        topics = [
            hexlify(b'whisper-chat-client'),
            hexlify(b'python-ethereum-client')
        ]
        payload = hexlify(b'OK')
        cb = lambda: self.client.shh_post(topics, payload, 100, 100)
        self.mock(cb, True)

    def test_shh_subscribe(self):
        topics = [hexlify(b'filter')]
        cb = lambda: self.client.shh_subscribe(topics)
        self.mock(cb, True)

    def test_shh_uninstall_filter(self):
        cb = lambda: self.client.shh_uninstall_filter(15)
        self.mock(cb, True)

    def test_shh_unsubscribe(self):
        cb = lambda: self.client.shh_unsubscribe(4714555447970118045)
        self.mock(cb, True)

    def test_shh_version(self):
        cb = lambda: self.client.shh_version()
        self.mock(cb, True)
