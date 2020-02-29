from unittest import TestCase

from Conundrum.repeated_letters import decrypt, decrypt_try_all

encrypted_msg = 'hello world'
decrypted_msg = 'helworl'


class RepeatedLettersTestCase(TestCase):
    def test_that_letters_after_repeated_letters_are_removed(self):
        self.assertEqual(decrypted_msg, decrypt(encrypted_msg, 'l'))

    def test_that_decrypt_try_all_finds_decrypted_message(self):
        self.assertIn(decrypted_msg, decrypt_try_all(encrypted_msg))