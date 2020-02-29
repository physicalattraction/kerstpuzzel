from unittest import TestCase

from Conundrum.key_cipher import encrypt, decrypt

DECRYPTED_MSG = 'meetmeatfivepm'
KEY = 'enigma'
ENCRYPTED_MSG = 'rsnazffhopifua'


class KeyCipherTestCase(TestCase):
    def test_that_encrypt_works(self):
        self.assertEqual(ENCRYPTED_MSG, encrypt(DECRYPTED_MSG, KEY))

    def test_that_decrypt_works(self):
        self.assertEqual(DECRYPTED_MSG, decrypt(ENCRYPTED_MSG, KEY))
