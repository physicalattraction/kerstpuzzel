from unittest import TestCase

from Conundrum.caesar import encrypt, decrypt, decrypt_try_all

DECRYPTED_MSG = 'helloworld'
INDEX = 4
ENCRYPTED_MSG = 'lippsasvph'


class CaesarTestCase(TestCase):
    def test_that_encrypt_works(self):
        self.assertEqual(ENCRYPTED_MSG, encrypt(DECRYPTED_MSG, INDEX))

    def test_that_decrypt_works(self):
        self.assertEqual(DECRYPTED_MSG, decrypt(ENCRYPTED_MSG, INDEX))

    def test_decrypt_try_all_works(self):
        self.assertIn(DECRYPTED_MSG, decrypt_try_all(ENCRYPTED_MSG))
