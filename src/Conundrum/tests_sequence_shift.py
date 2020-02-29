from unittest import TestCase

from Conundrum.sequence_shift import encrypt, decrypt

DECRYPTED_MSG = 'hello'
SEQUENCE = [1, 3, 5, 7, 9]
ENCRYPTED_MSG = 'ihqsx'


class KeyCipherTestCase(TestCase):
    def test_that_encrypt_works(self):
        self.assertEqual(ENCRYPTED_MSG, encrypt(DECRYPTED_MSG, SEQUENCE))

    def test_that_decrypt_works(self):
        self.assertEqual(DECRYPTED_MSG, decrypt(ENCRYPTED_MSG, SEQUENCE))
